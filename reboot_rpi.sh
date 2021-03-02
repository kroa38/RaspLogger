#!/bin/bash

sudo service influxdb stop
sudo killall -9 python3 & wait $!
sudo shutdown -r now & wait $!

