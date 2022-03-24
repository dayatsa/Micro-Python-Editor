# initialize the PIR sensor pin as an input:
pir_sensor = Pin(0, Pin.IN)

while True:
    # read the state of the PIR value:
    pir_state = pir_sensor.value()

    # check if the PIR detect motion. If it is, the pir_state is HIGH:
    if pir_state:
        print("Motion detected")
    else:
        print("..")

    # delay in between reads for stability
    delay(100)