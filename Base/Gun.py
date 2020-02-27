import pygame
import random
import copy
import math
from . import Bullet
from . import Config
from .Bullet import *
from .Config import config

class Gun(pygame.sprite.Sprite):
    def __init__(self, cd, angle, velocity, bullet, bullet_group, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.cd = int(cd)
        self.angle = angle
        self.velocity = velocity
        self.shoot_cd = 0
        self.bullet = bullet
        self.bullet_group = bullet_group

        self.time = -1

    def copy(self):
        return Gun(self.shoot_cd, self.angle, self.velocity,self.bullet, self.bullet_group, self.groups())
    
    def update(self):
        if self.time == 0:
            self.kill()
        elif self.time > 0:
            self.time -= 1
        self.shoot_cd = max(0, self.shoot_cd-1)

    def set_time(self, time):
        self.time = time*Config.get_val("fps")

    def shoot(self, pos):
        shooted = False
        if self.shoot_cd == 0:
            shooted = True
            Config.get_val("audio_fire").play(0, 500)
            self.shoot_cd = self.cd
            bullet = Bullet(self.bullet.images, self.bullet.die_images)

            velocity_x = self.velocity*math.cos(self.angle*math.pi/180)
            velocity_y = - self.velocity*math.sin(self.angle*math.pi/180)

            bullet.set_pos(pos)
            bullet.set_speed((velocity_x, velocity_y))
            bullet.set_life(2)

            self.bullet_group.add(bullet)
        return shooted

class RandomGun(pygame.sprite.Sprite):
    def __init__(self, bullet, bullet_group, *groups):
        pygame.sprite.Sprite.__init__(self, *groups)
        self.shoot_cd = 0
        self.bullet = bullet
        self.bullet_group = bullet_group
    
    def update(self):
        self.shoot_cd = max(0, self.shoot_cd-1)
        self.shoot()

    def shoot(self):
        if self.shoot_cd == 0:
            bullet = Bullet(self.bullet.images, self.bullet.die_images)
            bullet.set_over(self.bullet.OVER_ACTION)
            bullet.set_die(self.bullet.DIE_ACTION)
            self.shoot_cd = random.randint(0, 18)
            velocity = random.randint(3, 7)
            angle = random.randint(190, 350)
            mul = random.randint(1,10)
            bullet.images = [pygame.transform.scale(image, [image.get_width()*mul, image.get_height()*mul]) for image in bullet.images]
            bullet.die_images = [pygame.transform.scale(image, [image.get_width()*mul, image.get_height()*mul]) for image in bullet.die_images]
            bullet.set_life(5*mul*bullet.life)

            velocity_x = velocity*math.cos(angle*math.pi/180)
            velocity_y = - velocity*math.sin(angle*math.pi/180)

            bullet.set_pos([random.randint(0, Config.get_val("width")), random.randint(0, Config.get_val("height")/4)])
            bullet.set_speed((velocity_x, velocity_y))

            self.bullet_group.add(bullet)
