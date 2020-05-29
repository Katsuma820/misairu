# misairu
python プログラム

import tkinter #tkinterモジュールをインポート
import random #randomモジュールをインポート
import os

#fontの定義
fnt1 = ("Timer New Roman", 24)
fnt2 = ("Timer New Roman", 50)
index = 0
timer = 0
score = 0
bg_pos = 0 #背景の表示位置用の変数
px = 240 #プレイヤーのx座標の変数
py = 540 #プレイヤーのy座標の変数
METEO_MAX = 30 #流星の数
#流星のx,y座標を管理するリスト
mx = [0]*METEO_MAX
my = [0]*METEO_MAX

#キーの値を代入する変数
key = ""
#キーが離されたときに使う変数
koff = False

#keyが押されたときに実行する関数
def key_down(e):
    global key, koff
    key = e.keysym #keyにkeysymを代入
    koff = False

#keyが離されたときに実行する関数
def key_up(e):
    global koff
    koff = True

#main処理を行う
def main():
    global key, koff, index, timer, score, bg_pos, px
    timer = timer + 1
    bg_pos = (bg_pos + 1)%640 #背景の描画位置の計算
    canvas.delete("SCREEN") #いったん画面上全ての絵や文字をdelete
    canvas.create_image(240, bg_pos-320, image=img_bg, tag="SCREEN")
    canvas.create_image(240, bg_pos+320, image=img_bg, tag="SCREEN")

    #index0の処理　タイトル文字を表示
    if index == 0:
        canvas.create_text(240, 240, text="METEOR", fill="gold", font=fnt2, tag="SCREEN")
        canvas.create_text(240, 480, text="Press [SPACE] Key", fill="lime", font=fnt1, tag="SCREEN")
        if key == "space": #スペースkeyが押されたらscoreを0にする
            #scoreを0にする、宇宙船の位置を画面中央にする
            score = 0
            px = 240

            #流星の座標に初期値を入れる
            init_enemy()
            index = 1
    #index1の処理（ゲーム中）
    if index == 1:
        score = score + 1
        move_player() #宇宙船を動かす
        move_enemy() #流星を動かす
    if index == 2:
        move_enemy()
        canvas.create_text(240, timer*4, text="GAMEOVER", fill="red", font=fnt2, tag="SCREEN")
        if timer == 60:
            index = 0
            timer = 0
    canvas.create_text(240, 30, text="SCORE" + str(score), fill="white", font=fnt1, tag="SCREEN")
    if koff == True:
        key = " "
        koff = False
    root.after(50, main)

def hit_check(x1, y1, x2, y2):
    if((x1-x2)*(x1-x2) + (y1-y2)*(y1-y2) < 36*36):
        return True
    return False

def init_enemy():
    for i in range(METEO_MAX):
        mx[i] = random.randint(0, 480)
        my[i] = random.randint(-640, 0)

def move_enemy():
    global index, timer
    for i in range(METEO_MAX):
        my[i] = my[i] + 6+i/5
        if my[i] > 660:
            mx[i] = random.randint(0, 480)
            my[i] = random.randint(-640, 0)
        if index == 1 and hit_check(px, py, mx[i], my[i]) == True:
            index = 2
            timer = 0
        canvas.create_image(mx[i], my[i], image=img_enemy, tag="SCREEN")

def move_player():
    global px
    if key == "Left" and px > 30:
        px = px - 10
    if key == "Right" and px < 450:
        px = px + 10
    canvas.create_image(px, py, image=img_player[timer%2], tag="SCREEN")

img_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "stat0.png"))
img_path1 = os.path.abspath(os.path.join(os.path.dirname(__file__), "starship1.png"))
img_path2 = os.path.abspath(os.path.join(os.path.dirname(__file__), "meteo.png"))
img_path3 = os.path.abspath(os.path.join(os.path.dirname(__file__), "cosmo.png"))


root = tkinter.Tk()
root.title("Mini Game")
root.bind("<KeyPress>", key_down)
root.bind("<KeyRelease>", key_up)
canvas = tkinter.Canvas(width=480, height=640)
canvas.pack()
img_player = [
    tkinter.PhotoImage(file=img_path),
    #tkinter.PhotoImage(file="./stat0.png"),
    tkinter.PhotoImage(file=img_path1)
    #tkinter.PhotoImage(file="starship1.png")
]
img_enemy = tkinter.PhotoImage(file=img_path2)
img_bg = tkinter.PhotoImage(file=img_path3)
main()
root.mainloop()
