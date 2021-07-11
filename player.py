import pygame
import os
pygame.font.init()

width = 750
height = 750

# Assets
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "spaceship_red.png"))
YELLOW_SPACE_SHIP = pygame.image.load(
    os.path.join("assets", "spaceship_yellow.png"))
BULLET = pygame.image.load(os.path.join("assets", "bullet.png"))
BOMB = pygame.image.load(os.path.join("assets", "bomb.png"))
BEAM = pygame.image.load(os.path.join("assets", "beam.png"))
main_font = pygame.font.SysFont("comicsans", 50)

# Define
SHIP_WIDTH = 120
SHIP_HEIGHT = 110
BULLET_WIDTH = BULLET.get_width()
BULLET_HEIGHT = BULLET.get_height()
BEAM_WIDTH = BULLET.get_width()
BEAM_HEIGHT = BULLET.get_height() + 15
BULLET_CENTER = SHIP_WIDTH / 2 - 15
COOLDOWN_TIME = 30

# Transform
RED_SPACE_SHIP = pygame.transform.scale(
    RED_SPACE_SHIP, (SHIP_WIDTH, SHIP_HEIGHT))
YELLOW_SPACE_SHIP = pygame.transform.scale(
    YELLOW_SPACE_SHIP, (SHIP_WIDTH, SHIP_HEIGHT))
YELLOW_SPACE_SHIP = pygame.transform.rotate(YELLOW_SPACE_SHIP, 180)
BOMB = pygame.transform.scale(
    BOMB, (BULLET_WIDTH, BULLET_HEIGHT))
BEAM = pygame.transform.scale(
    BEAM, (BULLET_WIDTH, BULLET_HEIGHT))
BEAM = pygame.transform.rotate(BEAM, 90)


imageOfShip = [RED_SPACE_SHIP, YELLOW_SPACE_SHIP]
imageOfAmmo = [BULLET, BOMB, BEAM]


class Ship():

    def __init__(self, x, y, shipImage, ammoImage):
        self.x = x
        self.y = y
        self.health = 100
        self.cooldown = 0
        self.ammos = []
        self.vel = 5  # speed
        self.shipImage = shipImage
        self.ammoImage = ammoImage
        self.hitbox = (self.x, self.y, SHIP_WIDTH, SHIP_HEIGHT)
        self.damage = 10

    def draw(self, win):
        win.blit(imageOfShip[self.shipImage], (self.x, self.y))
        self.hitbox = (self.x, self.y, SHIP_WIDTH, SHIP_HEIGHT)

        for ammo in self.ammos:
            ammo.draw(win)

    def shoot(self):
        if (self.cooldown == 0):
            ammo = Ammo((self.x + BULLET_CENTER), self.y, self.ammoImage)
            self.ammos.append(ammo)
            self.cooldown = 1

    def moveAmmo(self, vel, obj):
        # cooldown
        if self.cooldown >= COOLDOWN_TIME:
            self.cooldown = 0
        elif self.cooldown > 0:
            self.cooldown += 1
        for ammo in self.ammos:
            if (ammo.y < obj.hitbox[1] + obj.hitbox[3] and ammo.y > obj.hitbox[1]):
                if (ammo.x > obj.hitbox[0] and ammo.x < obj.hitbox[0] + SHIP_WIDTH):
                    self.ammos.remove(ammo)
                    self.hit(obj)

            ammo.move(vel)
            if ammo.off_screen(height):
                self.ammos.remove(ammo)
                self.addScore(self.damage)

    def hit(self, p2):
        self.reduceHealth()
        p2.addScore(100)

    def getHealth(self):
        return self.health

    def reduceHealth(self):
        self.health -= self.getDamage()


class Player(Ship):
    def __init__(self, x, y, shipImage, ammoImage):
        super().__init__(x, y, shipImage, ammoImage)

        self.maxHealth = self.health
        self.score = 0
        self.lives = 3

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
        if keys[pygame.K_e]:
            self.shop()

    def addScore(self, val):
        self.score += val

    def getScore(self):
        return self.score

    def reduceScore(self, val):
        self.score -= val

    def getLives(self):
        return self.lives

    def reduceLives(self):
        self.lives -= 1

    def getHealth(self):
        return self.health

    def restoreHealth(self, health):
        self.health += health

    def getShip(self):
        return self.shipImage

    def getX(self):
        return self.x

    def getY(self):
        return self.y

    def upAmmo(self):
        self.ammoImage += 1

    def getAmmo(self):
        return self.ammoImage

    def getDamage(self):
        return self.damage

    def addDamage(self, val):
        self.damage += val

    def shop(self):
        if (self.getAmmo() == 0 and self.getScore() >= 100):
            self.reduceScore(100)
            self.upAmmo()
            self.addDamage(20)
        elif (self.getAmmo() == 1 and self.getScore() >= 250):
            self.reduceScore(250)
            self.upAmmo()
            self.addDamage(40)


class Ammo():
    def __init__(self, x, y, ammoImage):
        self.x = x
        self.y = y
        self.ammoImage = ammoImage
        self.hitbox = (self.x, self.y, 30, 15)

    def draw(self, win):
        win.blit(imageOfAmmo[self.ammoImage], (self.x, self.y))
        self.hitbox = (self.x, self.y, BULLET_WIDTH, BULLET_HEIGHT)

    def move(self, vel):
        self.y += vel

    def off_screen(self, height):
        return not(self.y <= height and self.y >= 0)
