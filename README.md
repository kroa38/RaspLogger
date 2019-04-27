# Install a Fresh Raspbian image.

1)  
Download a fresh Raspbian image( i recommand the light version)   
https://www.raspberrypi.org/downloads/raspbian/  

2)  
Format your SD card with this software from Tuxera :  
https://www.sdcard.org/  

3)  
Write the image on the the SD card :   
https://sourceforge.net/projects/win32diskimager/

# WIFI and SSH 

I recommand to read this blog for the first install on the Raspberry Pi Zero :  

How to setup Wifi  
How to setup SSH  

https://medium.com/@aallan/setting-up-a-headless-raspberry-pi-zero-3ded0b83f274  

# __Boot and start Install script__

After boot start the install script :
This script install packages and library for Python.  

```
sudo sh ./install.sh
```

# __TimeZone, UART, I2C__

Use the 'raspi-config' command to setup your timezone !

For I2C and UART edit the file /boot/config.txt and add this two
parameters:

```
#enable I2C
dtparam=i2c_arm=on

#Enable UART
enable_uart=1
```

Edit also the file /boot/cmdline.txt and suppress the text :
```
console=serial0,115200  
```

# __InfluxdB on RAPSBERRY PI__

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
- 2) Edit File influxdb.conf  

```
sudo nano /etc/influxdb/influxdb.conf
```
- 3) Uncomment the lines below  

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
