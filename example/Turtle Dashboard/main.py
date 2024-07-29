from machine import Pin, SPI, I2C
import framebuf, time
from lib.ssd1306 import SSD1306_SPI, SSD1306_I2C
from lib.img_lib import img_lib
from lib.TurtlePico import TurtlePico

led1 = Pin(TurtlePico.LED_R, Pin.OUT)
led2 = Pin(TurtlePico.LED_L, Pin.OUT)

SW_Sel = Pin(TurtlePico.SW_L, Pin.IN, Pin.PULL_DOWN)
SW_Down = Pin(TurtlePico.SW_R, Pin.IN, Pin.PULL_DOWN)

led1.high()
led2.high()

item_selected = 0
item_sel_previous = 0
item_sel_next = 0

button_sel_clicked = False
button_down_clicked = True

menu_item_fb = [
    framebuf.FrameBuffer(img_lib.icon_weather, 16, 16, framebuf.MONO_HLSB),
    framebuf.FrameBuffer(img_lib.icon_clock, 16, 16, framebuf.MONO_HLSB),
    framebuf.FrameBuffer(img_lib.icon_timer, 16, 16, framebuf.MONO_HLSB),
    framebuf.FrameBuffer(img_lib.icon_dashboard, 16, 16, framebuf.MONO_HLSB),
    framebuf.FrameBuffer(img_lib.icon_note, 16, 16, framebuf.MONO_HLSB),
]

menu_item_char = [
    'Weather',
    'Clock',
    'Timer',
    'Stopwatch',
    'Music'
]

num_items = len(menu_item_fb)
rect_height = int(64 / num_items)

current_screen = 0  #0 : メニュー画面, 1 : メイン画面

#spi設定
#spi = SPI( TurtlePico.SPI_ID, baudrate = 100000, sck = Pin(TurtlePico.SPI_SCK), mosi = Pin(TurtlePico.SPI_MOSI))
#i2c設定
i2c = I2C( id = 0, sda = TurtlePico.I2C_SDA, scl = TurtlePico.I2C_SCL)

#pin設定(SPI)
#oled_cs = Pin(TurtlePico.OLED_CS,Pin.OUT)
#dc = Pin(TurtlePico.OLED_DC,Pin.OUT)
#rst = Pin(TurtlePico.OLED_RST,Pin.OUT)
#display宣言(I2C)
display = SSD1306_I2C(128, 64, i2c)
#display宣言(SPI)
#display = SSD1306_SPI(128, 64, spi, dc, rst, oled_cs)

fb1 = framebuf.FrameBuffer(img_lib.item_sel_background, 128, 21, framebuf.MONO_HLSB)
fb2 = framebuf.FrameBuffer(img_lib.scrollbar_background, 3, 64, framebuf.MONO_HLSB)

while(current_screen == 0):

    if(SW_Sel.value() == 1 and not button_sel_clicked):
        #current_screen = current_screen + 1
        button_sel_clicked = True

    if(SW_Down.value() == 1 and not button_down_clicked):
        item_selected = item_selected + 1
        button_down_clicked = True
        if(item_selected >= num_items):
            item_selected = 0
    
    if(SW_Sel.value() == 0 and button_sel_clicked):
        button_up_clicked = False
    if(SW_Down.value() == 0 and button_down_clicked):
        button_down_clicked = False

    item_sel_previous = item_selected - 1
    if(item_sel_previous < 0):
        item_sel_previous = num_items - 1
    item_sel_next = item_selected + 1
    if(item_sel_next >= num_items):
        item_sel_next = 0

    #backgroundを表示
    display.fill(0)

    display.blit(fb1, 0, 22)
    display.blit(fb2, 125, 0)
    display.fill_rect(125, item_selected * rect_height, 3, rect_height, 1)

    #previous item
    display.blit(menu_item_fb[item_sel_previous], 5, 2)
    display.text(menu_item_char[item_sel_previous], 29, 7, 1)

    #selected item
    display.blit(menu_item_fb[item_selected], 5, 24)
    display.text(menu_item_char[item_selected], 29, 27, 1)

    #next item
    display.blit(menu_item_fb[item_sel_next], 5, 46)
    display.text(menu_item_char[item_sel_next], 29, 50, 1)

    display.show()

#while(current_screen == 1):
