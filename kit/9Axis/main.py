from machine import Pin, I2C
import time
import ustruct
import math

i2c = I2C(0, scl=Pin(17), sda=Pin(16), freq=100000)

# デバイスのアドレスをスキャンします
addr = i2c.scan()
print( "address is :" + str(addr) )

addr_ag = 0x6a
addr_m = 0x1c

CTRL_REG1_G = 0x10
CTRL_REG2_G = 0x11
CTRL_REG3_G = 0x12
ORIENT_CFG_G = 0x13
CTRL_REG4 = 0x1E
CTRL_REG5_XL = 0x1F
CTRL_REG6_XL = 0x20
CTRL_REG7_XL = 0x21

i2c.writeto_mem(addr_ag, CTRL_REG1_G, b'\x60')  #0110 0000
i2c.writeto_mem(addr_ag, CTRL_REG2_G, b'\x00')  #0000 0000
i2c.writeto_mem(addr_ag, CTRL_REG3_G, b'\x41')  #0100 0001
i2c.writeto_mem(addr_ag, ORIENT_CFG_G, b'\x40') #0100 0000
i2c.writeto_mem(addr_ag, CTRL_REG4, b'\x3a')    #0011 1010
i2c.writeto_mem(addr_ag, CTRL_REG5_XL, b'\x38') #0011 1000
i2c.writeto_mem(addr_ag, CTRL_REG6_XL, b'\x3c') #0011 1100
i2c.writeto_mem(addr_ag, CTRL_REG7_XL, b'\x00') #0000 0000

CTRL_REG1_M = 0x20
CTRL_REG2_M = 0x21
CTRL_REG3_M = 0x22
CTRL_REG4_M = 0x23
CTRL_REG5_M = 0x24

i2c.writeto_mem(addr_m, CTRL_REG1_M, b'\x14')  #0001 0100
i2c.writeto_mem(addr_m, CTRL_REG2_M, b'\x40')  #0100 0000
i2c.writeto_mem(addr_m, CTRL_REG3_M, b'\x00')  #0000 0000
i2c.writeto_mem(addr_m, CTRL_REG4_M, b'\x0c')  #0000 1100
i2c.writeto_mem(addr_m, CTRL_REG5_M, b'\x00')  #0000 0000

while True:

    print("=======================================================")
    #statusレジスタのアドレス0x27の下から1ビット目が加速度のデータ更新状態
    status = i2c.readfrom_mem(addr_ag, 0x27, 1)
    if status and 0x01 != 0x00:
        #加速度センサのデータの読み込み
        data = b''
        for i in range(0x28, 0x2e):
            data += i2c.readfrom_mem(addr_ag, i, 1)
        x = ustruct.unpack("<h", data[0:2])[0]
        y = ustruct.unpack("<h", data[2:4])[0]
        z = ustruct.unpack("<h", data[4:6])[0]
        x = x * 0.000244
        y = y * 0.000244
        z = z * 0.000244
        print("AccX:" + str(x) + " AccY:" + str(y) + " AccZ:" + str(z))
        #姿勢角の算出
        phi = math.atan(-y/z)
        thete = math.atan(x/math.sqrt(y*y+z*z))
        print("phi:" + str(phi) + " thete:" + str(thete))
    
    #statusレジスタのアドレス0x27の下から2ビット目がジャイロのデータ更新状態
    if status and 0x02 != 0x00:
        data = b''
        for i in range(0x18, 0x1e):
            data += i2c.readfrom_mem(addr_ag, i, 1)
        x = ustruct.unpack("<h", data[0:2])[0]
        y = ustruct.unpack("<h", data[2:4])[0]
        z = ustruct.unpack("<h", data[4:6])[0]
        x = x * 0.00875
        y = y * 0.00875
        z = z * 0.00875
        print("GyrX:" + str(x) + " GyrY:" + str(y) + " GyrZ:" + str(z))
    
    status = i2c.readfrom_mem(addr_m, 0x27, 1)
    #statusレジスタのアドレス0x27の下から4ビット目が磁気のデータ更新状態
    if status and 0x08 != 0x00:
        data = i2c.readfrom_mem(addr_m, 0x28, 6)
        x = ustruct.unpack("<h", data[0:2])[0]
        y = ustruct.unpack("<h", data[2:4])[0]
        z = ustruct.unpack("<h", data[4:6])[0]
        x = x * 0.00043
        y = y * 0.00043
        z = z * 0.00043
        print("MagX:" + str(x) + " MagY:" + str(y) + " MagZ:" + str(z))

    time.sleep(1)