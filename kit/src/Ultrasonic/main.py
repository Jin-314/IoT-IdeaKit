import time
from machine import Pin
from lib.TurtlePico import TurtlePico

#ピンを設定
trig = Pin(TurtlePico.TRIG_TX, Pin.OUT)
echo = Pin(TurtlePico.ECHO_RX, Pin.IN)
red = Pin(TurtlePico.LED_L, Pin.OUT)
blue = Pin(TurtlePico.LED_R, Pin.OUT)

while True:
    trig.low()
    time.sleep_us(2)
    trig.high()
    time.sleep_us(10)
    trig.low()
    signaloff, signalon = 0, 0
    while echo.value() == 0:
        signaloff = time.ticks_us()
    while echo.value() == 1:
        signalon = time.ticks_us()
    timepassed = signalon - signaloff
    distance = (timepassed * 0.0343) / 2
    print("dinstance: ",distance,"cm")
    blue.value(1)
    time.sleep(0.1)
