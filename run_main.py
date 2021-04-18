import pygame
import sys
from run import GameControl
from run2 import GameControl2
from constants import *


def main():
    pygame.init()
    pygame.display.set_caption('Pacman Remake')
    pygame.display.set_icon(icon) 
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode(screen_size, 0, 32)
    font = pygame.font.Font("PressStart2P-Regular.ttf", 16)
    text1 = font.render("Normal", 1, black)
    text2 = font.render("Chase", 1, black)
    text3 = font.render("Made by Tri, Khoa & Duc", 1, matcha)
    button1 = pygame.Rect(50, 350, 150, 50)
    button2 = pygame.Rect(250, 350, 150, 50)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos  # gets mouse position

                # checks if mouse position is over the button

                if button1.collidepoint(mouse_pos):
                    game = GameControl()
                    game.start_game()
                    while True:
                        game.update()
                if button2.collidepoint(mouse_pos):
                    # prints current location of mouse
                    game = GameControl2()
                    game.start_game()
                    while True:
                        game.update()
        screen.fill(black)
        pygame.draw.rect(screen, red, button1)
        pygame.draw.rect(screen, green, button2)
        screen.blit(logo,(0,70))
        p1 = (80, 370)
        screen.blit(text1, p1)
        p2 = (285, 370)
        screen.blit(text2, p2)
        p3 = (40,470)
        screen.blit(text3, p3)
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
    sys.exit


if __name__ == '__main__':
    main()

'''if __name__ == "__main__":


    mode = 2
    if mode == 1:
        game = GameControl()
        game.start_game()
        while True:
            game.update()
    else:
        game = GameControl2()
        game.start_game()
        while True:
            game.update()'''
