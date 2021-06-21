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
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "spaceship_red.png"))
YELLOW_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "spaceship_yellow.png"))
BULLET = pygame.image.load(os.path.join("assets", "bullet.png"))
BACKGROUND = pygame.transform.scale(pygame.image.load(
    os.path.join("assets", "space.png")), (width, height))

main_font = pygame.font.SysFont("comicsans", 50)

# banyak orang yang connect
clientNumber = 0
score1 = 0
score2 = 0
lives1 = 3
lives2 = 3


class Player():
    def __init__(self, x, y, width, height, health, color):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.health = health
        self.color = color
        self.ship_img = None
        self.ammo_img = None
        self.ammo = []
        self.cooldown = 0
        self.rect = (x, y, width, height)
        self.vel = 3  # speed

    def draw(self, win):
        pygame.draw.rect(win, self.color, self.rect)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.x -= self.vel
        if keys[pygame.K_RIGHT]:
            self.x += self.vel
        if keys[pygame.K_UP]:
            self.y -= self.vel
        if keys[pygame.K_DOWN]:
            self.y += self.vel
        self.update()

    def update(self):
        self.rect = (self.x, self.y, self.width, self.height)


# baca posisi player
def read_pos(str):
    str = str.split(",")
    return int(str[0]), int(str[1])


def make_pos(tup):
    return str(tup[0]) + "," + str(tup[1])


def redrawWindow(win, player, player2):
    #win.fill((255, 255, 255))
    win.blit(BACKGROUND, (0, 0))
    score1_label = main_font.render(f"score: {score1}", 1, (255, 255, 255))
    score2_label = main_font.render(f"score: {score2}", 1, (255, 255, 255))
    lives1_label = main_font.render(f"lives: {lives1}", 1, (255, 255, 255))
    lives2_label = main_font.render(f"lives: {lives2}", 1, (255, 255, 255))
    win.blit(score1_label, (10, lives2_label.get_height() + 10))
    win.blit(lives1_label, (10, 10))
    win.blit(score2_label, (width - score2_label.get_width() -
                            10, lives1_label.get_height() + 10))
    win.blit(lives2_label, (width - lives2_label.get_width() - 10, 10))

    player.draw(win)
    player2.draw(win)
    pygame.display.update()


def main():
    run = True
    FPS = 60
    n = Network()

    clock = pygame.time.Clock()

    # player pos
    startPos = read_pos(n.getPos())
    p = Player(startPos[0], startPos[1], 100, 100, 100, (0, 255, 0))
    p2 = Player(68, 60, 100, 100, 100, (255, 0, 0))

    while run:
        clock.tick(FPS)
        # kirim posisi
        p2Pos = read_pos(n.send(make_pos((p.x, p.y))))
        p2.x = p2Pos[0]
        p2.y = p2Pos[1]
        p2.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        p.move()
        redrawWindow(win, p, p2)


main()
