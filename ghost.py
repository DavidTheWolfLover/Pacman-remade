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
        self.speed = 100
        self.prev = ghostr
        self.goal = Vector2()
        self.node = nodes.points[10]
        self.target = self.node
        self.recent_position()
        self.ID = -1

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
        self.guideBack()

    def updateMode(self,t):
        self.modetime += t
        if (self.ID == 0):
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
        if self.mode[self.modeCount].name != "SPAWN" and self.mode[self.modeCount].name != "GUIDE":
            if self.mode[self.modeCount].name != "FRIGHT":
                if self.mode[self.modeCount].time is not None:
                    temp = self.mode[self.modeCount].time - self.modetime
                    self.mode[self.modeCount].time = temp
                self.mode.insert(self.modeCount,Mode("FRIGHT", time=7, speedMult=0.5))
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
        for x in self.guide:
            self.mode.insert(self.modeCount+1,Mode("GUIDE", speedMult=0.5, direction = x))

    def findSNode(self):
        for node in self.nodes.points:
            if node.spawnghost:
                break
        return node

    def spawn(self):
        self.goal = self.spawnnode.location

    def guideBack(self): #Let ghost go out of home :D
        self.guide = [UP]

    def update(self, t, pacman, blinky = None): #DONE
        speed = self.speed * self.mode[self.modeCount].speedMult
        self.location += self.move*speed*t
        self.updateMode(t)
        if (self.mode[self.modeCount].name == "SCATTER"):
            self.scatter() #Blinky goes on the top right of the map
        elif (self.mode[self.modeCount].name == "CHASE"): 
            self.chase(pacman,blinky) #time to chase pacman :D
        elif (self.mode[self.modeCount].name == "FRIGHT"):
            self.randomgoal() #scary
        elif (self.mode[self.modeCount].name == "SPAWN"): #time to go home
            self.spawn()
        self.move_self()

    def check_direction(self):
        directions = []
        for key in self.node.near.keys():
            if self.node.near[key] is not None:
                if key != self.move * -1 :
                    if not self.mode[self.modeCount].name == "SPAWN":
                        if not self.node.entrance:
                            directions.append(key)
                        else:
                            if (key != DOWN):
                                directions.append(key)
                    else:
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
                    self.move =self.mode[self.modeCount].direction
                    self.target = self.node.near[self.move]
                    self.recent_position()
            elif self.mode[self.modeCount].name == "GUIDE":
                self.mode.pop(self.modeCount)
                if self.mode[self.modeCount].name == "GUIDE":
                    self.move =self.mode[self.modeCount].direction
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

    def reverse(self):
        if (self.mode[self.modeCount].name != "SPAWN" and self.mode[self.modeCount].name != "GUIDE"):
            Base.reverse(self)

    def draw(self,screen,t): #DONE
        if self.visible:
            #p = (self.location.x,self.location.y)
            p = (self.location.x - 10, self.location.y - 13)
            ghost = self.prev
            if (self.mode[self.modeCount].name != "FRIGHT" and self.mode[self.modeCount].name != "SPAWN"):
                if self.move is UP:
                    ghost = ghostu[self.ID]
                if self.move is DOWN:
                    ghost = ghostd[self.ID]
                if self.move is RIGHT:
                    ghost = ghostr[self.ID]
                if self.move is LEFT:
                    ghost = ghostl[self.ID]
                self.prev = ghost
            else:
                ghost = ghosttarget
                self.prev = ghost
            screen.blit(ghost, p)
            #pygame.draw.circle(screen, self.color, p, self.radius)

class Blinky(Ghost):
    def __init__(self,nodes):
        Ghost.__init__(self,nodes)
        self.name = "Blinky"
        self.ID = 0

class Pinky(Ghost):
    def __init__(self, nodes):
        Ghost.__init__(self, nodes)
        self.name = "Pinky"
        self.ID = 1

    def scatter(self):
        self.goal = Vector2()

    def chase(self, pacman, blinky=None):
        self.goal = pacman.location + pacman.move * Tile_Width * 4

class Inky(Ghost):
    def __init__(self,nodes):
        Ghost.__init__(self,nodes)
        self.name = "Inky"
        self.ID = 2
    
    def scatter(self):
        self.goal = Vector2(Tile_Width * game_cols, Tile_Height * game_rows)

    def chase(self, pacman, blinky=None):
        v = pacman.location + pacman.move * Tile_Width * 2
        v1 = (v - blinky.location)*2
        self.goal = v1 + blinky.location
    
class Clyde(Ghost):
    def __init__(self,nodes):
        Ghost.__init__(self,nodes)
        self.name = "Clyde"
        self.ID = 3
    
    def scatter(self):
        self.goal = Vector2(0, Tile_Height * game_rows)

    def chase(self, pacman, blinky=None):
        d = pacman.location - self.location
        d1 = d.magnitudeSquared()
        if d1 <= (Tile_Width * 8)**2:
            self.scatter()
        else:
            self.goal = pacman.location + pacman.move * Tile_Width * 4

class Group_Ghosts(object):
    def __init__(self,nodes):
        self.nodes = nodes
        self.ghosts = [Blinky(nodes), Pinky(nodes), Inky(nodes), Clyde(nodes)]
    
    def update(self,t,pacman):
        for ghost in self.ghosts:
            ghost.update(t,pacman,self.ghosts[0])

    def fright(self):
        for ghost in self.ghosts:
            ghost.fright()
    
    def draw(self,screen,t):
        for ghost in self.ghosts:
            ghost.draw(screen,t)
    
    def up_points(self):
        for ghost in self.ghosts:
            ghost.points *= 2

    def reset_points(self):
        for ghost in self.ghosts:
            ghost.points = 200

    def hide(self):
        for ghost in self.ghosts:
            ghost.visible = False
    

    


