__author__ = "Romain CORTALE"
__copyright__ = "Copyright (C) 2021 Romain CORTALE"
__license__ = "MIT Open Source"
__version__ = "1.0"
import os
import sys

import pygame
from game import Game
from player import Player
from enemy import Enemy
from utilities import Group
import utilities
import random
from player_objects import Shield

RED = [255, 0, 0]
BLUE = [0, 0, 255]
GREEN = [0, 255, 0]
WHITE = [255, 255, 255]
BLACK = [0, 0, 0]
GREY = [50, 50, 50]
DARK_GREY = [20, 20, 20]
keys_pressed = dict()

pygame.init()

#background_sound = pygame.mixer.Sound("assets/background_music.mp3")
#background_sound.play()
#background_sound.set_volume(0.2)
pygame.mixer.music.load("assets/background_music.mp3")
pygame.mixer.music.play(999999)
pygame.mixer.music.set_volume(0.2)

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

def print_file(file_path):
    file_path = resource_path(file_path)
    with open(file_path) as fp:
        for line in fp:
            print(line)


def invertImg(img):
    """Inverts the colors of a pygame Screen"""

    img.lock()

    for x in range(img.get_width()):
        for y in range(img.get_height()):
            RGBA = img.get_at((x,y))
            for i in range(3):
                # Invert RGB, but not Alpha
                RGBA[i] = 255 - RGBA[i]
            img.set_at((x,y),RGBA)

    img.unlock()

pause_icon = pygame.transform.scale(pygame.image.load(resource_path('assets/pause.png')), (35, 35))
invertImg(pause_icon)
play_icon = pygame.transform.scale(pygame.image.load(resource_path('assets/play.png')), (35, 35))
invertImg(play_icon)
background_image = pygame.transform.scale(pygame.image.load("assets/back.gif"), (1500, 800))
paused_music_icon = pygame.transform.scale(pygame.image.load("assets/pause_music.png"), (35, 35))
play_music_icon = pygame.transform.scale(pygame.image.load("assets/unpause_music.png"), (35, 35))
projectile_sound = pygame.transform.scale(pygame.image.load("assets/projectile_sound.png"), (70, 35))
invertImg(projectile_sound)
no_projectile_sound = pygame.transform.scale(pygame.image.load("assets/no_projectile_sound.png"), (70, 35))
invertImg(no_projectile_sound)
arrow = pygame.image.load("assets/up_arrow.png")
space_bar = pygame.image.load("assets/space_bar.png")



screen = pygame.display.set_mode((1500, 800))
pygame.display.set_caption("Romain's Game")
clock = pygame.time.Clock()
pygame.display.set_icon(pygame.image.load(resource_path('logo.PNG')))


game = Game(screen)

running = True
general_music_state = True

while running:

    clock.tick(50)

    screen.fill(GREY)

    if not game.paused:

        if game.is_playing:


            # MOVE ENTITIES AND DELETE ONES
            for key in keys_pressed:
                if keys_pressed[key]:

                    if key == pygame.K_LEFT:
                        game.player.moveLeft()
                    if key == pygame.K_RIGHT:
                        game.player.moveRight()

            game.dataUpdate()

            # DRAW ENTITIES
            screen.fill(GREY)
            screen.blit(background_image, (0, 0))
            game.drawUpdate(screen)

        else:
            screen.fill(GREY)
            text_margin = 30
            font = pygame.font.SysFont(None, 200)
            img = font.render(f"PLAY", True, GREY)
            img_rect_centered = img.get_rect(center= screen.get_rect().center)
            pygame.draw.rect(screen, (255,255,255), (img_rect_centered.x-text_margin, img_rect_centered.y-text_margin, img.get_rect()[2]+text_margin*2, img.get_rect()[3]+text_margin*1))
            screen.blit(img, img.get_rect(center= screen.get_rect().center))


            font = pygame.font.SysFont(None, 32)
            img = font.render(f"SCORE : {game.score}", True, (255, 255, 255))
            screen.blit(img, (20, 20))

            c = 0
            img = font.render(f"to launch a projectile", True, (255,255,255))
            screen.blit(space_bar, (img.get_rect(center=screen.get_rect().center).x-int((space_bar.get_width())/2), 2*(screen.get_rect()[3]/3)+30*c))
            screen.blit(img, (img.get_rect(center=screen.get_rect().center).x+10+int((space_bar.get_width()-10)/2), 2*(screen.get_rect()[3]/3)+30*c + int(space_bar.get_height()/4)))

            c += 1
            img = font.render(f"to activate and deactivate your shield", True, (255, 255, 255))
            rotated_img = pygame.transform.rotate(arrow, 90)
            screen.blit(rotated_img, (img.get_rect(center=screen.get_rect().center).x - int((rotated_img.get_width()) / 2),2 * (screen.get_rect()[3] / 3) + 50 * c))
            screen.blit(img, (img.get_rect(center=screen.get_rect().center).x + 10 + int((rotated_img.get_width() - 10) / 2),2 * (screen.get_rect()[3] / 3) + 50 * c + int(rotated_img.get_height()/4)))

            c+= 1
            img = font.render(f"to move", True, (255,255,255))
            rotated_imgs = [pygame.transform.rotate(arrow, 180), arrow]
            screen.blit(rotated_imgs[0], (img.get_rect(center=screen.get_rect().center).x - int((rotated_imgs[0].get_width()) / 2),2 * (screen.get_rect()[3] / 3) + 50 * c))
            screen.blit(rotated_imgs[1], (img.get_rect(center=screen.get_rect().center).x - int((rotated_imgs[1].get_width()) / 2) + rotated_imgs[0].get_width(),2 * (screen.get_rect()[3] / 3) + 50 * c))
            screen.blit(img, (img.get_rect(center=screen.get_rect().center).x + 10 + int((rotated_imgs[0].get_width()*2 - 20)),2 * (screen.get_rect()[3] / 3) + 50 * c + int(rotated_img.get_height() / 4)))

    if game.paused:
        screen.blit(background_image, (0, 0))
        game.drawUpdate(screen)
        screen.blit(play_icon, (screen.get_rect()[2] - 45, 10))
    else:
        screen.blit(pause_icon, (screen.get_rect()[2] - 45, 10))

    if general_music_state:
        screen.blit(play_music_icon, (screen.get_rect()[2] - 45, 35+10+35))
    else:
        screen.blit(paused_music_icon, (screen.get_rect()[2] - 45, 35+10+35))

    if game.is_projectile_sound:
        screen.blit(projectile_sound, (screen.get_rect()[2] - 70, 35+10+35+10+35))
    else:
        screen.blit(no_projectile_sound, (screen.get_rect()[2] - 70, 35+10+35+10+35))


    pygame.display.flip()


    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            keys_pressed[event.key] = True
            game.keys_pressed[event.key] = True
            if game.is_playing:
                game.handleMarket(event.key)

            if event.key == pygame.K_SPACE and game.is_playing:
                game.player.launchProjectile()

            if event.key == pygame.K_UP and game.is_playing:
                if game.shield.durability > 0:
                    game.shield .toogle()


        if event.type == pygame.KEYUP:
            keys_pressed[event.key] = False
            game.keys_pressed[event.key] = False

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # check if the mouse is in collision with the button
            if pygame.Rect(screen.get_rect()[2]/3, screen.get_rect()[3]/3, 400, 200).collidepoint(event.pos) and game.is_playing == False:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                game.start()

            if game.is_playing:

                for item in game.objects_rects_market:
                    if game.objects_rects_market[item].collidepoint(pygame.mouse.get_pos()):
                        print(f'buy {item}')
                        game.handleMarket(game.player.objects[item][3])

                for item in game.upgrades_rects_market:
                    if game.upgrades_rects_market[item].collidepoint(pygame.mouse.get_pos()):
                        print(f'buy {item}')
                        game.handleMarketUpgrade(item, game.player.upgrades[item])

                utilities.delQueue(game.player.upgrades, game.delqueueUpgrades)

                if pygame.Rect(screen.get_rect()[2] - 45, 15, 35, 35).collidepoint(pygame.mouse.get_pos()):
                    if game.paused == True:
                        game.paused = False
                        print("unpaused")
                        pygame.mixer.music.unpause()
                    else:
                        game.paused = True
                        print("paused")
                        pygame.mixer.music.pause()

                if pygame.Rect(screen.get_rect()[2] - 45, 35+10+35, 35, 35).collidepoint(pygame.mouse.get_pos()):
                    if pygame.mixer.music.get_busy() == 1:
                        pygame.mixer.music.pause()
                        general_music_state = False
                    else:
                        pygame.mixer.music.unpause()
                        general_music_state = True

                if pygame.Rect(screen.get_rect()[2] - 70, 35+10+35+10+35, 35, 35).collidepoint(pygame.mouse.get_pos()):
                    if game.is_projectile_sound:
                        game.is_projectile_sound = False
                    else:
                        game.is_projectile_sound = True


        if game.is_playing == False:
            if pygame.Rect(screen.get_rect()[2]/3, screen.get_rect()[3]/3, 400, 200).collidepoint(pygame.mouse.get_pos()):
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        else:
            hand = False

            for item in game.upgrades_rects_market:
                if game.upgrades_rects_market[item].collidepoint(pygame.mouse.get_pos()):
                    hand = True

            for item in game.objects_rects_market:
                if game.objects_rects_market[item].collidepoint(pygame.mouse.get_pos()):
                    hand = True
            items = game.player.upgrades

            if pygame.Rect(screen.get_rect()[2] - 45, 15, 35, 35).collidepoint(pygame.mouse.get_pos()):
                hand = True

            if pygame.Rect(screen.get_rect()[2] - 45, 35+10+35, 35, 35).collidepoint(pygame.mouse.get_pos()):
                hand = True

            if pygame.Rect(screen.get_rect()[2] - 70, 35+10+35+10+35, 35, 35).collidepoint(pygame.mouse.get_pos()):
                hand = True

            if hand:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            else:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)



"""
CREDITS :
MUSIC : 
    The Great Battle by Alexander Nakarada | https://www.serpentsoundstudios.com
    Attribution 4.0 International (CC BY 4.0)
    https://creativecommons.org/licenses/by/4.0/
    Music promoted by https://www.chosic.com
"""
