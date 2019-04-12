'''
Parse data from BLE Sensor to Json dictionnaries
'''

import sys
from datetime import datetime
import time
#import DS1338
from beacontools import BeaconScanner,IBeaconFilter
from influxdb import InfluxDBClient


def callback(bt_addr, rssi, packet, additional_info):
    ble_data = "rssi,%d,%s" % (rssi, packet)
    json_body = set_json(ble_data)
    client = InfluxDBClient('localhost', 8086, 'root', 'root', 'example')
    client.create_database('example')
    client.write_points(json_body)


def set_json(ble_data):

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

    print ("date time is %s" % time_string )
    print ("rssi = %d" % rssi)
    print ("dbm_1m = %d" % dbm_1m)
    print ("sensor type = %d" % sensor_type)
    print ("sensor number = %d" % sensor_number)
    print ("batt_voltage = %.3f" % batt_voltage)
    print ("bme_temp = %.1f" % bme_temp)
    print ("altitude = %d" % altitude)
    print ("pressure = %.1f" % pressure)
    print ("gaz = %d" % gaz)
    print ("temperature = %.1f" % temperature)
    print ("humidity = %.2f" % humidity)

    json_body = [
        {

            "measurement": "Battery",
            "tags": {
                "Sensor": sensor_number,
                "Location": location
            },
            "time": time_string,
            "fields": {
                "value": batt_voltage
            }
        },
        {
            "measurement": "Temperature",
            "tags": {
                "Sensor": sensor_number,
                "Location": location
            },
            "time": time_string,
            "fields": {
                "value": temperature
            }
        },
        {
            "measurement": "Humidity",
            "tags": {
                "Sensor": sensor_number,
                "Location": location
            },
            "time": time_string,
            "fields": {
                "value": humidity
            }
        },

        {
            "measurement": "Pressure",
            "tags": {
                "Sensor": sensor_number,
                "Location": location
            },
            "time": time_string,
            "fields": {
                "value": pressure
            }
        }


    ]
    return json_body


scanner = BeaconScanner(callback, device_filter=IBeaconFilter(uuid="2332a4c2"))
scanner.start()

while True:
    time.sleep(5)
scanner.stop()
