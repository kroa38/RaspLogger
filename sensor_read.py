#!/usr/bin/env python

import os
import sys
import time
import pexpect
from datetime import datetime

adr = "78:C5:E5:6E:EA:0F"

logdir = "/tmp/pihome"

try:
    os.mkdir(logdir)
except:
    pass

cnt = 0
it = 0
at = 0
ht = 0
pt = 0
hu = 0
pr = 0
lt = 0
value_CO2 = 0
exc = 0
act = 0
post = ""
stamp = ""
handle = ""

ZERO_POINT_VOLTAGE = 0.324  # define the output of the sensor in volts when the concentration of
REACTION_VOLTAGE = 0.020  # define the voltage drop of the sensor when moving the sensor from air

DC_GAIN = 8.5
a = 2.602
b = ZERO_POINT_VOLTAGE
c = REACTION_VOLTAGE / (2.602 - 3)


def calcTmp(ambT, objT):

    m_tmpAmb = ambT/128.0
    Vobj2 = objT * 0.00000015625
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

    return (m_tmpAmb, tObj)

def calcHum(rawT, rawH):
    temp = -40 + 165.0/65536.0 * rawT # [deg C]
    hum = (float(rawH)/65536) * 100  # [%RH]
    return (temp, hum)

def calcBaro(rawPr):
    pr = rawPr/100.0
    return (pr)

def calcLight(rawL):
    m = rawL & 0x0FFF
    e = (rawL & 0xF000) >> 12
    return (m*(0.01*pow(2.0,e)))

def log_values():

    print adr, " Obj TMP %.1f" % it
    print adr, " Amb TMP %.1f" % at

while True:

    try:

        pexpect.spawn('sudo hciconfig hci0 down')
        time.sleep(1)
        pexpect.spawn('sudo hciconfig hci0 up')
        time.sleep(1)

        tool = pexpect.spawn('gatttool -b ' + adr + ' --interactive')
        tool.expect('\[LE\]>', timeout=600)
        print "Preparing to connect. You might need to press the side button..."
        tool.sendline('connect')
        # test for success of connect
        tool.expect('Connection successful.*\[LE\]>')
        print "connected !"

        print adr, " Enabling sensors ..."

        # enable IR temperature sensor
        tool.sendline('char-write-cmd 0x29 01')
        tool.expect('\[LE\]>')

        # wait for the sensors to become ready
        time.sleep(1)

        while True:
            # read IR temperature sensor
            tool.sendline('char-read-hnd 0x25')
            tool.expect('descriptor: .*? \r')
            v = tool.after.split()
            rawObjT = long(float.fromhex(v[2] + v[1]))
            rawAmbT = long(float.fromhex(v[4] + v[3]))
            (at, it) = calcTmp(rawAmbT, rawObjT)

            cnt = cnt + 1

            stamp = datetime.now().ctime()
            act = 0

            log_values()

            time.sleep(3)

    except KeyboardInterrupt:
        tool.sendline('quit')
        tool.close()
        sys.exit()

    except:
        if handle != "":
            pexpect.run('sudo hcitool ledc ' + handle)
        tool.sendline('quit')
        tool.close(force=True)
        exc = exc + 1
        act = 1
        log_values()


