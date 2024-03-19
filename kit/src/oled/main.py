from machine import Pin, SPI
import ssd1306
import img_lib
import framebuf

#spi設定
spi = SPI( 1,baudrate = 100000, sck = Pin(10), mosi = Pin(11))

#pin設定
oled_cs = Pin(7,Pin.OUT)
dc = Pin(6,Pin.OUT)
rst = Pin(5,Pin.OUT)
display = ssd1306.SSD1306_SPI(128, 64, spi, dc, rst, oled_cs)

fb = framebuf.FrameBuffer(img_lib.techring, 74, 64, framebuf.MONO_HLSB)

#jin_imgを表示
display.fill(0)
display.blit(fb, int((128-74) / 2), 0)
display.show()