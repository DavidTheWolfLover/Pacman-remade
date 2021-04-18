import pygame
from vector import Vector2
from constants import *

class Node(object):
    def __init__(self, row, column):
        self.row = row          # } Tile_location
        self.column = column    # }
        self.location = Vector2(column * Tile_Width,row * Tile_Height) #App_location
        self.near = {UP:None, DOWN:None, RIGHT:None, LEFT:None} #nearby neighbors
        self.portalNode = None
        self.homeguide = False #help draw the node
        self.entrance = False #entrance to home
        self.spawnghost = False #point in house
        self.pacmanloc = False #Pacman's initial location
        self.redloc = False
        self.greenloc = False
        self.blueloc = False
        self.purpleloc = False

        self.fruitloc = False

    def draw_near(self,screen):
        for i in self.near.keys():
            if (self.near[i] is not None):
                start = (self.location.x,self.location.y) #start point line
                end = (self.near[i].location.x,self.near[i].location.y) #finish point line
                pygame.draw.line(screen,blue,start,end,4)
                #pygame.draw.circle(screen,red,start,12)

class Group_Nodes(object):
    def __init__(self,map):
        self.points = []
        self.homepoints = []
        self.map = map
        self.grid = self.readFile(map)
        self.gridhome = self.getHomeArray()
        self.createNodeList(self.grid,self.points)
        self.createNodeList(self.gridhome,self.homepoints)
        self.moveHomeNodes()
        self.homepoints[0].entrance = True
    
    def readFile(self, textfile):
        f = open(textfile, "r")
        lines = [line.rstrip('\n') for line in f]
        lines = [line.rstrip('\r') for line in lines]
        return [line.split(' ') for line in lines]
    
    def createNodeList(self,grid,points):
        #near = self.First_Node(len(self.grid),len(self.grid[0]))
        #isWall = True
        portal = []
        first = self.First_Node(grid)
        self.way4(first,portal,grid,points)
        if (len(portal) != 0):
            portal[0].portalNode = portal[1]
            portal[1].portalNode = portal[0]

    def check(self, node, points):
        for inode in points:
            if node.row == inode.row and node.column == inode.column:
                return inode
        return None

    def way4(self,node,portal,grid,points):
        if (grid[node.row][node.column] == "1"):
            portal.append(node)
        elif (grid[node.row][node.column] == "H"):
            node.homeguide = True
        elif (grid[node.row][node.column] == "S"):
            node.spawnghost = True
            node.blueloc = True
        elif (grid[node.row][node.column] == "P"):
            node.pacmanloc = True
        elif (grid[node.row][node.column] == "R"):
            node.redloc = True
        elif (grid[node.row][node.column] == "A"):
            node.purpleloc = True
        elif (grid[node.row][node.column] == "G"):
            node.greenloc = True
        elif (grid[node.row][node.column] == "F"):
            node.fruitloc = True
        k=0
        nodeleft = None
        noderight = None
        nodeup = None
        nodedown = None
        i = node.row
        j = node.column
        points.append(node)
        if (i+1<len(grid)):
            if (grid[i+1][j] != "."):
                k = i+1
                while (k<len(grid)):
                    if (grid[k][j] == "+" or grid[k][j] == "1" or grid[k][j] == "H" or grid[k][j]== "S" or grid[k][j]== "P" or grid[k][j]== "A" or grid[k][j]== "G" or grid[k][j]== "R" or grid[k][j]== "F"):
                        nodedown = Node(k,j)
                        temp = self.check(nodedown,points)
                        if temp is not None:
                            node.near[DOWN] = temp
                            nodedown = None
                        else:
                            #points.append(nodedown)
                            node.near[DOWN] = nodedown
                        break
                    k+=1

        if (i-1>=0):
            if (grid[i-1][j] != "."):
                k = i-1
                while (k>=0):
                    if (grid[k][j] == "+" or grid[k][j] == "1" or grid[k][j] == "H" or grid[k][j]== "S" or grid[k][j]== "P" or grid[k][j]== "A" or grid[k][j]== "G" or grid[k][j]== "R" or grid[k][j]== "F"):
                        nodeup = Node(k,j)
                        temp = self.check(nodeup,points)
                        if temp is not None:
                            node.near[UP] = temp
                            nodeup = None
                        else:
                            #points.append(nodeup)
                            node.near[UP] = nodeup
                        break
                    k-=1
        
        if (j+1<len(grid[0]) and node.near[RIGHT] is None):
            if (grid[i][j+1] != "."):
                k = j+1
                while (k<len(grid[0])):
                    if (grid[i][k] == "+" or grid[i][k] == "1" or grid[i][k] == "H" or grid[i][k]== "S" or grid[i][k]== "P" or grid[i][k]== "A" or grid[i][k]== "G" or grid[i][k]== "R" or grid[i][k]== "F"):
                        noderight = Node(i,k)
                        temp = self.check(noderight,points)
                        if temp is not None:
                            node.near[RIGHT] = temp
                            noderight = None
                        else:
                            #points.append(noderight)
                            node.near[RIGHT] = noderight
                        break
                    k+=1
        if (j-1>=0 and node.near[LEFT] is None):
            if (grid[i][j-1] != "."):
                k = j-1
                while (k>=0):
                    if (grid[i][k] == "+" or grid[i][k] == "1" or grid[i][k]== "H" or grid[i][k]== "S" or grid[i][k]== "P" or grid[i][k]== "A" or grid[i][k]== "G" or grid[i][k]== "R" or grid[i][k]== "F"):
                        nodeleft = Node(i,k)
                        temp = self.check(nodeleft,points)
                        if temp is not None:
                            node.near[LEFT] = temp
                            nodeleft = None
                        else:
                            #points.append(nodeleft)
                            node.near[LEFT] = nodeleft
                        break
                    k-=1
        if (nodedown is not None):
            self.way4(nodedown,portal,grid,points)
        if (nodeup is not None):
            self.way4(nodeup,portal,grid,points)
        if (nodeleft is not None):
            self.way4(nodeleft,portal,grid,points)
        if (noderight is not None):
            self.way4(noderight,portal,grid,points)

    def First_Node(self,grid):
        nodeFound = False
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if (grid[i][j] == "+" or grid[i][j] == "1" or grid[i][j] == "H" or grid[i][j]== "S" or grid[i][j]== "P" or grid[i][j]== "A" or grid[i][j]== "G" or grid[i][j]== "R"):
                    return Node(i,j)
        return None
    
    def moveHomeNodes(self):
        for node in self.points:
            if node.homeguide:
                nodeA = node
                break
        nodeB = nodeA.near[LEFT]
        mid = (nodeA.location + nodeB.location) / 2.0
        mid = Vector2(int(mid.x), int(mid.y))
        vec = Vector2(self.homepoints[0].location.x, self.homepoints[0].location.y)
            
        for node in self.homepoints:
            node.location -= vec
            node.location += mid
            self.points.append(node)

        A = self.check(nodeA, self.points)
        B = self.check(nodeB, self.points)
        H = self.check(self.homepoints[0], self.points)
        A.near[LEFT] = H
        B.near[RIGHT] = H
        H.near[RIGHT] = A
        H.near[LEFT] = B
        
    def getHomeArray(self):
        return [['.', '.', 'R', '.', '.'],
                ['.', '.', '|', '.', '.'],
                ['+', '.', '|', '.', '+'],
                ['G', '-', 'S', '-', 'A'],
                ['+', '.', '.', '.', '+']]

    def refresh(self,screen):
        for i in self.points:
            i.draw_near(screen)
        #for i in range(len(self.points)-15,len(self.points)):
        #    self.points[i].draw_near(screen)

