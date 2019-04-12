import sys
import time
import datetime
import DS1338
from timefunc import TimeFunc
from beacontools import BeaconScanner, IBeaconFilter

rtc = DS1338.DS1338(1, 0x68)

def callback(bt_addr, rssi, packet, additional_info):
    print("%s,rssi,%d,%s" % (rtc.read_datetime(),rssi, packet))
# scan for all iBeacon advertisements from beacons with the specified uuid
scanner = BeaconScanner(callback, device_filter=IBeaconFilter(uuid="2332a4c2"))

scanner.start()

while True:
    time.sleep(5)
scanner.stop()
