import pygame
import math
from pygame.locals import *
from vector import Vector2
from constants import *
from base import Base

class Pacman(Base):
    def __init__(self,nodes):
        Base.__init__(self,nodes)
        self.name = "Pacman"
        self.prev =  pacr
        self.last = STOP
        self.lives = 3
        self.initial_location()

    def update(self,t):
        self.visible = True
        self.location += self.move*self.speed*t
        move = self.check_direction()
        if (move):
            self.move_key(move)
        else:
            self.move_self()

    def initial_location(self):
        self.move = LEFT
        for node in self.nodes.points:
            if node.pacmanloc == True:
                self.node = node
                self.target = self.node.near[self.move]
                self.recent_position()
                self.location.x -= (self.node.location.x - self.target.location.x)/2

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            d = self.location - pellet.location
            d1 = d.magnitudeSquared()
            r = (pellet.radius+self.touch)**2
            if d1<= r:
                return pellet
        return None

    def Ghosteat(self, ghosts):
        for ghost in ghosts.ghosts:
            d = self.location - ghost.location
            d1 = d.magnitudeSquared()
            r = (ghost.radius+self.touch)**2
            if d1 <= r:
                return ghost
        return None

    def eatFruit(self, fruit):
        d = self.location - fruit.location
        d1 = d.magnitudeSquared()
        r = (fruit.radius+self.touch)**2
        if d1 <= r:
            return fruit
        return None
    
    def check_direction(self):
        key = pygame.key.get_pressed()
        if (key[K_UP] == True or key[K_w] == True):
            return UP
        if (key[K_DOWN] == True or key[K_s] == True):
            return DOWN
        if (key[K_LEFT] == True or key[K_a] == True):
            return LEFT
        if (key[K_RIGHT] == True or key[K_d] == True):
            return RIGHT
        return None

    def move_self(self):
        if (self.last is not STOP and self.pass_target()):
            self.node = self.target
            if (self.node.near[self.last] is not None):
                if self.node.entrance == False:
                    self.target = self.node.near[self.last]
                    self.recent_position()
                    self.move = self.last
                    self.last = STOP
        if (self.move is not STOP):
            if (self.pass_target()):
                self.node = self.target
                self.portal()
                if (self.node.near[self.move] is not None):
                    self.target = self.node.near[self.move]
                else:
                    self.recent_position()
                    self.move = STOP

    def move_key(self, move):
        if (self.move is STOP):
            if (self.node.near[move] is not None):
                self.move = move
                self.target = self.node.near[self.move]
                self.recent_position()
        else:
            if (move == self.move * -1):
                self.reverse()
                self.last = STOP
            elif (move != self.move):
                self.last = move
            if (self.pass_target()):
                self.node = self.target
                self.portal()
                if (self.node.near[move] is not None):
                    if self.node.entrance:
                        if (self.node.near[self.move] is not None):
                            self.target = self.node.near[self.move]
                        else:
                            self.recent_position()
                            self.move = STOP
                    else:
                        self.target = self.node.near[move]
                        if (self.move != move):
                            self.recent_position()
                            self.move = move
                elif (self.node.near[self.move] is not None):
                    self.target = self.node.near[self.move]
                else:
                    self.recent_position()
                    self.move = STOP
        
    def draw(self,screen):
        if (self.visible == True):
            l = (self.location.x-10,self.location.y-10)
            pac = self.prev
            if self.move is UP:
                pac = pacu
            if self.move is DOWN:
                pac = pacd
            if self.move is RIGHT:
                pac = pacr
            if self.move is LEFT:
                pac = pacl
            self.prev = pac
            #l = (self.location.x,self.location.y)
            #pygame.draw.circle(screen,yellow,l,self.radius)
            screen.blit(pac,l)

    def draw_lives(self,screen):
        if self.lives >= -1:
            for i in range(self.lives):
                x = 7.5 + i * (5 + 30)
                y = (game_rows - 2.5) * Tile_Height
                screen.blit(strike_white,(x,y))
            if self.lives < 3:
                if self.lives < 0:
                    self.lives = 0
                for i in range(self.lives, 3):
                    x = 7.5 + i * (5 + 30)
                    y = (game_rows - 2.5) * Tile_Height
                    screen.blit(strike_red,(x,y))

