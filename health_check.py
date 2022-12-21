#!/bin/bash

# Check if ibeacon_scanner is running
ib=`ps -aux | grep -c 'python3 /home/pi/RaspLogger/ibeacon_scanner.py'`

if [ $ib -eq 2 ];
then
    echo "ibeacon is running"
else
    echo "ibeacon is not running"
    err_py=1
    echo "$(date) : Ibeacon_scanner not runnig => Reboot" >> /home/pi/RaspLogger/error.log
    /bin/bash /home/pi/RaspLogger/reboot_rpi.sh
    exit 1
fi

# Check if database is ok
data=`curl -s -G http://localhost:8086/query --data-urlencode "u=reader" --data-urlencode "p=123456" --data-urlencode "db=Sensors" --data-urlencode "q=SELECT count(*) FROM \"Temperature\" WHERE (\"Sensor Type\" = '1' AND \"Sensor Number\" = '1' AND time > now() -2h)" | grep 'Temperature'`

if [ $data ]
then
    echo "database ok"
    # Check if we have receive 4 bluetooth beacon since 2h
    val=`curl -s -G http://localhost:8086/query --data-urlencode "u=reader" --data-urlencode "p=123456" --data-urlencode "db=Sensors" --data-urlencode "q=SELECT count(*) FROM \"Temperature\" WHERE (\"Sensor Type\" = '1' AND \"Sensor Number\" = '1' AND time > now() -2h)" | jq -r '.results[0].series[0].values[0][1] | tonumber'`
    if [ $val -lt 4 ]
    then
        echo "bluetooth error"
        err_bt=1
        echo "$(date) : Ibeacon_scanner not runnig => Reboot" >> /home/pi/RaspLogger/error.log

    else
        echo "bluetooth ok"
    fi
else
    echo "database not ok"
    err_db=1
    echo " $(date) : Database not running => Reboot" >> /home/pi/RaspLogger/error.log      
    /bin/bash /home/pi/RaspLogger/reboot_rpi.sh
    exit 1  
fi

# if there is only one error we reboot the rapsberry-py
if [ $err_py -a $err_db -a $err_bt ];
then
    echo "reboot"
    /bin/bash /home/pi/RaspLogger/reboot_rpi.sh
    exit 1
else
    echo "You are in good health !"
fi
