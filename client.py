import pygame
import os
import random
import time
from network import Network
from player import Player
pygame.font.init()

# Inisialisasi
width = 750
height = 750
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Client")

# Assets Load
BACKGROUND = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "space.png")), (width, height))

main_font = pygame.font.SysFont("comicsans", 50)

lose = False


def redrawWindow(win, player, player2):
    #win.fill((255, 255, 255))
    win.blit(BACKGROUND, (0, 0))
    score1_label = main_font.render(
        f"score: {player.getScore()}", 1, (255, 255, 255))
    score2_label = main_font.render(
        f"score: {player2.getScore()}", 1, (255, 255, 255))
    lives1_label = main_font.render(
        f"lives: {player.getLives()}", 1, (255, 255, 255))
    lives2_label = main_font.render(
        f"lives: {player2.getLives()}", 1, (255, 255, 255))
    win.blit(score1_label, (10, lives2_label.get_height() + 10))
    win.blit(lives1_label, (10, 10))
    win.blit(score2_label, (width - score2_label.get_width() -
                            10, lives1_label.get_height() + 10))
    win.blit(lives2_label, (width - lives2_label.get_width() - 10, 10))

    if (lose == True):
        lose_label = main_font.render("You Lose", 1, (255, 255, 255))
        win.blit(lose_label, (width - lose_label.get_width()/2, height/2))

    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    FPS = 60
    n = Network()
    p = n.getObject()
    clock = pygame.time.Clock()
    while run:
        clock.tick(FPS)
        p2 = n.send(p)

        # print(p.getLives())

        if (p.getLives() == 3):
            lose = True
        # print(lose)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move()
        redrawWindow(win, p, p2)

        p.moveAmmo(5, p2)
        print(p.getHealth())


main()
