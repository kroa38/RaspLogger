# __Raspberrypi Zero-W with data Sensor and InfluxdB__

 Collect data from Bluetooth Sensor (Temp, Hum, Press,Gaz,Batt Level)  
 Collect Linky Smart Energy Counter  (Uart)
 Collect Air Quality (grad data from web)  
 Collect I/O Event  (door event or other)
 Store data to InfluxdB  

 -> Display data from Grafana Cloud service

## Install a Fresh Raspbian Lite image.

Use Raspberry Pi Imager for creating the SD card    
Choose OS :   **Raspebrry Pi OS Lite(32-bit)**

## Setup WiFi
Create a file : "wpa_supplicant.conf"  into the "boot" partition
insert the lines below and replace COUNTRY, SSID and PASSWORD by yours  

```
country=COUNTRY
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
network={
       ssid="SSID"
       psk="PASSWORD"
       key_mgmt=WPA-PSK
    }
```
## Setup SSH  

Create an empty file named "ssh" into the "boot" partition  
```
> sudo touch ssh
```
I recommend to read this good blog for the first install on the Raspberry Pi Zero :
https://medium.com/@aallan/setting-up-a-headless-raspberry-pi-zero-3ded0b83f274  

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
```
console=serial0,115200  
```
Example of lines
```
dwc_otg.lpm_enable=0 console=tty1 root=PARTUUID=dab3eba4-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait  
```

## Reboot

Plug the SD card into the raspberry-pi and reboot

login:

```
ssh pi@192.168.1.xx
```
use 'raspberry' as password

## TimeZone, Language

Set time-zone and language
```
sudo raspi-config

```

## Expand filesystem
Expand the root partition to use the full space of the SD card  
```
> sudo raspi-config
-> advance option
-> expand filesystem

When prompted reboot you raspberrypi
```

## Update and upgrade system:

This can be very long ......:confused:

```
> sudo apt-get update  
> sudo apt-get upgrade  
```

## Start the Install Script

After boot start the install script :
This script install all necessary packages.  

```
sudo su
sh ./install.sh
```
## Github : clone **rasplogger** project
```
> cd /home/pi
> sudo git clone https://github.com/kroa38/RaspLogger.git
```

## External SSD Disk

I recommend to save the database content to another location.  
I use a external SSD(128Gb M2 Type SATA) plugged to the Micro USB port of the Rpi Zero.  
This one is auto-mounted by adding a line on the fstab file :


Create a directory inside home directory
```
> mkdir /home/USB_SSD  
```

--> Plug the SSD on the usb port  and type the command.
```
> blkid  

/dev/sda1: UUID="b5292053-8e93-4e3d-b298-136ef6fee196" TYPE="ext4" PARTUUID="c20396db-01"


```
Note the **PARTUUID** of the usb ssd and then add a line
to the **/etc/fstab** file to mount the key at boot  

```
PARTUUID=11c4ae0c-05 /home/pi/USB_SSD ext4 rw,user,auto,exec,discard,noatime  0      1  
```

Now the USB SSD is auto-mounted into the new partition in '/home/USB_KEY'

## Database Backup

The script **db_backup.sh** automatically backup the entire database to the USB Key  
The script run once per day by using **Cron**.

---

# **SECURITY**
---

## __Configure SSH__

Good info from :
https://linux-audit.com/audit-and-harden-your-ssh-configuration/

i strongly recommand to setup this configuration for **/etc/ssh/sshd_config** file  

```
IgnoreRhosts yes  
PermitEmptyPasswords no  
MaxAuthTries 3  
PermitRootLogin no  
MaxSessions 1
```

Are you connected to the remote with SSH ?  
Yes: type this command to reload configuration  
```
systemctl reload ssh.service  
```

Check intrusion and attempt  
```
systemctl status ssh.service  
```
## __PAM__

Secure your ssh connexion by adding delay on failure on the file 'sshd' in pam.d
```
sudo nano /etc/pam.d/sshd
```
add the line below to add a delay of 10s on failure

```
auth  optional  pam_faildelay.so  delay=10000000
```


## __SYSLOG__



due to the huge amount of attack on ssh port i recommand
to remove auth log.

```
sudo nano /etc/rsyslog.conf
```
and comment the line :
```
#auth,authpriv.*               /var/log/auth.log
```
restart syslog
```
 sudo service rsyslog restart
```

## __InfluxdB on RAPSBERRY PI__

 Prefered Version: 1.7.6-1

- 1) Update, Upgrade, Install  

```
sudo apt-get update  
sudo apt-get upgrade  
sudo apt-get install apt-transport-https  
sudo apt-get install curl  
curl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -  
echo "deb https://repos.influxdata.com/debian stretch stable" | sudo tee /etc/apt/sources.list.d/influxdb.list     
sudo apt-get update  
sudo apt-get install influxdb  
```

switch to the directory /home/pi and type:
```
mkdir influxdb
chown influxdb:influxdb influxdb  
cd influxdb  
mkdir data  
chown influxdb:influxdb data
mkdir wal  
chown influxdb:influxdb wal
```

- 2) Edit File influxdb.conf  

```
sudo nano /etc/influxdb/influxdb.conf
```
- 3) modify data and http section  

```
[data]
  dir = "/home/pi/influxdb/data"
  wal-dir = "/home/pi/influxdb/wal"
  wal-fsync-delay = "5s"

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
sudo service influxdb restart
```
- 5) Enable service  

```
systemctl enable influxdb.service
```
- 6) or if you encounter an unmask error  


 ```
systemctl unmask influxdb.service
systemctl enable influxdb.service
```
- 7) Check if service is running  

```
systemctl status influxdb.service
```

- 7) Init the databases and users  

This create the 3 databases and one admin user and one reader user  

```
python util_dbase.py
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
