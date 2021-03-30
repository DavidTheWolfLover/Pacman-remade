from vector import Vector2
import pygame
Tile_Width = 16
Tile_Height = 16
game_rows = 36
game_cols = 28
screen_width = game_cols * Tile_Width 
screen_height = game_rows * Tile_Height
screen_size = (screen_width, screen_height) 
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0,0,255)
yellow = (255,255,0)

UP = Vector2(0,-1)
DOWN = Vector2(0,1)
LEFT = Vector2(-1,0)
RIGHT = Vector2(1,0)
STOP = Vector2(0,0)

pacr = pygame.image.load(r'C:\Users\kitty\Desktop\Pacman\Pacman-Remake\Pacman-remake-sprites\pacright.png')
pacl = pygame.image.load(r'C:\Users\kitty\Desktop\Pacman\Pacman-Remake\Pacman-remake-sprites\pacleft.png')
pacu = pygame.image.load(r'C:\Users\kitty\Desktop\Pacman\Pacman-Remake\Pacman-remake-sprites\pacup.png')
pacd = pygame.image.load(r'C:\Users\kitty\Desktop\Pacman\Pacman-Remake\Pacman-remake-sprites\pacdown.png')

ghost1 = pygame.image.load(r'C:\Users\kitty\Desktop\Pacman\Pacman-Remake\Pacman-remake-sprites\smallghosttest.png')


