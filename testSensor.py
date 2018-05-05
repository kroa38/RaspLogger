#!/usr/bin/env python

import sys
import time
from sensor_read import *
from cloudscope import *


count = 0
handle = init_sensor()

while count != 12*3:
    print "-----------------------------------------------------"
    data = read_sensor_humidity(handle)
    mesg =  str(" Temperature = %.1f , Humidity = %.1f" % (data["Hum_Temp"], data["Hum %"]))
    count += 1
    tweet_message(mesg)
    time.sleep(300)
handle.close()


