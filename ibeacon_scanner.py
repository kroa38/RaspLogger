#!/usr/bin/env python
import sys
import time
from datetime import datetime
#import DS1338
#from timefunc import TimeFunc
from beacontools import BeaconScanner,IBeaconFilter
from influxdb import InfluxDBClient
from util_dbase import write_to_dbase

#rtc = DS1338.DS1338(1, 0x68)

def callback(bt_addr, rssi, packet, additional_info):
    '''
    :param bt_addr:
    :param rssi:
    :param packet:
    :param additional_info:
    :return:
    '''
    global al
    global debug_ble
    bl = [1234567890,"hello"]
    bl[0] = int(time.time())
    bl[1] = str(packet).split(',')
    bl[1] = bl[1][3]
    bl[1] = bl[1][9:13]
    # if capture > 3s or sensor id is different.
    if (bl[0]-al[0] > 3) or (bl[1] != al[1]):
        al[0] = bl[0]
        al[1] = bl[1]
        ble_data = str("rssi,%d,%s" % (rssi, packet))
        jsony_body = set_json(ble_data)
        if debug_ble:
            print jsony_body
        else:
            write_to_dbase(jsony_body)

def set_json(ble_data):
    '''
    :param ble_data:
    :return:
    '''
    blueduino_sensor_type = 1
    csv_reader = ble_data.split(',')
    uuid = csv_reader[5]
    sensor_type = int(uuid[9:11], 0)
    rssi = 0
    dbm_1m = 0
    sensor_number = 0
    batt_voltage = 0.0
    bme_temp = 0.0
    altitude = 0
    pressure = 0.0
    gaz = 0
    temperature = 0.0
    humidity = 0.0
    now = datetime.now()
    localtime = time.localtime()
    if localtime.tm_isdst:
        time_string = now.strftime("%Y-%m-%dT%H:%M:%S")
    else:
        time_string = now.strftime("%Y-%m-%dT%H:%M:%S")

    if sensor_type == blueduino_sensor_type:
        rssi = int(csv_reader[1], 0)
        dbm_1m = int(csv_reader[3], 0)
        uuid_prefix = uuid[:8]
        sensor_number = int(uuid[11:13], 0)
        batt_voltage = float(int(uuid[14:18], 16))/1000
        bme_temp = float(int(uuid[20:23], 16))
        if bme_temp < 2000:
            bme_temp = (bme_temp-1000.0)/10.0
        else:
            bme_temp = (bme_temp - 2000.0)/(-10.0)
        altitude = int(uuid[24:28], 16)
        pressure = float(int(uuid[28:32], 16))/10
        gaz = int(uuid[32:36], 16)
        temperature = float(int(csv_reader[7], 0))
        if temperature < 2000:
            temperature = (temperature-1000.0)/10.0
        else:
            temperature = (temperature - 2000.0)/(-10.0)
        humidity = float(int(csv_reader[9], 0))/100

    if sensor_number == 1:
        location = "Chambre_Parents"
    else:
        location = "None"

    # print ("date time is %s" % time_string )
    # print ("rssi = %d" % rssi)
    # print ("dbm_1m = %d" % dbm_1m)
    # print ("sensor type = %d" % sensor_type)
    # print ("sensor number = %d" % sensor_number)
    # print ("batt_voltage = %.3f" % batt_voltage)
    # print ("bme_temp = %.1f" % bme_temp)
    # print ("altitude = %d" % altitude)
    # print ("pressure = %.1f" % pressure)
    # print ("gaz = %d" % gaz)
    # print ("temperature = %.1f" % temperature)
    # print ("humidity = %.2f" % humidity)

    jsony_body = [
        {
            "measurement": "Rssi",
            "tags": {
                "Sensor Number": sensor_number,
                "Sensor Type": sensor_type,
                "Location": location
            },
            "fields": {
                "value": rssi
            }
        },
         {
            "measurement": "Battery",
            "tags": {
                "Sensor Number": sensor_number,
                "Sensor Type": sensor_type,
                "Location": location
            },
            "fields": {
                "value": batt_voltage
            }
        },
        {
            "measurement": "Temperature",
            "tags": {
                "Sensor Number": sensor_number,
                "Sensor Type": sensor_type,
                "Location": location
            },
            "fields": {
                "value": temperature
            }
        },
        {
            "measurement": "Humidity",
            "tags": {
                "Sensor Number": sensor_number,
                "Sensor Type": sensor_type,
                "Location": location
            },
            "fields": {
                "value": humidity
            }
        },
        {
            "measurement": "Altitude",
            "tags": {
                "Sensor Number": sensor_number,
                "Sensor Type": sensor_type,
                "Location": location
            },
            "fields": {
                "value": altitude
            }
        },
        {
            "measurement": "Pressure",
            "tags": {
                "Sensor Number": sensor_number,
                "Sensor Type": sensor_type,
                "Location": location
            },
            "fields": {
                "value": pressure
            }
        },
        {
            "measurement": "Gaz",
            "tags": {
                "Sensor Number": sensor_number,
                "Sensor Type": sensor_type,
                "Location": location
            },
            "fields": {
                "value": gaz
            }
        }

    ]
    return jsony_body


if __name__ == "__main__":
    '''
    Start this script in background with : " sudo beacontest.py & "
    '''
    debug_ble = False
    al = [1555087419, "9999"]
    scanner = BeaconScanner(callback,device_filter=IBeaconFilter(uuid="2332a4c2"))
    scanner.start()
    while True:
        time.sleep(5)
    #scanner.stop()
