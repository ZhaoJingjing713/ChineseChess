import sys
from PyQt5.QtWidgets import QApplication
from UI import *
import pygame

if __name__=='__main__':
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load("music/The_Nightingale.ogg")
    pygame.mixer.music.set_volume(0.2)
    pygame.mixer.music.play(-1)
    app=QApplication(sys.argv)
    menu=main_UI()
    sys.exit(app.exec_())
    
    
    