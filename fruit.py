from constants import *
from base import Base

class Fruit(Base):
    def __init__(self,nodes):
        Base.__init__(self,nodes)
        self.name = "Fruit"
        self.points = 100
        self.color = matcha
        self.initial_location()
        self.disappear = False
        self.time = 5
        self.timer = 0
        self.radius = 13
    
    def update(self,t):
        self.timer += t
        if self.timer>=self.time:
            self.disappear = True
    
    def initial_location(self):
        for node in self.nodes.points:
            if node.fruitloc == True:
                self.node = node
                self.target = self.node.near[LEFT]
                self.recent_position()
                self.location.x = int(self.location.x - (self.node.location.x - self.target.location.x)/2)
    
    def draw(self, screen):
        p = (self.location.x - 13, self.location.y - 11)
        screen.blit(fruit, p)
        #pygame.draw.circle(screen, self.color, p, self.radius)