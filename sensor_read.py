#!/usr/bin/env python
# thanks to the project : https://github.com/junkai/SensorTag
# thanks to the project : https://github.com/msaunby/ble-sensor-pi


import sys
import time
import pexpect

it=0
at=0
ht=0
hu=0

adr = "78:C5:E5:6E:EA:0F"


def init():
    """
    init gatttool
    :return:
    """

    pexpect.run('sudo killall -SIGKILL gatttool')    # kill process if it is running
    pexpect.run('sudo hciconfig hci0 down')          # down hci
    pexpect.run('sudo hciconfig hci0 up')            # up  hci

    handle = pexpect.spawn('gatttool -b ' + adr + ' --interactive')
    handle.expect('\[LE\]>', timeout=600)
    print "Preparing to connect. You might need to press the side button..."
    handle.sendline('connect')
    # test for success of connect
    try:
        handle.expect('Connection successful.*\[LE\]>')
        # enable IR temperature sensor
        handle.sendline('char-write-cmd 0x29 01')
        handle.expect('\[LE\]>')
        # enable Humidity sensor
        handle.sendline('char-write-cmd 0x3C 01')
        handle.expect('\[LE\]>')
        time.sleep(1)
    except:
        print("Exception was thrown during expect")
        sys.exit()

    return handle

#-------------------------------------------------------------------------------------------
def read_sensor_humidity(handle):
    """

    :return: dictionnary
    """
    # read humidity sensor (temp + humidity)
    time.sleep(0.1)
    handle.sendline('char-read-hnd 0x38')
    handle.expect('descriptor: .*? \r')
    objhum = handle.after.split()

    rawT = long(float.fromhex(objhum[2]) * 256 + float.fromhex(objhum[1]))
    rawH = long(float.fromhex(objhum[4]) * 256 + float.fromhex(objhum[3]))

    t = -46.85 + 175.72/65536.0 * rawT # [deg C]
    rawH = float(int(rawH) & ~0x0003)
    hum = -6.0 + 125.0/65536.0 * rawH  # [%RH]

    dico = {"Hum_Temp %2f": round(t,1), "Hum %": round(hum,1)}
    print dico

#-------------------------------------------------------------------------------------------
def read_sensor_temperature(handle):
    """

    :return: dictionnary
    """
    # read IR temperature sensor TMP006
    time.sleep(0.1)
    handle.sendline('char-read-hnd 0x25')
    handle.expect('descriptor: .*? \r')
    objtemp = handle.after.split()

    obj_t = long(float.fromhex(objtemp[2]) * 256 + float.fromhex(objtemp[1]))
    die_t = long(float.fromhex(objtemp[4]) * 256 + float.fromhex(objtemp[3]))

    if obj_t > 0x7FFF:
        obj_t = obj_t - 0x10000

    m_tmpAmb = die_t/128.0

    Vobj2 = obj_t * 0.00000015625
    Tdie2 = m_tmpAmb + 273.15
    S0 = 6.4E-14            # Calibration factor
    a1 = 1.75E-3
    a2 = -1.678E-5
    b0 = -2.94E-5
    b1 = -5.7E-7
    b2 = 4.63E-9
    c2 = 13.4
    Tref = 298.15
    S = S0*(1+a1*(Tdie2 - Tref)+a2*pow((Tdie2 - Tref),2))
    Vos = b0 + b1*(Tdie2 - Tref) + b2*pow((Tdie2 - Tref),2)
    fObj = (Vobj2 - Vos) + c2*pow((Vobj2 - Vos),2)
    tObj = pow(pow(Tdie2,4) + (fObj/S),.25)
    tObj = (tObj - 273.15)

    dico = {"Temp_Amb": round(m_tmpAmb,1), "Temp_Obj": round(tObj,1)}

    print dico


handle = init()
read_sensor_temperature(handle)
read_sensor_humidity(handle)
