from machine import Pin, SPI
import os, sdcard
from wavplayer import WavPlayer

# ESP32 の場合
sck_pin = Pin(19)   # シリアルクロック出力
ws_pin = Pin(20)    # ワードクロック出力
sd_pin = Pin(21)    # シリアルデータ出力

spi = SPI( 1,
           baudrate = 25_000_000,
           polarity=0,
           phase=0,
           bits=8,
           firstbit=SPI.MSB,
           sck  = Pin(10),
           mosi = Pin(11),
           miso = Pin(12))

sd = sdcard.SDCard(spi, Pin(6))

os.mount(sd, '/sd')
os.chdir('sd')

list = os.listdir()
print(list)

wp = WavPlayer(
    id=0,
    sck_pin=sck_pin,
    ws_pin=ws_pin,
    sd_pin=sd_pin,
    ibuf=40000,
)

wp.play("Elden-Ring.wav", loop=False)
# wait until the entire WAV file has been played
while wp.isplaying() == True:
    # other actions can be done inside this loop during playback
    pass
