import pygame
import utilities


class Projectile:

    PLAYER = "target_player"
    ENEMY = "target_enemy"

    def __init__(self, game, target, from_entity):
        self.target = target
        self.game = game
        if self.game.is_projectile_sound: self.game.blaster.play()
        self.from_entity = from_entity
        self.width = 5
        self.height = 5
        self.rect = pygame.Rect(self.from_entity.rect.x + self.from_entity.width + 1, self.from_entity.rect.y + 20,self.width, self.height)
        if self.target == Projectile.PLAYER:
            self.color = (0, 200, 0)
            self.velocity = -5
            self.rect.y = self.game.player.screen_rect[3] - 75
        if self.target == Projectile.ENEMY:
            self.color = (255, 0, 0)
            self.velocity = 5
            self.rect.y = self.game.player.screen_rect[3] - 75
        self.removable = False
        self.enemy_projectile_attack = 3

    def draw(self, surface):
        #pygame.draw.rect(surface, self.color, self.rect)
        if self.target == Projectile.ENEMY:
            surface.blit(self.game.green_projectile, (self.rect.x, self.rect.y))
        if self.target == Projectile.PLAYER:
            surface.blit(self.game.red_projectile, (self.rect.x, self.rect.y))

    def remove(self):
        self.game.player.all_projectiles.remove(self)

    def move(self):
        self.rect.x += self.velocity

        if self.target == Projectile.ENEMY:
            for enemy in self.game.all_enemies.get():
                if utilities.collisionRect(self.rect, enemy.rect):
                    enemy.damage(self.game.player.attack)
                    self.remove()

        if self.target == Projectile.PLAYER:

            if utilities.collisionRect(self.rect,self.game.shield.rect) and self.game.shield.activated:
                self.game.shield.durability -= 1
                self.remove()

            if utilities.collisionRect(self.rect, self.game.player.rect):
                self.game.player.damage(self.enemy_projectile_attack)
                self.remove()

        if self.rect.x > self.game.player.screen_rect[2]:
            self.remove()
