import time

def delay(ms):
    time.sleep_ms(ms)

def millis():
    return time.ticks_ms()