#!/usr/bin/python
"""
This module add some function to monitor the Raspberrry health
- File Usage
- Space used on SD Card and USB Key
The collected info are sent to a database
"""

import subprocess


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
    sd_size = int(o.split(' ')[5])
    if debug_print:
        print ("Size %d" % sd_size)

    cmd = ['df', '-m', '--output=avail', '/']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    sd_avail = int(o.split(' ')[1])
    if debug_print:
        print ("Avail %d" % sd_avail)

    cmd = ['df', '-m', '--output=used', '/']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    sd_used = int(o.split(' ')[2])
    if debug_print:
        print ("Used %d" %sd_used)

    cmd = ['df', '-m', '--output=pcent', '/']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    o = o.split(' ')[1]
    sd_pcent = int(o.split('%')[0])
    if debug_print:
        print ("Percent %d" % sd_pcent)

    cmd = ['du', '-sm', '/var/lib/influxdb/meta']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    o = o.split('/')
    o = o[0]
    sd_meta = int(o)
    if debug_print:
        print ("Influxdb meta Used %d" % sd_meta)

    cmd = ['du', '-sm', '/home/pi/influxdb/data']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    o = o.split('/')
    o = o[0]
    sd_data = int(o)
    if debug_print:
        print ("Influxdb data Used %d" % sd_data)

    cmd = ['du', '-sm', '/home/pi/influxdb/wal']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    o = o.split('/')
    o = o[0]
    sd_wal = int(o)
    if debug_print:
        print ("Influxdb wal Used %d" % sd_wal)

    if debug_print:
        print "**** USB Key Usage ****"

    cmd = ['df', '-m', '--output=size', '/home/pi/USB_KEY']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    usb_size = int(o.split(' ')[5])
    if debug_print:
        print ("Size %d" % usb_size)

    cmd = ['df', '-m', '--output=avail', '/home/pi/USB_KEY']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    usb_avail = int(o.split(' ')[1])
    if debug_print:
        print ("Avail %d" %usb_avail)

    cmd = ['df', '-m', '--output=used', '/home/pi/USB_KEY']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    usb_used = int(o.split(' ')[5])
    if debug_print:
        print ("Used %d" % usb_used)

    cmd = ['df', '-m', '--output=pcent', '/home/pi/USB_KEY']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    o = o.split(' ')[2]
    usb_pcent = int(o.split('%')[0])
    if debug_print:
        print ("Percent %d" % usb_pcent)

    cmd = ['du', '-sm', '/home/pi/USB_KEY/influxdb_backup']
    proc = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    o, e = proc.communicate()
    o = o.split('\t')
    o = o[0]
    db_backup = int(o)
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
    debug_print = True

    json_body = rpi_sysinfo()

    if debug_print:
        print json_body
    else:
        write_to_dbase(json_body, "sysinfo")
