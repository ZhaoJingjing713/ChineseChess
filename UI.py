import sys
#from typing import get_args
import config
import numpy as np
from PyQt5 import QtWidgets
import pygame
from PyQt5 import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from board import *
#TODO:更改import*写法
import globalvar as gl
from online import *
import threading
import time
from NN import Net
from MCTS import MCTS

Init_stone_dict=gl.get_value('Init_stone_dict')
Init_stone_pos=gl.get_value('Init_stone_pos')
Board_pos=gl.get_value('Board_pos')
error_range=gl.get_value('error_range')

#TODO  加入音乐按钮

class music:
    def __init__(self) :
        pygame.init()
        self.sound_running=False
        self.path='music\\chess.mp3'
    def loop_play(self):
        while(1):
            pygame.mixer.music.play()
            pygame.time.delay(5)
    def play(self):
        pygame.mixer.music.load(self.path)
        self.sound_running=True
        self.loop_play()
    def stop(self):
        self.sound_running=False
        pygame.mixer.music.stop()
   



class main_UI(QWidget,music):
    def __init__(self,width=1280,high=720):
        super().__init__()
        self.width=width
        self.high=high
        self.button_width=128
        self.button_high=42
        self.button_space=70
        self.button_color_deepth=1
        self.initUI()
    def initUI(self):
#绘制主界面
        self.resize(self.width,self.high)
        self.center()
        self.setWindowTitle("Chinese Chess")
        self.setWindowIcon(QIcon("image\\icon.png"))
        palette_menu=QPalette()
        palette_menu.setBrush(QPalette.Background, QBrush(QPixmap("./image/menu.jpg")))
        palette_PVP=QPalette()
        palette_PVP.setBrush(QPalette.Background, QBrush(QPixmap("./image/bord.jpg")))
        # palette_PVC=QPalette()
        # palette_PVC.setBrush(QPalette.Background, QBrush(QPixmap("./image/menu.jpg")))
        
        self.setPalette(palette_menu)
        self.music=music()


        op0 = QGraphicsOpacityEffect()
        op1 = QGraphicsOpacityEffect()
        op2 = QGraphicsOpacityEffect()
# 设置透明度的值，0.0到1.0，最小值0是透明，1是不透明
        op0.setOpacity(self.button_color_deepth)
        op1.setOpacity(self.button_color_deepth)
        op2.setOpacity(self.button_color_deepth)

#PvP按钮
        PvP_button=QPushButton("PvP",self)
        PvP_button.setStyleSheet('background-color: rgb(		245,222,179);border-radius: 10px; border: 2px groove gray;border-style: outset;')
        PvP_button.setGeometry(QtCore.QRect(self.width//2-self.button_width//2,self.high//2+50,self.button_width,self.button_high))
        PvP_button.setGraphicsEffect(op1)
        PvP_button.clicked.connect(self.PvP_clicked)

#TODO  加入音乐按钮
#music按钮
        # music_button=QPushButton("music",self)
        # music_button.setStyleSheet('background-color: rgb(		245,222,179);border-radius: 10px; border: 2px groove gray;border-style: outset;')
        # music_button.setGeometry(QtCore.QRect(self.width-self.button_width-50,self.high-50,self.button_width,self.button_high))
        # music_button.setGraphicsEffect(op1)
        # music_button.clicked.connect(self.music_clicked)

#TODO 加入人机对战
# #PvC按钮
        PvC_button=QPushButton("PvC",self)
        PvC_button.setStyleSheet('background-color: rgb(			245,222,179);border-radius: 10px; border: 2px groove gray;border-style: outset;')
        PvC_button.setGeometry(QtCore.QRect(self.width//2-self.button_width//2,self.high//2+50+self.button_space,self.button_width,self.button_high))
        PvC_button.setGraphicsEffect(op2)
        PvC_button.clicked.connect(self.PvC_clicked)
#退出按钮
        quit_button=QPushButton('退出',self)
        quit_button.setStyleSheet('background-color: rgb(		245,222,179);border-radius: 10px; border: 2px groove gray;border-style: outset;')
        quit_button.setGeometry(QtCore.QRect(self.width//2-self.button_width//2,self.high//2+50+2*self.button_space,self.button_width,self.button_high))
        quit_button.setGraphicsEffect(op0)
        quit_button.clicked.connect(QCoreApplication.instance().quit)

        self.PvP_button=PvP_button
        # self.PvC_button=PvC_button
        self.quit_button=quit_button
        
        self.show()

#TODO 加入音乐
    # def music_clicked(self):
    #     if(self.music.sound_running):
    #         self.music.stop()
    #     else:
    #         self.music.play()

#PvP点击函数

    def PvP_clicked(self):
        self.hide()
        self.ui = PvP_UI()               
        self.ui.show()
    def PvC_clicked(self):
        self.hide()
        self.ui = board_UI(mode='PvC')               

#界面中心显示
    def center(self):
        window=self.frameGeometry()
        center_point=QDesktopWidget().availableGeometry().center()
        window.moveCenter(center_point)
        self.move(window.topLeft())

#PvP界面，继承main_UI类
class PvP_UI(main_UI):
    def __init__(self):
        super().__init__()
        self.initUI()
    def initUI(self):
#绘制主界面
        self.resize(self.width,self.high)
        self.center()
        self.setWindowTitle("Chinese Chess")
        self.setWindowIcon(QIcon("image\\icon.png"))
        palette=QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("./image/PVP_menu.jpg")))
        self.setPalette(palette)
#返回主菜单
        back_button=QPushButton("返回",self)
        back_button.setStyleSheet('background-color: rgb(245,222,179);border-radius: 10px; border: 2px groove gray;border-style: outset;')
        back_button.setGeometry(QtCore.QRect(self.width//2-self.button_width//2,self.high//2+50+2*self.button_space,self.button_width,self.button_high))
        back_button.clicked.connect(self.back_clicked)
#本地对战
        local_button=QPushButton("本地对战",self)
        local_button.setStyleSheet('background-color: rgb(245,222,179);border-radius: 10px; border: 2px groove gray;border-style: outset;')
        local_button.setGeometry(QtCore.QRect(self.width//2-self.button_width//2,self.high//2+50+self.button_space,self.button_width,self.button_high))
        local_button.clicked.connect(self.local_clicked)
#局域网联机
        Online_button=QPushButton("局域网联机",self)
        Online_button.setStyleSheet('background-color: rgb(245,222,179);border-radius: 10px; border: 2px groove gray;border-style: outset;')
        Online_button.setGeometry(QtCore.QRect(self.width//2-self.button_width//2,self.high//2+50,self.button_width,self.button_high))
        Online_button.clicked.connect(self.online_clicked)

    def back_clicked(self):
        self.hide()
        self.ui = main_UI()              
        self.ui.show()
    def local_clicked(self):
        self.hide()
        self.ui = board_UI()     
        # self.ui.initUI()       
        # self.ui.show()
    def online_clicked(self):
        self.hide()
        self.ui=PvP_Online_UI()
        #self.ui=board_UI("PVP_online")
        self.ui.show()

class PvP_Online_UI(PvP_UI):
    def __init__(self):
        super().__init__()  
#绘制主界面
        self.resize(self.width,self.high)
        self.center()
        self.setWindowTitle("Chinese Chess")
        self.setWindowIcon(QIcon("image\\icon.png"))
        palette=QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("./image/PVP_menu.jpg")))
        self.setPalette(palette)
#返回主菜单
        back_button=QPushButton("返回",self)
        back_button.setStyleSheet('background-color: rgb(245,222,179);border-radius: 10px; border: 2px groove gray;border-style: outset;')
        back_button.setGeometry(QtCore.QRect(self.width//2-self.button_width//2,self.high//2+50+2*self.button_space,self.button_width,self.button_high))
        back_button.clicked.connect(self.back_clicked)
#建立棋局
        build_button=QPushButton("建立棋局",self)
        build_button.setStyleSheet('background-color: rgb(245,222,179);border-radius: 10px; border: 2px groove gray;border-style: outset;')
        build_button.setGeometry(QtCore.QRect(self.width//2-self.button_width//2,self.high//2+50+self.button_space,self.button_width,self.button_high))
        build_button.clicked.connect(self.build_clicked)
#加入棋局
        join_button=QPushButton("加入棋局",self)
        join_button.setStyleSheet('background-color: rgb(245,222,179);border-radius: 10px; border: 2px groove gray;border-style: outset;')
        join_button.setGeometry(QtCore.QRect(self.width//2-self.button_width//2,self.high//2+50,self.button_width,self.button_high))
        join_button.clicked.connect(self.join_clicked)

    def back_clicked(self):
        self.hide()
        self.ui = main_UI()              
        self.ui.show()
    def build_clicked(self):
        self.hide()
        self.ui = board_UI(mode='PvP_online',status='service')         
        #self.ui.show()
    def join_clicked(self):
        ip, ok=QInputDialog.getText(self, 'input', '输入对方ip：')
        if ok and ip:
            self.hide()
            self.ui=board_UI('PvP_online',ip,'client')
            #self.ui.show()


#棋盘UI
class board_UI(QWidget):
    moveSignal=pyqtSignal()
    endSignal=pyqtSignal()
    def __init__(self,mode='PvP_local',ip='',status='service'):
        super().__init__()

#实现多线程
        global online_move
        online_move=False
        self.thread = Mythread()
#UI相关
        self.winner=''
        self.need_to_operator=True
        self.game_finished=False
        self.currentPlayer='red'
        self.width=1280
        self.high=720
        self.button_width=128
        self.button_high=42
        self.button_space=70
        self.button_color_deepth=1
#网络相关
        self.has_player=-1          #-1初始，本地值   0假 1真
        self.mode=mode
        self.status=status
        self.ip=ip
        self.online_op_move_one_step=False
#TODO 如果不成功，修改这里，以及后面创建self.service()/client()部分
        self.service=service()
        self.client=client(self.ip)
#棋子相关
        self.currentStone=""
        self.currentPos=[]
        self.nextPos=[]
#模式初始化
        self.initUI()

        if(self.mode=='PvP_local'):
            self.board=Board(1,2)   #1,2表示PvP_local, 1,3表示PvP_online，1,0表示PvC
        elif(self.mode=='PvP_online'):
            self.board=Board(1,3)
            if(self.status=='service'):
                #self.service=service()
                self.ip=self.service.ip
                QMessageBox.information(self, "Info", "本机ip："+self.ip )
            elif(self.status=='client'):
                #self.client=client(self.ip)
                online_move=True
                self.need_to_operator=False
            while(True):
                self.wait_player()
                if(self.has_player==1):
                    back2menu=False
                    break
                elif(self.has_player==0):
                    if(QMessageBox.question(self, "Warning", "未等到玩家，是否继续？", QMessageBox.Yes | QMessageBox.No)==QMessageBox.Yes):
                        continue
                    else:
                        self.back_clicked()
                        back2menu=True
                        break
            if(back2menu==False):
                threading._start_new_thread(self.interrupt)   #子线程判断是否连接中断
#TODO 解决接收信息问题
#2021.7.8目前通过多线程解决，但是需要等对方操作结束后一并显示，原因可能是QT的update和show的关系

                self.thread.updateSignal.connect(self.receive_info)
                self.thread.start()
        elif(self.mode=='PvC'):
            self.board = Board(1, 0)
            self.net = Net('./best_policy_1900.model')
            self.mcts = MCTS(self.net, self.board)
            self.AI_Turn=True
            self.AI_move()

    def initUI(self):
#绘制主界面
        self.num=0
        self.start=False
        self.label = QLabel('红棋先下\t\t\n\n', self)
        self.resize(self.width,self.high)
        self.center()
        self.setWindowTitle("Chinese Chess")
        self.setWindowIcon(QIcon("image\\icon.png"))
        palette=QPalette()
        palette.setBrush(QPalette.Background, QBrush(QPixmap("./image/board.jpg")))
        self.setPalette(palette)
#返回主菜单
        back_button=QPushButton("返回主菜单",self)
        back_button.setStyleSheet('background-color: rgb(245,222,179);border-radius: 10px; border: 2px groove gray;border-style: outset;')
        back_button.setGeometry(QRect(self.width-self.button_width-self.button_space,self.high-self.button_space,self.button_width,self.button_high))
        back_button.clicked.connect(self.back_clicked)

        if(self.start==False):
            self.drawStone()
        self.show()

#返回主菜单
    def back_clicked(self):
        if(self.mode=='PvP_online'):
            if(self.status=='service'):
                self.service.close()
            else:
                self.client.close()
        self.hide()
        self.ui = main_UI()              
        self.ui.show()

#画出棋子
    def drawStone(self):
        self.mp=[]
        self.op=[]
        for i in range(16):
            self.mp.append(QLabel(self))
            self.op.append(QLabel(self))
        for i in range(len(Init_stone_pos)):
            print(i)
            pos=Init_stone_pos[i]
            if(i<16):
                str='image\\stone\\'+Init_stone_dict[i+1]+'.png'
                self.op[i].setPixmap(QPixmap(str))
                self.op[i].setScaledContents(True)
                self.op[i].setMaximumSize(120,120)
                self.op[i].move(pos[0],pos[1])
            else:
                str='image\\stone\\'+Init_stone_dict[16-i-1]+'.png'
                self.mp[i-16].setPixmap(QPixmap(str))
                self.mp[i-16].setScaledContents(True)
                self.mp[i-16].setMaximumSize(120,120)
                self.mp[i-16].move(pos[0],pos[1])
        print("OK")
        self.update()


    def selectStone(self): 
        self.setMouseTracking(True)

#鼠标点击事件

    def mousePressEvent(self, event):
        global online_move
        self.online_op_move_one_step=online_move
        if(self.mode=='PvC' and self.AI_Turn):
            return
        if(self.has_player!=1 and self.mode=='PvP_online'):
            return
        if(self.game_finished):
            return
        if(self.need_to_operator==False):
            # if(self.mode=='PvP_online' ):
            #     self.online_op_move_one_step=True
            #     #threading._start_new_thread( self.receive_info)      #接收信息
            #     self.receive_info()
            return
        if(self.online_op_move_one_step==True):
            return
        self.start=True
        pos = event.pos()  
        print(pos) 
        if(self.currentStone==''):
            if_not_find=True
            i=0
            while(i<10 and if_not_find):
                for j in range(9):
                    self.currentStone,self.currentPos=self.board.selectStone(pos,i,j,self.mode)
                    if(self.currentStone!=''):
                        print(self.currentStone)
                        if_not_find=False
                        break
                i+=1
            self.label.clear()
            self.label.setText(self.currentPlayer+':选择'+self.currentStone)
        
        else:
            if_moveable=True
            if_moveable,self.nextPos=self.board.update(self.currentStone,self.currentPos,pos,mode=self.mode)
            
            if(if_moveable):
                print("move to ",self.nextPos)
                if(self.mode=='PvP_online'):
                    self.send_info()
                    time.sleep(1)
                    online_move=True
                self.currentPos=[-1,-1]
                self.currentStone=''
                self.move_stone()
            else:
                if(self.nextPos==[-2,-2]):  #重复点击相同棋子，即放下棋子
                    self.label.clear()
                    self.label.setText(self.currentPlayer+':放下'+self.currentStone)
                    self.currentStone=''
                    self.currentPos=[]      
                elif(self.nextPos==[-3,-3]):    #不符合规则
                    self.label.clear()
                    self.label.setText(self.currentPlayer+':'+self.currentStone+' 不符合规则') 
                    self.currentStone=''
                    self.currentPos=[]   
        self.winner=self.game_over()
        self.show_winner()
        if(self.game_finished):
            self.label.clear()
            self.label.setText("结束")
        self.update()
        self.show()
        if(self.mode=='PvC' and not self.game_finished):
            if(self.AI_Turn):
                self.AI_move()
        self.start=True

#移动棋子
    def move_stone(self):
        self.changePlayer()
        for i in range(16):
            self.mp[i].setPixmap(QtGui.QPixmap(''))
            self.op[i].setPixmap(QtGui.QPixmap(''))
        for i in range(len(self.board.my_stone)):
            index=np.argwhere(self.board.pos ==  self.board.my_stone[i])[0]
            name=self.board.decoder[self.board.my_stone[i]]
            pos=self.board.index2pos(index)
            self.mp.append(QtWidgets.QLabel(self))
            str='image\\stone\\'+name+'.png'
            self.mp[i].setPixmap(QPixmap(str))
            self.mp[i].setScaledContents(True)
            self.mp[i].setMaximumSize(120,120)
            self.mp[i].move(pos[0],pos[1])
        for i in range(len(self.board.op_stone)):
            index=np.argwhere(self.board.pos == self.board.op_stone[i])[0]
            name=self.board.decoder[self.board.op_stone[i]]
            pos=self.board.index2pos(index)
            self.op.append(QtWidgets.QLabel(self))
            str='image\\stone\\'+name+'.png'
            self.op[i].setPixmap(QPixmap(str))
            self.op[i].setScaledContents(True)
            self.op[i].setMaximumSize(120,120)
            self.op[i].move(pos[0],pos[1])
        self.label.clear()
        self.label.setText("轮到："+self.currentPlayer)
        self.update()

#画面中心
    def center(self):
        window=self.frameGeometry()
        center_point=QDesktopWidget().availableGeometry().center()
        window.moveCenter(center_point)
        self.move(window.topLeft())

#交换玩家
    def changePlayer(self):
        if(self.mode=='PvP_online'):
            if(self.need_to_operator):
                self.need_to_operator=False
            else:
                self.need_to_operator=True
        if(self.mode=='PvC'):
            if(not self.AI_Turn):
                self.board.change_side()
            self.AI_Turn=not self.AI_Turn
        if(self.currentPlayer=='black'):
            self.currentPlayer='red'
        else:
            self.currentPlayer='black'


#游戏结束
    
    def game_over(self):
        if(self.mode=='PvC'):
            decoder_key=[]
            jiang_index=0
            shuai_index=0
            for i in self.board.decoder:
                decoder_key.append(i)
            for i in decoder_key:
                if(self.board.decoder[i]=='jiang'):
                    jiang_index=i
                elif(self.board.decoder[i]=='shuai'):
                    shuai_index=i
            if(self.board.my_stone.count(jiang_index)==0 and self.board.op_stone.count(jiang_index)==0 ):
                return 'red'
            elif(self.board.op_stone.count(shuai_index)==0 and self.board.my_stone.count(shuai_index)==0):
                return 'black'
            else :
                return ''
        else:
            if(self.board.my_stone.count(104)==0):
                return 'black'
            elif(self.board.op_stone.count(-194)==0):
                return 'red'
            else :
                return ''
    def show_winner(self):
        if(self.winner=='red'):
            hbox = QHBoxLayout(self)
            pixmap = QPixmap('./image/red_win.png')         
            #设置标签
            win_label = QLabel(self)
            win_label.setPixmap(pixmap)
            win_label.setScaledContents(True)
            win_label.setMaximumSize(240,134)
            win_label.move(self.high//2-120,self.width//2-67)
            hbox.addWidget(win_label)
            #主窗口设置
            self.setLayout(hbox)
            self.game_finished=True
        elif (self.winner=='black'):
            hbox = QHBoxLayout(self)
            pixmap = QPixmap('./image/black_win.png')         
            #设置标签
            win_label = QLabel(self)
            win_label.setPixmap(pixmap)
            win_label.setScaledContents(True)
            win_label.setMaximumSize(240,134)
            win_label.move(self.high//2-120,self.width//2-67)
            hbox.addWidget(win_label)
            #主窗口设置
            self.setLayout(hbox)
            self.game_finished=True
        self.update()
#以下AI处理
    def AI_move(self):
        self.board.next_move=self.mcts.get_move()
        self.board.move()
        self.currentPos=[-1,-1]
        self.currentStone=''
        self.move_stone()
        self.winner=self.game_over()
        self.show_winner()
        if(self.game_finished):
            self.label.clear()
            self.label.setText("结束")
        self.update()
        self.show()
#以下网络处理

#等待玩家
    def wait_player(self):
        if(self.status=='service'):
            self.service.connect()
            self.has_player=self.service.if_connect
        elif(self.status=='client'):
            self.client.connect()
            self.has_player= self.client.if_connect
#网络中断连接
    def interrupt(self):
        while(True):
            if(self.status=='service'):
                if(self.service.loss_connection):
                    break
            elif(self.status=='client'):
                if(self.client.loss_connection):
                    break
        #QMessageBox.warning(self,"Warning", "对方失去连接，退出游戏", QMessageBox.Yes)
        self.back_clicked()
#传输信息
    def send_info(self):
        if(self.status=='service'):
            self.service.send(self.currentStone,self.currentPos,self.nextPos)    
        elif(self.status=='client'):
            self.client.send(self.currentStone,self.currentPos,self.nextPos)  
#接受信息
    def receive_info(self):
        global online_move
        if(self.status=='service'):
            self.service.receive()
        elif(self.status=='client'):
            self.client.receive()
        while(True):
            if(self.need_to_operator==False):
                time.sleep(2)
                if(self.status=='service'):
                    if(self.service.get_data==True):
                        self.currentStone=self.service.receive_name
                        self.currentPos=self.service.receive_current
                        self.nextPos=self.service.receive_target
                    else:
                        continue
                elif(self.status=='client'):
                    if(self.client.get_data==True):
                        self.currentStone=self.client.receive_name
                        self.currentPos=self.client.receive_current
                        self.nextPos=self.client.receive_target
                    else:
                        continue
                self.online_op_move_one_step=True
                self.label.clear()
                self.label.setText(self.currentPlayer+':移动'+self.currentStone+str(self.currentPos)+'2'+str(self.nextPos)) 
                self.update
                self.board.update_online(self.currentPos,self.nextPos)
                self.winner=self.game_over()
                self.show_winner()
                if(self.game_finished):
                    self.label.clear()
                    self.label.setText("结束")
                self.currentStone=''
                self.currentPos=[-1,-1]
                self.move_stone()
                self.online_op_move_one_step=False
                online_move=self.online_op_move_one_step
                break
            else:
                break




class Mythread(QThread):
    # 定义信号
    global online_move
    updateSignal = pyqtSignal()
    sendSignal=pyqtSignal()
    def __init__(self, parent=None):
        super().__init__(parent)
 
    def run(self,mode='rec'):
        if(mode=='rec'):
            while(True):
                if(online_move):
                    self.updateSignal.emit()
                    time.sleep(0.5)