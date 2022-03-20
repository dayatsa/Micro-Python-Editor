# initialize the adc pin.
pin = Pin(26)
adc = ADC(pin)


while True:
    # read the input on analog pin 26:
    analog_value = adc.read_u16()
    # print out the value you read:
    print(analog_value)
    delay(500) # delay in between reads for stability