
# initialize the pushbutton pin as an input:
button = Pin(1, Pin.IN)
# initialize the LED pin as an output:
led = Pin(25, Pin.OUT)

while True:
    # read the state of the pushbutton value:
    button_state = button.value()

    # check if the pushbutton is pressed. If it is, the buttonState is HIGH:
    if button_state:
        # turn LED on:
        led.on()
    else:
        # turn LED off:
        led.off()