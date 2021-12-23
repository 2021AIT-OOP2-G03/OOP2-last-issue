from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

from kivy.graphics import *
from kivy.core.window import Window

from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.properties import NumericProperty


Builder.load_file('game.kv')

class HomeScreen(Screen):
    music_text = StringProperty()
    music_number = 0
    music_list = 2
    level = StringProperty()
    
    
    def __init__(self, **kwargs) -> None:
        super(HomeScreen, self).__init__(**kwargs)
        self.music_text = 'images/music{}.jpg'.format(self.music_number)
        self.level = ''
    
    def pressed_left(self):
        if self.music_number <= 0:
            self.music_number = self.music_list
        else:
            self.music_number -= 1
        self.music_text = 'images/music{}.jpg'.format(self.music_number)
    
    def pressed_right(self):
        if self.music_number >= self.music_list:
            self.music_number = 0
        else:
            self.music_number += 1
        self.music_text = 'images/music{}.jpg'.format(self.music_number)
    
    def pressed_level(self, arg):
        self.level = arg



    

class PlayScreen(Screen):
   pass


sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(PlayScreen(name='play'))

class MyApp(App):
    def build(self):
        return sm
    
MyApp().run()
    
