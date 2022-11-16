#!/bin/sh

#this script monitor into the db the number of  beacon  received
#each beacon is sent every 15min (4 per hour)
#if we don't receive during the last 2h more than 4 beacon
#it means bluetooth is stuck and then we restart bleutooth


#create a variable for collecting the nb of beacon
val=0

#curl command to retrieve the count value in json and parse it using jq
#we retrieve the nb of beacons received during last 2 hours
val =`curl -s -G http://localhost:8086/query --data-urlencode "u=name" --data-urlencode "p=password" --data-urlencode "db=Sensors" --data-urlencode "q=SELECT count(*) FROM \"Temperature\" WHERE (\"Sensor Type\" = '1' AND \"Sensor Number\" = '1' AND time > now() -5h)" | jq -r '.results[0].series[0].values[0][1] | tonumber'`

wait

# compare the value with 4 be
if [ $val -lt 4 ]
then
    echo "bluetooth is stuck:  Count =  $val"
    killall -9 python3 > /dev/null 2>&1
    wait
    echo "kill python"
    systemctl stop bluetooth.service > /dev/null 2>&1
    wait
    echo "stop bluetooth"
    systemctl enable bluetooth.service > /dev/null 2>&1
    wait
    echo "enable bluetooth"
    systemctl restart bluetooth.service > /dev/null 2>&1
    wait
    echo "restart bluetooth"
    python3 /home/pi/RaspLogger/ibeacon_scanner.py& > /dev/null 2>&1
    echo "restart ibeacon scanner"
else
    echo "bluetooth is alive:  Count =  $val"
fi
