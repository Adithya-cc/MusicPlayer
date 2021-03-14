from tkinter import filedialog
import time
import tkinter as tk
import os
import sys
from PyQt5 import QtWidgets, QtCore
from mutagen.mp3 import MP3
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from pygame import mixer

mixer.init()
mixer.music.set_volume(1)
stat = "pl"
song_list = os.listdir()
global select
select = ""


def play_time():
    current_time = mixer.music.get_pos()
    print(current_time)

vp = False
fp = False

class Player(QMainWindow):
    def __init__(self):
        super(Player, self).__init__()
        loadUi("Player.ui", self)
        self.PauseB.clicked.connect(lambda: self.pause())
        self.PlayB.clicked.connect(lambda: self.play())
        self.StopB.clicked.connect(lambda: self.stop())
        self.selectbtn.clicked.connect(lambda: self.add_song())
        self.sound.clicked.connect(lambda: self.volumepop())
        self.fav_list.clicked.connect(lambda: self.fav_pop())
        self.add_fav.clicked.connect(lambda: self.fav_add())
        self.song_list.clicked.connect(lambda: self.play_list_play())
        self.fav_list_2.clicked.connect(lambda: self.fav_list_play())
        self.volumeslider.valueChanged.connect(lambda: self.volumecontrole())
        self.songlabel.setText(select)
        self.widget_fav.setVisible(False)
        self.volumeslider.setVisible(False)
        self.PlayB.setVisible(True)
        self.PauseB.setVisible(True)

    def add_song(self):
        root = tk.Tk()
        root.withdraw()
        song = filedialog.askopenfilename(title="Select a song", filetypes=(("mp3 files", "*.mp3"),))
        global select
        select = str(song)
        print(select)
        self.songlabel.setText(select)
        self.song_list.insertItem(0, song)
        self.PauseB.setVisible(True)
        self.PlayB.setVisible(True)

    def play_time(self):
        global current_time
        current_time = mixer.music.get_pos()//100
        song = curr_song
        song = f'{song}'
        song_mut = MP3(song)
        song_length =song_mut.info.length
        print(type(song_length), song_length)
        self.timeplay_slider.setMinimum(0)
        self.timeplay_slider.setMaximum(int(song_length*10))
        print(type(current_time))
        t = int(song_length)
        ctime = time.strftime('%M:%S', time.gmtime(int(current_time//10)))
        curr_time = time.strftime('%M:%S', time.gmtime(t))
        curr_time = str(curr_time)
        print(curr_time)
        self.time_2.setText(ctime)
        self.time.setText(curr_time)
        #self.timeplay_slider.setValue(0)
        self.timeplay_slider.setValue(current_time)
        QtCore.QTimer.singleShot(100, self.play_time)


    def play_list_play(self):
        song = str(self.song_list.currentItem().text())
        self.stop()
        global select
        select = str(song)
        mixer.music.load(song)
        mixer.music.play()
        global curr_song
        curr_song = str(song)
        self.play_time()
        self.PauseB.setVisible(True)
        self.songlabel.setText(song)

    def fav_list_play(self):
        song = str(self.fav_list_2.currentItem().text())
        self.stop()
        global select
        select = str(song)
        mixer.music.load(song)
        mixer.music.play()
        self.PauseB.setVisible(True)
        self.songlabel.setText(song)


    def fav_pop(self):
        if fp == False:
            self.widget_fav.setVisible(True)
            self.nexf()
        elif fp == True:
            self.widget_fav.setVisible(False)
            self.nextff()
    def nexf(self):
        global fp
        fp = True
    def nextff(self):
        global fp
        fp = False


    def volumepop(self):
        if vp == False:
            self.volumeslider.setVisible(True)
            self.nex()
        elif vp == True:
            self.volumeslider.setVisible(False)
            self.nextf()
    def nex(self):
        global vp
        vp = True
    def nextf(self):
        global vp
        vp = False

    def fav_add(self):
        fav_song = select
        if fav_song != "":
            self.fav_list_2.insertItem(0, fav_song)

    def volumecontrole(self):
        volume_value=str(self.volumeslider.value())
        if volume_value != 0.0:
            mixer.music.set_volume(int(volume_value)/10)
        elif volume_value == 0.0:
            mixer.music.set_volume(0)

    def pause(self):
        self.PauseB.setVisible(False)
        self.PlayB.setVisible(True)
        print("pause")
        mixer.music.pause()

    def play(self):
        print("play")
        self.PlayB.setVisible(False)
        self.PauseB.setVisible(True)
        play_time()
        mixer.music.unpause()

    def stop(self):
        print("stopped")
        self.PauseB.setVisible(False)
        self.PlayB.setVisible(True)
        mixer.music.stop()





app = QApplication(sys.argv)
mainwindow = Player()
widget = QtWidgets.QStackedWidget()
widget.addWidget(mainwindow)
widget.setFixedWidth(700)
widget.setFixedHeight(600)
widget.show()
try:
    sys.exit(app.exec_())
except:
    print("Exiting")

while False:
    print("P to pause, r to resume, s to stop")
    get = input(">>> ")
    if get == "p":
        mixer.music.pause()
    if get == "r":
        mixer.music.unpause()
    if get == "s":
        mixer.music.stop()
