# initialize temperature sensor on adc pin.
temp_sensor = LM35(26)


while True:
    # read celcius temperature 
    temp_celcius = temp_sensor.read_celcius()
    # read fahrenheit temperature 
    temp_fahrenheit = temp_sensor.read_fahrenheit()
    # read kelvin temperature 
    temp_kelvin = temp_sensor.read_kelvin()

    # print out the value you read:
    print("Temperature: {:.2f} C, {:.2f} F, {:.2f} K".format(temp_celcius, temp_fahrenheit, temp_kelvin))
    delay(500) # delay in between reads for stability