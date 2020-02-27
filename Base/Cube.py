import pygame
from . import Config
from .Config import *

class Cube(pygame.sprite.Sprite):
    def __init__(self, images, die_images, pos, speed, life, *groups):
        pygame.sprite.Sprite.__init__(self, groups)
        self.images = self.__animation_init(images)
        self.die_images = self.__animation_init(die_images)
        self.image_index = 0
        self.rect = pygame.Rect(-100, -100, 0, 0)
        self.__play_image()

        self.auto_guns = []
        self.key_guns = []

        self.set_pos(pos)
        self.set_speed(speed)
        self.set_life(life)

    def __animation_init(self, images):
        ret = []
        if type(images) == tuple or type(images) == list:
            for image in images:
                ret.append(image)
        else:
            ret.append(images)
        return ret

    def get_life(self):
        return self.life

    def isdie(self):
        return self.life <= 0

    def over(self):
        return self.isdie() and self.life == -len(self.images)

    def update(self):
        if self.isdie():
            if self.over():
                self.kill()
            elif self.life == 0:
                if hasattr(self, 'auto_guns'):
                    for gun in self.auto_guns:
                        gun.kill()
                if hasattr(self, 'key_guns'):
                    for gun in self.key_guns:
                        gun.kill()
                self.__update_die()
                self.life -= 1
            else:
                self.life -= 1
        else:
            self.__speed_move()
            self.__auto_gun()
        self.__play_image()

    def set_pos(self, pos):
        if pos:
            self.rect.center = (pos[0], pos[1])

    def set_speed(self, speed):
        if speed:
            self.speed = [speed[0], speed[1]]

    def set_life(self, life):
        if life != None:
            self.life = life

    def add_auto_gun(self, *guns):
        for gun in guns:
            self.auto_guns.append(guns)

    def __speed_move(self):
        self.rect.x += self.speed[0]
        self.rect.y += self.speed[1]

    def __auto_gun(self):
        for gun in self.auto_guns:
            if hasattr(gun, 'shoot'):
                gun.shoot()
    def __play_image(self):
        self.image_index = self.image_index%len(self.images)
        pos = self.rect.center
        self.image = self.images[self.image_index]
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.image_index += 1

    def __update_die(self):
        self.images = self.die_images
        self.image_index= 0
