import pygame


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
