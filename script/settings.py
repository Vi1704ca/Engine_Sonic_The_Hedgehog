import ctypes
import os

user32 = ctypes.windll.user32

WIDGHT_FULL = user32.GetSystemMetrics(0)
HEIGHT_FULL = user32.GetSystemMetrics(1)
WIDGHT, HEIGHT = 1040, 800

WIDGHT_NOW, HEIGHT_NOW = WIDGHT, HEIGHT


DIRECTORY = os.path.dirname(__file__) 
PATH_D = os.path.abspath(os.path.join(DIRECTORY, os.pardir))


key_held_for_duration = False  
key_up_start_time = None 
key_up_pressed = False
key_up_duration = 2

key_down_start_time = None 
key_down_pressed = False
key_down_duration = 2

FONT_SIZE = 35

score = 0
time = "0:0"
rings =0