import machine
from machine import PWM, Pin
import time
from lib.TurtlePico import TurtlePico

RSW = Pin(TurtlePico.SW_R, Pin.IN, Pin.PULL_DOWN)
LSW = Pin(TurtlePico.SW_L, Pin.IN, Pin.PULL_DOWN)

i = 0
status = 0

while True:
    print(RSW.value())
    print(LSW.value())
    
    time.sleep(0.1)