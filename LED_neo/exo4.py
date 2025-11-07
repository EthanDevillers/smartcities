from ws2812 import WS2812
from utime import sleep
from machine import ADC
from random import randint

black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
white = (255, 255, 255)
yellow = (255, 150, 0)
cyan = (0, 255, 255)
purple = (180, 0, 255)
orange = (255, 85, 0)
magenta = (255, 0, 255)
lime = (200, 255, 0)
pink = (255, 105, 180)
teal = (0, 128, 128)
navy = (0, 0, 128)
olive = (128, 128, 0)
maroon = (128, 0, 0)
silver = (192, 192, 192)
gold = (255, 215, 0)

colors = [red, green, blue, white,
        yellow, cyan,purple, orange,
        magenta, lime, pink, teal, navy,
        olive, maroon, silver, gold]
noise = 0
led = WS2812(18,1)  # GPIO18, 1 LED
SOUND_SENSOR = ADC(0)  # ADC0

previous_sound = SOUND_SENSOR.read_u16()//256 #divise en 256 pour obtenir une valeur entre 0 et 255
Seuil = 100

while True:
    try:
        raw = SOUND_SENSOR.read_u16()
    except Exception as e:
        print("ADC read error:", e)
        sleep(1)
        continue

    sound = raw // 256

    # ignorer les lectures nulles 
    if sound == 0:
        continue
    
    if sound - previous_sound > Seuil:
        color = colors[randint(0, len(colors) - 1)]
        print("Sound detected:", sound,'previous:', previous_sound) 
        led.pixels_fill(color)
        led.pixels_show()
        
    previous_sound = sound