#!/bin/bash
# Backup database

echo "Start db backup"
influxd backup -portable /home/pi/DB_BACKUP/tmp/ > /home/pi/RaspLogger/db_backup.log
if [ 'cat db_backup.log | grep "backup complete" ' ]
then
    echo "$(date) Influxd backup success " >> /home/pi/RaspLogger/event.log
    if [ -d "/home/pi/DB_BACKUP/influxdb_backup" ]
    then
        echo "remove and rename directory"
        rm -rf /home/pi/DB_BACKUP/influxdb_backup
        mv /home/pi/DB_BACKUP/tmp /home/pi/DB_BACKUP/influxdb_backup
    else
        echo "move only directory"
        mv /home/pi/DB_BACKUP/tmp /home/pi/DB_BACKUP/influxdb_backup
    fi
else
    echo " $(date) influd backup fail" >> /home/pi/RaspLogger/error.log
fi

echo "end backup"
