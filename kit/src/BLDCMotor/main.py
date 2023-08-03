from machine import Pin, PWM
import time

input1 = Pin(0, Pin.IN, Pin.PULL_DOWN)
input2 = Pin(1, Pin.IN, Pin.PULL_DOWN)

#duty cycle
Max_duty = 0.1 * 65536
Min_duty = 0.05 * 65536

#calibration
def calibration():
    duty = Max_duty
    status = 1
    print("Calibration start")
    for i in range(0, 3):
        for j in range(0, 10):
            if status == 1:
                duty -= 0.005 * 65536
            else:
                duty += 0.005 * 65536
            print(duty / 65536)
            BLDC.duty_u16(int(duty))
            time.sleep(0.1)
        status = status * -1
        time.sleep(3)
    print("Calibration done")

BLDC = PWM(Pin(2))
BLDC.freq(50)

duty = Max_duty
print(duty / 65536)
BLDC.duty_u16(int(duty))

isCalibrated = False

while True:
    if input1.value() == 1:
        if isCalibrated == False:
            calibration()
            isCalibrated = True
            duty = Min_duty
        else:
            if duty < Max_duty:
                duty += 0.001 * 65536
            print(duty / 65536)
            BLDC.duty_u16(int(duty))
            time.sleep(0.5)
    elif input2.value() == 1:
        if isCalibrated == True:
            if duty > Min_duty:
                duty -= 0.001 * 65536
            print(duty / 65536)
            BLDC.duty_u16(int(duty))
            time.sleep(0.5)