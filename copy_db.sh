#!/bin/bash
# make a copy of the database to a USB Key
# Test if USB key is mounted in /home/pi/USB_KEY
# install this script in cron and start it every day.

if [ 'mount | grep USB_KEY' ]
then
   cp -rf /home/pi/influxdb/ /home/pi/USB_KEY/.
fi
