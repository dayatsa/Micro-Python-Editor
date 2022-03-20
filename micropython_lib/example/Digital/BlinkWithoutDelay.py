
# initialize the digital pin as an output.
led_pin = Pin(25, Pin.OUT)
# Variables will change:
led_state = False
# will store last time LED was updated
previous_millis = 0
# interval at which to blink (milliseconds)
interval = 1000


while True:
    # read the milisecond counter
    current_millis = millis()
    
    if current_millis - previous_millis >= interval:
        # save the last time you blinked the LED
        previous_millis = current_millis
    
        # if the LED is off turn it on and vice-versa:
        if (led_state == False):
            led_state = True
            led.on()
        else:
            led_state = False
            led.off()
        