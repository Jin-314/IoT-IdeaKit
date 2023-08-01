from machine import Pin, SPI
import ssd1306
import img_lib
import framebuf
import utime

#spi設定
spi = SPI(0)

#pin設定
cs = Pin(17,Pin.OUT)
dc = Pin(20,Pin.OUT)
rst = Pin(21,Pin.OUT)

display = ssd1306.SSD1306_SPI(128, 64, spi, dc, rst, cs)
fb = framebuf.FrameBuffer(img_lib.kaikakuma, 128, 64, framebuf.MONO_HLSB)

#jin_imgを表示
display.fill(0)
display.blit(fb, 0, 0)
display.show()