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
fi

# Check if database is ok
data=`curl -s -G http://localhost:8086/query --data-urlencode "u=username" --data-urlencode "p=password" --data-urlencode "db=Sens>

if [ $data ]
then
    echo "database ok"
    # Check if we have receive 4 bluetooth beacon since 2h
    val=`curl -s -G http://localhost:8086/query --data-urlencode "u=username" --data-urlencode "p=password" --data-urlencode "db=S>
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
fi

# if there is only one error we reboot the rapsberry-py
if [ $err_py -a $err_db -a $err_bt ];
then
    echo "reboot"
    /bin/bash /home/pi/RaspLogger/reboot_rpi.sh
else
    echo "You are in good health !"
fi
