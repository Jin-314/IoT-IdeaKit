from machine import Pin, SPI
import ssd1306
import img_lib
import framebuf
import TurtlePico

led1 = Pin(TurtlePico.LED_R, Pin.OUT)
led2 = Pin(TurtlePico.LED_L, Pin.OUT)

led1.high()
led2.high()

#spi設定
spi = SPI( TurtlePico.SPI_ID, baudrate = 100000, sck = Pin(TurtlePico.SPI_SCK), mosi = Pin(TurtlePico.SPI_MOSI))

#pin設定
oled_cs = Pin(TurtlePico.OLED_CS,Pin.OUT)
dc = Pin(TurtlePico.OLED_DC,Pin.OUT)
rst = Pin(TurtlePico.OLED_RST,Pin.OUT)
display = ssd1306.SSD1306_SPI(128, 64, spi, dc, rst, oled_cs)

fb = framebuf.FrameBuffer(img_lib.jin_img, 128, 64, framebuf.MONO_HLSB)

#jin_imgを表示
display.fill(0)
display.blit(fb, int((128-74) / 2), 0)
display.show()