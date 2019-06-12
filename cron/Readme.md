Copy and replace the root file to /var/spool/cron/crontabs
```
cp -rf cron/root /var/spool/cron/crontabs/.
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
Update IP address to duckdns.org every 6 hours  
```
0 */6 * * * bash /home/pi/duckdns/duck.sh > /dev/null 2>&1  
```


