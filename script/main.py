import pygame as pg
import os
from settings import *
from player import *
from camera import *
from game_platform import *
from objective import *
from ring import *
import time

pg.init()

class Config():
    def __init__(self):
        self.clock = pg.time.Clock()
        self.camera_group = pg.sprite.Sprite()
        self.display = pg.display.set_mode((WIDGHT_FULL, HEIGHT_FULL), pg.RESIZABLE)
        self.directory = os.path.dirname(__file__) 
        self.path_d = os.path.abspath(os.path.join(self.directory, os.pardir))
        self.game_active = True 
        self.title_w = pg.display.set_caption("Sonic Engine")    
        self.start_time = time.time()      

c = Config()

platforms, rings, spikes_group = generate_platforms_and_rings()
rings_group.add(rings)

def restart_game():
    print("Restarting game...")
    cube.restart_game = True

def return_to_main_menu():
    c.game_active = False


gravity = False

while c.game_active: 

    c.display.fill((0, 0, 0))

    for plata in platforms:
        plata.draw_platform(c.display)

    rings_group.update(cube, rings_group)

    for ring in rings:  
        ring.draw(c.display, camera)

    spikes_group.update()
    
    for spike in spikes_group:
        spike.draw_spike(c.display)


    if cube.lives > 0:
        for plata in platforms:
            if not plata.hitbox.colliderect(cube.hitbox):
                cube.on_Ground = False

        for plata in platforms:
            if plata.hitbox.colliderect(cube.hitbox):
                cube.on_Ground = True
                cube.tick_air = 0
                cube.in_air = False

                if cube.hitbox.right >= plata.hitbox.left and cube.hitbox.left < plata.hitbox.left:
                    cube.hitbox.right = plata.hitbox.left
                    cube.velocity_x = 0  
                if cube.hitbox.left <= plata.hitbox.right and cube.hitbox.right > plata.hitbox.right:
                    cube.hitbox.left = plata.hitbox.right
                    cube.velocity_x = 0
                if cube.hitbox.bottom >= plata.hitbox.top and cube.hitbox.top < plata.hitbox.top:
                    cube.hitbox.bottom = plata.hitbox.top
                    cube.velocity_y = 0  
                    cube.on_Ground = True  
                if cube.hitbox.top <= plata.hitbox.bottom and cube.hitbox.bottom > plata.hitbox.bottom:
                    cube.hitbox.top = plata.hitbox.bottom
                    cube.velocity_y = 0 
            

        steps = int(max(5, abs(cube.velocity_y) // 5))  
        for step in range(steps):
            cube.hitbox.y += cube.velocity_y / steps  
            for plata in platforms:
                if cube.hitbox.colliderect(plata.hitbox):  
                    cube.hitbox.bottom = plata.hitbox.top  
                    cube.velocity_y = 0
                    cube.on_Ground = True
                    break

    if not cube.on_Ground or cube.lives == 0:
        cube.tick_air += 1
        if cube.tick_air >= 3:
            cube.in_air = True


    elapsed_time = int(time.time() - c.start_time)
    fps = c.clock.get_fps()

    camera.update(cube, cube.look_up, cube.look_down)
    cube.draw_player(c.display)
    
    lives_sonic.draw_icon(c.display)
    
    cube.checker_pos()
    display_time(elapsed_time, c.display)
    display_fps(int(fps), c.display)
    draw_obj(c.display)
    

    for i in pg.event.get():
        if i.type == pg.QUIT:
             c.game_active = False

        if i.type == pygame.MOUSEBUTTONDOWN:
            restart_text, main_menu_text = draw_obj(c.display)
            mouse_pos = pygame.mouse.get_pos()
            if restart_text is not None and restart_text.rect.collidepoint(mouse_pos):
                restart_game()
            elif main_menu_text is not None and main_menu_text.rect.collidepoint(mouse_pos):
                return_to_main_menu()
        
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

    def check_key_hold(key_start_time, key_duration, cube, look_up_or_down):
        if key_start_time is not None and not cube.dashing and cube.speed <= 0:
            elapsed_time = (pg.time.get_ticks() - key_start_time) / 1000
            if elapsed_time >= key_duration and not getattr(cube, f'{look_up_or_down}_held', False):
                setattr(cube, f'{look_up_or_down}_held', True)
                setattr(cube, look_up_or_down, 1)

    check_key_hold(key_up_start_time, key_up_duration, cube, 'look_up')
    check_key_hold(key_down_start_time, key_down_duration, cube, 'look_down')


    pg.display.flip()
    
    c.clock.tick(60)
pg.quit()