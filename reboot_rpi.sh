#!/bin/bash

service influxdb stop
wait
killall -9 python3
wait
shutdown -r now
