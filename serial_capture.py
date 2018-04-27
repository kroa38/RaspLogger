#!/usr/bin/env python

import time
import serial       # install pyserial package

# configure the serial connections (the parameters differs on the device you are connecting to)
# don't forget to add group for the user of tty : ex : add group toto tty
# The script capture the data from the ERDF counter at 1200 bauds
# it extract the value of HCHC and HCHP and take care to the CRC.
# take car about the port ttyAM0 or ttyS0


def capture_linky():
    """
    :return: dictionnary
    """

    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=1200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.SEVENBITS
    )

    if(ser.is_open):
        ser.close()
        ser.open()

    nb_line = 11      # la trame historique contient 11 lignes de champs
    HCHC = 3          # HCHC est a la ligne 3
    HCHP = 4          # HPHC est a la ligne 4
    LENGHT_HCHC = 14  # nb de caracteres a retenir
    LENGHT_HCHP = 14  # nb de caracteres
    IMAX = 7
    LENGHT_IMAX = 8

    linky = {}
    linky["HP"] = 0
    linky["HC"] = 0
    linky["IMAX"] = 0

    for i in range(0,10) :    # try 10 times

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

            if len(words) == nb_line:

                checksum = 0
                for i in range(LENGHT_HCHP):
                    checksum = (checksum + ord(words[HCHP][i])) & 0x3F
                checksum = (checksum + 0x20) % 256
                if chr(checksum) != words[HCHP][LENGHT_HCHP+1]:
                    checksum = False
                else:
                    linky["HP"] = int(words[HCHP].split()[1])

                checksum = 0
                for i in range(LENGHT_HCHC):
                    checksum = (checksum + ord(words[HCHC][i])) & 0x3F
                checksum = (checksum + 0x20) % 256
                if chr(checksum) != words[HCHC][LENGHT_HCHC+1]:
                    checksum = False
                else:
                    linky["HC"] = int(words[HCHC].split()[1])

                checksum = 0
                for i in range(LENGHT_IMAX):
                    checksum = (checksum + ord(words[IMAX][i])) & 0x3F
                checksum = (checksum + 0x20) % 256
                if chr(checksum) != words[IMAX][LENGHT_IMAX+1]:
                    checksum = False
                else:
                    linky["IMAX"] = int(words[IMAX].split()[1])

                if checksum :
                    break
    return linky









