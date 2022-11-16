#!/bin/sh

#this script check if database is responding
#if yes then check also bluetooth
#else reboot rapsberry-pi
# errors are logged into error.log file


#create a variable for collecting the nb of beacon
val=0

#query with curl command to retrieve the Atmo database 

val=`curl -s -G http://localhost:8086/query --data-urlencode "u=username" --data-urlencode "p=password" --data-urlencode "q=SHOW DATABASES" | grep Atmo`

wait

# compare the value with 4 be
if [ $val ]
then
    echo "$(date) : Influxdb is alive"
    /bin/bash /home/pi/RaspLogger/check_bluetooth.sh
    wait
else
    echo "$(date) : InfluxdB access error => Reboot" >>/home/pi/RaspLogger/error.log
    /bin/bash /home/pi/RaspLogger/reboot_rpi.sh
fi
