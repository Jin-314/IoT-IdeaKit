from machine import Pin,SPI,RTC
import ssd1306
import img_lib
import framebuf
import network
import utime
import ntptime

#spi設定
spi = SPI(0)

#pin設定
cs = Pin(17,Pin.OUT)
dc = Pin(20,Pin.OUT)
rst = Pin(21,Pin.OUT)

display = ssd1306.SSD1306_SPI(128, 64, spi, dc, rst, cs)
fb = framebuf.FrameBuffer(img_lib.jin_img, 128, 64, framebuf.MONO_HLSB)

ssid = 'SSID'
password = 'PASS'

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(ssid, password)

#wait for connection
max_count = 10
while max_count > 0:
    if wlan.status() < 0 or wlan.status() >= 3:
        break
    max_count -= 1
    print('wait for connection')
    utime.sleep(1)

#define blinking function for LED to indicate connection status
def blink_onboard_led(num_blinks):
    led = Pin("LED", Pin.OUT)
    for i in range(num_blinks):
        led.on()
        utime.sleep(.2)
        led.off()
        utime.sleep(.2)

wlan_status = wlan.status()
blink_onboard_led(wlan_status)

if wlan_status != 3:
    raise RuntimeError("Could not connect to the internet")
else:
    print("Connected to the internet")
    status = wlan.ifconfig()
    print("ip = "+status[0])


#NTPサーバーから時刻を取得
#wifi接続による時刻合わせ
ntptime.host = "ntp.nict.jp"
ntptime.settime()

timZone = 9
preSec = 0

while True:

    #wifiにて合わせた時刻から内部RTCモジュールでカウント
    t0 = RTC().datetime()

    if(preSec != t0[6]):
        preSec = t0[6]
        hour = t0[4] + timZone
        day = t0[2]

        # 24時を超えた場合、時間を-24する
        if hour >= 24:
            hour -= 24
            day += 1
            
        dateTxt = "{0}/{1:02d}/{2:02d}".format(t0[0],t0[1],day)
        timeTxt = "{0:02d}:{1:02d}:{2:02d}".format(hour,t0[5],preSec)

        #ログ表示
        print(dateTxt)
        print(timeTxt)

        #OLED表示
        display.fill(0)
        display.text(dateTxt, int(128/2-len(dateTxt)*8/2), int(64/2-8), 1)
        display.text(timeTxt, int(128/2-len(timeTxt)*8/2), int(64/2), 1)
        display.show()
    
    utime.sleep(0.1)