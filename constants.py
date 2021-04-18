from vector import Vector2
import pygame
import os
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
blue = (0, 0, 255)
yellow = (255, 255, 0)
pink = (255, 100, 150)
teal = (100, 255, 255)
orange = (230, 190, 40)
matcha = (0, 255, 170)
orange = (255, 85, 0)

UP = Vector2(0,-1)
DOWN = Vector2(0,1)
LEFT = Vector2(-1,0)
RIGHT = Vector2(1,0)
STOP = Vector2(0,0)

pacr = pygame.image.load(os.path.join("assets","pacright.png"))
pacl = pygame.image.load(os.path.join("assets","pacleft.png"))
pacu = pygame.image.load(os.path.join("assets","pacup.png"))
pacd = pygame.image.load(os.path.join("assets","pacdown.png"))

icon = pygame.image.load(os.path.join("assets","pacright.png"))

rr = pygame.image.load(os.path.join("assets","redrightsmall.png"))
rl = pygame.image.load(os.path.join("assets","redleftsmall.png"))
ru = pygame.image.load(os.path.join("assets","redupsmall.png"))
rd = pygame.image.load(os.path.join("assets","reddownsmall.png"))

br = pygame.image.load(os.path.join("assets","bluerightsmall.png"))
bl = pygame.image.load(os.path.join("assets","blueleftsmall.png"))
bu = pygame.image.load(os.path.join("assets","blueupsmall.png"))
bd = pygame.image.load(os.path.join("assets","bluedownsmall.png"))

gr = pygame.image.load(os.path.join("assets","greenrightsmall.png"))
gl = pygame.image.load(os.path.join("assets","greenleftsmall.png"))
gu = pygame.image.load(os.path.join("assets","greenupsmall.png"))
gd = pygame.image.load(os.path.join("assets","greendownsmall.png"))

pr = pygame.image.load(os.path.join("assets","purplerightsmall.png"))
pl = pygame.image.load(os.path.join("assets","purpleleftsmall.png"))
pu = pygame.image.load(os.path.join("assets","purpleupsmall.png"))
pd = pygame.image.load(os.path.join("assets","purpledownsmall.png"))

ar = pygame.image.load(os.path.join("assets","eyesrightsmall.png"))
al = pygame.image.load(os.path.join("assets","eyesleftsmall.png"))
au = pygame.image.load(os.path.join("assets","eyesupsmall.png"))
ad = pygame.image.load(os.path.join("assets","eyesdownsmall.png"))

ghostr = [rr,br,gr,pr]
ghostl = [rl,bl,gl,pl]
ghostu = [ru,bu,gu,pu]
ghostd = [rd,bd,gd,pd]

strike_white = pygame.image.load(os.path.join("assets","strike-white.png"))
strike_red = pygame.image.load(os.path.join("assets","strike-red.png"))

ghosttarget = pygame.image.load(os.path.join("assets","targetghostsmall.png"))
ghosttargetr = pygame.image.load(os.path.join("assets","targetghostrevertsmall.png"))

#fruit = pygame.image.load(os.path.join("assets","cherrybonussmall.png"))
fruit = pygame.image.load(os.path.join("assets","cherrybonus-1.png"))

logo = pygame.image.load(os.path.join("assets","logo_small.png"))



