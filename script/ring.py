"""
    ### Loogic generate rings
"""

import pygame
from PIL import Image, ImageSequence
from player import cube 
import json as js
from settings import PATH_D

with open(PATH_D + "/json/links.json", "r") as file:
       links = js.load(file)

gif = Image.open(PATH_D + links["Object_sprites"]["ring"])
new_size = (int(cube.hitbox.width // 2), int(cube.hitbox.height // 2))
frames = [
    pygame.image.fromstring(frame.resize(new_size).convert("RGBA").tobytes(), new_size, "RGBA")
    for frame in ImageSequence.Iterator(gif)
]

frame_index = 0
frame_counter = 0  
animation_speed = 45



class Ring(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = frames[frame_index]
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, player, rings_group):
        global frame_index, frame_counter

        frame_counter += 1
        if frame_counter >= animation_speed:
            frame_counter = 0
            frame_index = (frame_index + 1) % len(frames)
        self.image = frames[frame_index]

        if self.rect.colliderect(player.hitbox):  
            self.kill()
            cube.rings += 1


    def draw(self, screen, camera):
        screen.blit(self.image, camera.apply(self.rect))

rings_group = pygame.sprite.Group()