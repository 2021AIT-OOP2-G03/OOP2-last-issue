from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

from kivy.graphics import *
from kivy.core.window import Window

from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.clock import Clock


from kivy.uix.label import Label
from kivy.uix.scatter import Scatter


import sqlite3


Builder.load_file('game.kv')

class HomeScreen(Screen):
    # 曲名を格納する変数
    # game.kvで使用する変数
    music_name = StringProperty()
    # 現在の曲番号
    music_number = 0
    # 総曲数
    music_sum = 3
    
    # 曲名を格納
    music_list = ['aaa','bbb','ccc']
    # 曲名が格納されている要素と同じ要素番号にurl（画像）を格納
    music_image_url = ['images/music0.jpg','images/music1.jpg','images/music2.jpg']
    # game.kvで使用する変数（曲番号にあったurlが格納される）
    music_image = StringProperty()
    
    # 難易度を格納する変数
    # game.kvで使用する変数
    level = StringProperty()
    
    # １位２位３位のスコアを格納するための変数
    first_score = StringProperty()
    second_score = StringProperty()
    third_score = StringProperty()
    
    def __init__(self, **kwargs) -> None:
        super(HomeScreen, self).__init__(**kwargs)
        # 開始は曲番号０なので最初の曲を格納
        self.music_name = self.music_list[0]
        # 現在の曲番号のurlを格納
        self.music_image = self.music_image_url[0]
        self.level = ''
        
    def pressed_left(self):
        # 曲番号０にいるときは左矢印で最後の曲番号にしたいため最後の曲番号を格納
        if self.music_number <= 0:
            self.music_number = self.music_sum-1
        
        # 左矢印クリックごとに曲番号を−１
        else:
            self.music_number -= 1
        
        # 曲番号の名前と画像のurlをそれぞれ格納
        self.music_name = self.music_list[self.music_number]
        self.music_image = self.music_image_url[self.music_number]
            
           
    def pressed_right(self):
         # 曲番号２にいるときは右矢印で最初の曲番号にしたいため最初の曲番号を格納
        if self.music_number >= self.music_sum-1:
            self.music_number = 0
        
        # 左矢印クリックごとに曲番号を＋１
        else:
            self.music_number += 1
            
        # 曲番号の名前と画像のurlをそれぞれ格納
        self.music_name = self.music_list[self.music_number]
        self.music_image = self.music_image_url[self.music_number]
        
    def pressed_level(self, arg):
        # 押されたラベルの難易度を格納
        self.level = arg
        
        # データベースから取得したスコアを格納する
        score = []
        
        # データベースに接続
        con = sqlite3.connect('score.db')
        cur = con.cursor()
        # 現在の曲名と難易度のスコアを取得
        sql = "select score from 'oop2-last-issue' where music_name='" + self.music_name + "' and mode='"  + self.level + "'";
        cur.execute(sql)
        
        # 取得したデータをscoreに格納
        for data in cur:
            score.append(data)
        
        # game.kvで使用する変数に格納
        self.first_score = str(score[0][0])
        self.second_score = str(score[1][0])
        self.third_score = str(score[2][0])

        # クローズ
        con.close()

    def High_Score(self, arg):
        # 押されたラベルの難易度を格納
        self.level = arg

        sorted_score = []

        # 接続処理, カーソルオブジェクトを取得
        con = sqlite3.connect('score.db')
        cur = con.cursor()

        sql = 'insert into oop2-last-issue values(?,?,score)', [
            self.music_name, self.level]
        # 仮実装、曲名と難易度、スコアを挿入
        cur.execute(sql)
        cur.commit()

        # スコアのソーティング
        sort = 'select * from "oop2-last-issue" order by score desc where music_name=? and mode=?', [
            self.music_name, self.level]
        cur.execute(sort)

        # ソートしたデータをsorted_scoreに格納
        for data in cur:
            sorted_score.append(data)

        # game.kvで使用する変数, 最高スコアの格納
        for score in sorted_score:
            if score > self.first_score:
                self.first_score = str(score[0][0])
            elif score > self.second_score and score < self.first_score:
                self.second_score = str(score[1][0])
            elif score > self.third_score and score < self.second_score:
                self.third_score = str(score[2][0])
        # クローズ
        con.close()
        
class PlayScreen(Screen):

    dt = 1/30 #フレーム周期
    move_y = NumericProperty(1000) #ノーツのy軸上の位置
    text = StringProperty('Start')
    countgood = StringProperty('0')#kvファイル用に4つの変数分けています。わけないと1個の判定で全部に加算される動作が見られました。
    countgreat = StringProperty('0')
    countexcellent = StringProperty('0')
    countmiss = StringProperty('0')
    good = 0  # goodが出た回数のカウント
    great = 0  # greatが出た回数のカウント
    excellent = 0  # excellentが出た回数のカウント
    miss = 0  # missが出た回数のカウント
    dx = 5 #ノーツの落下速度
    def __init__(self, **kw):
        super(PlayScreen,self).__init__(**kw)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down = self._on_keyboard_down)
        #self._keyboard.bind(on_key_up = self._on_keyboard_up)

        #ノーツの描画処理
        with self.canvas:
            #ノーツの色設定
            Color(1,0,0,5,1)

            # レーンと行の設定(nレーン×m行(n=4or6, m=曲の長さ)分
            self.n = 4
            self.m = 30

            # ノーツを入れる二次元配列の初期設定
            self.rect = [[Rectangle(pos=(0,self.move_y-100),size=(0,0)) for column in range(self.m)] for row in range(self.n)]

            for l in range(self.n):
                #ノーツの描画
                # self.rect[l(=レーン番号)][0(=行の数)+3*l(=テストプログラム用の数(適当))] = 
                # Rectangle(pos=(200(=ノーツの横の長さ)*l(=レーンの数)+5*(l-1)(=レーンとレーンの隙間(5)) ,
                # 　　　　　　self.move_y+100(=ノーツの縦の長さ)*(0(=行の数)+3*l(=テストプログラム用の数(適当))),
                # 　　　　　　size=(200,100)(=ノーツの縦と横の長さ))
                self.rect[l][0+3*l] = Rectangle(pos=(200*l+5*(l-1) ,self.move_y+100*(0+3*l)),size=(200,100))
                self.rect[l][2+3*l] = Rectangle(pos=(200*l+5*(l-1) ,self.move_y+100*(2+3*l)),size=(200,100))
                self.rect[l][4+3*l] = Rectangle(pos=(200*l+5*(l-1) ,self.move_y+100*(4+3*l)),size=(200,100))
    
    def update(self, *args):
       #y軸上のノーツの位置を更新 
       self.move_y -= self.dx

       for l in range(self.n):
            #ノーツの描画
            # self.rect[l(=レーン番号)][0(=行の数)+3*l(=テストプログラム用の数(適当))].pos = 
            # 200(=ノーツの横の長さ)*l(=レーンの数)+5*(l-1)(=レーンとレーンの隙間(5)) ,
            # self.move_y+100(=ノーツの縦の長さ)*(0(=行の数)+3*l(=テストプログラム用の数(適当)))
            self.rect[l][0+3*l].pos = 200*l+5*(l-1) ,self.move_y+100*(0+3*l)
            self.rect[l][2+3*l].pos = 200*l+5*(l-1) ,self.move_y+100*(2+3*l)
            self.rect[l][4+3*l].pos = 200*l+5*(l-1) ,self.move_y+100*(4+3*l)
            
            #print(self.move_y+100*(0+3*0))
            #print(self.move_y+100*(2+3*l))
            #print(self.move_y+100*(4+3*l))

   
    def _keyboard_closed(self):
            self._keyboard.unbind(on_key_down = self._on_keyboard_down)
            self._keyboard = None
    
    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        #dfjkのキーボードを使う
        for i in range(0,self.n+1,2):
            if keycode[1] == 'd':
                if self.move_y+100*(i+3*0) > 0 and self.move_y+100*(i+3*0) <= 15:
                    self.excellent += 1
                    self.countexcellent = str(self.excellent)
                elif self.move_y+100*(i+3*0) > 15 and self.move_y+100*(i+3*0) <= 50:
                    self.great += 1
                    self.countgreat = str(self.great)
                elif self.move_y+100*(i+3*0) > 50 and self.move_y+100*(i+3*0) <= 100:
                    self.good += 1
                    self.countgood = str(self.good)
                elif self.move_y+100*(i+3*0) > 100 and self.move_y+100*(i+3*0) <= 125:
                    self.miss += 1
                    self.countmiss = str(self.miss)
                    

            if keycode[1] == 'f':
                if self.move_y+100*(i+3*1) > 0 and self.move_y+100*(i+3*1) <= 15:
                    self.excellent += 1
                    self.countexcellent = str(self.excellent)
                elif self.move_y+100*(i+3*1) > 15 and self.move_y+100*(i+3*1) <= 50:
                    self.great += 1
                    self.countgreat = str(self.great)
                elif self.move_y+100*(i+3*1) > 50 and self.move_y+100*(i+3*1) <= 100:
                    self.good += 1
                    self.countgood = str(self.good)
                elif self.move_y+100*(i+3*1) > 100 and self.move_y+100*(i+3*1) <= 125:
                    self.miss += 1
                    self.countmiss = str(self.miss)

            if keycode[1] == 'j':
                if self.move_y+100*(i+3*2) > 0 and self.move_y+100*(i+3*2) <= 15:
                    self.excellent += 1
                    self.countexcellent = str(self.excellent)
                elif self.move_y+100*(i+3*2) > 15 and self.move_y+100*(i+3*2) <= 50:
                    self.great += 1
                    self.countgreat = str(self.great)
                elif self.move_y+100*(i+3*2) > 50 and self.move_y+100*(i+3*2) <= 100:
                    self.good += 1
                    self.countgood = str(self.good)
                elif self.move_y+100*(i+3*2) > 100 and self.move_y+100*(i+3*2) <= 125:
                    self.miss += 1
                    self.countmiss = str(self.miss)

            if keycode[1] == 'k':
                if self.move_y+100*(i+3*3) > 0 and self.move_y+100*(i+3*3) <= 15:
                    self.excellent += 1
                    self.countexcellent = str(self.excellent)
                elif self.move_y+100*(i+3*3) > 15 and self.move_y+100*(i+3*3) <= 50:
                    self.great += 1
                    self.countgreat = str(self.great)
                elif self.move_y+100*(i+3*3) > 50 and self.move_y+100*(i+3*3) <= 100:
                    self.good += 1
                    self.countgood = str(self.good)
                elif self.move_y+100*(i+3*3) > 100 and self.move_y+100*(i+3*3) <= 125:
                    self.miss += 1
                    self.countmiss = str(self.miss)
                
    
            
       

    #ゲーム画面右下のStartボタンが押された時に実行される処理
    def start_game(self):
        #Startボタンのテキストを変更
        self.text = ''
        #update関数を一秒間に30回の周期で実行
        Clock.schedule_interval(self.update,self.dt)
        


sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(PlayScreen(name='play'))

class MyApp(App):
    def build(self):
        return sm
    
    
MyApp().run()
    
