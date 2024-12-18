import pygame as pg
from player import *

class Platform(Player):
    def __init__(self, x, y, speed=None):
        Player.__init__(self, x, y, speed)
        self.hitbox = pg.Rect(self.x, self.y, 2500, 70)

    def draw_platform(self, screen):
        pg.draw.rect(screen, (0, 25, 250), camera.apply(self.hitbox))

plata = Platform(200, 550)