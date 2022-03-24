
# initialize the digital pin as an output.
led = Pin(25, Pin.OUT)


while True:
    led.on()        # turn the LED on 
    delay(1000)     # wait for a second
    led.off()       # turn the LED off 
    delay(1000)     # wait for a second