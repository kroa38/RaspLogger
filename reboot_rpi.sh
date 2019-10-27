#!/bin/bash

sudo service influxdb stop
sudo killall -9 python & wait $!
sudo shutdown -r now & wait $!

