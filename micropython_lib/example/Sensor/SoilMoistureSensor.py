# initialize Soil Moisture Sensor on adc pin.
soil_sensor = SoilMoistureSensor(26)


while True:
    # read raw data
    raw = soil_sensor.read()

    # read data percentage
    percentage = soil_sensor.read_percentage()

    # print out the value you read:
    print("Moisture: {:.2f}, {:.2f}%".format(raw, percentage))
    delay(500) # delay in between reads for stability