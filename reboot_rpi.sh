#!/bin/bash
# Launch this script for rebooting the Rpi (sudo mode)

service influxdb stop
wait
killall -9 python3
wait
shutdown -r now
