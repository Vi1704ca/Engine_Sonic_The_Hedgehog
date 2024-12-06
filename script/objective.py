import pygame as pg
from settings import FONT_SIZE, PATH_D, rings, score, WIDGHT
import json as js
import time

pg.init()

with open(PATH_D + "/json/links.json", "r") as file:
       links_fonts = js.load(file)

print(PATH_D + links_fonts["Fonts"]["main"])

class Text():
    def __init__(self, text, pos):
        self.text = text
        self.pos = pos
        self.font = pg.font.Font(None, FONT_SIZE)
        self.font_link = PATH_D + links_fonts["Fonts"]["main"]
        self.shift = pg.font.Font(self.font_link, FONT_SIZE)
        self.text_shoft = self.shift.render(self.text, True, (250, 250, 250))

    def draw(self, screen):
        screen.blit(self.text_shoft, self.pos)

def display_time(seconds, screen):
    global time_value
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    time_value = f"{minutes}:{remaining_seconds:02}" 

def display_fps(fps, screen):
    global fps_text
    fps_text = f"{fps}" 
    
def draw_obj(screen):
    #screen.blit(self.text_shoft, self.pos)
    text_objects = [
        Text(f"Score: {score}", (10, 20)),
        Text(f"Time: {time_value}", (10, 100)),
        Text(f"Rings: {rings}", (10, 180)),
        Text(f"FPS: {fps_text}", (WIDGHT - 250, 20))
    ]

    for text in text_objects:
        text.draw(screen)
