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
    dx = 5 #ノーツの落下速度

    def __init__(self, **kw):
        super().__init__(**kw)
        #ノーツの描画処理
        with self.canvas:
            #ノーツの色設定
            Color(1,0,0,5,1)

            # レーンと行の設定(nレーン×m行(n=4or6, m=曲の長さ)分
            self.n = 4
            self.m = 30

            # #ノーツの描画
            # self.rect1 = Rectangle(pos=(100,self.move_y),size=(100,50))

            # #ノーツの描画
            # self.rect2 = Rectangle(pos=(300,self.move_y + 10),size=(100,50))

            self.rect = [[Rectangle(pos=(0,self.move_y-100),size=(0,0)) for column in range(self.m)] for row in range(self.n)]

            for l in range(self.n):
                #ノーツの描画
                self.rect[l][0+3*l] = Rectangle(pos=(100*l+10*(l-1) ,self.move_y+50*(0+3*l)),size=(100,50))
                self.rect[l][10+3*l] = Rectangle(pos=(100*l+10*(l-1) ,self.move_y+50*(10+3*l)),size=(100,50))
                self.rect[l][20+3*l] = Rectangle(pos=(100*l+10*(l-1) ,self.move_y+50*(20+3*l)),size=(100,50))

    def update(self, *args):
       #y軸上のノーツの位置を更新 
       self.move_y -= self.dx

       for l in range(self.n):
            #ノーツの描画
            self.rect[l][0+3*l].pos = 100*l+10*(l-1) ,self.move_y+50*(0+3*l)
            self.rect[l][10+3*l].pos = 100*l+10*(l-1) ,self.move_y+50*(10+3*l)
            self.rect[l][20+3*l].pos = 100*l+10*(l-1) ,self.move_y+50*(20+3*l)
       

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
    
