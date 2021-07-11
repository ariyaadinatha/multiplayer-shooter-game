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
second_font = pygame.font.SysFont("comicsans", 30)

lose = False


def redrawWindow(win, player, player2):
    win.blit(BACKGROUND, (0, 0))
    # Score
    score1_label = main_font.render(
        f"score: {player.getScore()}", 1, (255, 255, 255))
    score2_label = main_font.render(
        f"score: {player2.getScore()}", 1, (255, 255, 255))
    # Lives
    lives1_label = main_font.render(
        f"lives: {player.getLives()}", 1, (255, 255, 255))
    lives2_label = main_font.render(
        f"lives: {player2.getLives()}", 1, (255, 255, 255))
    # Health
    health1_label = main_font.render(
        f"hp: {player.getHealth()}", 1, (255, 255, 255))
    health2_label = main_font.render(
        f"hp: {player2.getHealth()}", 1, (255, 255, 255))
    # Command
    move_label = second_font.render(
        f"Use arrow key to move", 1, (255, 255, 255))
    shoot_label = second_font.render(
        f"Space to shoot", 1, (255, 255, 255))
    shop_label = second_font.render(
        f"E to upgrade weapon", 1, (255, 255, 255))
    price_label = second_font.render(
        f"Upgrade cost 1 / 2 = 100 / 250 score", 1, (255, 255, 255))

    win.blit(score1_label, (10, lives2_label.get_height() + 10))
    win.blit(lives1_label, (10, 10))
    win.blit(score2_label, (width - score2_label.get_width() -
                            10, lives1_label.get_height() + 10))
    win.blit(lives2_label, (width - lives2_label.get_width() - 10, 10))
    win.blit(health1_label, (player.getX() -
                             health1_label.get_width(), player.getY()))
    win.blit(health2_label, (player2.getX() -
                             health2_label.get_width(), player2.getY()))
    win.blit(move_label, (10, move_label.get_height() + 600))
    win.blit(shoot_label, (10, shoot_label.get_height() +
                           move_label.get_height() + 600))
    win.blit(shop_label, (10, shop_label.get_height() +
                          shoot_label.get_height() + move_label.get_height() + 600))
    win.blit(price_label, (10, price_label.get_height() + shop_label.get_height() +
                           shoot_label.get_height() + move_label.get_height() + 600))

    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def loseLabel():
    lose_label = main_font.render("You Lose", 1, (255, 255, 255))
    win.blit(lose_label, (width/2 - lose_label.get_width()/2, height/2))
    pygame.display.update()


def main():
    run = True
    FPS = 60
    n = Network()
    p = n.getObject()
    clock = pygame.time.Clock()
    ammoVel = -5

    if (p.getShip() == 1):
        ammoVel = -ammoVel

    while run:
        clock.tick(FPS)
        p2 = n.send(p)
        redrawWindow(win, p, p2)

        if (p.getHealth() <= 0):
            p.reduceLives()
            p.restoreHealth(100)
        if (p.getLives() <= 0):
            loseLabel()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move()

        p.moveAmmo(ammoVel, p2)


main()
