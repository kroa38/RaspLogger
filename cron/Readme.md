Copy and replace the root file to /var/spool/cron/crontabs
```
sudo cp -rf cron/root /var/spool/cron/crontabs/.
sudo service cron reload
```

# CRON file for schedulling Linky capture 

Linky capture every 15 minutes     
```
*/15 * * * * bash /home/pi/RaspLogger/linky.sh hour > /dev/null 2>&1  
```
Linky capture every day at 23h59   
```
59 23 * * * bash /home/pi/RaspLogger/linky.sh day > /dev/null 2>&1  
```
Linky capture every sunday at 23h58  
```
58 23 * * 0 bash /home/pi/RaspLogger/linky.sh week > /dev/null 2>&1  
```
Linky capture every 1 of day month at 00h00.  
```
00 00 1 * * bash /home/pi/RaspLogger/linky.sh month > /dev/null 2>&1  
```
Linky capture every year 31 december at 23h56  
```
56 23 31 12 * bash /home/pi/RaspLogger/linky.sh year > /dev/null 2>&1  
```
Update IP address to duckdns.org every hours  
```
5 * * * * bash /home/pi/RaspLogger/ip_update.sh > /dev/null 2>&1  
```
Database backup every day at 01h12  
```
12 01 * * * bash /home/pi/RaspLogger/db_backup.sh > /dev/null 2>&1
```
Update system info on database every day at 1h20  
```
20 01 * * * bash /home/pi/RaspLogger/rpi_sysinfo.sh > /dev/null 2>&1
```
Start ibeacon scanner after reboot  
```
@reboot bash /home/pi/RaspLogger/ibeacon_scanner.sh > /dev/null 2>&1
```
tweet ip adress after reboot  
```
@reboot bash /home/pi/RaspLogger/tweet_ip.sh > /dev/null 2>&1
```
Restart raspberry pi evry sunday at 1h04  
```
04 01 * * 7 /sbin/shutdown -r now > /dev/null 2>&1
```


