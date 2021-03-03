#!/bin/bash

# Backup database to USB SSD flash disk
# First test if Usb SSD is mounted
# then make a secure copy

echo "***********************************"
echo "         BACKUP DATABASE           "
echo "***********************************"
if [ 'mount | grep USB_SSD & wait $!' ]
then
    echo "USB SSD is present"
    echo "start backup"
    influxd backup -portable /home/pi/USB_SSD/tmp/ > db_backup.log
    if [ 'cat db_backup.log | grep "backup complete" ' ]
    then
        echo "influxd backup ok"
        if [ -d "/home/pi/USB_SSD/influxdb_backup" ]
        then
            echo "remove and rename directory"
            rm -rf /home/pi/USB_SSD/influxdb_backup
            mv /home/pi/USB_SSD/tmp /home/pi/USB_SSD/influxdb_backup
        else
            echo "move only directory"
            mv /home/pi/USB_SSD/tmp /home/pi/USB_SSD/influxdb_backup
        fi
    else
        echo "influd backup fail"
    fi
else
echo "USB SSD not present ! "
fi
echo "END BACKUP"
echo "***********************************"
