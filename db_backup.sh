
#!/bin/bash
# Backup database to USB key flash disk
# first test if usb key is mounted
# then make a secure copy

if [ 'mount | grep USB_KEY & wait $!' ]
then
    echo "USB key is present"
    echo "start backup"
    influxd backup -portable /home/pi/USB_KEY/tmp/ > db_backup.log
    if [ 'cat db_backup.log | grep "backup complete" ' ]
    then
        echo "influxd backup ok"
        if [ -d "/home/pi/USB_KEY/influxdb_backup" ]
        then
            echo "remove and rename directory"
            rm -rf /home/pi/USB_KEY/influxdb_backup
            mv /home/pi/USB_KEY/tmp /home/pi/USB_KEY/influxdb_backup
        else
            echo "move only directory"
            mv /home/pi/USB_KEY/tmp /home/pi/USB_KEY/influxdb_backup
        fi
    else
        echo "influd backup fail"
    fi
echo "USB Key not present ! "
fi
