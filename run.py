import pygame
from pygame.locals import *
from constants import *
from nodes import Group_Nodes
from pacman import *
from pellets import PelletGroups
from ghost import Group_Ghosts
from fruit import Fruit

class GameControl(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size, 0, 32)
        self.background = None
        #self.Fill_Back()
        pygame.display.set_caption('Pacman Remake')
        pygame.display.set_icon(icon) 
        self.clock = pygame.time.Clock()
        pygame.mixer.music.load('Pac-man theme 1.mp3')
        #pygame.mixer.music.set_volume(0.25)
        pygame.mixer.music.play(-1, 0.0)

        self.pellet_count=0
        self.fruit = None

        self.pause = False
        #self.pac = pygame.transform.scale(pacr, (20, 22))
        #self.clock.tick(30)

    #def Fill_Back(self):
    #    self.background = pygame.surface.Surface(screen_size).convert()
    #    self.background.fill(black)

    def eat_pellets(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if (pellet):
            self.pellet_count += 1
            if (self.pellet_count == 50 or self.pellet_count == 140) and self.fruit is None:
                self.fruit = Fruit(self.Nodes)
            self.pellets.pelletList.remove(pellet)
            if pellet.name == "powerpellet":
                self.ghosts.fright()
    
    def eat_ghost(self):
        ghost = self.pacman.Ghosteat(self.ghosts)
        if ghost is not None:
            if ghost.mode[ghost.modeCount].name == "FRIGHT":
                ghost.spawnMode(speed=2)
            elif ghost.mode[ghost.modeCount].name != "SPAWN":
                quit()

    def start_game(self):
        #pass
        self.Nodes = Group_Nodes("maze.txt")
        self.pellets = PelletGroups("mappellets.txt")
        self.pacman = Pacman(self.Nodes)
        self.ghosts = Group_Ghosts(self.Nodes)
    
    def update(self):
        t = self.clock.tick(60)/1000
        if self.pause == False:
            if self.fruit is not None:
                self.fruit.update(t)
            #self.pacman.update()
            self.pacman.update(t)
            self.ghosts.update(t,self.pacman)
            self.eat_pellets()
            self.ghosts.check_release(self.pellet_count)
            self.check_fruit()
            self.eat_ghost()
        self.pellets.update(t)
        self.checkEvents()
        self.redraw(t)

    def check_fruit(self):
        if self.fruit is not None:
            if self.fruit.disappear == True or self.pacman.eatFruit(self.fruit) is not None:
                self.fruit = None

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    self.pause = not self.pause
            #elif event.type == KEYUP:
            #    self.pacman.pressed = False
                
    def redraw(self,t):
        self.screen.fill(black)
        #for i in range(game_rows):
       #     for j in range(game_cols):
        #        pygame.draw.rect(self.screen, blue,(Tile_Width *(j+0.8) , Tile_Height * (i+0.8), 9, 9))
        self.Nodes.refresh(self.screen)
        self.pellets.draw(self.screen)
        if self.fruit is not None:
            self.fruit.draw(self.screen)
        self.pacman.draw(self.screen)
        self.ghosts.draw(self.screen,t)
        pygame.display.update()


if __name__ == "__main__":
    game = GameControl()
    game.start_game()
    while True:
        game.update()
