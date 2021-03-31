import pygame
import math
from pygame.locals import *
from vector import Vector2
from constants import *
from random import randint
from mode import Mode
from base import Base

class Ghost(Base):
    def __init__(self,nodes): #DONE
        Base.__init__(self,nodes)
        self.name = "Ghost"
        self.points = 200

        self.goal = Vector2()
        self.node = nodes.points[10]
        self.target = self.node
        self.recent_position()
        
        self.modetime = 0 #time for a mode counting...
        self.modeCount = 0
        self.mode = [Mode(name="SCATTER", time=7), Mode(name="CHASE", time=20), \
                     Mode(name="SCATTER", time=7), Mode(name="CHASE", time=20), \
                     Mode(name="SCATTER", time=5), Mode(name="CHASE", time=20), \
                     Mode(name="SCATTER", time=5), Mode(name="CHASE")]
        """self.reset = [Mode(name="SCATTER", time=7), Mode(name="CHASE", time=20), 
                      Mode(name="SCATTER", time=7), Mode(name="CHASE", time=20), 
                      Mode(name="SCATTER", time=5), Mode(name="CHASE", time=20), 
                      Mode(name="SCATTER", time=5), Mode(name="CHASE")]"""#reset the self.mode because it can be modified by frightened mode
                                                                          #I just put here in case I need it XD
        self.spawnnode = self.findSNode()

    def updateMode(self,t):
        self.modetime += t
        print(self.modetime,' ',self.mode[self.modeCount].name,end='\n')
        if (self.mode[self.modeCount].time is not None):
            if self.modetime >= self.mode[self.modeCount].time:
                self.reverse()
                self.modetime = 0
                self.modeCount += 1

    def scatter(self):
        self.goal = Vector2(screen_size[0], 0)

    def chase(self, pacman, blinky = None):
        self.goal = pacman.location
    
    def fright(self):
        if self.mode[self.modeCount].name != "SPAWN":
            if self.mode[self.modeCount].name != "FREIGHT":
                if self.mode[self.modeCount].time is not None:
                    temp = self.mode[self.modeCount].time - self.modetime
                    self.mode[self.modeCount].time = temp
                self.mode.insert(self.modeCount,Mode("FREIGHT", time=7, speedMult=0.5))
                self.modetime = 0
            else:
                self.modetime = 0
            self.reverse()
            
    def randomgoal(self):
        x = randint(0,screen_width) #random horizontal
        y = randint(0,screen_height) #random vertical
        self.goal = Vector2(x,y)

    def spawnMode(self, speed=1):
        self.mode.pop(self.modeCount)
        self.mode.insert(self.modeCount,Mode("SPAWN", speedMult=speed))
        self.modeTimer = 0

    def findSNode(self):
        for node in self.nodes.points:
            if node.spawnghost:
                break
        return node

    def spawn(self):
        self.goal = self.spawnnode.location

    def update(self, t, pacman, blinky = None): #DONE
        speed = self.speed * self.mode[self.modeCount].speedMult
        self.location += self.move*speed*t
        self.updateMode(t)
        if (self.mode[self.modeCount].name == "SCATTER"):
            self.scatter() #Blinky goes on the top right of the map
        elif (self.mode[self.modeCount].name == "CHASE"): 
            self.chase(pacman,blinky) #time to chase pacman :D
        elif (self.mode[self.modeCount].name == "FREIGHT"):
            self.randomgoal()
        elif (self.mode[self.modeCount].name == "SPAWN"):
            self.spawn()
        self.move_self()

    def check_direction(self):
        directions = []
        for key in self.node.near.keys():
            if self.node.near[key] is not None:
                if key != self.move * -1 :
                    directions.append(key)
        if (len(directions) == 0):
            directions.append(self.ReturnNode())
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
            if self.mode[self.modeCount].name == "SPAWN":
                if self.location == self.goal:
                    self.mode.pop(self.modeCount)


    def ReturnNode(self):
        if (self.move * -1 == UP):
            return UP
        elif (self.move * -1 == DOWN):
            return DOWN
        elif (self.move * -1 == LEFT):
            return LEFT
        elif (self.move * -1 == RIGHT):
            return RIGHT

    def draw(self,screen): #DONE
        if self.visible:
            #p = (self.location.x,self.location.y)
            p = (self.location.x - 10, self.location.y - 13)
            screen.blit(ghost1, p)
            #pygame.draw.circle(screen, self.color, p, self.radius)
