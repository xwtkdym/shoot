#!/usr/bin/env python3
import os
import sys
import random
import pygame
from pygame.color import THECOLORS as tc
sys.path.append('.')

from Base import *

audio_hit=None
audio_fire=None
audio_bgm=None


player_index=0
enemy_index=1
player_bullet_index=2
enemy_bullet_index=3
gun_index=4
system_index=5

score=None

collide_pair = (
        (player_index, enemy_index),
        (player_index, enemy_bullet_index),
        (player_bullet_index, enemy_index),
        (player_bullet_index, enemy_bullet_index)
    )

groups=None

class Panel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.font=pygame.font.Font(None, 45)
        self.image = self.__update_image()
        self.color_ctr = 0
        self.color = tc['green']

    def update(self):
        self.__update_image()

    def __update_image(self):
        global groups, score
        row = 0
        for sprite in groups[player_index].sprites():
            row += 1
            life = sprite.get_life()

            self.image = self.__to_image(life, score, tc['green'])

        if 0 == row:
            if self.color_ctr % 10 == 0:
                self.color = random_color()
            self.color_ctr += 1
            self.image = self.__to_image(0, score, self.color)

        self.rect = self.image.get_rect()
        self.rect.left = self.rect.top = 0


    def __to_image(self, life, score, color):
        percent = int(100*life/Config.get_val("max_life"))
        image = pygame.Surface([300, 100])
        if percent > 0:
            left = pygame.Surface([3*percent, 20])
            left.fill(tc['green'])
        else:
            left = pygame.Surface([1, 20])
            left.fill(tc['red'])
        image.blit(left, [0, 10])
        text = (str(percent)+'%').ljust(3, ' ')
        text += ' '*2 + str(score)
        image.blit(self.font.render(text, True, color), [0, 40])
        image.set_colorkey(tc['black'])
        return image


class Group(pygame.sprite.Group):
    def __init__(self):
        super().__init__(self)

    def kill_out_of_bounds(self):
        for sprite in self.sprites():
            if (sprite.rect.top > Config.get_val("height")
                    or sprite.rect.bottom < 0
                    or sprite.rect.left > Config.get_val("width")
                    or sprite.rect.right < 0):
                self.remove(sprite)
    def kill_over(self):
        for sprite in self.sprites():
            if sprite.over():
                self.remove(sprite)

def read_images(path, size=None):
    paths = sorted(os.listdir(os.path.join('images', path)))
    images = [pygame.image.load(os.path.join('images', path, img_path)).convert_alpha() for img_path in paths]
    if size:
        images = [pygame.transform.scale(image, size) for image in images]
    return images

def random_color():
    level = range(32, 256, 32)
    return tuple(random.choice(level) for _ in range(3))

def screen_flush(screen, clock):
    if Config.get_val("bg_ctr") % int(Config.get_val("fps")/6) == 0:
        Config.set_val("bg_image_index", (Config.get_val("bg_image_index")+1)%len(Config.get_val("bg_images")))
    Config.set_val("bg_ctr", Config.get_val("bg_ctr")+1)
    screen.blit(Config.get_val("bg_images")[Config.get_val("bg_image_index")], [0, 0])


def game_is_over():
    global player_group
    for sprite in groups[player_index].sprites():
        if not sprite.isdie():
            return False
    return True

def display_start(screen, clock):
    while True:
        clock.tick(Config.get_val("fps"))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                return

def game_init(screen, clock):
    global audio_hit, audio_fire, audio_bgm
    global groups, score
    score = 0

    groups=[]
    for i in range(6):
        groups.append(Group())


    Config.set_val("bg_ctr", 0)
    Config.set_val("bg_images", read_images('background', Config.get_val("size")))
    Config.set_val("bg_image_index", 0)
    Config.set_val("audio_hit" , pygame.mixer.Sound(os.path.join('music', 'hit.wav')))
    Config.set_val("audio_fire", pygame.mixer.Sound(os.path.join('music', 'fire.wav')))
    Config.set_val("audio_bgm", pygame.mixer.Sound(os.path.join('music', 'a.ogg')))
    Config.get_val("audio_hit").set_volume(0.7)
    Config.get_val("audio_fire").set_volume(0.7)
    Config.get_val("audio_bgm").set_volume(1)
    Config.get_val("audio_bgm").play(-1)

def game_prepare():
    #add player

    bullet = Bullet.Bullet(read_images('player_bullet/images', [20, 20]), read_images('player_bullet/die_images', [20, 20]) , [-100, -100])
    pos = [Config.get_val("width")/2, int(Config.get_val("height")*0.618)]

    player = Plane.KeyPlane(read_images('player_plane/images', [70, 70]), read_images('player_plane/die_images', [50, 50]), pos, [0,0], Config.get_val("max_life"))
    for x in range(63, 117, 9):
        gun = Gun.Gun(Config.get_val("fps")/5, x, 10, bullet, groups[player_bullet_index], groups[gun_index])
        player.add_key_gun(gun)
    groups[player_index].add(player)

    bullet = Bullet.Bullet(read_images('enemy_bullet/images', [20, 20]), read_images('enemy_bullet/die_images', [20, 20]) , [-100, -100])
    random_gun = Gun.RandomGun(bullet, groups[enemy_bullet_index], groups[gun_index])

    panel = Panel()
    groups[system_index].add(panel)


def game_run(screen, clock):
    global groups, score

    running = 100
    pause_flag = False
    old_image = None
    while running:
        clock.tick(Config.get_val("fps"))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not game_is_over():
                pause_flag = not pause_flag
        if pause_flag:
            screen.blit(old_image, [0,0])
            pygame.display.flip()
            continue
        else:
            old_image = screen

        screen_flush(screen, clock)
        
        for group in groups:
            group.update()

        for pair in collide_pair:
            for sprite1 in groups[pair[0]].sprites():
                if not sprite1.isdie():
                    for sprite2 in groups[pair[1]].sprites():
                        if not sprite2.isdie():
                            if pygame.sprite.collide_mask(sprite1, sprite2):
                                Config.get_val("audio_hit").play(0, 500)
                                attack = min(sprite1.get_life(), sprite2.get_life())
                                score += attack
                                sprite1.set_life(sprite1.get_life()-attack)
                                sprite2.set_life(sprite2.get_life()-attack)


        for group in groups:
            try:
                group.kill_out_of_bounds()
            except:
                pass

            try:
                group.kill_over()
            except:
                pass

            try:
                group.draw(screen)
            except:
                pass

        pygame.display.flip()

        running -= 1
        if game_is_over():
            continue
        else:
            running = 100



def game_over(screen, clock):
    font=pygame.font.Font(None, 70)
    color = None
    color_ctr = 0

    for group in groups:
        group.empty()
    while True:
        if color_ctr%10 == 0:
            color = random_color()
        color_ctr += 1

        clock.tick(Config.get_val("fps"))
        screen.fill(tc['black'])
        font_surf = font.render(str('Game Over!'), True, color)
        screen.blit(font_surf, [Config.get_val("width")/2-font_surf.get_width()/2, 
                                Config.get_val("height")/2-font_surf.get_height()/2])
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                return



def game_loop(screen, clock):
    game_init(screen, clock)
    loop_flag = True
    while loop_flag:
        game_prepare()
        game_run(screen, clock)
        game_over(screen, clock)

if __name__ == '__main__':
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(Config.get_val("size"))
    pygame.display.set_caption('YunXiaoZhu')
    clock = pygame.time.Clock()
    game_loop(screen, clock)
