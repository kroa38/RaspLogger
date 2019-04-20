#!/bin/sh
echo "Start of script..............................................................."
echo "Package update and upgrade...................................................."
apt-get update & wait $!
echo ".............................................................................."
apt-get upgrade -y  & wait $!
echo "install git..................................................................."
apt-get -y install git & wait $!
echo "install python................................................................"
apt-get -y install python-pip & wait $!
echo "install libbluetooth-dev......................................................"
apt-get -y install libbluetooth-dev & wait $!
echo "install python-dev............................................................"
apt-get -y install python-dev & wait $!
echo "install apt-transport-https..................................................."
apt-get -y install apt-transport-https & wait $!
echo "install curl.................................................................."
apt-get -y install curl & wait $!
echo ".............................................................................."
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -  & wait $!
echo ".............................................................................."
echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list
echo ".............................................................................."
echo "Package update" & wait $!
echo ".............................................................................."
apt-get update & wait $!
echo "install influxdb.............................................................."
apt-get -y install influxdb & wait $!
echo ".............................................................................."
echo ".............................................................................."
echo ".............START PIP INSTALLATION..........................................."
echo ".............................................................................."
echo "install pybluez..............................................................."
pip install pybluez & wait $!
echo "install beacontools..........................................................."
pip install beacontools & wait $!
echo "install influxdb.............................................................."
pip install influxdb & wait $!
echo "install oauth2client.........................................................."
pip install oauth2client & wait $!
echo "install RPi.GPIO.............................................................."
pip install RPi.GPIO & wait $!
echo "install requests.............................................................."
pip install requests & wait $!
echo "install twitter..............................................................."
pip install twitter & wait $!
echo "install smbus................................................................."
pip install smbus & wait $!
echo "install gspread..............................................................."
pip install gspread & wait $!
echo "install urllib2..............................................................."
pip install urllib2 & wait $!
echo "install httplib2.............................................................."
pip install httplib2 & wait $!
echo "install pyserial.............................................................."
pip install pyserial & wait $!
echo "install google-api-python-client.............................................."
pip install google-api-python-client & wait $!
echo ".............................................................................."
echo "End of script................................................................."
