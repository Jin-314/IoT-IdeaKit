from machine import Pin, SPI
import machine
import os, sdcard
import TurtlePico

cs = Pin(TurtlePico.SD_CS)

spi = SPI( TurtlePico.SPI_ID,
           baudrate = 100000,
           sck  = machine.Pin(TurtlePico.SPI_SCK),
           mosi = machine.Pin(TurtlePico.SPI_MOSI),
           miso = machine.Pin(TurtlePico.SPI_MISO))

sd = sdcard.SDCard(spi, cs)

os.mount(sd, '/sd')
os.chdir('sd')

list = os.listdir("/sd")
print(list)