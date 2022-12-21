
# Crontab file for root
```
> sudo crontab -e

#add this lines:

# check Influxdb and Bluetooth every hour
0 * * * * bash /home/pi/RaspLogger/health_check.sh > /dev/null 2>&1
# start ibeacon script at reboot
@reboot bash /home/pi/RaspLogger/ibeacon_scanner.sh > /dev/null 2>&1
# Log reboot date time to database
@reboot bash /home/pi/RaspLogger/reboot_info.sh > /dev/null 2>&1

#update ip every hour
1 * * * * bash /home/pi/RaspLogger/ip_update.sh > /dev/null 2>&1
#backup database every Saturday at 04h05min
5 4 * * 6 bash /home/pi/RaspLogger/db_backup.sh > /dev/null 2>&1
#reboot Rpi evry week Saturday at 02h02min
2 2 * * 6 bash /home/pi/RaspLogger/reboot_rpi.sh > /dev/null 2>&1

```

# Crontab file for user 'pi'        

```
> crontab -e pi

#add this lines:

#-----------------------------------------------------------------------

#linky every 15 minutes
*/15 * * * * bash /home/pi/RaspLogger/linky.sh > /dev/null 2>&1

#air quality update every hour
17 * * * * bash /home/pi/RaspLogger/air_quality.sh > /dev/null 2>&1

#check memory every hour
4 * * * * bash /home/pi/RaspLogger/memory_info.sh > /dev/null 2>&1

#-----------------------------------------------------------------------

#Close the editor:
```
As soon as this file will close, the Cron daemon will install the new crontab
verify that a crontab file exists for a user
```
sudo ls -l /var/spool/cron/crontabs

-rw------- 1 pi   crontab 1702 30 juin  22:02 pi
-rw------- 1 root crontab  201 30 juin  21:57 root
```
