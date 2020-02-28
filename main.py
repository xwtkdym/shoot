#!/usr/bin/env python3
import os
import sys
import random
import pygame
from pygame.color import THECOLORS as tc
sys.path.append('.')

from Base import *
from Base.Config import config

audio_hit=None
audio_fire=None
audio_bgm=None


player_index=0
enemy_index=1
player_bullet_index=2
enemy_bullet_index=3
gun_index=4
system_index=5

collide_pair = (
        (player_index, enemy_index),
        (player_index, enemy_bullet_index),
        (player_bullet_index, enemy_index),
        (player_bullet_index, enemy_bullet_index)
    )

groups=None

def is_prime(x):
    if x == 2:
        return True
    for i in range(2, x, 1):
        if x%i == 0:
            return False
        if i*i > x:
            return True
    return True

class EchoCtr(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

    def update(self):
        self.__update_image()

    def __update_image(self):
        game_ctr = config["game_ctr"]
        image = pygame.image.load(os.path.join("images", "player_plane", "images", "me1.png")).convert_alpha()
        image = pygame.transform.scale(image, [20, 30])
        bg = pygame.Surface([60, 30])
        bg.fill(tc['black'])
        for i in range(game_ctr):
            bg.blit(image, [i*20, 0])
        bg.set_colorkey(tc['black'])
        self.image = bg
        self.rect = self.image.get_rect()
        self.rect.left = config["width"] - 60
        self.rect.top = 0
        


class Panel(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.font=pygame.font.Font(None, 45)
        self.color_ctr = 0
        self.image = self.__update_image()
        self.color = tc['green']

    def update(self):
        self.__update_image()

    def __update_image(self):
        global groups
        row = 0
        for sprite in groups[player_index].sprites():
            row += 1
            life = sprite.get_life()

            self.image = self.__to_image(life, config["score"], tc['green'])

        if 0 == row:
            if self.color_ctr % 10 == 0:
                self.color = random_color()
            self.color_ctr += 1
            self.image = self.__to_image(0, config["score"], self.color)

        self.rect = self.image.get_rect()
        self.rect.left = self.rect.top = 0


    def __to_image(self, life, score, color):
        percent = int(100*life/config["max_life"])
        bg = pygame.Surface([210, 24])
        bg.fill(tc['pink'])
        image = pygame.Surface([220, 80])
        image.blit(bg, [5, 3])
        if percent > 0:
            left = pygame.Surface([2*percent, 18])
            left.fill(tc['green'])
        else:
            left = pygame.Surface([1, 18])
            left.fill(tc['red'])
        image.blit(left, [8, 7])
        text = (str(percent)+'%').ljust(3, ' ')
        text += ' '*2 + str(score)
        image.blit(self.font.render(text, True, color), [5, 40])
        image.set_colorkey(tc['black'])
        return image


class Group(pygame.sprite.Group):
    def __init__(self):
        super().__init__(self)

    def kill_out_of_bounds(self):
        for sprite in self.sprites():
            if (sprite.rect.top > config["height"]
                    or sprite.rect.bottom < 0
                    or sprite.rect.left > config["width"]
                    or sprite.rect.right < 0):
                self.remove(sprite)
    def kill_over(self):
        for sprite in self.sprites():
            if sprite.over():
                if hasattr(sprite, "over_action"):
                    sprite.over_action()
                self.remove(sprite)

def read_images(path, size=None, colorkey=None):
    paths = sorted(os.listdir(os.path.join('images', path)))
    image = None
    if colorkey != None:
        images = [pygame.image.load(os.path.join('images', path, img_path)).convert() for img_path in paths]
        for image in images:
            image.set_colorkey(colorkey)
    else:
        images = [pygame.image.load(os.path.join('images', path, img_path)).convert_alpha() for img_path in paths]
    if size != None:
        images = [pygame.transform.scale(image, size) for image in images]
    return images

def random_color():
    level = range(32, 256, 32)
    return tuple(random.choice(level) for _ in range(3))

def screen_flush(screen, clock):
    if config["bg_ctr"] % int(config["fps"]/6) == 0:
        config["bg_image_index"] = (config["bg_image_index"]+1)%len(config["bg_images"])
    config["bg_ctr"] = config["bg_ctr"]+1
    screen.blit(config["bg_images"][config["bg_image_index"]], [0, 0])


def game_is_over():
    global player_group
    for sprite in groups[player_index].sprites():
        if not sprite.isdie():
            return False
    return True

def display_start(screen, clock):
    while True:
        clock.tick(config["fps"])
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                return

def game_init(screen, clock):
    global audio_hit, audio_fire, audio_bgm
    global groups
    config["score"] = 0

    groups=[]
    for i in range(6):
        groups.append(Group())

#for ClearScreeen
    config["enemy_bullet_group"] = groups[enemy_bullet_index]
    config["clear_screen_images"] = read_images("clear_screen/images", [40, 40], tc['white'])
    config["clear_screen_die_images"] = read_images("clear_screen/die_images", [40, 40], tc['white'])


    config["dec_cd_images"] = read_images("dec_cd/images", [40, 40], tc['white'])
    config["dec_cd_die_images"] = read_images("dec_cd/die_images", [40, 40], tc['white'])
    config["re_life_images"] = read_images("re_life/images", [40, 40], tc['white'])
    config["re_life_die_images"] = read_images("re_life/die_images", [40, 40], tc['white'])
    config["bg_ctr"] = 0
    config["bg_images"]  = read_images('background', config["size"])
    config["bg_image_index"]= 0
    config["player_plane_images"] =read_images('player_plane/images', [70, 70])
    config["player_plane_die_images"] = read_images('player_bullet/die_images', [70, 70])
    config["player_bullet_images"] =read_images('player_bullet/images', [30, 30])
    config["player_bullet_die_images"] = read_images('player_plane/die_images', [30, 30])
    config["audio_hit" ] = pygame.mixer.Sound(os.path.join('music', 'hit.wav'))
    config["audio_fire"] = pygame.mixer.Sound(os.path.join('music', 'fire.wav'))
    config["audio_bgm"] = pygame.mixer.Sound(os.path.join('music', 'a.ogg'))
    config["audio_hit"].set_volume(0.7)
    config["audio_fire"].set_volume(0.7)
    config["audio_bgm"].set_volume(1)
    config["audio_bgm"].play(-1)


    panel = Panel()
    groups[system_index].add(panel)
    echoctr = EchoCtr()
    groups[system_index].add(echoctr)
    bullet = Bullet.Bullet(read_images('enemy_bullet/images', [20, 20]), read_images('enemy_bullet/die_images', [20, 20]) , [-100, -100])
    bullet.set_over(True)
    random_gun = Gun.RandomGun(bullet, groups[enemy_bullet_index], groups[gun_index])


    font=pygame.font.Font(None, 70)
    color = None
    color_ctr = 0
    while True:
        if color_ctr >= 3*config["fps"]:
            return
        if color_ctr%10 == 0:
            color = random_color()
        color_ctr += 1

        clock.tick(config["fps"])
        screen_flush(screen, clock)
        font_surf = font.render(str('Enter any key!'), True, color)
        screen.blit(font_surf, [int(config["width"]/2)-font_surf.get_width()/2, 
                                int(config["height"]*3/4)-font_surf.get_height()/2])
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                return


def game_prepare():
    #add player

    bullet = Bullet.Bullet(read_images('player_bullet/images', [30, 30]), read_images('player_bullet/die_images', [30, 30]) , [-100, -100])
    pos = [config["width"]/2, int(config["height"]*0.618)]

    player = Plane.KeyPlane(config["player_plane_images"], config["player_plane_die_images"], pos, [0,0], config["max_life"])

    gun = Gun.Gun(config["fps"]/10, 90, 10, bullet, groups[player_bullet_index], groups[gun_index])
    player.add_key_gun(gun)
    groups[player_index].add(player)

    bullet = Bullet.Bullet(config['player_bullet_images'],  config['player_bullet_die_images'] , [-100, -100])
    for x in range(0, 350, 40):
        gun = Gun.Gun(config["fps"]/5, x, 10, bullet, groups[player_bullet_index], groups[gun_index])
        player.add_auto_gun(gun)




def game_run(screen, clock):
    global groups

    running = 100
    pause_flag = False
    old_image = None
    while running:
        clock.tick(config["fps"])
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE and not game_is_over():
                pause_flag = not pause_flag
        if pause_flag:
            if old_image != None:
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
                                sprite2.collide_action(sprite1)
                                #attack = min(sprite1.get_life(), sprite2.get_life())
                                #score += attack
                                #sprite1.set_life(sprite1.get_life()-attack)
                                #sprite2.set_life(sprite2.get_life()-attack)


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
        if color_ctr >= 3*config["fps"]:
            return
        if color_ctr%10 == 0:
            color = random_color()
        color_ctr += 1

        clock.tick(config["fps"])
        screen.fill(tc['black'])
        font_surf = font.render(str('Game Over!'), True, color)
        screen.blit(font_surf, [config["width"]/2-font_surf.get_width()/2, 
                                config["height"]/2-font_surf.get_height()/2])
        
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            elif event.type == pygame.KEYDOWN:
                return



def game_loop(screen, clock):
    loop_flag = True
    while loop_flag:
        game_init(screen, clock)
        config["game_ctr"]= 3
        while config["game_ctr"] > 0:
            game_prepare()
            game_run(screen, clock)
            config["game_ctr"]= config["game_ctr"]-1
        game_over(screen, clock)

if __name__ == '__main__':
    global config
    config = Config.ConfigClass()
    pygame.init()
    pygame.mixer.init()
    screen = pygame.display.set_mode(config["size"])
    pygame.display.set_caption('YunXiaoZhu')
    clock = pygame.time.Clock()
    game_loop(screen, clock)
