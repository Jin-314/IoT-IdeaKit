from machine import Pin
from lib.TurtlePico import TurtlePico
import time

led = Pin(TurtlePico.ESC_SERVO_RL, Pin.OUT)
led_test = Pin(TurtlePico.LED_R, Pin.OUT)
led.value(0)
led_test.value(0)

while True:
    led.value(1)
    led_test.value(1)
    time.sleep(1)
    led.value(0)
    led_test.value(0)
    time.sleep(1)