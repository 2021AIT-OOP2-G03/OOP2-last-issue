from select import select
from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder

from kivy.graphics import *
from kivy.core.window import Window

from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.uix.label import Label
from kivy.uix.scatter import Scatter

from kivy.uix.popup import Popup

import sqlite3
import music_list


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
    music_list = ['aaa', 'bbb', 'ccc']
    # 曲名が格納されている要素と同じ要素番号にurl（画像）を格納
    music_image_url = ['images/music0.jpg',
                       'images/music1.jpg', 'images/music2.jpg']
    # game.kvで使用する変数（曲番号にあったurlが格納される）
    music_image = StringProperty()

    # 難易度を格納する変数
    # game.kvで使用する変数
    level = StringProperty()

    # １位２位３位のスコアを格納するための変数
    first_score = StringProperty()
    second_score = StringProperty()
    third_score = StringProperty()

    def __init__(self, **kwargs):
        super(HomeScreen, self).__init__(**kwargs)
        # 開始は曲番号０なので最初の曲を格納
        self.music_name = self.music_list[0]
        # 現在の曲番号のurlを格納
        self.music_image = self.music_image_url[0]
        self.level = ''

        print(Window.size)

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
        sql = "select score from 'oop2-last-issue' where music_name='" + \
            self.music_name + "' and mode='" + self.level + "'order by score desc"
        cur.execute(sql)

        # 取得したデータをscoreに格納
        for data in cur:
            score.append(data)
            # print(score)

        # game.kvで使用する変数に格納
        self.first_score = str(score[0][0])
        self.second_score = str(score[1][0])
        self.third_score = str(score[2][0])

        # クローズ
        con.close()

    # プレイボタンを選択した時にPlayScreenに曲名と難易度の情報を引き渡す
    def select_game(self, music_name, level):
        PlayScreen.music_name = music_name
        PlayScreen.level = level
        PlayScreen.first_score = self.first_score
        PlayScreen.second_score = self.second_score
        PlayScreen.third_score = self.third_score


class PlayScreen(Screen):

    # dt = 0  # フレーム周期
    # move_y = NumericProperty(1000)  # ノーツのy軸上の位置
    # text = StringProperty('Start')
    # dy = 0  # ノーツの落下速度
    # dist = 400
    # music_sound_url = ''  # 曲(.mp3)のファイルパス
    # melody = []  # 曲の01譜面
    # melody_comp = []  # 曲の01譜面のうち、各レーンごとの音符の座標をリスト化したもの(補足より)
    # sound = SoundLoader.load(music_sound_url)

    # 補足: melody -> melody_comp 変換の例
    '''
    [                           [
        [1,0,0,0,1,0,0,0],         [0,4],
        [0,1,0,0,0,0,1,0],  ->     [1,6],
        [0,0,1,0,0,1,0,0],         [2,5],
        [0,0,0,1,0,0,0,1],         [3,7],
    ]                           ]
    '''
    '''
    # HomeScreen().select_gameから選択される曲名と難易度
    music_name = ''
    level = ''

    rect = []
    '''

    '''
    def __init__(self, **kw):
        super().__init__(**kw)
    '''

    startisEnable = False

    dt = 1/30  # フレーム周期
    move_y = NumericProperty(1000)  # ノーツのy軸上の位置
    text = StringProperty('Start')
    # kvファイル用に4つの変数分けています。わけないと1個の判定で全部に加算される動作が見られました。
    countscore = StringProperty('0')
    countgood = StringProperty('0')
    countgreat = StringProperty('0')
    countexcellent = StringProperty('0')
    countmiss = StringProperty('0')
    countbad = StringProperty('0')
    good = 0  # goodが出た回数のカウント
    great = 0  # greatが出た回数のカウント
    excellent = 0  # excellentが出た回数のカウント
    miss = 0  # missが出た回数のカウント
    dy = 0  # ノーツの落下速度
    dist = 400
    # dx = 5 #ノーツの落下速度
    music_sound_url = ''  # 曲(.mp3)のファイルパス
    melody = []  # 曲の01譜面
    melody_comp = []  # 曲の01譜面のうち、各レーンごとの音符の座標をリスト化したもの(補足より)
    sound = SoundLoader.load(music_sound_url)
    # 補足: melody -> melody_comp 変換の例
    '''
    [                           [
        [1,0,0,0,1,0,0,0],         [0,4],
        [0,1,0,0,0,0,1,0],  ->     [1,6],
        [0,0,1,0,0,1,0,0],         [2,5],
        [0,0,0,1,0,0,0,1],         [3,7],
    ]                           ]
    '''
    
    # HomeScreen().select_gameから選択される曲名と難易度
    music_name = ''
    level = ''
    score = 0  # 合計スコア

    first_score = 0
    second_score = 0
    third_score = 0
    # 順位判定用

    rect = []

    def __init__(self, **kw):
        super(PlayScreen, self).__init__(**kw)
        self._keyboard = Window.request_keyboard(self._keyboard_closed, self)
        self._keyboard.bind(on_key_down=self._on_keyboard_down)
        #self._keyboard.bind(on_key_up = self._on_keyboard_up)

        # ノーツの描画処理
        with self.canvas:
            # ノーツの色設定
            Color(1, 0, 0, 5, 1)

            # レーンの限界幅及び、音符の限界長さを指定する
            self.limit_col = 6  # レーン幅
            self.limit_row = 5000
            

            # ノーツを入れる二次元配列の初期設定

            # self.rect = [[Rectangle(pos=(0,self.move_y),size=(0,0)) for column in range(self.m)] for row in range(self.n)]
            self.rect = [[Rectangle(pos=(0, 0), size=(0, 0)) for row in range(
                self.limit_row)] for col in range(self.limit_col)]

            '''
            self.rect = [[Rectangle(pos=(0,self.move_y-100),size=(0,0)) for column in range(self.m)] for row in range(self.n)]

            for l in range(self.n):
                #ノーツの描画
                # self.rect[l(=レーン番号)][0(=行の数)+3*l(=テストプログラム用の数(適当))] = 
                # Rectangle(pos=(200(=ノーツの横の長さ)*l(=レーンの数)+5*(l-1)(=レーンとレーンの隙間(5)) ,
                # self.move_y+100(=ノーツの縦の長さ)*(0(=行の数)+3*l(=テストプログラム用の数(適当))),
                # size=(200,100)(=ノーツの縦と横の長さ))
                self.rect[l][0+3*l] = Rectangle(pos=(200*l+5*(l-1) ,self.move_y+100*(0+3*l)),size=(200,100))
                self.rect[l][2+3*l] = Rectangle(pos=(200*l+5*(l-1) ,self.move_y+100*(2+3*l)),size=(200,100))
                self.rect[l][4+3*l] = Rectangle(pos=(200*l+5*(l-1) ,self.move_y+100*(4+3*l)),size=(200,100))
            '''


    def goukeinotes(self):
        count = 0
        for i in range(self.n):
            count += len(self.melody_comp[i])
        self.goukei_notes = count  
        return self.goukei_notes
        
        
    def update(self, *args):
        # y軸上のノーツの位置を更新
        self.move_y -= self.dy

        # print(self.move_y)
        #print(self.goukeinotes())
        for col in range(len(self.melody_comp)):
          
            # ノーツの描画
            # self.rect[l(=レーン番号)][0(=行の数)+3*l(=テストプログラム用の数(適当))].pos =
            # 200(=ノーツの横の長さ)*l(=レーンの数)+5*(l-1)(=レーンとレーンの隙間(5)) ,
            # self.move_y+100(=ノーツの縦の長さ)*(0(=行の数)+3*l(=テストプログラム用の数(適当)))

            for row in range(len(self.melody_comp[col])):
                self.rect[col][self.melody_comp[col][row]].pos = 200 * \
                    col, self.move_y+(self.dist*self.melody_comp[col][row])


        # 任意のノーツの座標の流れを確認できる(デバッグ用)
        # print(self.rect[0][0].pos, self.rect[3][3].pos)

        # コンフリクトが起きていたため片方コメントアウトしました。
            # print(self.move_y+(self.dist*self.melody_comp[col][1]))
        ''' 
            self.rect[l][0+3*l].pos = 200*l+5*(l-1) ,self.move_y+100*(0+3*l)
            self.rect[l][2+3*l].pos = 200*l+5*(l-1) ,self.move_y+100*(2+3*l)
            self.rect[l][4+3*l].pos = 200*l+5*(l-1) ,self.move_y+100*(4+3*l)

            #print(self.move_y+100*(0+3*0))
            #print(self.move_y+100*(2+3*l))
            #print(self.move_y+100*(4+3*l))
        '''
        
    def _keyboard_closed(self):
        self._keyboard.unbind(on_key_down=self._on_keyboard_down)
        self._keyboard = None

    def _on_keyboard_down(self, keyboard, keycode, text, modifiers):
        # dfjkのキーボードを使う
        for i in range(len(self.melody_comp[0])):
            if keycode[1] == 'd':
                if self.move_y+(self.dist*self.melody_comp[0][i]) > 0 and self.move_y+(self.dist*self.melody_comp[0][i]) <= 15:
                    self.excellent += 1
                    self.countexcellent = str(self.excellent)
                    self.score += 50
                    self.countscore = str(self.score)
                    self.delete(0, i)  # delete
                elif self.move_y+(self.dist*self.melody_comp[0][i]) > 15 and self.move_y+(self.dist*self.melody_comp[0][i]) <= 50:
                    self.great += 1
                    self.countgreat = str(self.great)
                    self.score += 30
                    self.countscore = str(self.score)
                    self.delete(0, i)  # delete
                elif self.move_y+(self.dist*self.melody_comp[0][i]) > 50 and self.move_y+(self.dist*self.melody_comp[0][i]) <= 100:
                    self.good += 1
                    self.countgood = str(self.good)
                    self.score += 10
                    self.countscore = str(self.score)
                    self.delete(0, i)  # delete
                elif self.move_y+(self.dist*self.melody_comp[0][i]) > 100 and self.move_y+(self.dist*self.melody_comp[0][i]) <= 125:
                    self.miss += 1
                    self.countmiss = str(self.miss)
                    self.countscore = str(self.score)
                    self.delete(0, i)  # delete

        for i in range(len(self.melody_comp[1])):
            if keycode[1] == 'f':
                if self.move_y+(self.dist*self.melody_comp[1][i]) > 0 and self.move_y+(self.dist*self.melody_comp[1][i]) <= 15:
                    self.excellent += 1
                    self.countexcellent = str(self.excellent)
                    self.score += 50
                    self.countscore = str(self.score)
                    self.delete(1, i)  # delete
                elif self.move_y+(self.dist*self.melody_comp[1][i]) > 15 and self.move_y+(self.dist*self.melody_comp[1][i]) <= 50:
                    self.great += 1
                    self.countgreat = str(self.great)
                    self.score += 30
                    self.countscore = str(self.score)
                    self.delete(1, i)  # delete
                elif self.move_y+(self.dist*self.melody_comp[1][i]) > 50 and self.move_y+(self.dist*self.melody_comp[1][i]) <= 100:
                    self.good += 1
                    self.countgood = str(self.good)
                    self.score += 10
                    self.countscore = str(self.score)
                    self.delete(1, i)  # delete
                elif self.move_y+(self.dist*self.melody_comp[1][i]) > 100 and self.move_y+(self.dist*self.melody_comp[1][i]) <= 125:
                    self.miss += 1
                    self.countmiss = str(self.miss)
                    self.countscore = str(self.score)
                    self.delete(1, i)  # delete

        for i in range(len(self.melody_comp[2])):
            if keycode[1] == 'j':
                if self.move_y+(self.dist*self.melody_comp[2][i]) > 0 and self.move_y+(self.dist*self.melody_comp[2][i]) <= 15:
                    self.excellent += 1
                    self.countexcellent = str(self.excellent)
                    self.score += 50
                    self.countscore = str(self.score)
                    self.delete(2, i)  # delete
                elif self.move_y+(self.dist*self.melody_comp[2][i]) > 15 and self.move_y+(self.dist*self.melody_comp[2][i]) <= 50:
                    self.great += 1
                    self.countgreat = str(self.great)
                    self.score += 30
                    self.countscore = str(self.score)
                    self.delete(2, i)  # delete
                elif self.move_y+(self.dist*self.melody_comp[2][i]) > 50 and self.move_y+(self.dist*self.melody_comp[2][i]) <= 100:
                    self.good += 1
                    self.countgood = str(self.good)
                    self.score += 10
                    self.countscore = str(self.score)
                    self.delete(2, i)  # delete
                elif self.move_y+(self.dist*self.melody_comp[2][i]) > 100 and self.move_y+(self.dist*self.melody_comp[2][i]) <= 125:
                    self.miss += 1
                    self.countmiss = str(self.miss)
                    self.countscore = str(self.score)
                    self.delete(2, i)  # delete
                    
        for i in range(len(self.melody_comp[3])):
            if keycode[1] == 'k':
                if self.move_y+(self.dist*self.melody_comp[3][i]) > 0 and self.move_y+(self.dist*self.melody_comp[3][i]) <= 15:
                    self.excellent += 1
                    self.countexcellent = str(self.excellent)
                    self.score += 50
                    self.countscore = str(self.score)
                    self.delete(3, i)  # delete
                elif self.move_y+(self.dist*self.melody_comp[3][i]) > 15 and self.move_y+(self.dist*self.melody_comp[3][i]) <= 50:
                    self.great += 1
                    self.countgreat = str(self.great)
                    self.score += 30
                    self.countscore = str(self.score)
                    self.delete(3, i)  # delete
                elif self.move_y+(self.dist*self.melody_comp[3][i]) > 50 and self.move_y+(self.dist*self.melody_comp[3][i]) <= 100:
                    self.good += 1
                    self.countgood = str(self.good)
                    self.score += 10
                    self.countscore = str(self.score)
                    self.delete(3, i)  # delete
                elif self.move_y+(self.dist*self.melody_comp[3][i]) > 100 and self.move_y+(self.dist*self.melody_comp[3][i]) <= 125:
                    self.miss += 1
                    self.countmiss = str(self.miss)
                    self.countscore = str(self.score)
                    self.delete(3, i)  # delete

    # ゲーム画面右下のStartボタンが押された時に実行される処理
    def start_game(self):
        # Startボタンのテキストを変更
        self.text = ''

        # 曲名と難易度を入力して、フレーム周期と移動速度とノーツ間の距離と曲のパスと譜面を取得
        # self.dt, self.dy, self.dist, self.music_sound_url, self.melody = music_list.get_melody(self.music_name,self.level)
        self.dt, self.dy, self.dist, self.music_sound_url, self.melody = music_list.get_melody(
            self.music_name, self.level)

        # パスにある曲を読み込む
        self.sound = SoundLoader.load(self.music_sound_url)

        # レーンと行の設定(nレーン×m行(n=4or6, m=曲の長さ)分
        self.n = len(self.melody)
        self.m = len(self.melody[0])

        # ノーツの横幅
        # width = Window.size[0] / (2*self.n)

        print(self.music_name, self.level)
        print(self.dt, self.dy, self.dist, self.music_sound_url)
        print(self.n, self.m)
        
        with self.canvas:
            # ノーツの色設定
            Color(1, 0, 0, 5, 1)
            for col in range(self.n):
                # melody_compのレーンを追加する
                self.melody_comp.append([])
                for row in range(self.m):
                    # ノーツの描画
                    # self.rect[l(=レーン番号)][0(=行の数)+3*l(=テストプログラム用の数(適当))] =
                    # Rectangle(pos=(200(=ノーツの横の長さ)*l(=レーンの数)+5*(l-1)(=レーンとレーンの隙間(5)) ,
                    # 　　　　　　self.move_y+100(=ノーツの縦の長さ)*(0(=行の数)+3*l(=テストプログラム用の数(適当))),
                    # size=(200,100)(=ノーツの縦と横の長さ))
                    # self.rect[col(=レーン番号)][row(=行)]
                    if self.melody[col][row] == 1:
                        # self.rect.append(Rectangle(pos=(width*col,self.move_y),size=(width,100)))
                        self.rect[col][row] = Rectangle(
                            pos=(200*col+10*(col-1), self.move_y+(self.dist*row)), size=(200, 100))

                        # それぞれのレーンで音符が合った座標を追加する
                        self.melody_comp[col].append(row)
                        # print(col, row, self.rect[col][row].pos) # 音符のある座標を出力する(デバッグ用)

                    # self.rect[l][0+3*l] = Rectangle(pos=(200*l+5*(l-1) ,self.move_y+100*(0+3*l)),size=(200,100))
                    # self.rect[l][2+3*l] = Rectangle(pos=(200*l+5*(l-1) ,self.move_y+100*(2+3*l)),size=(200,100))
                    # self.rect[l][4+3*l] = Rectangle(pos=(200*l+5*(l-1) ,self.move_y+100*(4+3*l)),size=(200,100))
            print(self.melody_comp) # melody_compの結果を出力する(デバッグ用)

        # 曲が無事ロードされていれば曲を流す
        if self.sound:
            self.sound.play()

            # update関数を一秒間に1/dt回の周期で実行
            self.event = Clock.schedule_interval(self.update, self.dt)


    # ゲーム画面右下のBackボタンが押された時に実行される処理
    def end_game(self):
        # 音楽が再生されていれば
        if self.sound:
            #  音を止める
            self.sound.stop()

            # Clockを停止させる
            self.event.cancel()
        
        # Startボタンのテキストを元に戻す
        self.text = "Start"
       
        
        # self.rect = [[Rectangle(pos=(0, 0), size=(0, 0)) for row in range(
        #         self.limit_row)] for col in range(self.limit_col)]

        for col in range(len(self.melody_comp)):
            for row in range(len(self.melody_comp[col])):
                # self.rect[col][row] = Rectangle(pos=(0, 0), size=(0, 0))
                self.rect[col][row].size=0,0
                self.delete(col,row)


        # for i in range(0, 2):
        #         for j in range(0, 4):
        #             if self.move_y+(self.dist*self.melody_comp[j][i]) > -150:
        #                 self.delete(j, i)

        # ハイスコアを更新
        self.High_Score

        # まずはmelody_comp関数をクリア
        self.melody_comp.clear()

        self.move_y = 1000



    # ノーツを消す処理
    def delete(self, row, number):
        # 当たり判定があった時にノーツを消します。
        # ノーツを消すことのよって多重判定を回避します。
        # row=レーン番号　number=行の数　※ここの引数は基本的にノーツの描画と同じものになっています。
        # print('ok')
        self.canvas.remove(
            self.rect[row][self.melody_comp[row][number]])

    """ 
        作業時メモ
    
    下のコードだとノーツが止まる
        self.rect[0][i+3*0] = Rectangle(pos=(0,self.move_y-100),size=(0,0))
                    
    ノーツをぶっ飛ばす方法。これだと列全体が下に下がってダメになってしまう。
        #self.move_y = self.move_y+100*(i+3*0) - 500
    """

    def High_Score(self):
        # print(self.music_name, self.level, self.score)
        # 押されたラベルの難易度を格納

        # 接続処理, カーソルオブジェクトを取得
        con = sqlite3.connect('score.db')
        cur = con.cursor()

        # 仮実装、曲名と難易度、スコアを挿入
        con.execute('insert into "oop2-last-issue" values(?,?,?)', [
            self.music_name, self.level, self.score])
        con.commit()

        # スコアのソーティング

        cur.execute('select * from "oop2-last-issue" where music_name =? and mode =? order by score desc limit 3', [
            self.music_name, self.level])

        # クローズ
        con.close()

    def popup_open(self):
        PopupMenu.score = self.score
        self.popup_result()
        content = PopupMenu(popup_close=self.popup_close)
        self.popup = Popup(title='Result', content=content,
                           size_hint=(0.5, 0.5), auto_dismiss=False)
        self.popup.open()

    def popup_result(self):
        if int(self.score) > int(self.first_score):
            PopupMenu.result = 'Congratulations!\nYou got a 1st Place!'
        elif int(self.score) > int(self.second_score) and int(self.score) < int(self.first_score):
            PopupMenu.result = 'Congratulations!\nYou got a 2nd Place!'
        elif int(self.score) > int(self.third_score) and int(self.score) < int(self.second_score):
            PopupMenu.result = 'Congratulations!\nYou got a 3rd Place!'
        else:
            PopupMenu.result = 'You did not enter the top 3 scores,\nbut nice job! Try better next time!'

    def popup_close(self):
        self.popup.dismiss()
        self.end_game()
        self.manager.current = 'home'


class PopupMenu(BoxLayout):
    score = 0
    result = ''
    popup_close = ObjectProperty()


sm = ScreenManager()
sm.add_widget(HomeScreen(name='home'))
sm.add_widget(PlayScreen(name='play'))


class MyApp(App):
    def build(self):
        return sm


MyApp().run()
