#!/usr/bin/env python
# thanks to the project : https://github.com/junkai/SensorTag
# thanks to the project : https://github.com/msaunby/ble-sensor-pi


import sys
import time
import pexpect

adr = "78:C5:E5:6E:EA:0F"


def tosigned(n):
    if n > 0x7fff:
        return float(n-0x10000)
    else:
        return float(n)


def tosignedbyte(n):
    if n > 0x7f:
        return float(n-0x100)
    else:
        return float(n)

def magforce(v):
    return (tosigned(v) * 1.0) / (65536.0 / 2000.0)

def accel(v):
    return tosignedbyte(v) / 64.0

def gyro(v):
    return (tosigned(v) * 1.0) / (65536/500)

def init():
    """
    init gatttool
    :return: handle
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
        print "Sensor Connected !"
        time.sleep(1)
    except:
        print("Exception was thrown during expect")
        sys.exit()

    return handle


def read_sensor_humidity(handle):
    """

    :return: dictionnary
    """

    # enable humidity sensor
    handle.sendline('char-write-cmd 0x3c 01')
    handle.expect('\[LE\]>')
    time.sleep(1)
    # read humidity sensor (temp + humidity)
    handle.sendline('char-read-hnd 0x38')
    handle.expect('descriptor: .*? \r')
    objhum = handle.after.split()
    # disable humidity sensor
    handle.sendline('char-write-cmd 0x3c 00')
    handle.expect('\[LE\]>')

    rawT = long(float.fromhex(objhum[2]) * 256 + float.fromhex(objhum[1]))
    rawH = long(float.fromhex(objhum[4]) * 256 + float.fromhex(objhum[3]))

    t = -46.85 + 175.72/65536.0 * rawT # [deg C]
    rawH = float(int(rawH) & ~0x0003)
    hum = -6.0 + 125.0/65536.0 * rawH  # [%RH]

    dico = {"Hum_Temp": round(t,1), "Hum %": round(hum,1)}
    print dico


def read_sensor_temperature(handle):
    """

    :return: dictionnary
    """

    # enable temp sensor
    handle.sendline('char-write-cmd 0x29 01')
    handle.expect('\[LE\]>')
    time.sleep(1)
    # read IR temperature sensor TMP006
    handle.sendline('char-read-hnd 0x25')
    handle.expect('descriptor: .*? \r')
    objtemp = handle.after.split()
    # disable IR  temp sensor
    handle.sendline('char-write-cmd 0x29 00')
    handle.expect('\[LE\]>')

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


def read_sensor_gyroscope(handle):
    """

    :return: dictionnary
    """

    # enable magnet
    handle.sendline('char-write-cmd 0x5b 07')
    handle.expect('\[LE\]>')
    time.sleep(2)    # wait at least 2s
    # read magnet values
    handle.sendline('char-read-hnd 0x57')
    handle.expect('descriptor: .*? \r')
    objmag = handle.after.split()
    # disable magnet
    handle.sendline('char-write-cmd 0x5b 00')
    handle.expect('\[LE\]>')

    xmag = float.fromhex(objmag[2]) * 256 + float.fromhex(objmag[1])
    ymag = float.fromhex(objmag[4]) * 256 + float.fromhex(objmag[3])
    zmag = float.fromhex(objmag[6]) * 256 + float.fromhex(objmag[5])

    dico = {"Gyro x": round(gyro(xmag),1), "Gyro y": round(gyro(ymag),1), "Gyro z": round(gyro(zmag),1)}
    print dico


def read_sensor_accelerometer(handle):
    """

    :return: dictionnary
    """

    # enable magnet
    handle.sendline('char-write-cmd 0x31 01')
    handle.expect('\[LE\]>')
    time.sleep(2)    # wait at least 2s
    # read magnet values
    handle.sendline('char-read-hnd 0x2D')
    handle.expect('descriptor: .*? \r')
    objmag = handle.after.split()
    # disable magnet
    handle.sendline('char-write-cmd 0x31 00')
    handle.expect('\[LE\]>')

    xmag = float.fromhex(objmag[1])
    ymag = float.fromhex(objmag[2])
    zmag = float.fromhex(objmag[3])

    dico = {"Acc x": round(accel(xmag),1), "Acc y": round(accel(ymag),1), "Acc z": round(accel(zmag),1)}
    print dico


def read_sensor_magnet(handle):
    """

    :return: dictionnary
    """

    # enable magnet
    handle.sendline('char-write-cmd 0x44 01')
    handle.expect('\[LE\]>')
    time.sleep(2)    # wait at least 2s
    # read magnet values
    handle.sendline('char-read-hnd 0x40')
    handle.expect('descriptor: .*? \r')
    objmag = handle.after.split()
    # disable magnet
    handle.sendline('char-write-cmd 0x44 00')
    handle.expect('\[LE\]>')

    xmag = float.fromhex(objmag[2]) * 256 + float.fromhex(objmag[1])
    ymag = float.fromhex(objmag[4]) * 256 + float.fromhex(objmag[3])
    zmag = float.fromhex(objmag[6]) * 256 + float.fromhex(objmag[5])

    dico = {"Mag x": round(magforce(xmag),1), "Mag y": round(magforce(ymag),1), "Mag z": round(magforce(zmag),1)}
    print dico


def read_sensor_barometer(handle):
    """

    :return: dictionnary
    """

    # fetch barometer calibration
    global barometer
    handle.sendline('char-write-cmd 0x4f 02')
    handle.expect('\[LE\]>')
    time.sleep(2)
    # read calibration factors
    handle.sendline('char-read-hnd 0x52')
    handle.expect('descriptor: .*? \r')
    rawcal = handle.after.split()
    barometer = Barometer(rawcal)
    # enable barometer
    handle.sendline('char-write-cmd 0x4f 01')
    handle.expect('\[LE\]>')
    time.sleep(2)
    handle.sendline('char-read-hnd 0x4b')
    handle.expect('descriptor: .*? \r')
    baro = handle.after.split()
    handle.sendline('char-write-cmd 0x4f 00')
    handle.expect('\[LE\]>')
    rawT = long(float.fromhex(baro[2]) * 256 + float.fromhex(baro[1]))
    rawP = long(float.fromhex(baro[4]) * 256 + float.fromhex(baro[3]))
    (temp, pres)= barometer.calc(rawT, rawP)

    alt = ((pow((1013.25/pres),1/5.257)-1)*(temp+273.15))/0.0065
    dico = {"Temp_Baro": round(temp,1), "Pressure": round(pres,1), "Alt":round(alt,1)}
    print dico


class Barometer:

    # Ditto.
    # Conversion algorithm for barometer temperature
    #
    #  Formula from application note, rev_X:
    #  Ta = ((c1 * Tr) / 2^24) + (c2 / 2^10)
    #
    #  c1 - c8: calibration coefficients the can be read from the sensor
    #  c1 - c4: unsigned 16-bit integers
    #  c5 - c8: signed 16-bit integers
    #

    def __init__(self, rawCalibration):
        self.m_barCalib = self.Calib(rawCalibration)
        return

    def calc(self, rawT, rawP):
        self.m_raw_temp = tosigned(rawT)
        self.m_raw_pres = rawP  # N.B.  Unsigned value
        bar_temp = self.calcBarTmp(self.m_raw_temp)
        bar_pres = self.calcBarPress(self.m_raw_temp, self.m_raw_pres)
        return (bar_temp, bar_pres)

    def calcBarTmp(self, raw_temp):
        c1 = self.m_barCalib.c1
        c2 = self.m_barCalib.c2
        val = long((c1 * raw_temp) * 100)
        temp = val >> 24
        val = long(c2 * 100)
        temp += (val >> 10)
        return float(temp) / 100.0

    # Conversion algorithm for barometer pressure (hPa)
    #
    # Formula from application note, rev_X:
    # Sensitivity = (c3 + ((c4 * Tr) / 2^17) + ((c5 * Tr^2) / 2^34))
    # Offset = (c6 * 2^14) + ((c7 * Tr) / 2^3) + ((c8 * Tr^2) / 2^19)
    # Pa = (Sensitivity * Pr + Offset) / 2^14
    #
    def calcBarPress(self, Tr, Pr):
        c3 = self.m_barCalib.c3
        c4 = self.m_barCalib.c4
        c5 = self.m_barCalib.c5
        c6 = self.m_barCalib.c6
        c7 = self.m_barCalib.c7
        c8 = self.m_barCalib.c8
        # Sensitivity
        s = long(c3)
        val = long(c4 * Tr)
        s += (val >> 17)
        val = long(c5 * Tr * Tr)
        s += (val >> 34)
        # Offset
        o = long(c6) << 14
        val = long(c7 * Tr)
        o += (val >> 3)
        val = long(c8 * Tr * Tr)
        o += (val >> 19)
        # Pressure (Pa)
        pres = ((s * Pr) + o) >> 14
        return float(pres) / 100.0

    class Calib:

        # This works too
        # i = (hi<<8)+lo
        @staticmethod
        def bld_int(lobyte, hibyte):
            return int(float.fromhex(hibyte) * 256 + float.fromhex(lobyte))

        def __init__(self, pData):
            self.c1 = self.bld_int(pData[1], pData[2])
            self.c2 = self.bld_int(pData[3], pData[4])
            self.c3 = self.bld_int(pData[5], pData[6])
            self.c4 = self.bld_int(pData[7], pData[8])
            self.c5 = tosigned(self.bld_int(pData[9], pData[10]))
            self.c6 = tosigned(self.bld_int(pData[11], pData[12]))
            self.c7 = tosigned(self.bld_int(pData[13], pData[14]))
            self.c8 = tosigned(self.bld_int(pData[15], pData[16]))

count = 0
handle = init()
while count != 5:
    print "------------------------"
    read_sensor_temperature(handle)
    read_sensor_humidity(handle)
    read_sensor_barometer(handle)
    read_sensor_magnet(handle)
    read_sensor_accelerometer(handle)
    read_sensor_gyroscope(handle)
    count += 1
handle.close()