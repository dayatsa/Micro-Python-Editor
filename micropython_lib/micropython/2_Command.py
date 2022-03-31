import time
from machine import *

def delay(ms):
    time.sleep_ms(ms)

def millis():
    return time.ticks_ms()