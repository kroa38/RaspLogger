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
    :return: dictionnary {'IINST': 410, 'HP': 213059463, 'IMAX': 90, 'HC': 123512034, 'PTEC': 'HC..', 'PAPP': 20165}
    """

    ser = serial.Serial(
        port='/dev/ttyS0',
        baudrate=1200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.SEVENBITS,
        timeout=1
    )

    if not (ser.is_open):
        ser.open()

    nb_line = 11      # la trame historique contient 11 lignes de champs
    HCHC = 3          # HCHC est a la ligne 3
    LENGHT_HCHC = 14  # nb de caracteres a retenir
    HCHP = 4          # HPHC est a la ligne 4
    LENGHT_HCHP = 14  # nb de caracteres
    PTEC = 5
    LENGHT_PTEC = 9
    IINST = 6
    LENGHT_IINST = 9
    IMAX = 7
    LENGHT_IMAX = 8
    PAPP = 8
    LENGHT_PAPP = 10

    linky = {}
    linky["HP"] = 0
    linky["HC"] = 0
    linky["PTEC"] = ''
    linky["IINST"] = 0
    linky["PAPP"] = 0
    linky["IMAX"] = 0

    tmp = ser.read(10)

    if len(tmp) == 10:

        for count in range(0,10) :    # try 10 times

                time.sleep(2)
                out = ''
                tmp = ''

                for loop in range(0,220):
                        tmp = ser.read(1)
                        if tmp == chr(2): # wait for STX
                            break
                tmp = ser.read()

                for loop in range(0, 220):
                        tmp = ser.read(1)
                        if tmp != chr(3): # ETX found
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
                    for i in range(LENGHT_PTEC):
                        checksum = (checksum + ord(words[PTEC][i])) & 0x3F
                    checksum = (checksum + 0x20) % 256
                    if chr(checksum) != words[PTEC][LENGHT_PTEC+1]:
                        checksum = False
                    else:
                        linky["PTEC"] = (words[PTEC].split()[1])[0,1]

                    checksum = 0
                    for i in range(LENGHT_IINST):
                        checksum = (checksum + ord(words[IINST][i])) & 0x3F
                    checksum = (checksum + 0x20) % 256
                    if chr(checksum) != words[IINST][LENGHT_IINST+1]:
                        checksum = False
                    else:
                        linky["IINST"] = int(words[IINST].split()[1])

                    checksum = 0
                    for i in range(LENGHT_IMAX):
                        checksum = (checksum + ord(words[IMAX][i])) & 0x3F
                    checksum = (checksum + 0x20) % 256
                    if chr(checksum) != words[IMAX][LENGHT_IMAX+1]:
                        checksum = False
                    else:
                        linky["IMAX"] = int(words[IMAX].split()[1])

                    checksum = 0
                    for i in range(LENGHT_PAPP):
                        checksum = (checksum + ord(words[PAPP][i])) & 0x3F
                    checksum = (checksum + 0x20) % 256
                    if chr(checksum) != words[PAPP][LENGHT_PAPP+1]:
                        checksum = False
                    else:
                        linky["PAPP"] = int(words[PAPP].split()[1])

                    if checksum :
                        break

    ser.close()
    return linky









