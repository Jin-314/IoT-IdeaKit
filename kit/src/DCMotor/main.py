from machine import Pin
import time

enable = Pin(18, Pin.OUT)
left = Pin(22, Pin.OUT)
right = Pin(26, Pin.OUT)

while True:
    enable.value(1)
    left.value(1)
    right.value(1)

    time.sleep(10)

    left.value(0)
    right.value(1)

    time.sleep(10)

    left.value(1)
    right.value(0)

    time.sleep(10)

    left.value(0)
    right.value(0)

    time.sleep(10)

    enable.value(0)

    time.sleep(10)