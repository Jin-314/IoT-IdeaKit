from machine import Pin
import time
 
led=Pin("LED",Pin.OUT)
 
print("LED starts flashing...")
while True:
    led.toggle()
    time.sleep(0.5)