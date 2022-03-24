from machine import ADC

class LM35:
    def __init__(self, pin):
        self.__temperature_pin = ADC(pin)
        self.__conversion_factor = 3.3 / (65535)
        self.READ_COUNTER = 50

    def read_celcius(self):
        raw = 0.0
        for i in range(self.READ_COUNTER):
            raw += self.__temperature_pin.read_u16()
            delay(1)
        raw_average = raw/self.READ_COUNTER
        convert_voltage = raw_average * self.__conversion_factor
        temp = convert_voltage / (10.0 / 1000)
        return temp

    def read_fahrenheit(self):
        temp_celcius = self.read_celcius()
        temp_fahrenheit = (temp_celcius * (9/5)) + 32
        return temp_fahrenheit

    def read_kelvin(self):
        return self.read_celcius() + 273.15