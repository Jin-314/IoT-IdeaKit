import time
from machine import Pin

#ピンを設定
trig = Pin(15, Pin.OUT)
echo = Pin(14, Pin.IN)
red = Pin(4, Pin.OUT)
blue = Pin(18, Pin.OUT)

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
