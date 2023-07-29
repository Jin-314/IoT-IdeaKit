from machine import I2S
from machine import Pin
import math
import struct
import time
from wavplayer import WavPlayer

# ESP32 の場合
sck_pin = Pin(19)   # シリアルクロック出力
ws_pin = Pin(20)    # ワードクロック出力
sd_pin = Pin(21)    # シリアルデータ出力

wp = WavPlayer(
    id=0,
    sck_pin=sck_pin,
    ws_pin=ws_pin,
    sd_pin=sd_pin,
    ibuf=20000,
    root="/",
)

wp.play("music-16k-16bits-mono.wav", loop=False)
# wait until the entire WAV file has been played
while wp.isplaying() == True:
    # other actions can be done inside this loop during playback
    pass
