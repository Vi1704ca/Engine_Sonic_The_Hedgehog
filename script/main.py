import pygame as pg
import os
from settings import *
from player import *
from camera import *
from platform import *
from objective import *
import time

pg.init()

class Config():
    def __init__(self):
        self.clock = pg.time.Clock()
        self.camera_group = pg.sprite.Sprite()
        self.display = pg.display.set_mode((WIDGHT_FULL, HEIGHT_FULL), pg.SCALED)
        self.directory = os.path.dirname(__file__) 
        self.path_d = os.path.abspath(os.path.join(self.directory, os.pardir))
        self.game_active = True 
        self.title_w = pg.display.set_caption("Sonic Engine")    
        self.start_time = time.time()      
        self.full_screen = False  

c = Config()

gravity = False

while c.game_active: 

    c.display.fill((0, 0, 0))


    if plata.hitbox.colliderect(cube.hitbox):
        cube.on_Ground = True
        cube.tick_air = 0
        cube.in_air = False
        if cube.hitbox.right >= plata.hitbox.left and cube.hitbox.right <= plata.hitbox.left + cube.speed_defualt:
            cube.hitbox.right = plata.hitbox.left
        if cube.hitbox.left <= plata.hitbox.right and cube.hitbox.left >= plata.hitbox.right - cube.speed_defualt:
            cube.hitbox.left = plata.hitbox.right                    
        if cube.hitbox.top <= plata.hitbox.bottom and cube.hitbox.top >= plata.hitbox.bottom - cube.speed_defualt:
            cube.hitbox.top = plata.hitbox.bottom                    
        if cube.hitbox.bottom >= plata.hitbox.top and cube.hitbox.bottom <= plata.hitbox.top + cube.speed_defualt:
            cube.hitbox.bottom = plata.hitbox.top

    else: 
        cube.on_Ground = False

    if cube.on_Ground == False:
        cube.tick_air += 1
    
    if cube.tick_air >= 3:
        cube.in_air = True
        

    elapsed_time = int(time.time() - c.start_time)
    fps = c.clock.get_fps()

    camera.update(cube, cube.look_up, cube.look_down)
    cube.draw_player(c.display)
    plata.draw_platform(c.display)
    cube.checker_pos()
    display_time(elapsed_time, c.display)
    display_fps(int(fps), c.display)
    draw_obj(c.display)
    

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
                cube.touch_R_key = False
                cube.touch_L_key = False
            if i.key == pg.K_DOWN:
                cube.lower_head = 0
                cube.look_down = 0
                key_down_start_time = None 
                key_held_for_duration = False
            if i.key == pg.K_LEFT:
                cube.left_side = True
                cube.right_side = False
                cube.go_LEFT = 0
                cube.touch_R_key = False
                cube.touch_L_key = False
            if i.key == pg.K_UP:
                cube.raise_head = 0
                cube.look_up = 0
                key_up_start_time = None 
                key_held_for_duration = False
            if i.key == pg.K_x:
                cube.brake = 0
            


        if i.type == pg.KEYDOWN:
            if (i.key == pg.K_a or i.key == pg.K_s) and not cube.dashing:
                cube.go_jump = 1
            if i.key == pg.K_RIGHT:
                cube.touch_R_key = True
                cube.touch_L_key = False
                cube.go_RIGHT = 1
            if i.key == pg.K_DOWN and key_down_start_time is None:  
                cube.lower_head = 1
                key_down_start_time = pg.time.get_ticks()
            if i.key == pg.K_LEFT:
                cube.touch_R_key = False
                cube.touch_L_key = True
                cube.go_LEFT = 1
            if i.key == pg.K_UP and key_up_start_time is None:  
                cube.raise_head = 1
                key_up_start_time = pg.time.get_ticks()   
            if i.key == pg.K_x:
                cube.brake = 1

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