reader = MFRC522(spi_id=0, sck=2, mosi=3, miso=4, rst=0, cs=1)
 
print("Bring TAG closer...")
print("")


while True:
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL)
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            print("CARD ID: "+str(card))
    delay(500) 