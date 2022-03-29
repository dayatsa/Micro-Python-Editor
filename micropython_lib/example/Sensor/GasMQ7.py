# initialize the adc pin.
pin = Pin(26)
adc = ADC(pin)

RL = 1000
Ro = 830

while True:
    # read the input on analog pin 26:
    analog_value = adc.read_u16()
    
    # change adc value (0-65535) to voltage value (0-3.3 volt) 
    VRL = analog_value*3.30/65535
    print("VRL : " + str(VRL) + " volt")

    # find Rs value
    Rs = ( 3.30 * RL / VRL ) - RL
    print("Rs : " + str(Rs) + " Ohm");

    # ppm = 100 * ((rs/ro)^-1.53)
    ppm = 100 * pow(Rs / Ro,-1.53); 
    print("CO : " + str(ppm) + " ppm")
    
    print()
    delay(500) # delay in between reads for stability