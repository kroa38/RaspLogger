#!/bin/sh
echo "##############################################################################"
echo "Start of script..............................................................."
echo "##############################################################################"
echo "Package update ..............................................................."
apt-get update & wait $!
echo "##############################################################################"
echo "Package upgrade ..............................................................."
apt-get upgrade -y  & wait $!
echo "##############################################################################"
echo "install git..................................................................."
apt-get -y install git & wait $!
echo "##############################################################################"
echo "install apt-transport-https..................................................."
apt-get -y install apt-transport-https & wait $!
echo "##############################################################################"
echo "install bluetooth............................................................."
apt-get -y install bluetooth & wait $!
echo "##############################################################################"
echo "install libbluetooth-dev......................................................"
apt-get -y install libbluetooth-dev & wait $!
echo "##############################################################################"
echo "install python-dev............................................................"
apt-get -y install python-dev & wait $!
echo "##############################################################################"
echo "install python-pip............................................................"
apt-get -y install python-pip & wait $!
echo "##############################################################################"
echo "install curl.................................................................."
apt-get -y install curl & wait $!
echo "##############################################################################"
echo ".............................................................................."
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -  & wait $!
echo ".............................................................................."
echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list  
echo ".............................................................................."
echo "##############################################################################"
echo "Package update" & wait $!
apt-get update & wait $!
echo "##############################################################################"
echo "install influxdb.............................................................."
apt-get -y install influxdb & wait $!
echo "##############################################################################"
echo ".............INSTALL PYTHON LIBRARY .........................................."
echo "##############################################################################"
echo "install pybluez..............................................................."
pip install pybluez & wait $!
echo "##############################################################################"
echo "install beacontools..........................................................."
pip install beacontools & wait $!
echo "##############################################################################"
echo "install influxdb.............................................................."
pip install influxdb & wait $!
echo "##############################################################################"
echo "install oauth2client.........................................................."
pip install oauth2client & wait $!
echo "##############################################################################"
echo "install RPi.GPIO.............................................................."
pip install RPi.GPIO & wait $!
echo "##############################################################################"
echo "install requests.............................................................."
pip install requests & wait $!
echo "##############################################################################"
echo "install twitter..............................................................."
pip install twitter & wait $!
echo "##############################################################################"
echo "install smbus................................................................."
pip install smbus & wait $!
echo "##############################################################################"
echo "install google-api-python-client.............................................."
pip install google-api-python-client & wait $!
echo "##############################################################################"
echo "install google-auth..........................................................."
pip install google-auth & wait $!
echo "##############################################################################"
echo "install google-auth-httplib2.................................................."
pip install google-auth-httplib2 & wait $!
echo "##############################################################################"
echo "install uritemplate..........................................................."
pip install uritemplate & wait $!
echo "##############################################################################"
echo "install urllib3..............................................................."
pip install urllib3 & wait $!
echo "##############################################################################"
echo "install gspread..............................................................."
pip install gspread & wait $!
echo "##############################################################################"
echo "install urllib2..............................................................."
pip install urllib2 & wait $!
echo "##############################################################################"
echo "install httplib2.............................................................."
pip install httplib2 & wait $!
echo "##############################################################################"
echo "install pyserial.............................................................."
pip install pyserial & wait $!
echo "##############################################################################"
echo "Copy timezone file ..........................................................."
cp -f /home/pi/RaspLogger/etc/timezone /etc/.
echo "##############################################################################"
echo "Create influxdb directory Wal and Data
mkdir /home/pi/influxdb
mkdir /home/pi/influxdb/data
mkdir /home/pi/influxdb/wal
chown -R influxdb:influxdb /home/pi/influxdb
echo "##############################################################################"
echo "End of script................................................................."
echo "##############################################################################"
