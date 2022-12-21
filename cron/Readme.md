
# Crontab file for root
```
> sudo crontab -e

#add this lines:

# check Influxdb and Bluetooth every hour
0 * * * * bash /home/pi/RaspLogger/health_check.sh > /dev/null 2>&1

# start ibeacon script at reboot
@reboot bash /home/pi/RaspLogger/ibeacon_scanner.sh > /dev/null 2>&1
# log date time at reboot
@reboot bash /home/pi/RaspLogger/reboot_info.sh > /dev/null 2>&1

# update IP address every hour
1 * * * * bash /home/pi/RaspLogger/ip_update.sh > /dev/null 2>&1
```

# Crontab file for user 'pi'        

```
> crontab -e pi

#add this lines:

#-----------------------------------------------------------------------

# update linky avery 15min
*/15 * * * * bash /home/pi/RaspLogger/linky.sh > /dev/null 2>&1
# update air quality every hour
17 * * * * bash /home/pi/RaspLogger/air_quality.sh > /dev/null 2>&1

# if you want to tweet your IP address uncomment the line below
#@reboot bash /home/pi/RaspLogger/tweet_ip.sh > /dev/null 2>&1

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
