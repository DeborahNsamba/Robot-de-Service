import socket
import struct
import speech_recognition as sr
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.slider import MDSlider
from kivy.clock import Clock
import threading

Window.size = (800, 600)
Window.fullscreen = False

PORT = 4444
SERVER = ""
FORMAT = "utf-8"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Updated layout with Battery Voltage Label, Voice Command Button, and Speed Slider
screen_helper = """
ScreenManager:
    FirstScreen:
    SecondScreen:

<FirstScreen>:
    name: 'first'
    FloatLayout:
        canvas.before:
            Color:
                rgba: 0.7, 0.7, 0.7, 1
            Rectangle:
                pos: self.pos
                size: self.size
        MDLabel:
            text: 'Robot de Service 1.4'
            halign: "center"
            font_size: "30sp"
            pos_hint: {'center_x': 0.5, 'center_y': 0.92}
        MDTextField:
            id: ipaddress
            text: "192.168.1.67"
            hint_text: 'Enter IP Address'
            size_hint: (0.6, None)
            pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        MDRaisedButton:
            text: 'Proceed'
            pos_hint: {'center_x': 0.5, 'center_y': 0.3}
            on_press: root.next()

<SecondScreen>:
    name: 'second'
    on_enter: root.start_client()
    FloatLayout:
        canvas.before:
            Color:
                rgba: 0.75, 0.75, 0.8, 1
            Rectangle:
                pos: self.pos
                size: self.size
        MDLabel:
            text: 'Robot de Service'
            halign: "center"
            font_size: "25sp"
            pos_hint: {'center_x': 0.5, 'center_y': 0.95}
        GridLayout:
            cols: 3
            spacing: 10
            size_hint: (0.8, 0.3)
            pos_hint: {'center_x': 0.5, 'center_y': 0.7}
            MDLabel:
                text: ""
            MDRaisedButton:
                text: "Avancer"
                size_hint: (0.8, 0.6)
                md_bg_color: 0.5, 0.5, 1, 1
                on_press: root.send_command(100)
            MDLabel:
                text: ""
            MDRaisedButton:
                text: "Gauche"
                size_hint: (0.8, 0.6)
                md_bg_color: 0.5, 0.5, 1, 1
                on_press: root.send_command(102)
            MDLabel:
                text: ""
            MDRaisedButton:
                text: "Droite"
                size_hint: (0.8, 0.6)
                md_bg_color: 0.5, 0.5, 1, 1
                on_press: root.send_command(103)
            MDLabel:
                text: ""
            MDRaisedButton:
                text: "Réculer"
                size_hint: (0.8, 0.6)
                md_bg_color: 0.5, 0.5, 1, 1
                on_press: root.send_command(101)
            MDLabel:
                text: ""

        GridLayout:
            cols: 3
            spacing: 20
            padding: [30, 30, 30, 30]
            size_hint: (0.9, 0.4)
            pos_hint: {'center_x': 0.5, 'center_y': 0.35}
            MDRaisedButton:
                text: "Table 1"
                size_hint: (0.8, 0.6)
                on_press: root.send_command(1)
            MDRaisedButton:
                text: "Table 2"
                size_hint: (0.8, 0.6)
                on_press: root.send_command(2)
            MDRaisedButton:
                text: "Table 3"
                size_hint: (0.8, 0.6)
                on_press: root.send_command(3)
            MDRaisedButton:
                text: "Table 4"
                size_hint: (0.8, 0.6)
                on_press: root.send_command(4)
            MDRaisedButton:
                text: "Table 5"
                size_hint: (0.8, 0.6)
                on_press: root.send_command(5)
            MDRaisedButton:
                text: "Table 6"
                size_hint: (0.8, 0.6)
                on_press: root.send_command(6)
            MDRaisedButton:
                text: "Table 7"
                size_hint: (0.8, 0.6)
                on_press: root.send_command(7)
            MDRaisedButton:
                text: "Table 8"
                size_hint: (0.8, 0.6)
                on_press: root.send_command(8)
            MDRaisedButton:
                text: "Table 9"
                size_hint: (0.8, 0.6)
                on_press: root.send_command(9)
            MDRaisedButton:
                text: "Table 10"
                size_hint: (0.8, 0.6)
                on_press: root.send_command(10)
            MDRaisedButton:
                text: "Home"
                size_hint: (0.8, 0.6)
                on_press: root.send_command(0)
            MDRaisedButton:
                text: "Turn Off"
                size_hint: (0.8, 0.6)
                md_bg_color: 1, 0, 0, 1
                on_press: root.send_command(-1)
        MDRaisedButton:
            text: 'Voice Command'
            pos_hint: {'center_x': 0.5, 'center_y': 0.05}
            on_press: root.voice_command()
        MDRaisedButton:
            text: 'Returner'
            pos_hint: {'center_x': 0.3, 'center_y': 0.05}
            on_press: app.go_back()
        MDRaisedButton:
            text: 'Quitter'
            pos_hint: {'center_x': 0.7, 'center_y': 0.05}
            on_press: app.stop()

        MDLabel:
            id: status
            text: 'Not Connected'
            halign: "center"
            font_size: "14sp"
            color: 1, 0, 0, 1
            pos_hint: {'center_x': 0.5, 'center_y': 0.1}
        MDLabel:
            id: voltage
            text: 'Voltage: -- V'
            halign: "center"
            font_size: "18sp"
            color: 0, 0, 0, 1
            pos_hint: {'center_x': 0.5, 'center_y': 0.15}
        MDSlider:
            id: speed_slider
            min: 0
            max: 100
            value: 50
            pos_hint: {'center_x': 0.5, 'center_y': 0.9}
            size_hint: (0.8, None)
            on_value: root.set_speed(self.value)
        MDLabel:
            id: speed_label
            text: 'Speed: 50%'
            halign: "center"
            font_size: "18sp"
            color: 0, 0, 0, 1
            pos_hint: {'center_x': 0.25, 'center_y': 0.92}
"""

class FirstScreen(Screen):
    def next(self):
        global SERVER
        SERVER = self.ids.ipaddress.text
        self.manager.current = 'second'

class SecondScreen(Screen):
    def start_client(self):
        threading.Thread(target=self._connect_client, daemon=True).start()

    def _connect_client(self):
        try:
            ADDR = (SERVER, PORT)
            client.connect(ADDR)
            Clock.schedule_once(lambda dt: setattr(self.ids.status, 'text', "Connected"))
            Clock.schedule_once(lambda dt: setattr(self.ids.status, 'color', (0, 1, 0, 1)))
            Clock.schedule_interval(lambda dt: threading.Thread(target=self.request_voltage, daemon=True).start(), 5)
        except Exception as e:
            Clock.schedule_once(lambda dt: setattr(self.ids.status, 'text', "Connection Failed"))
            Clock.schedule_once(lambda dt: setattr(self.ids.status, 'color', (1, 0, 0, 1)))
            print(f"Connection error: {e}")

    def send_command(self, command):
        threading.Thread(target=self._send_command_thread, args=(command,), daemon=True).start()

    def _send_command_thread(self, command):
        try:
            data_to_send = struct.pack('i', command)
            client.send(data_to_send)
        except Exception as e:
            Clock.schedule_once(lambda dt: setattr(self.ids.status, 'text', "Error Sending Command"))
            Clock.schedule_once(lambda dt: setattr(self.ids.status, 'color', (1, 0, 0, 1)))
            print(f"Send error: {e}")

    def set_speed(self, value):
        self.ids.speed_label.text = f"Speed: {int(value)}%"
        self.send_command(200 + int(value))

    def request_voltage(self):
        try:
            command = -2
            data_to_send = struct.pack('i', command)
            client.send(data_to_send)
            voltage_data = client.recv(4)
            voltage = struct.unpack('f', voltage_data)[0]
            Clock.schedule_once(lambda dt: setattr(self.ids.voltage, 'text', f"Voltage: {voltage:.2f} V"))
            if voltage < 11.0:
                Clock.schedule_once(lambda dt: setattr(self.ids.status, 'text', "Low Battery! Stopping Robot."))
                Clock.schedule_once(lambda dt: setattr(self.ids.status, 'color', (1, 0, 0, 1)))
                self.send_command(-1)
        except Exception as e:
            Clock.schedule_once(lambda dt: setattr(self.ids.status, 'text', "Error Reading Voltage"))
            Clock.schedule_once(lambda dt: setattr(self.ids.status, 'color', (1, 0, 0, 1)))
            print(f"Voltage read error: {e}")

    def voice_command(self):
        threading.Thread(target=self._listen_for_command, daemon=True).start()

    def _listen_for_command(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            Clock.schedule_once(lambda dt: setattr(self.ids.status, 'text', "Listening for command..."))
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio).lower()
                Clock.schedule_once(lambda dt: self.process_voice_command(command))
            except sr.UnknownValueError:
                Clock.schedule_once(lambda dt: setattr(self.ids.status, 'text', "Could not understand the command"))
            except sr.RequestError as e:
                Clock.schedule_once(lambda dt: setattr(self.ids.status, 'text', f"Error with recognition service: {e}"))
            except Exception as e:
                Clock.schedule_once(lambda dt: setattr(self.ids.status, 'text', f"Error: {e}"))

    def process_voice_command(self, command):
        commands = {
            "forward": 100,
            "backward": 101,
            "left": 102,
            "right": 103,
            "stop": -1,
            "home": 0
        }
        if command in commands:
            self.ids.status.text = f"Executing: {command}"
            self.send_command(commands[command])
        elif command.startswith("table"):
            try:
                table_number = int(command.split(" ")[1])
                if 1 <= table_number <= 10:
                    self.ids.status.text = f"Going to Table {table_number}"
                    self.send_command(table_number)
                else:
                    self.ids.status.text = "Invalid table number"
            except ValueError:
                self.ids.status.text = "Invalid table command"
        else:
            self.ids.status.text = "Unknown command"

class RoverControlApp(MDApp):
    def build(self):
        self.title = "Commande Robot"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(screen_helper)

    def go_back(self):
        self.root.current = 'first'

if __name__ == "__main__":
    RoverControlApp().run()