#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import time
import site
from datetime import datetime
# import DS1338
# from timefunc import TimeFunc
from beacontools import BeaconScanner, IBeaconFilter, BluetoothAddressType
from influxdb import InfluxDBClient
from util_dbase import write_to_dbase

"""
Bluetooth sensor
Type 1 = T°,Hum, Press, Alt
Type 2 = T°,Hum, Gaz, Alt, Lum, With ST BLUENRG-2 CHipset
"""

# rtc = DS1338.DS1338(1, 0x68)


def callback(bt_addr, rssi, packet, additional_info):
    '''
    :param bt_addr:
    :param rssi:
    :param packet:
    :param additional_info:
    :return:
    '''
    global al
    global debug_print
    bl = [1234567890, "hello"]
    bl[0] = int(time.time())
    bl[1] = str(packet).split(',')
    bl[1] = bl[1][3]
    bl[1] = bl[1][9:13]
    # if capture > 10s or sensor id is different.
    if (bl[0] - al[0] > 10) or (bl[1] != al[1]):
        al[0] = bl[0]
        al[1] = bl[1]
        ble_data = str("rssi,%d,%s" % (rssi, packet))
        jsony_body = set_json(ble_data)
        if debug_print:
            print(jsony_body)
        else:
            write_to_dbase(jsony_body, "Sensors")


def set_json(ble_data):
    '''
    :param ble_data:
    :return:
    '''
    csv_reader = ble_data.split(',')
    uuid = csv_reader[5]
    type = int(uuid[9:11])
    id = int(uuid[11:13])
    mydict = {}
    points = []
    meas = "none"
    Location = 'None'
    
    if type == 1:
        mydict["Rssi"] = int(csv_reader[1], 0)
        mydict["Battery"] = float(int(uuid[14:18], 16)) / 1000
        mydict["Altitude"] = int(uuid[24:28], 16)
        mydict["Pressure"] = float(int(uuid[28:32], 16)) / 10
        mydict["Gaz"] = int(uuid[32:36], 16)
        mydict["Humidity"] = float(int(csv_reader[9], 0)) / 100
        mydict["Temperature"] = float(int(csv_reader[7], 0))
        if mydict["Temperature"] < 2000:
            mydict["Temperature"] = (mydict["Temperature"] - 1000) / 10
        else:
            mydict["Temperature"] = (2000 - mydict["Temperature"]) / 10

        Location = id


    if type == 2:
        mydict["Rssi"] = int(csv_reader[1], 0)
        mydict["Battery"] = float(int(uuid[14:18], 16)) / 1000
        mydict["Luminosity"] = int(uuid[19:23], 16)
        mydict["Pressure"] = float(int(uuid[28:32], 16)) / 10
        mydict["Gaz"] = int(uuid[32:36], 16)
        mydict["Humidity"] = float(int(csv_reader[9], 0)) / 100
        mydict["Temperature"] = float(int(csv_reader[7], 0))
        if mydict["Temperature"] > 1000:
            mydict["Temperature"] = (mydict["Temperature"] - 1100) / 10
            mydict["ILS"] = 1
        else:
            mydict["Temperature"] = (mydict["Temperature"] - 100) / 10
            mydict["ILS"] = 0

        Location = id

    for meas in mydict:
        point = {
            "measurement": meas,
            "tags": {
                "Sensor Number": id,
                "Sensor Type": type,
                "Location": Location
            },
            "fields": {
                "value": mydict[meas]
            }
        }
        points.append(point)

    return points


if __name__ == "__main__":
    '''
    Start this script in background with : " sudo beacontest.py & "
    '''
    debug_print = True
    site.ENABLE_USER_SITE = False
    al = [1555087419, "9999"]
    scanner = BeaconScanner(callback,
                        device_filter=IBeaconFilter(uuid="2332a4c2"),
                        scan_parameters={"address_type": BluetoothAddressType.PUBLIC}
                        )
    scanner.start()
    while True:
        time.sleep(5)
    # scanner.stop()
