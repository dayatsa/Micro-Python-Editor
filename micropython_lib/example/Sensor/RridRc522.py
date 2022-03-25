
from machine import I2C, Pin, SPI

sck = Pin(6, Pin.OUT)
mosi = Pin(7, Pin.OUT)
miso = Pin(4, Pin.OUT)
spi = SPI(0, baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
sda = Pin(5, Pin.OUT)
rst = Pin(22, Pin.OUT)

while True:
    # rdr = MFRC522(spi, sda, rst)
    rdr = MFRC522(spi=0,sck=6,miso=4,mosi=7,cs=5,rst=22)
    uid = ""
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            uid = ("0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3]))
            print(uid)