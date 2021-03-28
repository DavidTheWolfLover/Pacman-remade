import pygame
from pygame.locals import *
from constants import *
from nodes import Group_Nodes
from pacman import *
from pellets import PelletGroups
from ghost import Ghost

class GameControl(object):
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(screen_size, 0, 32)
        self.background = None
        #self.Fill_Back()
        pygame.display.set_caption('Pacman Remake')
        self.clock = pygame.time.Clock()
        #pygame.mixer.music.load('Pac-man theme.mp3')
        #pygame.mixer.music.play(-1, 0.0)


        #self.pac = pygame.transform.scale(pacr, (20, 22))
        #self.clock.tick(30)

    #def Fill_Back(self):
    #    self.background = pygame.surface.Surface(screen_size).convert()
    #    self.background.fill(black)

    def eat_pellets(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if (pellet):
            self.pellets.pelletList.remove(pellet)

    def start_game(self):
        #pass
        self.Nodes = Group_Nodes("maze.txt")
        self.pellets = PelletGroups("mappellets.txt")
        self.pacman = Pacman(self.Nodes)
        self.ghost = Ghost(self.Nodes)
    
    def update(self):
        t = self.clock.tick(30)/1000
        #self.pacman.update()
        self.pacman.update(t)
        self.ghost.update(t,self.pacman)
        self.pellets.update(t)
        self.eat_pellets()
        if (self.pacman.Ghosteat(self.ghost) == True):
            exit()
        self.checkEvents()
        self.redraw()

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            #elif event.type == KEYUP:
            #    self.pacman.pressed = False
                
    def redraw(self):
        self.screen.fill(black)
        #for i in range(game_rows):
       #     for j in range(game_cols):
        #        pygame.draw.rect(self.screen, blue,(Tile_Width *(j+0.8) , Tile_Height * (i+0.8), 9, 9))
        self.Nodes.refresh(self.screen)
        self.pellets.draw(self.screen)
        self.pacman.draw(self.screen)
        self.ghost.draw(self.screen)
        pygame.display.update()


if __name__ == "__main__":
    game = GameControl()
    game.start_game()
    while True:
        game.update()
