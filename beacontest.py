import sys
import time
from datetime import datetime
#import DS1338
from timefunc import TimeFunc
from beacontools import BeaconScanner,IBeaconFilter

#rtc = DS1338.DS1338(1, 0x68)

def callback(bt_addr, rssi, packet, additional_info):
    global al
    bl = [1234567890,"hello"]
    bl[0] = int(time.time())
    bl[1] = str(packet).split(',')
    bl[1] = bl[1][3]
    bl[1] = bl[1][9:13]
    if (bl[0]-al[0] > 3) or (bl[1] != al[1]):
        al[0] = bl[0]
        al[1] = bl[1]
        #print  lst_cmp 
        print("rssi,%d,%s" % (rssi, packet))


al=[1555087419, "9999"]
scanner = BeaconScanner(callback,device_filter=IBeaconFilter(uuid="2332a4c2"))
scanner.start()
while True:
    time.sleep(5)
scanner.stop()
