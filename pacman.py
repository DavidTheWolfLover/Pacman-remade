import pygame
import math
from pygame.locals import *
from vector import Vector2
from constants import *

class Pacman(object):
    def __init__(self,nodes):
        self.name = "Pacman"
        self.move = STOP
        self.speed = 100
        self.radius = 10
        self.touch = 5
        self.nodes = nodes
        self.node = nodes.points[0]
        self.target = self.node
        self.prev =  pacr
        self.recent_position()
        self.last = STOP

    def recent_position(self):
        self.location = self.node.location.copy()

    def update(self,t):
        self.location += self.move*self.speed*t
        move = self.check_direction()
        if (move):
            self.move_key(move)
        else:
            self.move_self()

    def pass_target(self):
        if self.target is not None:
            v1 =  self.location - self.node.location
            v2 = self.target.location - self.node.location
            d1 = v1.magnitudeSquared()
            d2 = v2.magnitudeSquared()
            return d1>=d2
        return False
    
    def portal(self):
        if (self.node.portalNode):
            self.node = self.node.portalNode
            self.recent_position()

    def eatPellets(self, pelletList):
        for pellet in pelletList:
            d = self.location - pellet.location
            d1 = d.magnitudeSquared()
            r = (pellet.radius+self.touch)**2
            if d1<= r:
                return pellet
        return None

    def Ghosteat(self,ghost):
        d = self.location - ghost.location
        d1 = d.magnitudeSquared()
        r = (ghost.radius+self.touch)**2
        if d1< r:
            return True
        return False

    def check_direction(self):
        key = pygame.key.get_pressed()
        if (key[K_UP] == True):
            return UP
        if (key[K_DOWN] == True):
            return DOWN
        if (key[K_LEFT] == True):
            return LEFT
        if (key[K_RIGHT] == True):
            return RIGHT
        return None

    def move_self(self):
        if (self.last is not STOP and self.pass_target()):
            self.node = self.target
            if (self.node.near[self.last] is not None):
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
                    self.target = self.node.near[move]
                    if (self.move != move):
                        self.recent_position()
                        self.move = move
                elif (self.node.near[self.move] is not None):
                    self.target = self.node.near[self.move]
                else:
                    self.recent_position()
                    self.move = STOP

    def reverse(self):
        if (self.move is UP):
            self.move = DOWN
        elif (self.move is DOWN):
            self.move = UP
        elif (self.move is LEFT):
            self.move = RIGHT
        elif (self.move is RIGHT):
            self.move = LEFT
        self.target, self.node = self.node, self.target
        
    def draw(self,screen):
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
