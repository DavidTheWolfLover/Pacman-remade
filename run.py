import pygame
import time
from pygame.locals import *
from constants import *
from nodes import Group_Nodes
from pacman import *
from pellets import PelletGroups
from ghost import Group_Ghosts
from fruit import Fruit
from pause import Pause
from text import Group_Text

class Level(object):
    def __init__(self):
        self.lvl = [["maze.txt","mappellets.txt",0]]
        self.current_lvl = 0

    def new_lvl(self):
        return self.lvl[self.current_lvl % len(self.lvl)]


class GameControl(object):
    def __init__(self):
        pygame.mixer.init()
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
        self.text = Group_Text()
        self.score = 0
        self.highscore = 0

        self.pause = Pause(True)
        self.level = Level()
        self.end_game = False
        self.chase_music = pygame.mixer.Sound("chase_theme_2.wav")
        self.switch_music = False
        self.switch_time = 0

        self.quit = False
        #self.pac = pygame.transform.scale(pacr, (20, 22))
        #self.clock.tick(30)

    #def Fill_Back(self):
    #    self.background = pygame.surface.Surface(screen_size).convert()
    #    self.background.fill(black)

    def eat_pellets(self):
        pellet = self.pacman.eatPellets(self.pellets.pelletList)
        if (pellet):
            self.score += pellet.points
            self.pellet_count += 1
            if (self.pellet_count == 50 or self.pellet_count == 140) and self.fruit is None:
                self.fruit = Fruit(self.Nodes)
            self.pellets.pelletList.remove(pellet)
            if (len(self.pellets.pelletList) == 0):
            #if (self.pellet_count == 10): #debug mode (check next lvl immediately)
                self.ghosts.hide()
                self.pacman.visible = False
                self.pause.start(3, "finish")
            if pellet.name == "powerpellet":
                self.ghosts.reset_points()
                self.ghosts.fright()
                self.chase_music.stop()
                self.chase_music.play()
                pygame.mixer.music.pause()
                self.switch_music = True
                self.switch_time = 0
    
    def eat_ghost(self):
        ghost = self.pacman.Ghosteat(self.ghosts)
        if ghost is not None:
            if ghost.mode[ghost.modeCount].name == "FRIGHT":
                self.switch_time -= 1
                self.score += ghost.points
                self.text.Create_Temptxt(ghost.points,ghost.location.x-10,ghost.location.y)
                self.ghosts.up_points()
                ghost.spawnMode(speed=2)
                self.pause.start(1)
                self.pacman.visible = False
                ghost.visible = False
            elif ghost.mode[ghost.modeCount].name != "SPAWN":
                self.pacman.lives -= 1
                self.ghosts.hide()
                self.pause.start(3,"dead")

    def start_game(self):
        #pass
        self.level.current_lvl = 0
        maze = self.level.new_lvl()
        self.Nodes = Group_Nodes(maze[0])
        self.pellets = PelletGroups(maze[1])
        self.pacman = Pacman(self.Nodes)
        self.ghosts = Group_Ghosts(self.Nodes)
        self.pellet_count = 0
        self.fruit = None
        self.pause.force(True)
        self.pause.pauseType = None
        self.end_game = False

        self.text.Reset_Color(self.highscore)
        self.score = 0

        self.text.Ready()
        self.text.Update_Level(self.level.current_lvl)

    def next_lvl(self):
        self.level.current_lvl += 1
        maze = self.level.new_lvl()
        self.Nodes = Group_Nodes(maze[0])
        self.pellets = PelletGroups(maze[1])
        self.pacman.initial_location()
        self.ghosts = Group_Ghosts(self.Nodes)
        self.pellet_count = 0
        self.fruit = None
        self.pause.force(True)
        self.screen.fill(black)
        pygame.display.update()
        time.sleep(0.8)
        self.text.Ready()
        self.text.Update_Level(self.level.current_lvl)

    def restart_lvl(self):
        self.pacman.initial_location()
        self.ghosts = Group_Ghosts(self.Nodes)
        self.fruit = None
        self.pause.force(True)
        self.text.Ready()

    def update(self):
        t = self.clock.tick(60)/1000
        if self.end_game == False:
            if self.switch_music == True:
                self.switch_time += t
                if self.switch_time >= 7:
                    pygame.mixer.music.unpause()
                    self.switch_time = 0
                    self.switch_music = False
                #self.pacman.update()
            if self.pause.check_pause == False:
                if self.fruit is not None:
                    self.fruit.update(t)
                self.pacman.update(t)
                self.ghosts.update(t,self.pacman)
                if self.pause.pauseType == "finish":
                    self.resolve_clear_lvl()
                elif self.pause.pauseType == "dead":
                    self.resolve_restart_lvl()
                self.eat_pellets()
                self.ghosts.check_release(self.pellet_count)
                self.check_fruit()
                self.eat_ghost()
            self.pause.update(t)
            self.pellets.update(t)
            self.text.update(t)
        self.checkEvents()
        self.text.Update_Score(self.score)
        if self.score > self.highscore:
            self.highscore = self.score
            self.text.Update_Highscore(self.highscore)
        self.redraw(t)

    def resolve_clear_lvl(self):
        self.next_lvl()
        self.pause.pauseType = None
    
    def resolve_restart_lvl(self):
        if self.pacman.lives == 0:
            self.end_game = True
            self.pacman.visible = False
            self.text.GameOver()
        else:
            self.restart_lvl()
        self.pause.pauseType = None

    def check_fruit(self):
        if self.fruit is not None:
            if self.pacman.eatFruit(self.fruit) is not None:
                self.score += self.fruit.points
                self.text.Create_Temptxt(self.fruit.points,self.fruit.location.x-10,self.fruit.location.y)
                self.fruit = None
            elif self.fruit.disappear == True:
                self.fruit = None

    def checkEvents(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    if self.end_game == True:
                        self.start_game()
                    else:
                        self.pause.player()
                        if self.pause.check_pause == True:
                            self.text.Pause()
                        else:
                            self.text.Hide_All()
                elif event.key == K_ESCAPE:
                    self.quit = True


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
        self.pacman.draw_lives(self.screen)
        self.ghosts.draw(self.screen,t)
        self.text.draw(self.screen)
        pygame.display.update()


'''if __name__ == "__main__":
    game = GameControl()
    game.start_game()
    while True:
        game.update()'''
