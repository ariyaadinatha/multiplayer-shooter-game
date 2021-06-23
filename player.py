import pygame
import os

width = 750
height = 750
# Assets
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "spaceship_red.png"))
YELLOW_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "spaceship_yellow.png"))
BULLET = pygame.image.load(os.path.join("assets", "bullet.png"))

# Define
SHIP_WIDTH = 120
SHIP_HEIGHT = 110

# Transform
RED_SPACE_SHIP = pygame.transform.scale(
    RED_SPACE_SHIP, (SHIP_WIDTH, SHIP_HEIGHT))
YELLOW_SPACE_SHIP = pygame.transform.scale(
    YELLOW_SPACE_SHIP, (SHIP_WIDTH, SHIP_HEIGHT))

imageOfShip = [RED_SPACE_SHIP, YELLOW_SPACE_SHIP]
imageOfAmmo = [BULLET]


class Ship():
    COOLDOWN = 30

    def __init__(self, x, y, shipImage, ammoImage):
        self.x = x
        self.y = y
        self.health = 100
        self.cooldown = 0
        self.ammos = []
        self.vel = 5  # speed
        # self.color = color
        self.shipImage = shipImage
        self.ammoImage = ammoImage
        # self.height = 100
        # self.width = 100

    def draw(self, win):
        # pygame.draw.rect(win, self.color, self.rect)
        # rect = imageOfShip[self.shipImage].get_rect()
        win.blit(imageOfShip[self.shipImage], (self.x, self.y))

        for ammo in self.ammos:
            ammo.draw(win)
        # pygame.mask.from_surface(imageOfShip[self.shipImage])

    def shoot(self):
        if (self.cooldown == 0):
            ammo = Ammo(self.x, self.y, self.ammoImage)
            self.ammos.append(ammo)
            self.cooldown = 1

    def cooldown(self):
        if self.cooldown >= self.COOLDOWN:
            self.cooldown = 0
        elif self.cooldown > 0:
            self.cooldown += 1

    def moveAmmo(self, vel, obj):
        self.cooldown()
        for ammo in self.ammos:
            ammo.move(vel)
        if ammo.off_screen(height):
            self.ammos.remove(ammo)
        elif ammo.collision(obj):
            obj.health -= 10
            self.ammos.remove(ammo)


class Player(Ship):
    def __init__(self, x, y, shipImage, ammoImage):
        super().__init__(x, y, shipImage, ammoImage)
        # self.ship_img = RED_SPACE_SHIP
        # self.ammo_img = BULLET
        # self.mask = pygame.mask.from_surface(imageOfShip[self.shipImage])

        self.maxHealth = self.health
        self.score = 0
        self.lives = 3
        # self.rect = (self.x, self.y, self.width, self.height)

    def move(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and (self.x - self.vel > 0):
            self.x -= self.vel
        if keys[pygame.K_RIGHT] and (self.x + self.vel + SHIP_WIDTH < 750):
            self.x += self.vel
        if keys[pygame.K_UP] and (self.y - self.vel > 0):
            self.y -= self.vel
        if keys[pygame.K_DOWN] and (self.y + self.vel + SHIP_HEIGHT < 750):
            self.y += self.vel
        if keys[pygame.K_SPACE]:
            self.shoot()
        # self.update()

    def moveAmmo(self, vel, objs):
        # self.cooldown()
        for ammo in self.ammos:
            ammo.move(vel)
        # if ammo.off_screen(height):
        #     self.ammos.remove(ammo)
        # else:
        #     for obj in objs:
        #         if ammo.collision(obj):
        #             objs.remove(obj)
        #             self.ammos.remove(ammo)

    def getScore(self):
        return self.score

    def getLives(self):
        return self.lives

    def getHealth(self):
        return self.health


def collide(obj1, obj2):
    offsetX = obj2.x - obj1.x
    offsety = obj2.y - obj1.y
    return obj1.mask.overlap(obj2, (offsetX, offsety)) != None


class Ammo():
    def __init__(self, x, y, ammoImage):
        self.x = x
        self.y = y
        self.ammoImage = ammoImage

    def draw(self, win):
        win.blit(imageOfAmmo[self.ammoImage], (self.x, self.y))

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return (self.y <= height and self.y >= 0)

    def collision(self, obj):
        return collide(self, obj)
