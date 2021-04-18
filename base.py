import pygame
from vector import Vector2
from constants import *

class Base(object):
    def __init__(self,nodes):
        self.name = ""
        self.move = STOP
        self.speed = 100
        self.radius = 10
        self.touch = 5
        self.nodes = nodes
        self.node = nodes.points[0]
        self.target = self.node
        self.recent_position()
        self.visible = True

    def recent_position(self):
        self.location = self.node.location.copy()

    def update(self,t):
        self.location += self.move*self.speed*t
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
