#!/usr/bin/env python

import time
import sys
import serial       # install pyserial package
from util_dbase import write_to_dbase
from util_funct import log_error

# configure the serial connections (the parameters differs on the device you are connecting to)
# don't forget to add group for the user of tty : ex : add group toto tty
# The script capture the data from the Linky counter at 1200 bauds
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

    linky = {"HP": 0, "HC": 0, "PTEC": '', "IINST": 0, "PAPP": 0, "IMAX": 0}

    tmp = ser.read(10)              # read 10 char on serial

    if len(tmp) == 10:              # if linky is present ok go for capture

        for count in range(0,10) :    # try 10 times

                chksum_err = False
                time.sleep(2)
                out = ''
                tmp = ''

                for loop in range(0,220):   # read max 220 char
                        tmp = ser.read(1)
                        if tmp == chr(2): # Search for STX char
                            break
                tmp = ser.read()

                for loop in range(0, 220):
                        tmp = ser.read(1)
                        if tmp != chr(3): # ETX Char found
                            out += tmp
                        else:
                            break
                words = out.split(chr(10))    #Split each line at New Line Char

                if len(words) == nb_line:   # Test if we retrieve the entire frame

                    if linky["HP"] == 0:
                        checksum = 0
                        for i in range(LENGHT_HCHP):
                            checksum = (checksum + ord(words[HCHP][i])) & 0x3F
                        checksum = (checksum + 0x20) % 256
                        if chr(checksum) != words[HCHP][LENGHT_HCHP+1]:
                            chksum_err = True
                        else:
                            linky["HP"] = int(words[HCHP].split()[1])

                    if linky["HC"] == 0:
                        checksum = 0
                        for i in range(LENGHT_HCHC):
                            checksum = (checksum + ord(words[HCHC][i])) & 0x3F
                        checksum = (checksum + 0x20) % 256
                        if chr(checksum) != words[HCHC][LENGHT_HCHC+1]:
                            chksum_err = True
                        else:
                            linky["HC"] = int(words[HCHC].split()[1])

                    if linky["PTEC"] == '':
                        checksum = 0
                        for i in range(LENGHT_PTEC):
                            checksum = (checksum + ord(words[PTEC][i])) & 0x3F
                        checksum = (checksum + 0x20) % 256
                        if chr(checksum) != words[PTEC][LENGHT_PTEC+1]:
                            chksum_err = True
                        else:
                            linky["PTEC"] = (words[PTEC].split()[1])[0:2]

                    if linky["IINST"] == 0:
                        checksum = 0
                        for i in range(LENGHT_IINST):
                            checksum = (checksum + ord(words[IINST][i])) & 0x3F
                        checksum = (checksum + 0x20) % 256
                        if chr(checksum) != words[IINST][LENGHT_IINST+1]:
                            chksum_err = True
                        else:
                            linky["IINST"] = int(words[IINST].split()[1])

                    if linky["IMAX"] == 0:
                        checksum = 0
                        for i in range(LENGHT_IMAX):
                            checksum = (checksum + ord(words[IMAX][i])) & 0x3F
                        checksum = (checksum + 0x20) % 256
                        if chr(checksum) != words[IMAX][LENGHT_IMAX+1]:
                            chksum_err = True
                        else:
                            linky["IMAX"] = int(words[IMAX].split()[1])

                    if linky["PAPP"] == 0:
                        checksum = 0
                        for i in range(LENGHT_PAPP):
                            checksum = (checksum + ord(words[PAPP][i])) & 0x3F
                        checksum = (checksum + 0x20) % 256
                        if chr(checksum) != words[PAPP][LENGHT_PAPP+1]:
                            chksum_err = True
                        else:
                            linky["PAPP"] = int(words[PAPP].split()[1])

                    if chksum_err == False:
                        break

    ser.close()
    return linky


def linky_to_json(linky_dict, occurence):
    """
    :param   dictionnary
    :return: json array
    """


    json_body = [
        {
            "measurement": "Index_HC",
            "tags": {
                "Location": "Linky",
                "Occurence": occurence
            },
            "fields": {
                "value": linky_dict['HC']
            }
        },
        {
            "measurement": "Index_HP",
            "tags": {
                "Location": "Linky",
                "Occurence": occurence
            },
            "fields": {
                "value": linky_dict['HP']
            }
        },
        {
            "measurement": "Current_A",
            "tags": {
                "Location": "Linky",
                "Occurence": occurence
            },
            "fields": {
                "value": linky_dict['IINST']
            }
        },
        {
            "measurement": "Power_VA",
            "tags": {
                "Location": "Linky",
                "Occurence": occurence
            },
            "fields": {
                "value": linky_dict['PAPP']
            }
        },
        {
            "measurement": "Imax_A",
            "tags": {
                "Location": "Linky",
                "Occurence": occurence
            },
            "fields": {
                "value": linky_dict['IMAX']
            }
        }
    ]
    return json_body


if __name__ == "__main__":
    '''
    start this script with cron : sudo crontab -e 
    for example every 15 minute
    0/15 * * * * python ../../this_script.py > /dev/null 2>&1
    
    argv : hour, day, week, month, year
    '''
    argv = str(sys.argv)

    linky = capture_linky()
    # test if we have receive data from serial
    if linky['HC'] != 0:
        json_body = linky_to_json(linky, argv[1])
        # print json_body
        write_to_dbase(json_body, "test_db")
    else:
        log_error("Linky Serial error !")






