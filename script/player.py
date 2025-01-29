"""
    #### All mechanics and logic of the player sonic:
    - Logic run
    - Animation character
    - Logic of deat+

"""


import pygame as pg
from camera import *
import json as js
from settings import PATH_D


with open(PATH_D + "/json/links.json", "r") as file:
       links = js.load(file)

pg.init()

class Player(pg.sprite.Sprite):
    def __init__(self, x, y, speed, speed_defualt):
        self.x, self.y = x, y
        self.speed = speed
        self.speed_defualt = speed_defualt
        self.SIZE_S = 65
        self.hitbox = pg.Rect(self.x, self.y, self.SIZE_S, self.SIZE_S)
        self.go_jump = False
        self.look_down = False
        self.look_up = False
        self.go_LEFT = False
        self.go_RIGHT = False
        self.count_run_walk = 0
        self.run_lost_speed = False

        self.velocity_x = 0
        self.velocity_y = 0

        self.touch_R_key = False
        self.touch_L_key = False
        self.brake = False
        self.count_dontmove = 0

        self.dashing = False 
        self.dash_cooldown = 0
        self.dash_delay_ms = 1000  
        self.dash_speed = 30  
        self.dash_duration = 20  
        self.dash_frames_remaining = 0  
        self.on_Ground = False
        self.jump_count = 0
        self.jump_cooldown = 0
        self.jump_delay_ms = 500
        self.left_side, self.right_side = False, True
        self.raise_head, self.lower_head = False, False

        self.animation_count = 0
        self.current_frame = 0
        self.animation_speed = 5
        self.total_frames = 20
        self.num_frames_to_use = 5

        self.sprites = {
            "0" : pg.image.load(PATH_D + links["Sprites"]["turn_R"]),
            "1" : pg.image.load(PATH_D + links["Sprites"]["turn_L"]),
            "3" : pg.image.load(PATH_D + links["Sprites"]["jump"]),
            "2" : pg.image.load(PATH_D + links["Sprites"]["look_up_l"]),
            "4" : pg.image.load(PATH_D + links["Sprites"]["look_down_l"]),
            "5" : pg.image.load(PATH_D + links["Sprites"]["look_down_r"]),
            "6" : pg.image.load(PATH_D + links["Sprites"]["look_up_r"]),
            "7" : pg.image.load(PATH_D + links["Sprites"]["stop_break"]),
            "8" : pg.image.load(PATH_D + links["Sprites"]["stop_break_L"]),
        }

        self.sprite_animation = {
            "right": pg.image.load(PATH_D + links["Sprites"]["run_R"]),
            "left": pg.image.load(PATH_D + links["Sprites"]["run_L"]),
            "walk" : pg.image.load(PATH_D + links["Sprites"]["walk_R"]),
            "walk_l" : pg.image.load(PATH_D + links["Sprites"]["walk_L"]),
            "idle_animations" : pg.image.load(PATH_D + links["Sprites"]["dont_move_animation"]),
            "idle_animations_l" : pg.image.load(PATH_D + links["Sprites"]["dont_move_animation_l"]),
        }

        self.jump = pg.transform.scale(self.sprites["3"], (self.SIZE_S, self.SIZE_S))
        self.turn_l = pg.transform.scale(self.sprites["1"], (self.SIZE_S, self.SIZE_S))
        self.turn_r = pg.transform.scale(self.sprites["0"], (self.SIZE_S, self.SIZE_S))
        self.l_up_L = pg.transform.scale(self.sprites["2"], (self.SIZE_S, self.SIZE_S))
        self.l_down_L = pg.transform.scale(self.sprites["4"], (self.SIZE_S, self.SIZE_S))
        self.l_up_R = pg.transform.scale(self.sprites["6"], (self.SIZE_S, self.SIZE_S))
        self.l_down_R = pg.transform.scale(self.sprites["5"], (self.SIZE_S, self.SIZE_S))
        self.stop_break = pg.transform.scale(self.sprites["7"], (self.SIZE_S, self.SIZE_S))
        self.stop_break_left = pg.transform.scale(self.sprites["8"], (self.SIZE_S, self.SIZE_S))

        self.run_frames_right = self.load_run_frames(self.sprite_animation["right"], self.total_frames, self.num_frames_to_use)
        self.run_frames_left = self.load_run_frames(self.sprite_animation["left"], self.total_frames, self.num_frames_to_use)
        self.walk_frames_R = self.load_run_frames(self.sprite_animation["walk"], self.total_frames, self.num_frames_to_use)
        self.walk_frames_L = self.load_run_frames(self.sprite_animation["walk_l"], self.total_frames, self.num_frames_to_use)
        self.idle_frames_R = self.load_run_frames(self.sprite_animation["idle_animations"], self.total_frames, self.num_frames_to_use)        
        self.idle_frames_L = self.load_run_frames(self.sprite_animation["idle_animations_l"], self.total_frames, self.num_frames_to_use)

        self.current_frames = self.run_frames_right
        self.sprite_now = self.current_frames[0]

        self.in_air = False
        self.tick_air = 0
        self.animation_count = 0
        self.current_frame = 0
        self.animation_speed = 10

    def load_run_frames(self, spritesheet, total_frames, num_frames_to_use):
        frames = []
        sheet_width, sheet_height = spritesheet.get_size()
        frame_width = sheet_width // total_frames

        for i in range(num_frames_to_use):
            if i < total_frames:
                frame = spritesheet.subsurface((i * frame_width, 0, frame_width, sheet_height))
                frame = pg.transform.scale(frame, (self.SIZE_S + 10, self.SIZE_S))
                frames.append(frame)
        return frames

    def update_animation(self):
        self.animation_count += 1
        if self.animation_count >= self.animation_speed:
            self.animation_count = 0
            self.current_frame = (self.current_frame + 1) % len(self.current_frames)
            self.sprite_now = self.current_frames[self.current_frame]


    def draw_player(self, screen):
        #pg.draw.rect(screen, (0, 250, 25), camera.apply(self.hitbox))
        screen.blit(self.sprite_now, camera.apply(self.hitbox))

    def start_dash(self):
        current_time = pg.time.get_ticks()
        if current_time > self.dash_cooldown and self.dash_frames_remaining == 0:
            self.dashing = True
            self.dash_frames_remaining = self.dash_duration
            self.dash_cooldown = current_time + self.dash_delay_ms  

    def checker_pos(self):
        current_time = pg.time.get_ticks()
        keys = pg.key.get_pressed()

        if keys[pg.K_DOWN] and (keys[pg.K_a] or keys[pg.K_s]):
            self.dashing = True
            self.start_dash()
            
        if self.go_jump and self.on_Ground and not self.dashing:
            if current_time > self.jump_cooldown:
                self.jump_cooldown = current_time + self.jump_delay_ms
                self.jump_count = 10
                self.on_Ground = False
                self.sprite_now = self.jump

        if self.jump_count > 0:
            self.hitbox.y -= self.speed_defualt + 35
            self.jump_count -= 1

        if self.dashing and self.dash_frames_remaining > 0 and self.speed <= 0:
            if self.left_side:
                self.sprite_now = self.jump
                self.hitbox.x -= self.dash_speed
                self.speed = 25
            elif self.right_side:
                self.sprite_now = self.jump
                self.hitbox.x += self.dash_speed
                self.speed = 25
            self.dash_frames_remaining -= 1
        else:
            self.dashing = False

        if not self.dashing and (not self.lower_head or not self.raise_head) and self.count_dontmove < 35:
            if self.go_LEFT:
                self.hitbox.x -= self.speed
                self.left_side, self.right_side = True, False
                if self.speed < 6:
                    self.current_frames = self.walk_frames_L
                else:
                    self.current_frames = self.run_frames_left
                self.update_animation()
            elif self.go_RIGHT:
                self.hitbox.x += self.speed
                self.left_side, self.right_side = False, True
                if self.speed < 6:
                    self.current_frames = self.walk_frames_R
                else:
                    self.current_frames = self.run_frames_right
                self.update_animation()

            else:
                self.animation_count = 0
                self.current_frame = 0


        if self.on_Ground == False:
            self.hitbox.y += self.speed_defualt
        else:
            pass
            #if not self.dashing and self.on_Ground:
            #   if self.right_side:
            #       self.sprite_now = self.turn_r
            #   elif self.left_side:
            #       self.sprite_now = self.turn_l

        if self.in_air == True:
            self.sprite_now = self.jump

        if not self.dashing and self.speed <= 0 and self.on_Ground:
            if self.lower_head == True:
                if self.right_side:
                    self.sprite_now = self.l_down_R
                elif self.left_side:
                    self.sprite_now = self.l_down_L
            elif self.raise_head == True:
                if self.right_side:
                    self.sprite_now = self.l_up_R
                elif self.left_side:
                    self.sprite_now = self.l_up_L
            

        if (self.touch_L_key or self.touch_R_key) and self.speed < 35:
            self.speed += 0.05
            if self.touch_R_key:
                self.go_RIGHT = True
                self.go_LEFT = False
                self.right_side = True
                self.left_side = False
            elif self.touch_L_key:
                self.go_LEFT = True
                self.go_RIGHT = False
                self.left_side = True
                self.right_side = False

        elif self.speed > 0 and not self.touch_L_key and not self.touch_R_key:
            self.speed -= 0.05
            if not self.dashing and self.on_Ground:
                if self.right_side:
                    self.go_RIGHT = True
                    self.go_LEFT = False
                elif self.left_side:
                    self.go_LEFT = True
                    self.go_RIGHT = False

        if self.speed <= 0:
            if not self.dashing and not self.raise_head and not self.lower_head and self.on_Ground and self.count_dontmove < 35:
                if self.right_side:
                    self.sprite_now = self.turn_r
                elif self.left_side:
                    self.sprite_now = self.turn_l

            
        if self.speed <= 0 and not self.dashing and not self.raise_head and not self.lower_head:
            self.count_dontmove = min(self.count_dontmove + 0.01, 35)  
        else:
            self.count_dontmove = 0

        if self.count_dontmove >= 35 and self.on_Ground:
            self.update_animation()
            if self.right_side:
                self.current_frames = self.idle_frames_R
            elif self.left_side:
                self.current_frames = self.idle_frames_L
                    

        if self.brake and self.speed > 0:
            self.speed -= 0.5
            if self.speed >= 7:
                if self.right_side:
                    self.sprite_now = self.stop_break_left
                elif self.left_side:
                    self.sprite_now = self.stop_break


        if self.hitbox.y >= 1200:   
            self.hitbox.x = 500
            self.hitbox.y = 500


        self.hitbox.x = max(0, min(102000 - self.hitbox.width, self.hitbox.x))
        self.hitbox.y = max(0, self.hitbox.y)


cube = Player(500, 100, 0, 15)
