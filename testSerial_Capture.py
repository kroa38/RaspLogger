#!/usr/bin/env python
import RPi.GPIO as GPIO
import time
from serial_capture import capture_linky

GPIO.setmode(GPIO.BCM)
GPIO.setup(20, GPIO.OUT)
GPIO.setup(21, GPIO.OUT)

while True:
    d = capture_linky()
    if d["HC"] != 0:
        GPIO.output(20, 1)
        time.sleep(0.3)
        GPIO.output(20, 0)
    time.sleep(2)

