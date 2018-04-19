import time
import serial

# configure the serial connections (the parameters differs on the device you are connecting to)
# don't forget to add group for the user of tty : ex : add group toto tty
# The script capture the data from the ERDF counter at 1200 bauds
# it extract the value of HCHC and HCHP and take care to the CRC.

ser = serial.Serial(
        port='/dev/ttyAMA0',
        baudrate=1200,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE,
        bytesize=serial.SEVENBITS
)
frame_number = 13	'frame buffer lenght'
HCHC = 4			'index in the frame for HCHC'
HCHP = 5			'index in the frame for HCHP'
LENGHT_HCHC = 14	'Lenght for the string'
LENGHT_HCHP = 14	'Lenght for the string'

ser.open()
ser.isOpen()
while 1:
        time.sleep(2)
        out = ''
        tmp = ''
        while ser.inWaiting() > 0:
                out = ser.read(1)
                if out == chr(2):
                        break
        while ser.inWaiting() > 0:
                tmp = ser.read(1)
                if tmp != chr(3):
                        out += tmp
                else:
                        break
        words = out.split(chr(10))
        if len(words) == frame_number:
                print words[HCHP]
                sum = 0
                for i in range(LENGHT_HCHP):
                        sum = (sum + ord(words[HCHP][i])) & 0x3F
                sum = (sum + 0x20) % 256
                if chr(sum) != words[HCHP][LENGHT_HCHP+1]:
                        print '**** Bad checksum ****'
                else:
                        value = int(words[HCHP].split()[1])
                        print value
                print '--------------------'				

                sum = 0
                for i in range(LENGHT_HCHC):
                        sum = (sum + ord(words[HCHC][i])) & 0x3F
                sum = (sum + 0x20) % 256
                if chr(sum) != words[HCHC][LENGHT_HCHC+1]:
                        print '**** Bad checksum ****'
                else:
                        value = int(words[HCHC].split()[1])
                        print value
                print '--------------------'