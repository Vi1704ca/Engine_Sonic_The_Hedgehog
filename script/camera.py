import pygame as pg
from settings import *

class Camera:
    def __init__(self, width, height):
        self.offset_x = 0
        self.offset_y = 0
        self.additional_offset_y = 0  
        self.width = width
        self.height = height

    def apply(self, rect):
        return rect.move(self.offset_x, self.offset_y)

    def update(self, target, look_up, look_down):
        self.offset_x = -(target.hitbox.centerx - WIDGHT_FULL // 2)
        self.offset_y = -(target.hitbox.centery - HEIGHT_FULL // 2) + 800

        if look_up:
            self.additional_offset_y = 200  
        elif look_down:
            self.additional_offset_y = -200  
        else:
            self.additional_offset_y = 0  

        self.offset_x = max(-(self.width - WIDGHT_FULL), min(0, self.offset_x))
        self.offset_y = max(-(self.height - HEIGHT_FULL), min(0, self.offset_y))


        self.offset_y += self.additional_offset_y

camera = Camera(102000, 2000)