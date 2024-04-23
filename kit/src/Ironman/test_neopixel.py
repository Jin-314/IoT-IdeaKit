import time
from machine import Pin
import neopixel

pixelNum = 15
np1 = neopixel.NeoPixel(Pin(13), pixelNum)

# 循環
for i in range(15):
    np1[i % 15] = (0, 32, 0)
    np1.write()
    time.sleep_ms(25)

time.sleep_ms(1000)

for i in range(15):
    np1[i] = (0, 0, 0)
    
np1.write()