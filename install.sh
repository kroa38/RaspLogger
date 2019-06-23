#!/bin/sh
echo "##############################################################################"
echo "Start of script..............................................................."
echo "##############################################################################"
echo "Package update ..............................................................."
sudo apt-get update & wait $!
echo "##############################################################################"
echo "Package upgrade ..............................................................."
sudo apt-get upgrade -y  & wait $!
echo "##############################################################################"
echo "install git..................................................................."
sudo apt-get -y install git & wait $!
echo "##############################################################################"
echo "install apt-transport-https..................................................."
sudo apt-get -y install apt-transport-https & wait $!
echo "##############################################################################"
echo "install bluetooth............................................................."
sudo apt-get -y install bluetooth & wait $!
echo "##############################################################################"
echo "install libbluetooth-dev......................................................"
sudo apt-get -y install libbluetooth-dev & wait $!
echo "##############################################################################"
echo "install python-dev............................................................"
sudo apt-get -y install python-dev & wait $!
echo "##############################################################################"
echo "install python-pip............................................................"
sudo apt-get -y install python-pip & wait $!
echo "##############################################################################"
echo "install curl.................................................................."
sudo apt-get -y install curl & wait $!
echo "##############################################################################"
echo ".............................................................................."
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -  & wait $!
echo ".............................................................................."
echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list  
echo ".............................................................................."
echo "##############################################################################"
echo "Package update" & wait $!
sudo apt-get update & wait $!
echo "##############################################################################"
echo "install influxdb.............................................................."
sudo apt-get -y install influxdb & wait $!
echo "##############################################################################"
echo ".............INSTALL PYTHON PACKAGES .........................................."
echo "##############################################################################"
sudo pip install -r requirements.txt & wait $!
echo "##############################################################################"
echo ".............SYSTEM TIPS AND TRICKS .........................................."
echo "##############################################################################"
echo "##############################################################################"
echo "Copy timezone file ..........................................................."
sudo p -f /home/pi/RaspLogger/etc/timezone /etc/.
echo "##############################################################################"
echo "Copy cron file ..........................................................."
sudo cp -rf /home/pi/RaspLogger/cron/root /var/spool/cron/crontabs/.
echo "##############################################################################"
echo "Restart cron service .................... ......................................."
sudo service cron restart & wait $!
echo "##############################################################################"
echo "Copy sshd_config file ..........................................................."
cp -rf /home/pi/RaspLogger/ssh/sshd_config /etc/ssh/.
echo "##############################################################################"
echo "Reload SSH service ..........................................................."
sudo systemctl reload ssh.service & wait $!
echo "##############################################################################"
echo "Copy influxdb.conf file ..........................................................."
sudo cp -rf /home/pi/RaspLogger/influxdb/influxdb.conf /etc/influxdb/.
echo "##############################################################################"
echo "Create influxdb directory Wal,Data,Meta
if [ ! -d /home/pi/USB_KEY/influxdb ]
then
    sudo mkdir /home/pi/USB_KEY/influxdb
fi

if [ ! -d /home/pi/USB_KEY/influxdb/meta ]
then
   sudo mkdir /home/pi/USB_KEY/influxdb/meta
fi

if [ ! -d /home/pi/USB_KEY/influxdb/data ]
then
    sudo mkdir /home/pi/USB_KEY/influxdb/data
fi

if [ ! -d /home/pi/USB_KEY/influxdb/wal ]
then
    sudo mkdir /home/pi/USB_KEY/influxdb/wal
fi
chown -R influxdb:influxdb /home/pi/influxdb
echo "##############################################################################"
echo "Create Users in database......................................................"
if [ -f /home/pi/RaspLogger/credential.txt ]
then
	sudo python util_dbase.py & wait $!
else
	echo "No credential file  : Database Users not created"
fi
echo "##############################################################################"
echo "Restart Influxdb......................................................"
sudo service influxdb restart & wait $!
echo "##############################################################################"
echo "Enable Influxdb......................................................"
sudo systemctl enable influxdb.service & wait $!
echo "##############################################################################"
echo "End of script................................................................."
echo "##############################################################################"
