import time
import pygame
import random
import utilities
from utilities import collisionRect


class Shield:

    def __init__(self, game):
        self.shield_image = pygame.transform.scale(pygame.image.load("assets/aura.png"), (200,200))
        self.game = game
        self.width = 10
        self.height = self.game.player.height
        self.distance_with_player = 20
        print(self.game.player.rect)
        self.rect = pygame.Rect(self.game.player.rect[0] + self.distance_with_player, self.game.player.rect.y,
                                self.width, self.height)
        self.color = (100, 70, 35)
        self.activated = True
        self.durability = 200
        self.max_durability = 400

    def draw(self, surface):
        if self.activated:
            #pygame.draw.rect(surface, self.color, self.rect)
            surface.blit(self.shield_image, (self.game.player.rect.x-25, self.game.player.rect.y-10))

    def handle(self):
        if self.game.shield.durability < 0:
            self.game.shield.activated = False
        self.rect.x = self.game.player.rect.x + self.game.player.width + self.distance_with_player

    def toogle(self):
        if self.activated:
            self.activated = False
        else:
            self.activated = True


class Turret:

    def __init__(self, game):
        self.game = game
        self.durability = 50
        self.health = 20
        self.max_health = 20
        self.width = 90
        self.height = 70
        self.turret_image = pygame.transform.scale(pygame.image.load("assets/turret.png"), (self.width, self.height))
        self.rect = pygame.Rect(self.game.player.rect.x, int(self.game.player.screen_rect[3] / (120 / 100)), self.width, self.height)
        self.gun_rect = pygame.Rect(self.rect.x + 70, self.rect.y + 5, 25, 10)
        self.color = (50, 50, 200)

    def handle(self):
        if self.rect.bottomleft[1] < self.game.ground_origin[1]:
            self.rect.y += 1
            self.gun_rect.y += 1

        if self.durability > 0:
            if random.randint(0, 20) == 5:
                self.game.player.all_projectiles.add(self.game.Projectile(self.game, self.game.Projectile.ENEMY, self))
                self.durability -= 1
        else:
            self.game.player.all_objects.remove(self)

        self.updateHealth()

    def draw(self, surface):
        #pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, self.game.projectile_launcher.color, self.gun_rect)
        surface.blit(self.turret_image, (self.rect.x, self.rect.y))
        self.drawHealthBar(surface)

    def updateHealth(self):
        for obj in self.game.all_enemies.get():
            if collisionRect(self.rect, obj.rect):
                self.health -= obj.attack

        for pro in self.game.player.all_projectiles.get():
            if pro.target == self.game.Projectile.PLAYER:
                if collisionRect(self.rect, pro.rect):
                    self.health -= obj.attack
                    pro.remove()

        if self.health < 0:
            self.game.player.all_objects.remove(self)

    def drawHealthBar(self, surface):
        pygame.draw.rect(surface, (100, 100, 100), (self.rect.x+25, self.rect.y-10, int(self.max_health/self.max_health*50), 3))
        pygame.draw.rect(surface, (20, 200, 20), (self.rect.x+25, self.rect.y-10, int(self.health/self.max_health*50), 3))


class Medic_Kit:

    def __init__(self, game):
        self.amount = 50
        self.game = game

    def handle(self):
        if self.game.player.health + 50 > self.game.player.max_health:
            self.game.player.health = self.game.player.max_health
        else:
            self.game.player.health += self.amount

        self.game.player.all_objects.remove(self)

    def draw(self):
        pass


class Multi_Gun:

    def __init__(self, game):
        self.game = game
        self.factor = 2
        self.durability = 50
        self.rect = pygame.Rect(self.game.player.rect.x + self.game.player.rect[2] - 15, self.game.player.rect[1] + 116,35, 10)



    def handle(self):
        self.rect = pygame.Rect(self.game.player.rect.x + self.game.player.rect[2] - 15, self.game.player.rect[1] + 116,35, 10)
        if self.durability > 0:
            if random.randint(0, 10) == 5:
                self.game.player.all_projectiles.add(
                    self.game.Projectile(self.game, self.game.Projectile.ENEMY, self.game.player))
                self.durability -= 1
        else:
            self.game.player.all_objects.remove(self)

    def draw(self, surface):
        pygame.draw.rect(surface, (30, 30, 30), self.rect)


class Money_Magnet:

    def __init__(self, game):
        self.game = game
        self.durability = 50
        self.time_durability = 25
        self.time_start = time.time()

    def handle(self):
        if self.durability > 0 or self.time_start + self.time_durability > time.time():
            coins = self.game.player.all_coins

            for coin in coins.get():
                if self.game.player.rect.x < coin.rect.x:
                    coin.rect.x -= 3
                if self.game.player.rect.x > coin.rect.x:
                    coin.rect.x += 3
                if utilities.collisionRect(pygame.Rect(coin.rect.x, coin.rect.y, coin.rect[2]+20, coin.rect[3]+20), self.game.player.rect):
                    self.durability -= 1

        else:
            self.game.player.all_objects.remove(self)

    def draw(self, surface):
        pass


class Shield_Manager:

    def __init__(self, game):
        self.game = game
        self.add_durability = 50

    def handle(self):
        if self.game.shield.durability + self.add_durability > self.game.shield.max_durability:
            self.game.shield.durability = self.game.shield.max_durability
        else:
            self.game.shield.durability += self.add_durability

        self.game.player.all_objects.remove(self)

    def draw(self, surface):
        pass

class Armor:

    def __init__(self, game):
        self.game = game
        self.pos = (self.game.player.rect.x, self.game.player.rect.y)
        self.width = 2
        self.color = [100, 200, 100]

    def handle(self):
        self.pos = (self.game.player.rect.x, self.game.player.rect.y)

    def draw(self, surface):
        #pygame.draw.line(surface, self.color, self.pos, (self.pos[0] + self.game.player.width, self.pos[1]), self.width)
        #pygame.draw.line(surface, self.color, (self.pos[0] + self.game.player.width, self.pos[1]), (self.pos[0] + self.game.player.width, self.pos[1] + self.game.player.height), self.width)
        #pygame.draw.line(surface, self.color, (self.pos[0] + self.game.player.width, self.pos[1] + self.game.player.height), (self.pos[0], self.pos[1] + self.game.player.height), self.width)
        #pygame.draw.line(surface, self.color, (self.pos[0], self.pos[1] + self.game.player.height), self.pos, self.width)
        pass

class Projectile_Launcher:

    def __init__(self, game):
        self.game = game
        self.rect = pygame.Rect(self.game.player.rect.x + 5, self.game.player.rect.y + 15, 35, 10)
        self.color = (80, 50, 15)

    def handle(self):
        self.rect = pygame.Rect(self.game.player.rect.x + self.game.player.rect[2] - 15, self.game.player.rect[1] + 116, 35, 10)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)