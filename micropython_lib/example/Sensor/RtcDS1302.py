# initialize pin on DS1302
# CONNECTIONS:
# DS1302 CLK/SCLK --> 5
# DS1302 DAT/DIO --> 18
# DS1302 RST/CS --> 19
# DS1302 VCC --> 3.3v - 5v
# DS1302 GND --> GND
ds = DS1302(clk=5, dio=18, cs=19)

# returns the current datetime.
# [Year, month, day, hour, minute, second]
print(ds.read_date_time()) 

ds.set_date_time([2022, 2, 1, 12, 0, 0]) # set datetime.
print(ds.read_date_time())

while True:
    # read date and time on rtc
    date_time = ds.read_date_time()

    # print date time
    print("{}-{}-{} {}:{}:{}".format(date_time[0], 
                                    date_time[1], 
                                    date_time[2], 
                                    date_time[3], 
                                    date_time[4], 
                                    date_time[5]))
    delay(1000) # delay 1000 microsecond