import pygame as pg
import os
from settings import *

pg.init()

class Config():
    def __init__(self):
        self.clock = pg.time.Clock()
        self.camera_group = pg.sprite.Sprite()
        self.display = pg.display.set_mode((WIDGHT, HEIGHT))
        self.directory = os.path.dirname(__file__) 
        self.game_active = True 
        self.title_w = pg.display.set_caption("Sonic Engine") 

c = Config()

class Camera:
    def __init__(self, width, height):
        self.offset_x = 0
        self.offset_y = 0
        self.additional_offset_y = 0  
        self.width = width
        self.height = height

    def apply(self, rect):
        
        return rect.move(self.offset_x, self.offset_y)

    def update(self, target):
        self.offset_x = -(target.hitbox.centerx - WIDGHT // 2)
        self.offset_y = -(target.hitbox.centery - HEIGHT // 2) + 800

        if cube.look_up:
            self.additional_offset_y = 200  
        elif cube.look_down:
            self.additional_offset_y = -200  
        else:
            self.additional_offset_y = 0  

        self.offset_x = max(-(self.width - WIDGHT), min(0, self.offset_x))
        self.offset_y = max(-(self.height - HEIGHT), min(0, self.offset_y))

        self.offset_y += self.additional_offset_y

camera = Camera(3000, 2000)

class Player():
    def __init__(self, x, y, speed):
        self.x, self.y = x, y
        self.hitbox = pg.Rect(self.x, self.y, 60, 60)
        self.go_jump = False
        self.look_down = False
        self.look_up = False
        self.go_LEFT = False
        self.go_RIGHT = False
        self.dashing = False 
        self.dash_cooldown = 0
        self.dash_delay_ms = 1000  
        self.speed = speed
        self.dash_speed = 30  
        self.dash_duration = 20  
        self.dash_frames_remaining = 0  
        self.on_Ground = False
        self.jump_count = 0
        self.jump_cooldown = 0
        self.jump_delay_ms = 500
        self.left_side = False
        self.right_side = True
        self.animation_count= 0

    def draw_player(self):
        pg.draw.rect(c.display, (0, 250, 25), camera.apply(self.hitbox))

    def start_dash(self):
        current_time = pg.time.get_ticks()
        if current_time > self.dash_cooldown and self.dash_frames_remaining == 0:
            self.dashing = True
            self.dash_frames_remaining = self.dash_duration
            self.dash_cooldown = current_time + self.dash_delay_ms  # Установка кулдауна

    def checker_pos(self):
        current_time = pg.time.get_ticks()
        keys = pg.key.get_pressed()

        if keys[pg.K_DOWN] and (keys[pg.K_a] or keys[pg.K_s]):
            self.dashing = True
            self.start_dash()
            

        if self.go_jump and self.on_Ground and self.dashing == False:
            if current_time > self.jump_cooldown:
                self.jump_cooldown = current_time + self.jump_delay_ms
                self.jump_count = 10
                self.on_Ground = False

        if self.jump_count > 0:
            self.hitbox.y -= self.speed + 35
            self.jump_count -= 1

        if self.dashing and self.dash_frames_remaining > 0:
            if self.left_side:  
                self.dashing = True
                self.hitbox.x -= self.dash_speed
            elif self.right_side:  
                self.dashing = True
                self.hitbox.x += self.dash_speed
            self.dash_frames_remaining -= 1
        else:
            self.dashing = False  

        if not self.dashing:
            if self.go_LEFT:
                if self.hitbox.x - 15 >= 0:
                    self.hitbox.x -= self.speed

            if self.go_RIGHT:
                if self.hitbox.x + self.hitbox.width <= 3000:
                    self.hitbox.x += self.speed

        if not self.on_Ground:
            self.hitbox.y += self.speed

        self.hitbox.x = max(0, min(3000 - self.hitbox.width, self.hitbox.x))
        self.hitbox.y = max(0, self.hitbox.y)  # Ограничение по верхней границе


cube = Player(500, 500, 10)


class Platform(Player):
    def __init__(self, x, y, speed=None):
        Player.__init__(self, x, y, speed)
        self.hitbox = pg.Rect(self.x, self.y, 3000, 70)

    def draw_platform(self):
        pg.draw.rect(c.display, (0, 25, 250), camera.apply(self.hitbox))

plata = Platform(200, 550)


while c.game_active: 

    c.display.fill((0, 0, 0))

    cube.on_Ground = False

    if plata.hitbox.colliderect(cube.hitbox):
        cube.on_Ground = True
        if cube.hitbox.right >= plata.hitbox.left and cube.hitbox.right <= plata.hitbox.left + cube.speed:
            cube.hitbox.right = plata.hitbox.left
        if cube.hitbox.left <= plata.hitbox.right and cube.hitbox.left >= plata.hitbox.right - cube.speed:
            cube.hitbox.left = plata.hitbox.right                    
        if cube.hitbox.top <= plata.hitbox.bottom and cube.hitbox.top >= plata.hitbox.bottom - cube.speed:
            cube.hitbox.top = plata.hitbox.bottom                    
        if cube.hitbox.bottom >= plata.hitbox.top and cube.hitbox.bottom <= plata.hitbox.top + cube.speed:
            cube.hitbox.bottom = plata.hitbox.top

    camera.update(cube)
    plata.draw_platform()
    cube.draw_player()
    cube.checker_pos()

    for i in pg.event.get():
        if i.type == pg.QUIT:
             c.game_active = False
        
        if i.type == pg.KEYUP:
            if i.key == pg.K_ESCAPE:
                c.game_active = False

            if (i.key == pg.K_a or i.key == pg.K_s):
                cube.go_jump = 0
            if i.key == pg.K_RIGHT:
                cube.left_side = False
                cube.right_side = True
                cube.go_RIGHT = 0
            if i.key == pg.K_DOWN:
                cube.look_down = 0
                key_down_start_time = None 
                key_held_for_duration = False
            if i.key == pg.K_LEFT:
                cube.left_side = True
                cube.right_side = False
                cube.go_LEFT = 0
            if i.key == pg.K_UP:
                cube.look_up = 0
                key_up_start_time = None 
                key_held_for_duration = False


        if i.type == pg.KEYDOWN:
            if (i.key == pg.K_a or i.key == pg.K_s) and not cube.dashing:
                cube.go_jump = 1
            if i.key == pg.K_RIGHT:
                cube.go_RIGHT = 1
            if i.key == pg.K_DOWN and key_down_start_time is None:  
                key_down_start_time = pg.time.get_ticks()
            if i.key == pg.K_LEFT:
                cube.go_LEFT = 1
            if i.key == pg.K_UP and key_up_start_time is None:  
                key_up_start_time = pg.time.get_ticks()   


    if key_up_start_time is not None and cube.dashing == False:
        elapsed_time = (pg.time.get_ticks() - key_up_start_time) / 1000  
        if elapsed_time >= key_up_duration and not key_held_for_duration:
            key_held_for_duration = True 
            cube.look_up = 1
    elif key_down_start_time is not None and cube.dashing == False:
        elapsed_time = (pg.time.get_ticks() - key_down_start_time) / 1000  
        if elapsed_time >= key_down_duration and not key_held_for_duration:
            key_held_for_duration = True 
            cube.look_down = 1

    pg.display.flip()
    c.clock.tick(60)
pg.quit()
