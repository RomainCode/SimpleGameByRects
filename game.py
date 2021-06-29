import pygame

import utilities
from utilities import Group
from utilities import *
from projectile import Projectile
from player import Player
from enemy import Enemy
from player_objects import Shield
from player_objects import Turret
from player_objects import Armor
from player_objects import Projectile_Launcher

class Game:

    def __init__(self, screen):
        self.is_projectile_sound = True
        self.upgrades_rects_market = {}
        self.objects_rects_market = {}
        self.screen = screen
        self.font = pygame.font.SysFont(None, 32)
        self.color_text = (255, 255, 255)
        self.red_projectile = pygame.transform.scale(pygame.image.load("assets/red_projectile.png"), (25,5))
        self.green_projectile = pygame.transform.scale(pygame.image.load("assets/green_projectile.png"), (25,5))
        self.small_xp = pygame.transform.scale(pygame.image.load("assets/xp_small.png"), (10, 10))
        self.medium_xp = pygame.transform.scale(pygame.image.load("assets/xp_medium.png"), (15, 15))
        self.big_xp = pygame.transform.scale(pygame.image.load("assets/xp_big.png"), (20, 20))
        self.health_logo = pygame.transform.scale(pygame.image.load("assets/shield_logo.png"), (50,50))
        self.multigun_logo = pygame.transform.scale(pygame.image.load("assets/multigun.png"), (50, 50))
        self.turret_logo = pygame.transform.scale(pygame.image.load("assets/turret.png"), (50, 50))
        self.magnet_logo = pygame.transform.scale(pygame.image.load("assets/magnet.png"), (50, 50))
        self.medic_kit_logo = pygame.transform.scale(pygame.image.load("assets/medic_kit.png"), (50, 50))
        self.blank_logo = pygame.transform.scale(pygame.image.load("assets/blank.png"), (50, 50))
        self.aura_logo = pygame.transform.scale(pygame.image.load("assets/aura.png"), (50, 50))
        utilities.fill(self.aura_logo, pygame.Color(100, 10, 100))
        self.hp_boost_logo = pygame.transform.scale(pygame.image.load("assets/HP_Boost.png"), (50, 50))
        self.blaze_logo = pygame.transform.scale(pygame.image.load("assets/Blaze.png"), (50, 50))
        self.blaster = pygame.mixer.Sound("assets/blaster.mp3")
        self.hp_logo = pygame.transform.scale(pygame.image.load("assets/hp_logo.png"), (40,40))
        self.explosion_sound = pygame.mixer.Sound("assets/explosion.mp3")
        self.explosion_sound.set_volume(0.2)
        self.explosion_image = pygame.transform.scale(pygame.image.load("assets/explosion.png"), (300,300))
        self.blaster.set_volume(0.10)
        self.is_playing = False
        self.score = 0
        self.keys_pressed = {}
        self.Shield = Shield
        self.Projectile = Projectile
        self.paused = False

    def start(self):
        self.player = Player(self, self.screen)
        self.shield = Shield(self)
        #self.player.all_objects.add(self.shield)
        self.all_enemies = Group()
        for i in range(2):
            self.all_enemies.add(Enemy(self, self.screen))
        self.score = 0
        self.player.money = 0
        self.all_enemies_projectiles = Group()
        self.armor = Armor(self)
        self.player.all_objects.add(self.armor)
        self.projectile_launcher = Projectile_Launcher(self)
        self.player.all_objects.add(self.projectile_launcher)
        self.ground_origin = (0, self.player.rect.bottomleft[1])
        self.player.upgrades = {
            'Shield upgrade': [1000, 'max_durability', self.shield, 800, self.aura_logo, False],
            'HP boost': [1500, 'max_health', self.player, 300, self.hp_boost_logo, False],
            'Hot projectiles': [2000, 'attack', self.player, 20, self.blaze_logo, False]}
        self.delqueueUpgrades = list()
        self.is_playing = True


    def addEnemy(self):
        self.all_enemies.add(Enemy(self, self.screen))


    def dataUpdate(self):
        for projectile in self.player.all_projectiles.get():
            try:
                projectile.move()
            except Exception as e:
                print(f"error : {e}")
                pass

        for projectile in self.all_enemies_projectiles.get():
            try:
                projectile.move()
            except:
                pass

        for enemy in self.all_enemies.get():
            enemy.moveLeft()

        for coin in self.player.all_coins.get():
            coin.handle()

        for object in self.player.all_objects.get():
            object.handle()

        self.shield.handle()

    def drawUpdate(self, screen):
        pygame.draw.line(screen, (255, 255, 255), self.ground_origin, (self.screen.get_rect()[2], self.ground_origin[1]))
        self.player.all_projectiles.draw(screen)  # draw projectiles
        self.player.draw(screen)  # draw player
        self.player.all_objects.draw(screen)
        self.all_enemies.draw(screen)  # draw enemies
        self.all_enemies_projectiles.draw(screen)
        self.player.updateHealth(screen)
        for enemy in self.all_enemies.get():  # drawn the enemy health bar
            enemy.updateHealth(screen)
        self.player.all_coins.draw(screen)
        self.shield.draw(screen)

        img = self.font.render(f"SCORE : {self.score}", True, self.color_text)
        screen.blit(img, (20, 20))

        img = self.font.render(f"XP : {self.player.money}", True, self.color_text)
        screen.blit(img, (20, 60))


        pygame.draw.rect(screen, (0, 0, 0), (20 + 20 - 3, 140 + 15 - 3-50, 1 * 200 + 2 * 3, 15 + 2 * 3), border_radius=5)
        pygame.draw.rect(screen, (190, 95, 125),(20 + 20, 140 + 15 -50, (self.shield.durability / self.shield.max_durability) * 200, 15), border_radius=5)
        if self.shield.durability / self.shield.max_durability > 0.1:
            pygame.draw.rect(screen, (255, 255, 255),((self.shield.durability / self.shield.max_durability) * 200 + 15, 140 + 15 + 2 -50, 15, 5),border_radius=3)
        if self.shield.durability / self.shield.max_durability > 0.3:
            pygame.draw.polygon(screen, (105,25,90), (((self.shield.durability / self.shield.max_durability) * 150, 155-50), (40, 155-50), (40, 169-50),((self.shield.durability / self.shield.max_durability) * 170, 169-50)))
        pygame.draw.circle(screen, (20, 20, 20),((15 + int(self.aura_logo.get_width() / 2)), 135 + int(self.aura_logo.get_height() / 2)-50),(int(self.aura_logo.get_width() / 2)))
        screen.blit(self.aura_logo, (15, 135-50))


        pygame.draw.rect(screen, (0,0,0), (20+20-3, 140+15-3, 1*200+2*3, 15+2*3), border_radius=5)
        pygame.draw.rect(screen, (255, 75, 75), (20 + 20, 140 + 15, (self.player.health/self.player.max_health) * 200, 15), border_radius=5)
        if self.player.health / self.player.max_health > 0.1:
            pygame.draw.rect(screen, (255,255,255), ((self.player.health/self.player.max_health) * 200 + 15, 140 + 15 + 2, 15, 5), border_radius=3)
        if self.player.health / self.player.max_health > 0.3:
            pygame.draw.polygon(screen, (219, 26, 27), ( ((self.player.health/self.player.max_health) * 150,155), (40, 155), (40, 169), ((self.player.health/self.player.max_health) * 170,169))  )
        screen.blit(self.hp_logo, (20, 140))

        self.drawShop(screen)
        self.drawUpgrades(screen)


    def drawMarket(self, surface):
        font = pygame.font.SysFont(None, 25)
        c = 1
        items = self.player.upgrades
        for item in items:
            if self.player.money >= items[item][0]:
                img = font.render(f"{item} : {items[item][0]} coins", True, self.color_text)
                surface.blit(img, (40, 180+30*c))
                c += 1

    def handleMarket(self, key):
        items = self.player.objects
        for item in items:
            if items[item][3] == key:
                if self.player.money >= items[item][1]:
                    print(f"You bought a {item} for {items[item][1]} coins")
                    self.player.money -= items[item][1]
                    self.player.all_objects.add(items[item][4](self))
                else:
                    print("Not enough money")

    def handleMarketUpgrade(self, key, key_res):
        print(self.player.upgrades[key][5])
        if self.player.money >= key_res[0]:
            if key_res[1] == "max_durability":
                key_res[2].max_durability = key_res[3]
                if key_res[2] == self.shield:
                    self.shield.color = (190, 190, 190)
                    utilities.fill(self.shield.shield_image, pygame.Color(100, 10, 100))
                self.player.money -= key_res[0]
                self.delqueueUpgrades.append(key)
                self.player.upgrades[key][5] = False
            elif key_res[1] == "max_health":
                key_res[2].max_health = key_res[3]
                self.player.money -= key_res[0]
                self.armor.color = (190, 190, 190)
                self.delqueueUpgrades.append(key)
                self.player.upgrades[key][5] = False
            elif key_res[1] == "attack":
                key_res[2].attack = key_res[3]
                self.projectile_launcher.color = (150, 150, 150)
                self.player.money -= key_res[0]
                self.delqueueUpgrades.append(key)
                self.player.upgrades[key][5] = False
            else:
                print("error upgrade")
                print(key_res[1])
            print(f"you tryed to bought {key}")


    def drawShop(self, surface):
        self.objects_rects_market = {}
        """self.objects = {'Multi gun': (False, 10, '1', pygame.K_1, Multi_Gun, image),
                        'Turret': (False, 20, '2', pygame.K_2, Turret),
                        'Money magnet': (False, 5, '4', pygame.K_4, Money_Magnet),
                        'Medic kit': (False, 8, '3', pygame.K_3, Medic_Kit),
                        'Shield health': (False, 5, '5', pygame.K_5, Shield_Manager)}"""
        init_pos = [450, 30]
        font = pygame.font.SysFont(None, 20)
        for item_name in self.player.objects:
            surface.blit(self.player.objects[item_name][5], init_pos)

            img = font.render(f"{self.player.objects[item_name][1]}XP (key {self.player.objects[item_name][2]})", True, self.color_text)
            surface.blit(img, (init_pos[0]-int(1/2*img.get_width())+25, init_pos[1] + 50))

            img_times = font.render(f'({len(self.player.all_objects.getByClass(self.player.objects[item_name][4]))}x)', True, self.color_text)
            surface.blit(img_times, (init_pos[0]-int(1/2*img_times.get_width())+25, init_pos[1] + 50 + img.get_height()))

            self.objects_rects_market[item_name] = pygame.Rect(init_pos[0]-int(1/2*img.get_width())+25, init_pos[1], img.get_width(),img.get_height() + 50 + img_times.get_height())
            #pygame.draw.rect(surface, (200, 0, 0), self.objects_rects_market[item_name], 2)

            init_pos[0] += 100

    def drawUpgrades(self, surface):
        self.upgrades_rects_market = {}
        """
            'Silver shield': (1000, 'max_durability', self.shield, 800),
            'HP boost': (1500, 'max_health', self.player, 300),
            'Hot projectiles': (2000, 'attack', self.player, 20)}
        """
        init_pos = [500, 120]
        font = pygame.font.SysFont(None, 20)
        for item_name in self.player.upgrades:
            if (not self.player.upgrades[item_name][5]) and (self.player.upgrades[item_name][0] <= self.player.money):

                surface.blit(self.player.upgrades[item_name][4], init_pos)

                img = font.render(f"{self.player.upgrades[item_name][0]}XP {item_name}", True,self.color_text)
                if self.player.money < self.player.upgrades[item_name][0]:
                    img.set_alpha(100)
                surface.blit(img, (init_pos[0]-int(1/2*img.get_width())+25, init_pos[1] + 50))

                self.upgrades_rects_market[item_name] = pygame.Rect(init_pos[0]-int(1/2*img.get_width())+25, init_pos[1], img.get_width(),img.get_height() + 50)
                #pygame.draw.rect(surface, (200, 0, 0), self.upgrades_rects_market[item_name], 2)

                init_pos[0] += 140



