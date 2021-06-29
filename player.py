import time

import pygame

import utilities
from utilities import Group
from projectile import Projectile
from player_objects import Shield
from player_objects import Turret, Medic_Kit, Multi_Gun, Money_Magnet, Shield_Manager


class Player:

    def __init__(self, game, screen):
        self.game = game
        self.screen_rect = screen.get_rect()
        self.width = 150
        self.height = 170
        self.player_image = pygame.transform.scale(pygame.image.load("assets/player.png"), (self.width, self.height))
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.x = 50
        self.rect.y = self.screen_rect[3] - self.height - 20
        self.color = [100, 200, 100]
        self.velocity = 5
        self.all_projectiles = Group()
        self.all_coins = Group()
        self.attack = 15
        self.health = 150
        self.max_health = 150
        self.money = 0
        self.objects = {'Multi gun':(False, 10, '1', pygame.K_1, Multi_Gun, self.game.multigun_logo), 'Turret':(False, 20, '2', pygame.K_2, Turret, self.game.turret_logo), 'Money magnet' : (False, 5, '4', pygame.K_4, Money_Magnet, self.game.magnet_logo), 'Medic kit':(False, 8, '3', pygame.K_3, Medic_Kit, self.game.medic_kit_logo), 'Shield health':(False, 5, '5', pygame.K_5, Shield_Manager,self.game.health_logo)}
        self.all_objects = Group()
        self.health_bar_size = 80


    def draw(self, surface):
        #pygame.draw.rect(surface, self.color, self.rect)
        surface.blit(self.player_image, (self.rect[0], self.rect[1]))

    def moveLeft(self):
        if self.rect.x > 0:
            self.rect.x -= self.velocity

    def moveRight(self):
        collision = False
        for enemy in self.game.all_enemies.get():
            if utilities.collisionRect(enemy.rect, self.rect):
                collision = True

        if self.rect.x < self.screen_rect[2] - self.width and collision == False:
            self.rect.x += self.velocity

    def launchProjectile(self):
        if not self.game.shield.activated:
            self.all_projectiles.add(Projectile(self.game, Projectile.ENEMY, self.game.player))
        else:
            self.game.shield.toogle()

    def damage(self, amount):
        if self.health - amount > 0:
            self.health -= amount

        else:
            print("Playe is dead")
            self.game.explosion_sound.play()
            self.game.screen.fill((0,0,0))
            self.game.screen.blit(pygame.transform.scale(pygame.image.load("assets/back.gif"), (1500, 800)), (0,0))
            self.game.drawUpdate(self.game.screen)
            self.game.screen.blit(self.game.explosion_image, (self.rect.x-int(self.width/2), self.rect.y-int(self.height/2)))
            pygame.display.flip()
            time.sleep(3)
            self.game.is_playing = False
            self.health = self.max_health

    def updateHealth(self, surface):
        maxPV = self.max_health
        c = 0
        while maxPV >= 100:
            pygame.draw.rect(surface, (150, 150, 150), [self.rect.x - int((self.health_bar_size-self.width)/2), self.rect.y - 15, self.health_bar_size, 5])
            maxPV -= 100
        if maxPV != 0:
            pygame.draw.rect(surface, (150, 150, 150), [self.rect.x - int((self.health_bar_size-self.width)/2), self.rect.y - 15, self.health_bar_size, 5])

        PV = self.health
        c = 0
        while PV >= 100:
            pygame.draw.rect(surface, (50, 250-40*c, 50+40*c), [self.rect.x - int((self.health_bar_size-self.width)/2), self.rect.y - 15, self.health_bar_size, 5])
            PV -= 100
            c += 1
        if PV != 0:
            pygame.draw.rect(surface, (50, 250-40*c, 50+40*c), [self.rect.x - int((self.health_bar_size-self.width)/2), self.rect.y - 15, PV/100*self.health_bar_size, 5])
