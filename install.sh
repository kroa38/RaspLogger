#!/bin/bash
echo "##############################################################################"
echo "Start of script..............................................................."
echo "##############################################################################"
echo "Package update ..............................................................."
apt-get update & process_id=$!
wait $process_id
echo "##############################################################################"
echo "Package upgrade ..............................................................."
apt-get upgrade -y  & process_id=$!
wait $process_id
echo "##############################################################################"
echo "install git..................................................................."
apt-get -y install git & process_id=$!
wait $process_id
echo "##############################################################################"
echo "install apt-transport-https..................................................."
apt-get -y install apt-transport-https & process_id=$!
wait $process_id
echo "##############################################################################"
echo "install bluetooth............................................................."
apt-get -y install bluetooth & process_id=$!
wait $process_id
echo "##############################################################################"
echo "install libbluetooth-dev......................................................"
apt-get -y install libbluetooth-dev & process_id=$!
wait $process_id
echo "##############################################################################"
echo "install python-dev............................................................"
apt-get -y install python-dev & process_id=$!
wait $process_id
echo "##############################################################################"
echo "install python-pip............................................................"
apt-get -y install python-pip & process_id=$!
wait $process_id
echo "##############################################################################"
echo "install curl.................................................................."
apt-get -y install curl & process_id=$!
wait $process_id
echo "##############################################################################"
echo ".............................................................................."
curl -sL https://repos.influxdata.com/influxdb.key | apt-key add -  & process_id=$!
wait $process_id
echo ".............................................................................."
echo "deb https://repos.influxdata.com/debian stretch stable" | tee /etc/apt/sources.list.d/influxdb.list
echo ".............................................................................."
echo "##############################################################################"
echo "Package update"
apt-get update & process_id=$!
wait $process_id
echo "##############################################################################"
echo "install influxdb.............................................................."
apt-get -y install influxdb & process_id=$!
wait $process_id
echo "##############################################################################"
echo ".............INSTALL PYTHON PACKAGES .........................................."
echo "##############################################################################"
pip install -r requirements.txt & process_id=$!
wait $process_id
echo "##############################################################################"
echo ".............SYSTEM TIPS AND TRICKS .........................................."
echo "##############################################################################"
echo "##############################################################################"
echo "Copy timezone file ..........................................................."
cp -rf /home/pi/RaspLogger/etc/timezone /etc/.
echo "##############################################################################"
echo "Copy cron file ..........................................................."
cp -rf /home/pi/RaspLogger/cron/root /var/spool/cron/crontabs/.
echo "##############################################################################"
echo "Restart cron service .................... ......................................."
service cron restart & process_id=$!
wait $process_id
echo "##############################################################################"
echo "Copy sshd_config file ..........................................................."
cp -rf /home/pi/RaspLogger/ssh/sshd_config /etc/ssh/.
echo "##############################################################################"
echo "Reload SSH service ..........................................................."
systemctl reload ssh.service & process_id=$!
echo "##############################################################################"
echo "Copy influxdb.conf file ..........................................................."
cp -rf /home/pi/RaspLogger/influxdb/influxdb.conf /etc/influxdb/.
echo "##############################################################################"
echo "Create influxdb directory Wal,Data,Meta"
if [ ! -d /home/pi/USB_KEY/influxdb ]
then
    mkdir /home/pi/USB_KEY/influxdb
fi

if [ ! -d /home/pi/USB_KEY/influxdb/meta ]
then
   mkdir /home/pi/USB_KEY/influxdb/meta
fi

if [ ! -d /home/pi/USB_KEY/influxdb/data ]
then
    mkdir /home/pi/USB_KEY/influxdb/data
fi

if [ ! -d /home/pi/USB_KEY/influxdb/wal ]
then
    mkdir /home/pi/USB_KEY/influxdb/wal
fi
chown -R influxdb:influxdb /home/pi/influxdb
echo "##############################################################################"
echo "Create Users in database......................................................"
if [ -f /home/pi/RaspLogger/credential.txt ]
then
	python util_dbase.py & process_id=$!
	wait $process_id
else
	echo "No credential file  : Database Users not created"
fi
echo "##############################################################################"
echo "Restart Influxdb......................................................"
service influxdb restart & process_id=$!
wait $process_id
echo "##############################################################################"
echo "Enable Influxdb......................................................"
systemctl enable influxdb.service & process_id=$!
wait $process_id
echo "##############################################################################"
echo "End of script................................................................."
echo "##############################################################################"

