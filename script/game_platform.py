'''
    ### This file is responsible for creating, rendering and generating random platforms for games.
'''

import pygame as pg
from player import *
import random
from ring import Ring


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
    current_x = 0
    for i in range(1000):  # генерируем 1000 платформ
        width = random.randint(500, 1500)
        height = random.randint(300, 500)
        y = random.randint(500, 800)
        platforms.append(Platform(current_x, y, width, height))
        current_x += width 
        
        # Уменьшаем количество колец: пусть кольца появляются на каждой 3-й платформе
        if i % 3 == 0 and random.random() < 0.7:  # 70% шанс генерации на выбранной платформе
            ring_count = random.randint(2, 4)  # От 2 до 4 колец
            for j in range(ring_count):
                ring_x = current_x + (width // ring_count) * j + (width // (ring_count * 2))
                ring_y = y - (height // 2) - 100  # Над платформой
                
                # Проверка, чтобы кольцо не было в платформе
                if ring_y >= y:
                    ring_y = y - height - 100
                
                ring = Ring(ring_x, ring_y)
                rings_group.add(ring)
    
    return platforms, rings_group