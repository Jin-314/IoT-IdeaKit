import os
from machine import I2S
from machine import Pin
from wavplayer import WavPlayer
from sdcard import SDCard
from machine import SPI
import TurtlePico

cs = Pin(TurtlePico.SD_CS)

spi = SPI( 1,
           baudrate = 25_000_000,
           polarity=0,
           phase=0,
           bits=8,
           firstbit=SPI.MSB,
           sck  = Pin(TurtlePico.SPI_SCK),
           mosi = Pin(TurtlePico.SPI_MOSI),
           miso = Pin(TurtlePico.SPI_MISO))

sd = SDCard(spi, cs)
sd.init_spi(25_000_000)  # increase SPI bus speed to SD card
os.mount(sd, "/sd")
list = os.listdir("/sd")
print(list)

WAV_FILE = "12-Inner-Universe.wav"

wp = WavPlayer(
    id=TurtlePico.I2S_ID,
    sck_pin=TurtlePico.I2S_BCLK,
    ws_pin=TurtlePico.I2S_LRCLK,
    sd_pin=TurtlePico.I2S_SDATA,
    ibuf=40000,
    volume=-2
)
print("==========  START PLAYBACK ==========")
try:
    wp.play(WAV_FILE)
except (KeyboardInterrupt, Exception) as e:
    print("caught exception {} {}".format(type(e).__name__, e))

while wp.isplaying():
    pass
