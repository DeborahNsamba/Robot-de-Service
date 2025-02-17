# import time
# from time import *
from kivy.clock import Clock
# from kivy.core.window import Window
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivymd.app import MDApp
from kivy.lang.builder import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivymd.uix.button import MDRectangleFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton
# from kivy.garden.joystick import Joystick
from g.joystick.joystick import Joystick
import socket
import threading
import struct
from kivy.core.window import Window
Window.size = (800, 600)
Window.fullscreen = False
# HEADER = 64
PORT = 4444

SERVER = ""
#SERVER = "192.168.43.136"
FORMAT = "utf-8"
#ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

screen_helper = """
#: import FadeTransition kivy.uix.screenmanager.FadeTransition
#: import Joystick g.joystick.joystick.Joystick

ScreenManager:
    transition: FadeTransition()
    FirstScreen:
    SecondScreen:

<FirstScreen>:
    name: 'first'
    canvas.before:
        Color:
            rgba: (1,1,1,1)
        Rectangle:
            pos: self.pos
            size: self.size
    FloatLayout:
        orientation: 'vertical'
        pos_hint: {'center_x':0.5,'center_y':0.5}
        canvas:
            Color:
                rgba: (183/255,244/255,216/255, 0.9)
              
            Rectangle:
                size: self.size
                pos: self.pos  
                #source: "Makers2.png"
                 
        Image:
            id: imageView
            source: 'Makers2.png'
            pos_hint: {'center_x':0.5,'center_y':0.5}
            # size_hint_y: 1.2
            size_hint: (0.99,0.99)
            #width: 1
            #allow_stretch: True
        MDLabel:
            text: 'Logistic Rover 1.0'
            halign: "center"
            font_size: "30sp"
            color: (60/225,179/225,113/225, 1)
            # height: "14sp"
            pos_hint: {'center_x':0.5,'center_y':0.92}
            font_name: "Nebula-Regular.otf"
            
        MDTextField:
            id: ipaddress
            icon_left: 'wifi'
            text: "192.168.1.67"
            hint_text: 'enter ipaddress'
            size_hint: (0.4,None)
            font_size: "20sp"
            pos_hint: {'center_x':0.25,'center_y':0.1}
            color: (60/225,179/225,113/225, 1)
            
        MDRaisedButton:
            text: 'proceed'
            line_color: [255/255,255/255,255/255,1] 
            bold: True
            pos_hint: {'center_x':0.8,'center_y':0.1}
            on_press: root.next()
            md_bg_color: app.theme_cls.primary_dark
            #size_hint: (0.5,0.5)
            text_color: 1,1,1
            font_size: "10sp"
<SecondScreen>:
    name: 'second'
    on_enter: root.start_client()
    canvas.before:
        Color:
            rgba: 1,1,1,1
        Rectangle:
            pos: self.pos
            size: self.size
    FloatLayout:
        orientation: 'vertical'
        pos_hint: {'center_x':0.5,'center_y':0.5}
        MDLabel:
            text: 'Logistic rover'
            halign: "center"
            font_size: "35sp"
            color: app.theme_cls.primary_dark
            pos_hint: {'center_x':0.5,'center_y':0.9}
            font_name: "Nebula-Regular.otf"
        MDLabel:
            text: 'Not connected'
            id: status
            halign: "center"
            font_size: "12sp"
            color: (255/255, 99/255, 71/255, 0.8)
            #color: app.theme_cls.primary_dark
            pos_hint: {'center_x':0.5,'center_y':0.81}
            #font_name: "Arial"
            
        BoxLayout:
            orientation: 'horizontal'
            #spacing: 60
            #padding: 70
            pos_hint: {'center_x':0.5,'center_y':0.5}
            Joystick:
                id: j1
                sticky: True
                outer_size: 0.5
                # inner_size: 0.35
                pad_size:   0.5
                outer_line_width: 0.01
                inner_line_width: 0.01
                pad_line_width:   0.01
                size_hint: (0.7, 0.7)
                outer_background_color:  app.theme_cls.primary_dark
                outer_line_color:       app.theme_cls.primary_dark
                inner_background_color: app.theme_cls.primary_light
                inner_line_color:       app.theme_cls.primary_dark
                pad_background_color:   (60/225,179/225,113/225, 1)
                pad_line_color:         app.theme_cls.primary_dark 
                pos_hint: {'center_x':-0.2,'center_y':0.45}
                #on_touch_move: root.joy1()
                #on_touch_up: root.joy_1()

            Joystick:
                id: j2
                sticky: False
                outer_size: 0.5
                # inner_size: 0.35
                pad_size:   0.5
                outer_line_width: 0.01
                inner_line_width: 0.01
                pad_line_width:   0.01
                size_hint: (0.7, 0.7)
                outer_background_color:  app.theme_cls.primary_dark
                outer_line_color:       app.theme_cls.primary_dark
                inner_background_color: app.theme_cls.primary_light
                inner_line_color:       app.theme_cls.primary_dark
                pad_background_color:   (60/225,179/225,113/225, 1)
                pad_line_color:         app.theme_cls.primary_dark 
                pos_hint: {'center_x':2,'center_y':0.45}
                #on_touch_move: root.joy2()
                #on_touch_up: root.joy_2()
            """


class FirstScreen(Screen):
    def next(self):
        global SERVER
        SERVER = self.ids.ipaddress.text

        self.manager.current = 'second'

class SecondScreen(Screen):
    def start_client(self):
        try:
            print("connecting to client..")
            #SERVER = self.ids.ipaddress.text
            print(SERVER)
            print(PORT)
            ADDR = (SERVER, PORT)
            client.connect(ADDR)
            Clock.schedule_interval(self.send, 0)
        except:
            print("unable to connect")

    def send(self, instance):
        try:
            data_to_send = struct.pack('ffffff',60.0, self.ids.j1.pad[0],self.ids.j1.pad[1],self.ids.j2.pad[0],self.ids.j2.pad[1],60.0)
            #print(data_to_send)
            client.send(data_to_send)
            try:
                received_data = client.recv(2048).decode(FORMAT)
                if received_data=="Rover Connected":
                    #rover connected
                    self.ids.status.text = "connected"
                    self.ids.status.color = (60 / 225, 179 / 225, 113 / 225, 1)
                else:
                    #roveer not connected
                    self.ids.status.text = "Not connected"
                    self.ids.status.color = (255/255, 99/255, 71/255, 0.8)


                # (60 / 225, 179 / 225, 113 / 225, 1)
                # print(client.recv(2048).decode(FORMAT))
            except:
                pass
        except:
            # roveer not connected
            self.ids.status.text = "Not connected"
            self.ids.status.color = (255 / 255, 99 / 255, 71 / 255, 0.8)
            print("unable to send")

sm = ScreenManager()
sm.add_widget(FirstScreen(name='first'))
sm.add_widget(SecondScreen(name='second'))


class DemoApp(MDApp):

    def build(self):
        self.title = "Joystick"
        # self.icon = "pic.png"
        self.theme_cls.primary_palette = "Green"
        screen = Builder.load_string(screen_helper)

        # screen.current = 'first'
        # def cur(self):
        #     screen.current = 'second'

        # screen.current='first'
        #Clock.schedule_once(cur, 2)

        return screen


if __name__ == '__main__':
    DemoApp().run()