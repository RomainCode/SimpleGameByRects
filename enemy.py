import random
from utilities import  Group
import pygame
from projectile import Projectile
import game
import utilities
from coin import Coin


class Enemy:

    def __init__(self, game, screen):
        self.game = game
        self.screen = screen.get_rect()
        self.screen_rect = screen.get_rect()
        self.width = 75
        self.height = 120
        self.max_health = 100
        self.health = 100
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.enemy_image = pygame.transform.scale(pygame.image.load("assets/enemy.png"), (self.width, self.height))
        self.rect.x = int(self.screen[2] - 100)
        self.rect.y = self.screen_rect[3] - self.height - 20
        self.color = [200, 100, 100]
        self.velocity = random.randint(1, 4)
        self.attack = 0.9
        self.projectile_attack = 3
        self.health_bar_size = 50

    def draw(self, surface):
        #pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.enemy_image, (self.rect[0], self.rect[1]))

    def moveLeft(self):
        if utilities.collisionRect(self.rect, self.game.player.rect):
            self.game.player.damage(self.attack)
        else:
            if self.rect.x > 0:
                self.rect.x -= self.velocity

    def moveRight(self):
        if utilities.collisionRect(self.rect, self.game.player.rect):
            self.game.player.damage(self.attack)
        else:
            if self.rect.x < self.screen[2] - self.width:
                self.rect.x += self.velocity

    def damage(self, amount):
        self.health -= amount

        if self.health < 0:
            self.game.addEnemy()
            self.game.score += 1
            self.game.player.all_projectiles.add(Projectile(self.game, Projectile.PLAYER, self))
            self.game.player.all_coins.add(Coin(self.game, (self.rect.x, self.rect.y), random.randint(1, 4)))
            self.game.all_enemies.remove(self)


    def updateHealth(self, surface):
        pygame.draw.rect(surface, (150, 150, 150 ), [self.rect.x - int((self.health_bar_size-self.width)/2), self.rect.y-10, int(self.max_health/self.max_health*self.health_bar_size), 5])
        pygame.draw.rect(surface, (50, 250, 50), [self.rect.x - int((self.health_bar_size-self.width)/2), self.rect.y-10, int(self.health/self.max_health*self.health_bar_size), 5])

