# digital pin 2 has a pushbutton attached to it. make the pushbutton's pin an input:
push_button = Pin(2, Pin.IN)


while True:
    # read the input PIN
    button_state = push_button.value()
    # print out the state of the button:
    print(button_state)
    delay(500) # delay in between reads for stability