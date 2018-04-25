#!/usr/bin/env python

import time
import serial       # install pyserial package

# configure the serial connections (the parameters differs on the device you are connecting to)
# don't forget to add group for the user of tty : ex : add group toto tty
# The script capture the data from the ERDF counter at 1200 bauds
# it extract the value of HCHC and HCHP and take care to the CRC.
# take car about the port ttyAM0 or ttyS0

ser = serial.Serial(
    port='/dev/ttyS0',
    baudrate=1200,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.SEVENBITS
)

if(ser.is_open):
    print("port is  opened!")
    ser.close()
    ser.open()
    print (" port was closed and opened again")

nb_line = 11      # la trame historique contient 11 lignes de champs
HCHC = 3          # HCHC est a la ligne 3
HCHP = 4          # HPHC est a la ligne 4
LENGHT_HCHC = 14  # nb de caracteres a retenir
LENGHT_HCHP = 14  # nb de caracteres
IMAX = 7
LENGHT_IMAX = 8
checksum = True

#tmp = ser.read(122)
#print (tmp)
#ser.close()
#exit()

while True :

        time.sleep(2)
        out = ''
        tmp = ''

        while ser.inWaiting() > 0:
                tmp = ser.read(1)
                if tmp == chr(2):
                      break
        tmp = ser.read()            # avoid chr(2)
        while ser.inWaiting() > 0:
                tmp = ser.read(1)
                if tmp != chr(3):
                        out += tmp
                else:
                      break
        words = out.split(chr(10))
        #print words
        #print len(words)
        if len(words) == nb_line:
                print words[HCHP]
                sum = 0
                for i in range(LENGHT_HCHP):
                        sum = (sum + ord(words[HCHP][i])) & 0x3F
                sum = (sum + 0x20) % 256
                if chr(sum) != words[HCHP][LENGHT_HCHP+1]:
			checksum = FALSE
                else:
                        value = int(words[HCHP].split()[1])
                        print value

                sum = 0

                print words[HCHC]
                for i in range(LENGHT_HCHC):
                        sum = (sum + ord(words[HCHC][i])) & 0x3F
                sum = (sum + 0x20) % 256
                if chr(sum) != words[HCHC][LENGHT_HCHC+1]:
                        checksum = False
                else:
                        value = int(words[HCHC].split()[1])
                        print value

                sum = 0
                print words[IMAX]
                for i in range(LENGHT_IMAX):
                        sum = (sum + ord(words[IMAX][i])) & 0x3F
                sum = (sum + 0x20) % 256
                if chr(sum) != words[IMAX][LENGHT_IMAX+1]:
                        checksum = False
                else:
                        value = int(words[IMAX].split()[1])
                        print value

                if checksum == True:
                        break;









