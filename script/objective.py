import pygame as pg
from settings import FONT_SIZE, PATH_D, score, WIDGHT_FULL, HEIGHT_FULL
import json as js
from player import cube, camera
import os

pg.init()

with open(PATH_D + "/json/links.json", "r") as file:
       links_fonts = js.load(file)

#print(PATH_D + links_fonts["Fonts"]["main"])

class Text:
    def __init__(self, text, pos, font_size=FONT_SIZE, text_color=(250, 250, 250), outline_color=(67, 119, 204), outline_thickness=5):
        self.text = text
        self.pos = pos
        self.font_size = font_size
        self.text_color = text_color
        self.outline_color = outline_color
        self.outline_thickness = outline_thickness

        self.font_link = os.path.abspath(os.path.join(PATH_D + links_fonts["Fonts"]["game"]))
        try:
            self.font = pg.font.Font(self.font_link, self.font_size)
        except FileNotFoundError:
            self.font = pg.font.Font(None, self.font_size)

        self.text_surface = self.render_outlined_text()

        # Создание self.rect для коллизий
        self.rect = self.text_surface.get_rect(topleft=self.pos)  


    def render_outlined_text(self):
        text_surf = self.font.render(self.text, True, self.text_color)
        outline_surf = self.font.render(self.text, True, self.outline_color)

        text_width, text_height = text_surf.get_size()
        outline_size = self.outline_thickness * 2
        surface = pg.Surface((text_width + outline_size, text_height + outline_size))
        surface.set_colorkey((0, 0, 0)) 

        for dx in (-self.outline_thickness, 0, self.outline_thickness):
            for dy in (-self.outline_thickness, 0, self.outline_thickness):
                if dx != 0 or dy != 0: 
                    surface.blit(outline_surf, (dx + self.outline_thickness, dy + self.outline_thickness))

        surface.blit(text_surf, (self.outline_thickness, self.outline_thickness))

        return surface

    def draw(self, screen):
        screen.blit(self.text_surface, self.pos)

def display_time(seconds, screen):
    global time_value  # Добавляем global
    minutes = seconds // 60
    remaining_seconds = seconds % 60
    time_value = f"{minutes}:{remaining_seconds:02}" 


def display_fps(fps, screen):
    global fps_text
    fps_text = f"{fps}" 
    

restart_text = None
main_menu_text = None
def draw_obj(screen):
    global restart_text, main_menu_text
    text_objects = []

    if cube.lives > 0:
        text_objects = [
            Text(f"Score: {score}", (10, 20)),
            Text(f"Time: {time_value}", (10, 100)),
            Text(f"Speed: {int(cube.speed)}", (10, 180)),
            Text(f"Rings: {cube.rings}", (10, 260)),
            Text(f"FPS: {fps_text}", (WIDGHT_FULL - 250, 20)),
            Text(f"x{cube.lives}", (10, HEIGHT_FULL - FONT_SIZE - 10)),
        ]
    elif cube.lives <= 0:
        text_objects = [
            Text("GAME OVER", ((WIDGHT_FULL - 450) // 4.5, (HEIGHT_FULL // 2) - 250), font_size=250), 
        ]
        restart_text = Text(
            "Restart",
            (WIDGHT_FULL // 2.5 - 50, HEIGHT_FULL // 2 + 80),  
            font_size=100, 
            text_color=(255, 255, 255),  
            outline_color=(67, 119, 204),  
            outline_thickness=5,
        )
        text_objects.append(restart_text)

        main_menu_text = Text(
            "Main Menu",
            (WIDGHT_FULL // 2.5 - 50, HEIGHT_FULL // 2 + 200), 
            font_size=100,  
            text_color=(255, 255, 255),  
            outline_color=(67, 119, 204), 
            outline_thickness=5, 
        )
        text_objects.append(main_menu_text)

    for text in text_objects:
        text.draw(screen)

    return restart_text, main_menu_text  # <-- Возвращаем переменные


class Spike(pg.sprite.Sprite):
    def __init__(self, x, y, width=cube.SIZE_S, height=cube.SIZE_S):
        super().__init__()
        
        self.image = pg.image.load(PATH_D + links_fonts["Object_sprites"]["spikes"])
        self.image = pg.transform.scale(self.image, (width, height))
        self.rect = self.image.get_rect(topleft=(x, y))

    def draw_spike(self, screen):
        screen.blit(self.image, camera.apply(self.rect))

    def update(self):
        if self.rect.colliderect(cube.hitbox):
            self.push_player()

    def push_player(self):
        if cube.rings <= 0:
            cube.loss = True
        
        if cube.dashing:
            cube.rings = 0
            cube.speed = 0

        cube.rings = 0 
        cube.speed = 0  

        push_x = 450  
        push_y = 200   

        moving_right = cube.right_side
        moving_left = cube.left_side

        if cube.hitbox.bottom > self.rect.top and cube.hitbox.y > self.rect.y:
            cube.hitbox.bottom = self.rect.top
            cube.hitbox.y -= push_y  

            if moving_right:
                cube.hitbox.x -= push_x // 2 
            elif moving_left:
                cube.hitbox.x += push_x // 2  

        elif cube.hitbox.left < self.rect.right and cube.hitbox.centerx < self.rect.centerx:
            cube.hitbox.left = self.rect.right
            cube.hitbox.x -= push_x 

        elif cube.hitbox.right > self.rect.left and cube.hitbox.centerx > self.rect.centerx:
            cube.hitbox.right = self.rect.left
            cube.hitbox.x += push_x  

        elif cube.hitbox.top < self.rect.bottom:
            cube.hitbox.top = self.rect.bottom
            cube.hitbox.y += 10

class Icons():
    def __init__(self, x, y, image_path, width=65, height=65):
        self.width, self.height = width, height
        self.x, self.y = x, HEIGHT_FULL - self.height - 25

        self.image = pg.image.load(image_path) 
        self.image = pg.transform.scale(self.image, (self.width, self.height))

    def draw_icon(self, screen):
        if cube.lives > 0:
            screen.blit(self.image, (self.x, self.y))

lives_sonic = Icons(50, 250, os.path.abspath(os.path.join(PATH_D + links_fonts["Icons"]["sonic_lives"])))


#~ absolute_path = os.path.abspath(os.path.join(PATH_D, links["Object_sprites"]["spikes"]))