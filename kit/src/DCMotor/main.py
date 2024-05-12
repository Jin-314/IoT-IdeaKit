from machine import Pin
import time
from lib.TurtlePico import TurtlePico

enable = Pin(TurtlePico.MOTOR_EN, Pin.OUT)
left = Pin(TurtlePico.MOTOR_L, Pin.OUT)
right = Pin(TurtlePico.MOTOR_R, Pin.OUT)

while True:

    time.sleep(5)
    enable.value(1)
    left.value(1)
    right.value(1)
    print("forward")

    time.sleep(5)
    left.value(0)
    right.value(1)
    print("turn right")

    time.sleep(5)
    left.value(1)
    right.value(0)
    print("forward")

    time.sleep(5)
    left.value(0)
    right.value(0)
    print("backward")

    time.sleep(5)
    enable.value(0)
    print("stop")
