#!/bin/bash

# Check if ibeacon_scanner is running
ib=`ps -aux | grep -c 'python3 /home/pi/RaspLogger/ibeacon_scanner.py'`

err=0
err_py=0
err_db=0
err_bt=0

if [ $ib -eq 2 ];
then
    echo "ibeacon is running"
else
    echo "ibeacon is not running"
    err_py=1
    echo "$(date) : Ibeacon_scanner not runnig => Reboot" >> /home/pi/RaspLogger/error.log
fi

# Check if database is ok


# Check if database is ok
data=`curl -s -G http://localhost:8086/query --data-urlencode "u=reader" --data-urlencode "p=123456" --data-urlencode "db=Sensors" --data-urlencode "q=SELECT count(*) FROM \"Temperature\" WHERE (\"Sensor Type\" = '1' AND \"Sensor Number\" = '1' AND time > now() -2h)" | grep 'Temperature'`

if [ $data ]
then
    echo "database ok"
    # Check if we have receive 4 bluetooth beacon since 2h
    val=`curl -s -G http://localhost:8086/query --data-urlencode "u=reader" --data-urlencode "p=123456" --data-urlencode "db=Sensors" --data-urlencode "q=SELECT count(*) FROM \"Temperature\" WHERE (\"Sensor Type\" = '1' AND \"Sensor Number\" = '1' AND time > now() -2h)"  | jq -r '.results[0].series[0].values[0][1] | tonumber'`
    if [ $val -lt 4 ]
    then
        echo "bluetooth error"
        err_bt=1
        echo "$(date) : Bluetooth Error => Reboot" >> /home/pi/RaspLogger/error.log
    else
        echo "bluetooth ok"
    fi

else
    echo "database not ok"
    err_db=1
    echo " $(date) : Database not running => Reboot" >> /home/pi/RaspLogger/error.log
fi

if [ $err_py -gt 0 ] || [ $err_db -gt 0 ] || [ $err_bt -gt 0 ]
then
 echo 'Au moins une erreur trouvée'
 /home/pi/RaspLogger/reboot_rpi.sh
else
 echo 'Aucune  erreur trouvée'
fi

