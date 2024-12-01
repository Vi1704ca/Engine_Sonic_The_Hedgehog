import ctypes

user32 = ctypes.windll.user32

#WIDGHT = user32.GetSystemMetrics(0)
#HEIGHT = user32.GetSystemMetrics(1)

WIDGHT, HEIGHT = 1040, 800

key_held_for_duration = False  
key_up_start_time = None 
key_up_pressed = False
key_up_duration = 2

key_down_start_time = None 
key_down_pressed = False
key_down_duration = 2