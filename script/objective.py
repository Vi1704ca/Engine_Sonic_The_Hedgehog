import pygame as pg
from settings import FONT_SIZE, PATH_D, score, WIDGHT_FULL
import json as js
from player import cube, camera

pg.init()

with open(PATH_D + "/json/links.json", "r") as file:
       links_fonts = js.load(file)

#print(PATH_D + links_fonts["Fonts"]["main"])

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
        Text(f"Speed: {int(cube.speed)}", (10, 180)),
        Text(f"Rings: {cube.rings}", (10, 260)),
        Text(f"FPS: {fps_text}", (WIDGHT_FULL - 250, 20))
    ]

    for text in text_objects:
        text.draw(screen)


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
        cube.rings = 0 
        cube.speed = 0  

        push_x = 300  
        push_y = 55   

        # Определяем направление движения игрока перед столкновением
        moving_right = cube.right_side
        moving_left = cube.left_side

        # Если игрок падает сверху на шипы → сильный отскок вверх + в сторону
        if cube.hitbox.bottom > self.rect.top and cube.hitbox.y > self.rect.y:
            cube.hitbox.bottom = self.rect.top
            cube.hitbox.y -= push_y  # Отскок вверх

            # Откидываем в противоположную сторону от движения
            if moving_right:
                cube.hitbox.x -= push_x // 2  # Если двигался вправо → откидываем влево
            elif moving_left:
                cube.hitbox.x += push_x // 2  # Если двигался влево → откидываем вправо

        # Если игрок врезается в правый бок шипов → отталкиваем ВЛЕВО
        elif cube.hitbox.left < self.rect.right and cube.hitbox.centerx < self.rect.centerx:
            cube.hitbox.left = self.rect.right
            cube.hitbox.x -= push_x  # Отталкиваем влево

        # Если игрок врезается в левый бок шипов → отталкиваем ВПРАВО
        elif cube.hitbox.right > self.rect.left and cube.hitbox.centerx > self.rect.centerx:
            cube.hitbox.right = self.rect.left
            cube.hitbox.x += push_x  # Отталкиваем вправо

        # Если игрок ударяется снизу (редкий случай) → отталкиваем вниз
        elif cube.hitbox.top < self.rect.bottom:
            cube.hitbox.top = self.rect.bottom
            cube.hitbox.y += 10




#~ absolute_path = os.path.abspath(os.path.join(PATH_D, links["Object_sprites"]["spikes"]))