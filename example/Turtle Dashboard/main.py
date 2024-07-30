from machine import Pin, SPI, I2C
import framebuf, os
import lib, network, time

led1 = Pin(lib.TurtlePico.LED_R, Pin.OUT)
led2 = Pin(lib.TurtlePico.LED_L, Pin.OUT)

SW_Sel = Pin(lib.TurtlePico.SW_L, Pin.IN, Pin.PULL_DOWN)
SW_Up = Pin(lib.TurtlePico.SW_R, Pin.IN, Pin.PULL_DOWN)

led1.high()
led2.high()

item_selected = 0
item_sel_previous = 0
item_sel_next = 0

button_sel_clicked = False
button_up_clicked = False

menu_item_fb = [
    framebuf.FrameBuffer(lib.img_lib.icon_weather, 16, 16, framebuf.MONO_HLSB),
    framebuf.FrameBuffer(lib.img_lib.icon_clock, 16, 16, framebuf.MONO_HLSB),
    framebuf.FrameBuffer(lib.img_lib.icon_timer, 16, 16, framebuf.MONO_HLSB),
    framebuf.FrameBuffer(lib.img_lib.icon_dashboard, 16, 16, framebuf.MONO_HLSB),
    framebuf.FrameBuffer(lib.img_lib.icon_note, 16, 16, framebuf.MONO_HLSB),
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
i2c = I2C( id = 0, sda = lib.TurtlePico.I2C_SDA, scl = lib.TurtlePico.I2C_SCL)

#pin設定(SPI)
#oled_cs = Pin(TurtlePico.OLED_CS,Pin.OUT)
#dc = Pin(TurtlePico.OLED_DC,Pin.OUT)
#rst = Pin(TurtlePico.OLED_RST,Pin.OUT)
#display宣言(I2C)
display = lib.SSD1306_I2C(128, 64, i2c)
#display宣言(SPI)
#display = SSD1306_SPI(128, 64, spi, dc, rst, oled_cs)

fb1 = framebuf.FrameBuffer(lib.img_lib.item_sel_background, 128, 21, framebuf.MONO_HLSB)
fb2 = framebuf.FrameBuffer(lib.img_lib.scrollbar_background, 3, 64, framebuf.MONO_HLSB)

os.chdir('/fonts')
po = lib.FontDrawer( frame_buffer=display, font_name = 'PixelOperator' )
po_b = lib.FontDrawer( frame_buffer=display, font_name = 'PixelOperatorBold')

#スクリーンオブジェクト
sc = None

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(lib.wifi_config.ssid, lib.wifi_config.pw)

max_wait = 10
while max_wait > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_wait -= 1
    print('接続待ち...')
    time.sleep(1)

if wlan.status() != 3:
    print(wlan.status())
    raise RuntimeError('ネットワーク接続失敗')
else:
    print('接続完了')
    status = wlan.ifconfig()
    print( 'IPアドレス = ' + status[0] )

while(True):

    while(current_screen == 0):

        if(SW_Sel.value() == 1 and not button_sel_clicked):
            current_screen = current_screen + 1
            if(menu_item_char[item_selected] == 'Clock'):
                sc = lib.screens.clock(display)
            else:
                raise Exception( "Invalid Menu Item!" )
            button_sel_clicked = True

        if(SW_Up.value() == 1 and not button_up_clicked):
            item_selected = item_selected + 1
            button_up_clicked = True
            if(item_selected >= num_items):
                item_selected = 0
        
        if(SW_Sel.value() == 0 and button_sel_clicked):
            button_sel_clicked = False
        if(SW_Up.value() == 0 and button_up_clicked):
            button_up_clicked = False

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
        #scroll barの表示
        display.fill_rect(125, item_selected * rect_height, 3, rect_height, 1)

        #previous item
        display.blit(menu_item_fb[item_sel_previous], 5, 2)
        #display.text(menu_item_char[item_sel_previous], 29, 7, 1)
        po.print_str(menu_item_char[item_sel_previous], 29, 5)

        #selected item
        display.blit(menu_item_fb[item_selected], 5, 24)
        #display.text(menu_item_char[item_selected], 29, 27, 1)
        po_b.print_str(menu_item_char[item_selected], 29, 25)

        #next item
        display.blit(menu_item_fb[item_sel_next], 5, 46)
        #display.text(menu_item_char[item_sel_next], 29, 50, 1)
        po.print_str(menu_item_char[item_sel_next], 29, 48)

        display.show()

    while(current_screen == 1):

        if(SW_Sel.value() == 1 and not button_sel_clicked):
            if(sc.selMenu() < 0):
                current_screen = 0
            button_sel_clicked = True

        if(SW_Up.value() == 1 and not button_up_clicked):
            sc.upMenu()
            button_up_clicked = True
        
        if(SW_Sel.value() == 0 and button_sel_clicked):
            button_sel_clicked = False
        if(SW_Up.value() == 0 and button_up_clicked):
            button_up_clicked = False

        sc.showDisplay()