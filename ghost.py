import pygame
import math
from pygame.locals import *
from vector import Vector2
from constants import *
from random import randint

class Ghost(object):
    def __init__(self,nodes): #DONE
        self.name = "Ghost"
        self.move = STOP
        self.color = white
        self.speed = 100
        self.radius = 10
        self.touch = 5
        self.points = 200
        self.nodes = nodes
        self.node = nodes.points[10]
        self.target = self.node
        self.recent_position()
        self.goal = Vector2()
        self.visible = True

    def recent_position(self): #DONE
        self.location = self.node.location.copy()

    def update(self,t): #DONE
        self.location += self.move*self.speed*t
        self.move_self()

    def pass_target(self): #DONE
        if self.target is not None:
            v1 =  self.location - self.node.location
            v2 = self.target.location - self.node.location
            d1 = v1.magnitudeSquared()
            d2 = v2.magnitudeSquared()
            return d1>=d2
        return False
    
    def portal(self): #DONE
        if (self.node.portalNode):
            self.node = self.node.portalNode
            self.recent_position()

    def check_direction(self):
        directions = []
        for key in self.node.near.keys():
            if self.node.near[key] is not None and key != self.move * -1 :
                directions.append(key)
        if (len(directions) == 0):
            directions.append(self.move * -1)
        return directions

    def shortest_way(self,direction):
        length = []
        for i in direction:
            s = self.node.location + i*Tile_Width - self.goal
            length.append(s.magnitudeSquared())
        index = length.index(min(length))
        return direction[index]

    def move_self(self): #DONE
        if (self.pass_target()):
            self.node = self.target
            self.portal()
            direction = self.check_direction()
            #index = randint(0, len(direction) - 1) }   Random way
            #self.move = direction[index]           }   
            self.move = self.shortest_way(direction)
            self.target = self.node.near[self.move]
            self.recent_position()

    def ReturnNode(self):
        if (self.move * -1 == UP):
            return UP
        elif (self.move * -1 == DOWN):
            return DOWN
        elif (self.move * -1 == LEFT):
            return LEFT
        elif (self.move * -1 == RIGHT):
            return RIGHT
        
    def reverse(self): #DONE
        if (self.move is UP):
            self.move = DOWN
        elif (self.move is DOWN):
            self.move = UP
        elif (self.move is LEFT):
            self.move = RIGHT
        elif (self.move is RIGHT):
            self.move = LEFT
        self.target, self.node = self.node, self.target

    def draw(self,screen): #DONE
        if self.visible:
            #p = (self.location.x,self.location.y)
            p = (self.location.x - 10, self.location.y - 13)
            screen.blit(ghost1, p)
            #pygame.draw.circle(screen, self.color, p, self.radius)
