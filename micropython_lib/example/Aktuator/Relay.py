
# initialize the Relay pin as an output:
relay = Pin(0, Pin.OUT)

while True:
    # turn relay ON, relay is active LOW
    relay.off()
    # delay for 1000 microseconds
    delay(1000) 

    # turn relay OFF
    relay.on()
    # delay for 1000 microseconds
    delay(1000) 