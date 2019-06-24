#!/usr/bin/python
"""
This module add some function to monitor the Raspberrry health
- File Usage
- Space used on SD Card and USB Key
The collected info are sent to a database
"""
from util_dbase import write_to_dbase
import subprocess
import re

def rpi_sysinfo():
    """

    :return: json data
    """
    global debug_print

    if debug_print:
        print "**** SD Card Usage ****"

    cmd = ['df', '-m', '--output=size', '/']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    try:
        sd_size = int(re.findall('\d+',o)[1]) 
    except:
        sd_size = 0
    if debug_print:
        print ("Size %d" % sd_size)

    cmd = ['df', '-m', '--output=avail', '/']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    try:
        sd_avail = int(re.findall('\d+',o)[0]) 
    except:
        sd_avail = 0
    if debug_print:
        print ("Avail %d" % sd_avail)

    cmd = ['df', '-m', '--output=used', '/']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    try:
        sd_used = int(re.findall('\d+',o)[0]) 
    except:
        sd_used = 0
    if debug_print:
        print ("Used %d" %sd_used)

    cmd = ['df', '-m', '--output=pcent', '/']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    o = o.split(' ')[1]
    try:
        sd_pcent = int(re.findall('\d+',o)[0])
    except:
        sd_pcent = 0
    if debug_print:
        print ("Percent %d" % sd_pcent)




    cmd = ['du', '-sm', '/home/pi/USB_KEY/influxdb/meta']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    try:
        sd_meta = int(re.findall('\d+',o)[0])
    except:
        sd_meta = 0
    if debug_print:
        print ("Influxdb meta Used %d" % sd_meta)

    cmd = ['du', '-sm', '/home/pi/USB_KEY/influxdb/data']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    try:
        sd_data = int(re.findall('\d+',o)[0])
    except:
        sd_data = 0
    if debug_print:
        print ("Influxdb data Used %d" % sd_data)

    cmd = ['du', '-sm', '/home/pi/USB_KEY/influxdb/wal']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    try:
        sd_wal = int(re.findall('\d+',o)[0])
    except:
        sd_wal = 0
    if debug_print:
        print ("Influxdb wal Used %d" % sd_wal)

    if debug_print:
        print "**** USB Key Usage ****"

    cmd = ['df', '-m', '--output=size', '/home/pi/USB_KEY']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    try:
        usb_size = int(re.findall('\d+',o)[1]) 
    except:
        usb_size = 0
    if debug_print:
        print ("Size %d" % usb_size)

    cmd = ['df', '-m', '--output=avail', '/home/pi/USB_KEY']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    try:
        usb_avail = int(re.findall('\d+',o)[0])
    except:
        usb_avail = 0
    if debug_print:
        print ("Avail %d" %usb_avail)

    cmd = ['df', '-m', '--output=used', '/home/pi/USB_KEY']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    try:
        usb_used = int(re.findall('\d+',o)[0])
    except:
        usb_used = 0
    if debug_print:
        print ("Used %d" % usb_used)

    cmd = ['df', '-m', '--output=pcent', '/home/pi/USB_KEY']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    try:
        usb_pcent = int(re.findall('\d+',o)[0])
    except:
        usb_pcent = 0
    if debug_print:
        print ("Percent %d" % usb_pcent)

    cmd = ['du', '-sm', '/home/pi/USB_KEY/influxdb_backup']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    try:
        db_backup = int(re.findall('\d+',o)[0])
    except:
        db_backup = 0
    if debug_print:
        print ("Influxdb backup size %d" % db_backup)

    json_body = [
        {"measurement": "SD_SIZE", "fields": {"value": sd_size}},
        {"measurement": "SD_AVAIL", "fields": {"value": sd_avail}},
        {"measurement": "SD_USED", "fields": {"value": sd_used}},
        {"measurement": "SD_PCENT", "fields": {"value": sd_pcent}},
        {"measurement": "SD_META", "fields": {"value": sd_meta}},
        {"measurement": "SD_DATA", "fields": {"value": sd_data}},
        {"measurement": "SD_WAL", "fields": {"value": sd_wal}},
        {"measurement": "USB_SIZE", "fields": {"value": usb_size}},
        {"measurement": "USB_AVAIL", "fields": {"value": usb_avail}},
        {"measurement": "USB_USED", "fields": {"value": usb_used}},
        {"measurement": "USB_PCENT", "fields": {"value": usb_pcent}},
        {"measurement": "DB_BACKUP", "fields": {"value": db_backup}}
    ]

    return json_body


if __name__ == "__main__":
    '''
    start this script with cron : sudo crontab -e 
    for example every day
    0 * * * * python /this_script.py > /dev/null 2>&1
    '''
    debug_print = False

    json_body = rpi_sysinfo()

    if debug_print:
        print json_body
    else:
        write_to_dbase(json_body, "sysinfo")
