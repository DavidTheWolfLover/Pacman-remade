import pygame
from vector import Vector2
from constants import *

class Pellet(object):
    def __init__(self, x, y):
        self.name = "pellet"
        self.location = Vector2(x, y)
        self.color = white
        self.radius = 2
        self.points = 10
        self.visible = True
        
    def draw(self, screen):
        if self.visible:
            p = (self.location.x,self.location.y)
            pygame.draw.circle(screen, self.color, p, self.radius)

class PowerPellet(Pellet):
    def __init__(self, x, y):
        Pellet.__init__(self,x,y)
        self.color = green
        self.name = "powerpellet"
        self.radius = 8
        self.points = 50
        self.flashTime = 0.2
        self.time= 0

    def update(self,t):
        self.time += t
        if (self.time >=self.flashTime):
            self.time = 0
            self.visible = not self.visible

class PelletGroups(object):
    def __init__(self, pelletmap):
        self.pelletList = []
        self.powerpellet = []
        self.createPelletList(pelletmap)
    
    def update(self,t):
        for i in self.powerpellet:
            i.update(t)

    def readFile(self, textfile):
        f = open(textfile, "r")
        lines = [line.rstrip('\n') for line in f]
        lines = [line.rstrip('\r') for line in lines]
        return [line.split(' ') for line in lines]

    def createPelletList(self,pelletmap):
        grid = self.readFile(pelletmap)
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if (grid[i][j] == "x"):
                    self.pelletList.append(Pellet(j*Tile_Width,i*Tile_Height))
                elif (grid[i][j] == "X"):
                    temp = PowerPellet(j*Tile_Width,i*Tile_Height)
                    self.powerpellet.append(temp)
                    self.pelletList.append(temp)
    
    def draw(self,screen):
        for i in self.pelletList:
            i.draw(screen)


    

