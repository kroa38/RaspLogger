## Create a crontab file for user 'pi'        

```
> crontab -e pi

#add this lines:

#-----------------------------------------------------------------------

*/15 * * * * bash /home/pi/RaspLogger/linky.sh hour > /dev/null 2>&1
59 23 * * * bash /home/pi/RaspLogger/linky.sh day > /dev/null 2>&1
58 23 * * 0 bash /home/pi/RaspLogger/linky.sh week > /dev/null 2>&1
00 00 1 * * bash /home/pi/RaspLogger/linky.sh month > /dev/null 2>&1
56 23 31 12 * bash /home/pi/RaspLogger/linky.sh year > /dev/null 2>&1
17 * * * * bash /home/pi/RaspLogger/air_quality.sh > /dev/null 2>&1
21 */2 * * * bash /home/pi/RaspLogger/ip_update.sh > /dev/null 2>&1
#12 02 * * * bash /home/pi/RaspLogger/db_backup.sh > /dev/null 2>&1
#20 01 * * * bash /home/pi/RaspLogger/rpi_sysinfo.sh > /dev/null 2>&1
#reboot commented(sometimes raspberry pi freeze at reboot)
#5 3 * * 6 bash /home/pi/RaspLogger/reboot_pi.sh > /dev/null 2>&1
@reboot bash /home/pi/RaspLogger/ibeacon_scanner.sh > /dev/null 2>&1
@reboot bash /home/pi/RaspLogger/tweet_ip.sh > /dev/null 2>&1

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

