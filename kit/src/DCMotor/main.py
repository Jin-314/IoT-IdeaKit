from machine import Pin
import time

enable = Pin(18, Pin.OUT)
left = Pin(0, Pin.OUT)
right = Pin(1, Pin.OUT)

while True:

    time.sleep(5)
    enable.value(1)
    left.value(1)
    right.value(1)
    print("forward")

    time.sleep(5)
    left.value(0)
    right.value(0)
    print("backward")

    time.sleep(5)
    enable.value(0)
    print("stop")
