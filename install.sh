#!/bin/sh
echo "Start of script........................................."
echo "Package update and upgrade"
apt-get update
echo "........................................................"
apt-get upgrade
echo "........................................................"
echo "Install usefull Package"
apt-get install git
echo "........................................................"
apt-get install python-pip
echo "........................................................"
apt-get install libbluetooth-dev
echo "........................................................"
apt-get install apt-transport-https
echo "........................................................"
apt-get install curl
echo "........................................................"
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
echo "........................................................"
echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
echo "........................................................"
echo "Package update"
echo "........................................................"
apt-get update
echo "........................................................"
apt-get install influxdb
echo "........................................................"
echo "........................................................"
echo "........................................................"
echo "Install usefull Python library"
echo "........................................................"
echo "........................................................"
echo "........................................................"
pip install pybluez
echo "........................................................"
pip install beacontools
echo "........................................................"
pip install influxdb
echo "........................................................"
pip install oauth2client
echo "........................................................"
pip install RPi.GPIO
echo "........................................................"
pip install requests
echo "........................................................"
pip install twitter
echo "........................................................"
pip install smbus
echo "........................................................"
pip install gspread
echo "........................................................"
pip install urllib2
echo "........................................................"
pip install httplib2
echo "........................................................"
pip install pyserial
echo "........................................................"
pip install google-api-python-client
echo "........................................................"
echo "End of script"