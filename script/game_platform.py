'''
    ### This file is responsible for creating, rendering and generating random platforms for games.
'''

import pygame as pg
from player import *
import random
from ring import Ring
from objective import Spike


class Platform(Player):
    def __init__(self, x, y, width, height, speed=0):
        super().__init__(x, y, speed, speed_defualt=None) 
        self.width = width  
        self.height = height
        self.hitbox = pg.Rect(self.x, self.y, width, height)  


    def draw_platform(self, screen):
        pg.draw.rect(screen, (0, 25, 250), camera.apply(self.hitbox))
#plata = Platform(200, 550)

platforms = []

def generate_platforms_and_rings():
    platforms = []
    rings_group = pg.sprite.Group()
    spikes_group = pg.sprite.Group()

    current_x = 0
    for i in range(1000):  
        width = random.randint(500, 1500)
        height = random.randint(300, 500)
        y = random.randint(500, 800)
        platform = Platform(current_x, y, width, height)
        platforms.append(platform)
        current_x += width  

        if i % 3 == 0 and random.random() < 0.7:
            ring_count = random.randint(2, 4)
            segment_width = width // ring_count
            for j in range(ring_count):
                ring_x = current_x + segment_width * j + segment_width // 2
                ring_y = y - height // 2 - 100
                ring_y = max(ring_y, y - height - 100)  

                rings_group.add(Ring(ring_x, ring_y))

        if i % 6 == 0 and random.random() < 0.8:
            spike_count = random.randint(3, 5)
            spike_x_start = platform.hitbox.left + random.randint(20, 50)
            spike_spacing = cube.SIZE_S + 10

            for j in range(spike_count):
                spike_x = spike_x_start + j * spike_spacing
                if spike_x + cube.SIZE_S > platform.hitbox.right:
                    break 
                
                spike_y = platform.hitbox.top - cube.SIZE_S
                spikes_group.add(Spike(spike_x, spike_y))

    return platforms, rings_group, spikes_group


