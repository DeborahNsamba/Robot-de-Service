import socket
import struct
from kivy.core.window import Window
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.app import MDApp
from kivymd.uix.button import MDRaisedButton
from kivy.clock import Clock

Window.size = (800, 600)
Window.fullscreen = False

PORT = 4444
SERVER = ""
FORMAT = "utf-8"
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Add this updated layout in the `screen_helper` string
screen_helper = """
ScreenManager:
    FirstScreen:
    SecondScreen:

<FirstScreen>:
    name: 'first'
    FloatLayout:
        canvas.before:
            Color:
                rgba: 0.7, 0.7, 0.7, 1  # Light greyish color
            Rectangle:
                pos: self.pos
                size: self.size
        MDLabel:
            text: 'Robot de Service 1.2'
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
                rgba: 0.75, 0.75, 0.8, 1  # Light greyish color
            Rectangle:
                pos: self.pos
                size: self.size
        MDLabel:
            text: 'Robot de Service'
            halign: "center"
            font_size: "25sp"
            pos_hint: {'center_x': 0.5, 'center_y': 0.9}
        
        # GridLayout for joystick control with arrow buttons
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
                on_press: root.send_command(100)  # Forward
            MDLabel:
                text: ""
            MDRaisedButton:
                text: "Gauche"
                size_hint: (0.8, 0.6)
                md_bg_color: 0.5, 0.5, 1, 1
                on_press: root.send_command(102)  # Left
            MDLabel:
                text: ""
            MDRaisedButton:
                text: "Droite"
                size_hint: (0.8, 0.6)
                md_bg_color: 0.5, 0.5, 1, 1
                on_press: root.send_command(103)  # Right
            MDLabel:
                text: ""
            MDRaisedButton:
                text: "Reculer"
                size_hint: (0.8, 0.6)
                md_bg_color: 0.5, 0.5, 1, 1
                on_press: root.send_command(101)  # Backward
            MDLabel:
                text: ""

        # GridLayout for table buttons (as before)
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

        # Status Label
        MDLabel:
            id: status
            text: 'Not Connected'
            halign: "center"
            font_size: "14sp"
            color: 1, 0, 0, 1
            pos_hint: {'center_x': 0.5, 'center_y': 0.1}
"""


class FirstScreen(Screen):
    def next(self):
        global SERVER
        SERVER = self.ids.ipaddress.text
        self.manager.current = 'second'

class SecondScreen(Screen):
    def start_client(self):
        try:
            ADDR = (SERVER, PORT)
            client.connect(ADDR)
            self.ids.status.text = "Connected"
            self.ids.status.color = (0, 1, 0, 1)
        except Exception as e:
            self.ids.status.text = "Connection Failed"
            self.ids.status.color = (1, 0, 0, 1)
            print(f"Connection error: {e}")

    def send_command(self, command):
        """
        Send specific commands:
        - 100: Forward
        - 101: Backward
        - 102: Turn Left
        - 103: Turn Right
        - 1-10: Table numbers
        - 0: Go Home
        - -1: Turn off
        """
        try:
            data_to_send = struct.pack('i', command)
            client.send(data_to_send)
        except Exception as e:
            self.ids.status.text = "Error Sending Command"
            self.ids.status.color = (1, 0, 0, 1)
            print(f"Send error: {e}")



sm = ScreenManager()
sm.add_widget(FirstScreen(name='first'))
sm.add_widget(SecondScreen(name='second'))

class RoverControlApp(MDApp):
    def build(self):
        self.title = "Commande Robot"
        self.theme_cls.primary_palette = "Green"
        return Builder.load_string(screen_helper)

if __name__ == "__main__":
    RoverControlApp().run()
