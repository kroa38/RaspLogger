# __Raspberrypi Zero-W with data Sensor and InfluxdB__

 Collect data from Bluetooth Sensor (Temp, Hum, Press,Gaz,Batt Level)  
 Collect Linky Smart Energy Counter  (Uart)
 Collect Air Quality (grad data from web)  
 Collect I/O Event  (door event or other)
 Store data to InfluxdB  

 -> Display data from Grafana Cloud service

## Bootcode.bin

The Rpi can't boot directly from USB but this little bootcode can help you.

Format an SD card as FAT32 and copy on the latest bootcode.bin. The SD card must be 
present in the Raspberry Pi for it to boot. Once bootcode.bin is loaded from the SD card,
the Raspberry Pi continues booting using USB host mode.

link for bootcode.bin
https://github.com/raspberrypi/firmware/raw/master/boot/bootcode.bin


## Install a Fresh Raspbian Lite image.(USB SSD disk)

Use Raspberry Pi Imager for creating the system on your USB SSD Disk    
Choose OS :   **Raspebrry Pi OS Lite(32-bit)**
This version use less than 400Mb of storage

Use **Option** to set Wifi, SSH, and Account Password


## UART, I2C

To enable I2C and UART edit the file /boot/config.txt and add this two
parameters:

```
> sudo vi /boot/config.txt

#enable I2C
dtparam=i2c_arm=on

#Enable UART
enable_uart=1
```
## Edit cmdline.txt

Edit also the file /boot/cmdline.txt and suppress the text :
The Uart port is dedicated for Linky data acquisition
```
console=serial0,115200  
```

## Reboot

Plug the SD card into the raspberry-pi, connect the USB SSD disk
to the port and reboot (wait almost 3min before login)

login:

```
> ssh pi@192.168.1.xx
```
use your password for login

## Configure TimeZone, Language

Set time-zone and language
```
> sudo raspi-config
```

## Update and upgrade system:

This can be very long ......:confused:

```
> sudo apt-get update  
> sudo apt-get upgrade  
```

## Install Git
```
> sudo apt-get install git -y
```

## Github : clone **rasplogger** project
```
> cd $home
> sudo git clone https://github.com/kroa38/RaspLogger.git
> cd Rasplogger/
```

## Add new Packages

After boot install new packages.
```
> sudo apt-get install $(cat pkglist.txt) -y
```
## Use PIP to install new Python Packages

```
> sudo pip install -r requirements
```

## Database Backup

The script **db_backup.sh** automatically backup the entire database to the USB Key  
The script run once per day by using **Cron**.

---


## __InfluxdB on RAPSBERRY PI__


- 1) Install  

```
> sudo apt-get install apt-transport-https  
> sudo apt-get install curl  
> curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -  
> echo "deb https://repos.influxdata.com/debian bullseye stable" | sudo tee /etc/apt/sources.list.d/influxdb.list     
> sudo apt-get install influxdb  
```

- 2) Edit File influxdb.conf  

```
> sudo nano /etc/influxdb/influxdb.conf
```
- 3) Modify data and http section  

```
[http]
  # Determines whether HTTP endpoint is enabled.
  enabled = true

  # The bind address used by the HTTP service.
  bind-address = ":8086"

  # Determines whether user authentication is enabled over HTTP/HTTPS.
  auth-enabled = false

```
- 4) Start service  

```
> sudo service influxdb restart
```
- 5) Enable service  

```
> systemctl enable influxdb.service
```
- 6) or if you encounter an unmask error  


 ```
> systemctl unmask influxdb.service
> systemctl enable influxdb.service
```
- 7) Check if service is running  

```
> systemctl status influxdb.service
```

- 7) Init the databases and users  

This create the 3 databases and one admin user and one reader user  

```
> python util_dbase.py
```
Important !!
option "auth-enabled = false" must be declared into  /etc/influxdb/influxdb.conf  
and be changed to "auth-enabled = true" after !

- 8) Export database into CSV format

Use influx_inspect command  
```  
influx_inspect export -database ibeacon -datadir "/home/pi/USB_KEY/influxdb/data/" -waldir "/home/pi/USB_KEY/influxdb/wal/" -out "/home/pi/USB_KEY/tmp/ibeacon.csv"
```  
- 9) Import database  

Drop the previous database  

Influx CLI :  
```
 Drop database ibeacon  
```
After that exit influx cli and use influx command to import the database  
```
influx -username 'admin' -password 'aP45YhN45' -import -path "/home/pi/USB_KEY/tmp/ibeacon2.csv"  
```

After this import you must re-allow grants privileges for users and databases:  

 ex :  
```
grant all on "ibeacon" to "admin"  
grant read on "ibeacon" to "reader"  
```
