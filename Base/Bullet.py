import pygame
from Base import Cube
from .Cube import *

class Bullet(Cube):
    def __init__(self, image, die_image, pos=None, speed=None, life=1, *groups):
        Cube.__init__(self, image, die_image, pos, speed, life, groups)
