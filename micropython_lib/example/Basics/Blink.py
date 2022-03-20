
# initialize the digital pin as an output.
led = Pin(25, Pin.OUT)


while True:
    led.on()        # turn the LED on (HIGH is the voltage level)
    delay(1000)     # wait for a second
    led.off()       # turn the LED off by making the voltage LOW
    delay(1000)     # wait for a second