'''
    ### This file is responsible for creating, rendering and generating random platforms for games.
'''

import pygame as pg
from player import *
import random
import numpy as np

class Platform(Player):
    def __init__(self, x, y, width, height, speed=0):
        super().__init__(x, y, speed, speed_defualt=None) 
        self.hitbox = pg.Rect(self.x, self.y, width, height)  


    def draw_platform(self, screen):
        pg.draw.rect(screen, (0, 25, 250), camera.apply(self.hitbox))
#plata = Platform(200, 550)

platforms = []



def generate_platforms():
    platforms = []
    current_x = 0
    for _ in range(1000):
        width = random.randint(500, 1500)
        height = random.randint(300, 500)
        y = random.randint(500, 800)
        platforms.append(Platform(current_x, y, width, height))
        current_x += width 
    return platforms