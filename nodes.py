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
        self.map = map
        self.grid = None
        self.createNodeList(map)
    
    def readFile(self, textfile):
        f = open(textfile, "r")
        lines = [line.rstrip('\n') for line in f]
        lines = [line.rstrip('\r') for line in lines]
        return [line.split(' ') for line in lines]
    
    def createNodeList(self,textfile):
        #near = self.First_Node(len(self.grid),len(self.grid[0]))
        #isWall = True
        portal = []
        self.grid = self.readFile(textfile)
        first = self.First_Node()
        self.way4(first,portal)
        portal[0].portalNode = portal[1]
        portal[1].portalNode = portal[0]

    def check(self, node):
        for inode in self.points:
            if node.row == inode.row and node.column == inode.column:
                return inode
        return None

    def way4(self,node,portal):
        if (self.grid[node.row][node.column] == "1"):
            portal.append(node)
        k=0
        nodeleft = None
        noderight = None
        nodeup = None
        nodedown = None
        i = node.row
        j = node.column
        self.points.append(node)
        if (i+1<len(self.grid)):
            if (self.grid[i+1][j] != "."):
                k = i+1
                while (k<len(self.grid)):
                    if (self.grid[k][j] == "+" or self.grid[k][j] == "1"):
                        nodedown = Node(k,j)
                        temp = self.check(nodedown)
                        if temp is not None:
                            node.near[DOWN] = temp
                            nodedown = None
                        else:
                            self.points.append(nodedown)
                            node.near[DOWN] = nodedown
                        break
                    k+=1

        if (j-1>=0):
            if (self.grid[i-1][j] != "."):
                k = i-1
                while (k>=0):
                    if (self.grid[k][j] == "+" or self.grid[k][j] == "1"):
                        nodeup = Node(k,j)
                        temp = self.check(nodeup)
                        if temp is not None:
                            node.near[UP] = temp
                            nodeup = None
                        else:
                            self.points.append(nodeup)
                            node.near[UP] = nodeup
                        break
                    k-=1
        
        if (j+1<len(self.grid[0]) and node.near[RIGHT] is None):
            if (self.grid[i][j+1] != "."):
                k = j+1
                while (k<len(self.grid[0])):
                    if (self.grid[i][k] == "+" or self.grid[i][k] == "1"):
                        noderight = Node(i,k)
                        temp = self.check(noderight)
                        if temp is not None:
                            node.near[RIGHT] = temp
                            noderight = None
                        else:
                            self.points.append(noderight)
                            node.near[RIGHT] = noderight
                        break
                    k+=1
        if (j-1>=0 and node.near[LEFT] is None):
            if (self.grid[i][j-1] != "."):
                k = j-1
                while (k>=0):
                    if (self.grid[i][k] == "+" or self.grid[i][k] == "1"):
                        nodeleft = Node(i,k)
                        temp = self.check(nodeleft)
                        if temp is not None:
                            node.near[LEFT] = temp
                            nodeleft = None
                        else:
                            self.points.append(nodeleft)
                            node.near[LEFT] = nodeleft
                        break
                    k-=1
        if (nodedown is not None):
            self.way4(nodedown,portal)
        if (nodeup is not None):
            self.way4(nodeup,portal)
        if (nodeleft is not None):
            self.way4(nodeleft,portal)
        if (noderight is not None):
            self.way4(noderight,portal)

    def First_Node(self):
        nodeFound = False
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if (self.grid[i][j] == "+"):
                    return Node(i,j)
        return None
    
    """
    def create_nodes(self):
        A = Node(5, 5)
        B = Node(5, 10)
        C = Node(10, 5)
        D = Node(10, 10)
        E = Node(10, 13)
        F = Node(20, 5)
        G = Node(20, 13)
        A.near[RIGHT] = B
        A.near[DOWN] = C
        B.near[LEFT] = A
        B.near[DOWN] = D
        C.near[UP] = A
        C.near[RIGHT] = D
        C.near[DOWN] = F
        D.near[UP] = B
        D.near[LEFT] = C
        D.near[RIGHT] = E
        E.near[LEFT] = D
        E.near[DOWN] = G
        F.near[UP] = C
        F.near[RIGHT] = G
        G.near[UP] = E
        G.near[LEFT] = F
        self.points = [A, B, C, D, E, F ,G]

    """

    def refresh(self,screen):
        for i in self.points:
            i.draw_near(screen)
        pygame.draw.line(screen,green,(3*Tile_Width,5*Tile_Height),(3*Tile_Width,10*Tile_Height),2)

