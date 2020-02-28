import pygame
import random

from Base import Cube
from Base import Gun
from .Cube import *
from .Config import *

class Bullet(Cube):
    def __init__(self, images, die_images, pos=None, speed=None, life=1, *groups):
        Cube.__init__(self, images, die_images, pos, speed, life, groups)
    def collide_action(self, sprite):
        drop_life = min(sprite.get_life(), self.get_life())
        sprite.set_life(sprite.get_life()-drop_life)
        self.set_life(self.get_life()-drop_life)
        Config.get_val("audio_hit").play(0, 500)
        Config.set_val("score", Config.get_val("score")+drop_life)
    def die_action(self):
        pass

    def over_action(self):
        if not self.OVER_ACTION:
            return
        rand_val = random.randint(1,100)
        if rand_val < 30:
            DecCd(Config.get_val("dec_cd_images"), Config.get_val("dec_cd_die_images"), 
                    self.rect.center, [0, self.speed[1]+1], 1, self.groups())
        elif rand_val < 30:
            ReLife(Config.get_val("re_life_images"), Config.get_val("re_life_die_images"), 
                    self.rect.center, [0, self.speed[1]+1], 1, self.groups())
        elif rand_val < 100:
            ClearScreen(Config.get_val("clear_screen_images"), Config.get_val("clear_screen_die_images"), 
                    self.rect.center, [0, self.speed[1]+1], 1, self.groups())

class DecCd(Cube):
    def __init__(self, images, die_images, pos, speed, life=1,  *groups):
        Cube.__init__(self, images, die_images, pos, speed, life, groups)
        self.cd = 10

    def set_cd(self, cd):
        self.cd = cd

    def collide_action(self, sprite):
        if sprite.get_name() != "KeyPlane":
            return
        self.__double_attr(sprite, "key_guns")
        self.kill()

    def __double_attr(self, sprite, attr_name):
        if not hasattr(sprite, attr_name):
            return
        guns = getattr(sprite, attr_name)
        tmp = []
        for gun in guns: 
            if gun.time > -1 or len(guns) + len(tmp) >= 3*Config.get_val(attr_name+"_ctr"):
                continue
            tmp_gun = gun.copy()
            tmp_gun.set_time(self.cd)
            tmp.append(tmp_gun)
        for gun in tmp:
            guns.add(gun)


class ReLife(Cube):
    def __init__(self, images, die_images, pos, speed, life=1,  *groups):
        Cube.__init__(self, images, die_images, pos, speed, life, groups)
        self.cd = 10

    def collide_action(self, sprite):
        if sprite.get_name() != "KeyPlane":
            return
        sprite.set_life(int(Config.get_val("max_life")*0.1 + sprite.get_life()));
        sprite.set_life(min(sprite.get_life(), Config.get_val("max_life")))
        self.kill()

class ClearScreen(Cube):
    def __init__(self, images, die_images, pos, speed, life=1,  *groups):
        Cube.__init__(self, images, die_images, pos, speed, life, groups)

    def update(self):
        pass

    def collide_action(self, sprite):
        Config.get_val("enemy_bullet_group").empty()
        #self.kill()

