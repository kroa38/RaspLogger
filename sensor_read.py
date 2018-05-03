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

def calcTmp(objT,ambT):

    if objT > 0x7FFF:
        objT = objT - 0x10000

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

    return (tObj,m_tmpAmb)

def calcHum(rawT, rawH):

    t = -46.85 + 175.72/65536.0 * rawT # [deg C]
    rawH = float(int(rawH) & ~0x0003)
    hum = -6.0 + 125.0/65536.0 * rawH  # [%RH]
    return (t, hum)

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
    print adr, " Hum TMP %.1f" % ht
    print adr, " Humidity %.1f" % hu

while True:

    try:

        pexpect.run('sudo killall -SIGKILL gatttool')
        pexpect.run('sudo hciconfig hci0 down')
        pexpect.run('sudo hciconfig hci0 up')

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
        # enable Humidity sensor
        tool.sendline('char-write-cmd 0x3C 01')
        tool.expect('\[LE\]>')
        # wait for the sensors to become ready
        time.sleep(1)

        while True:
            # read IR temperature sensor
            tool.sendline('char-read-hnd 0x25')
            tool.expect('descriptor: .*? \r')
            v = tool.after.split()
            rawObjT = long(float.fromhex(v[2])*256 + float.fromhex(v[1]) )
            rawAmbT = long(float.fromhex(v[4])*256 + float.fromhex(v[3]) )
            (it, at) = calcTmp(rawObjT,rawAmbT)
            # read Humidity sensor
            tool.sendline('char-read-hnd 0x38')
            tool.expect('descriptor: .*? \r')
            v = tool.after.split()
            rawT = long(float.fromhex(v[2])*256 + float.fromhex(v[1]) )
            rawH = long(float.fromhex(v[4])*256 + float.fromhex(v[3]) )
            (ht, hu) = calcHum(rawT, rawH)
            log_values()
            time.sleep(3)

    except KeyboardInterrupt:
        pexpect.run('sudo killall -SIGKILL gatttool')
        pexpect.run('sudo hciconfig hci0 down')
        sys.exit()

    except:
        pexpect.run('sudo killall -SIGKILL gatttool')
        pexpect.run('sudo hciconfig hci0 down')
        sys.exit()

