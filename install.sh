#!/bin/sh
echo "Start of script........................................."
echo "Package update and upgrade"
apt-get update & wait $!
echo "........................................................"
apt-get upgrade -y  & wait $!
echo "........................................................"
echo "Install usefull Package"
apt-get install git & wait $!
echo "........................................................"
apt-get install python-pip & wait $!
echo "........................................................"
apt-get install libbluetooth-dev & wait $!
echo "........................................................"
apt-get install apt-transport-https & wait $!
echo "........................................................"
apt-get install curl & wait $!
echo "........................................................"
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -  & wait $!
echo "........................................................"
echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
echo "........................................................"
echo "Package update" & wait $!
echo "........................................................"
apt-get update & wait $!
echo "........................................................"
apt-get install influxdb & wait $!
echo "........................................................"
echo "........................................................"
echo "........................................................"
echo "Install usefull Python library"
echo "........................................................"
echo "........................................................"
echo "........................................................"
pip install pybluez & wait $!
echo "........................................................"
pip install beacontools & wait $!
echo "........................................................"
pip install influxdb & wait $!
echo "........................................................"
pip install oauth2client & wait $!
echo "........................................................"
pip install RPi.GPIO & wait $!
echo "........................................................"
pip install requests & wait $!
echo "........................................................"
pip install twitter & wait $!
echo "........................................................"
pip install smbus & wait $!
echo "........................................................"
pip install gspread & wait $!
echo "........................................................"
pip install urllib2 & wait $!
echo "........................................................"
pip install httplib2 & wait $!
echo "........................................................"
pip install pyserial & wait $!
echo "........................................................"
pip install google-api-python-client & wait $!
echo "........................................................"
echo "End of script"
