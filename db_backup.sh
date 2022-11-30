#!/bin/bash
# Backup database to DB_BACKUP directory
# make sure dir home/pi/DB_BACKUP exist
# make sure dir home/pi/DB_BACKUP/tmp exist
# or modify this script to create and test theses dir...

echo "***********************************"
echo "         BACKUP DATABASE           "
echo "***********************************"

echo "USB key is present"
echo "start backup"
influxd backup -portable /home/pi/DB_BACKUP/tmp/ > db_backup.log
if [ 'cat db_backup.log | grep "backup complete" ' ]
then
    echo "influxd backup ok"
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
    echo "influd backup fail"
fi

echo "END BACKUP"
echo "***********************************"

