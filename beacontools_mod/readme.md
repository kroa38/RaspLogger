This is a fork of beacontool package : https://pypi.org/project/beacontools/

This two file add device filter on the prefix of the uuid.
and simplify the packet string.

Replace this two files in the beacontools package directory  

```
type : python -m site  
```
The package is located in a 'dist-packages' or 'site-packages' directory   

```
sys.path = [
    '/home/pi/RaspLogger',  
    '/usr/lib/python2.7',  
    '/usr/lib/python2.7/plat-arm-linux-gnueabihf',  
    '/usr/lib/python2.7/lib-tk',  
    '/usr/lib/python2.7/lib-old',  
    '/usr/lib/python2.7/lib-dynload',  
    '/usr/local/lib/python2.7/dist-packages',  
    '/usr/lib/python2.7/dist-packages',      <--- Beacontools was installed here for me.  
]  
USER_BASE: '/root/.local' (doesn't exist)  
USER_SITE: '/root/.local/lib/python2.7/site-packages' (doesn't exist)  
ENABLE_USER_SITE: True  

```
  

