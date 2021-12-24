from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

from kivy.graphics import *
from kivy.core.window import Window

from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.properties import NumericProperty

import sqlite3


Builder.load_file('game.kv')

class HomeScreen(Screen):
    
    music_name = StringProperty()
    music_number = 0
    music_sum = 3
    music_list = ['aaa','bbb','ccc']
    music_image_url = ['images/music0.jpg','images/music1.jpg','images/music2.jpg']
    music_image = StringProperty()
    
    level = StringProperty()
    
    first_score = StringProperty()
    second_score = StringProperty()
    third_score = StringProperty()
    
    def __init__(self, **kwargs) -> None:
        super(HomeScreen, self).__init__(**kwargs)
        self.music_name = self.music_list[0]
        self.music_image = self.music_image_url[0]
        self.level = ''
        
        
    def pressed_left(self):
        if self.music_number <= 0:
            self.music_number = self.music_sum-1
            
        else:
            self.music_number -= 1
        self.music_name = self.music_list[self.music_number]
        self.music_image = self.music_image_url[self.music_number]
            
           
    def pressed_right(self):
        if self.music_number >= self.music_sum-1:
            self.music_number = 0
            
        else:
            self.music_number += 1
        self.music_name = self.music_list[self.music_number]
        self.music_image = self.music_image_url[self.music_number]
        
        
    def pressed_level(self, arg):
        self.level = arg
        
        score = []
        con = sqlite3.connect('score.db')
        cur = con.cursor()
        
        sql = "select score from 'oop2-last-issue' where music_name='" + self.music_name + "' and mode='"  + self.level + "'";
        cur.execute(sql)
        
        for data in cur:
            score.append(data)
            
        self.first_score = str(score[0][0])
        self.second_score = str(score[1][0])
        self.third_score = str(score[2][0])
        
        print(score)
        
        
class PlayScreen(Screen):
   pass

sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(PlayScreen(name='play'))

class MyApp(App):
    def build(self):
        return sm
    
    
MyApp().run()
    
