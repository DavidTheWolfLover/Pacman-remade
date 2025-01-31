import pygame
from vector import Vector2
from constants import *

class Text(object):
    def __init__(self, text, color, x, y, size, visible = True):
        self.text = text
        self.color = color
        self.size = size
        self.location = Vector2(x, y)
        self.font = pygame.font.Font("PressStart2P-Regular.ttf", self.size)
        self.setup_txt()
        self.visible = visible
        self.count_time = 0
        self.total_time = 0

    def setup_txt(self):
        self.show_text = self.font.render(self.text, 1, self.color)

    def update_txt(self, newtext):
        self.text = newtext
        self.setup_txt()

    def update(self, t):
        if self.total_time > 0:
            self.count_time += t
            if self.count_time >= self.total_time:
                self.count_time = 0
                self.total_time = 0
                self.visible = False

    def draw(self, screen):
        if self.visible == True:
            p = (self.location.x, self.location.y)
            screen.blit(self.show_text, p)

class Group_Text(object):
    def __init__(self):
        self.texts = [Text("SPACE TO START",matcha,105,330,16), 
                      Text("GAME OVER!",red,151,330,16),
                      Text("TIME",orange,10,10,16),
                      Text("BEST TIME",orange,160,10,16),
                      Text("PAUSED:D", yellow,160,330,16),
                      Text("GUUD",orange,368,10,16),
                      Text("0".zfill(4),white,10,26,16), #score
                      Text("0".zfill(4),white,185,26,16), #best time
                      Text("LUCK!",orange,368,30,16),
                      Text("DO NOT EAT ALL >w<!",red,180,540,13),]
        self.tempText = []

    def update(self, t):
        if len(self.tempText) > 0:
            tempText = []
            for text in self.tempText:
                text.update(t)
                if text.visible:
                    tempText.append(text)
            self.tempText = tempText
            
    def Update_Time(self, score):
        self.texts[6].update_txt(str(score).zfill(5))

    def Update_Besttime(self, score): 
        self.texts[7].color = yellow
        self.texts[7].update_txt(str(score).zfill(5))  

    def Reset_Color(self, score):
        self.texts[7].color = white
        self.texts[7].update_txt(str(score).zfill(5)) 

    def Ready(self):
        self.texts[0].visible = True
        self.texts[4].visible = False
        self.texts[1].visible = False
        
    def Pause(self):
        self.texts[0].visible = False
        self.texts[4].visible = True
        self.texts[1].visible = False
        
    def GameOver(self):
        self.texts[0].visible = False
        self.texts[4].visible = False
        self.texts[1].visible = True
        
    def Hide_All(self):
        self.texts[0].visible = False
        self.texts[4].visible = False
        self.texts[1].visible = False
        
    def Create_Temptxt(self, value, x,y):
        text = Text(str(value), white, x, y, 8)
        text.total_time = 1
        self.tempText.append(text)

    def draw(self, screen):
        for i in range(len(self.texts)):
            self.texts[i].draw(screen)
        for text in self.tempText:
            text.draw(screen)



