from machine import Pin, SPI
import machine
import os, sdcard

cs = Pin(6)

spi = SPI( 1,
           baudrate = 100000,
           sck  = machine.Pin(10),
           mosi = machine.Pin(11),
           miso = machine.Pin(12))

sd = sdcard.SDCard(spi, cs)

os.mount(sd, '/sd')
os.chdir('sd')

list = os.listdir("/sd")
print(list)