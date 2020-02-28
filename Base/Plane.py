import pygame
import random

from . import Config
from . import Gun
from . import Cube
from .Cube import *
from .Config import *


class KeyPlane(Cube):
    def __init__(self, images, die_images, pos, speed, life, *groups):
        Cube.__init__(self, images, die_images, pos, speed, life, groups)
        self.key_map_move = (
                    (pygame.K_UP, 0, -5), 
                    (pygame.K_DOWN, 0, 5), 
                    (pygame.K_LEFT, -5, 0), 
                    (pygame.K_RIGHT, 5, 0), 
        )

    def update(self):
        super().update()
        self.__key_move()
        self.__move_modify()
        shooted = self.__key_gun()
#        if shooted and random.randint(1,100) == 1:
#            self.set_life(min(self.get_life()+max(1,int(0.01*Config.get_val("max_life"))), Config.get_val("max_life")))


    def __key_move(self):
        keys = pygame.key.get_pressed()
        for row in self.key_map_move:
            if True == keys[row[0]]:
                self.rect.centerx += row[1]
                self.rect.centery += row[2]

    def __key_gun(self):
        print('Quick-firing gun: ', len(self.key_guns), 'Slow-firing gun: ',  len(self.auto_guns))
        shooted = False
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            for gun in self.key_guns:
                if hasattr(gun, "shoot"):
                    gun.shoot(self.rect.midtop)
                    shooted = True
        return shooted


    def add_key_gun(self, gun):
        self.key_guns.add(gun)
        #self.key_guns.append(gun)

    def __move_modify(self):
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > Config.get_val("height"):
            self.rect.bottom = Config.get_val("height")
        if self.rect.right > Config.get_val("width"):
            self.rect.right = Config.get_val("width")

class AutoPlane(Cube):
    def __init__(self, images, die_images, pos, speed, life, *group):
        Cube.__init__(self, images, die_images, pos, speed, life, *groups)
