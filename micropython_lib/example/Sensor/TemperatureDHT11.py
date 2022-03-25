# initialize DHT sensor on adc pin.
dht = DHT11(26)


while True:
    # read temperature 
    temperature = dht.read_temperature()
    # read humidity
    humidity = dht.read_humidity()

    # print out the value you read:
    print("Temperature: {:.2f} C, Humidity: {:.2f}".format(temperature, humidity))
    delay(500) # delay in between reads for stability