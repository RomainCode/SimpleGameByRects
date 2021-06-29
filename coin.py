import pygame
from utilities import collisionRect
import time

class Coin:

    def __init__(self, game, position, value):
        self.game = game
        self.width = 5
        self.height = 5
        self.radius = 5
        self.time_durability = 20
        self.time_creation = time.time()
        self.visibility = 1
        self.rect = pygame.Rect(position[0], position[1], self.width, self.height)
        self.value = value
        self.color = (200, 200, 255-40*self.value)
        if self.value <=2:
            self.img = self.game.small_xp
        elif self.value <=3:
            self.img = self.game.medium_xp
        else:
            self.img = self.game.big_xp

    def draw(self, surface):
        #pygame.draw.circle(surface, (self.color[0]*self.visibility, self.color[1]*self.visibility, self.color[2]*self.visibility), (self.rect.x, self.rect.y), self.radius)
        surface.blit(self.img, (self.rect.x-self.img.get_size()[0]+self.width, self.rect.y-self.img.get_size()[1]+self.height))

    def handle(self):
        if self.time_creation + self.time_durability < time.time():
            self.visibility -= 0.02
        if self.visibility <= 0.5:
            self.game.player.all_coins.remove(self)
        if self.rect.y + self.radius < self.game.ground_origin[1]:
            self.rect.y += 2
        if collisionRect(self.game.player.rect, self.rect):
            self.game.player.money += self.value
            self.game.player.all_coins.remove(self)