WIDTH  = 128                                            # oled display width
HEIGHT = 64                                             # oled display height
 
i2c = I2C(0, scl=Pin(9), sda=Pin(8))       # Init I2C using pins GP8 & GP9 (default I2C0 pins)
print("I2C Address      : "+hex(i2c.scan()[0]).upper()) # Display device address
print("I2C Configuration: "+str(i2c))                   # Display I2C config
 

oled = SSD1306_I2C(WIDTH, HEIGHT, i2c)                  # Init oled display
counter = 0


while True:
    # add counter
    counter += 1
    print(counter)
 
    # Clear the oled display in case it has junk on it.
    oled.fill(0)       
    
    # Add some text on column=6, row=8
    oled.text("Counter: ", 6, 8)
    # print counter value
    oled.text(str(counter), 95, 8)
    # print hello world
    oled.text("Hello World", 20, 32)
 
    # Finally update the oled display so the image & text is displayed
    oled.show()
    delay(1000)