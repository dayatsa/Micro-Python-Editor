from machine import ADC

class SoilMoistureSensor:
    def __init__(self, pin):
        self._pin = ADC(pin)
        self.MAX = 20000
        self.MIN = 65535
        self.READ_COUNTER = 50

    def read(self):
        raw = 0.0
        for i in range(self.READ_COUNTER):
            raw += self._pin.read_u16()
            delay(1)
        raw_average = raw/self.READ_COUNTER
        return raw_average

    def read_percentage(self):
        old_value = self.read()
        old_range = (self.MAX - self.MIN)  
        new_range = (100 - 0)  
        new_value = (((old_value - self.MIN) * new_range) / old_range) + 0
        if new_value > 100:
            new_value = 100
        return new_value
