#!/usr/bin/python
import RPi.GPIO as GPIO
import time


def interrupt_handler(channel):
    """
    Interrupt based GPIO handler
    """
    global state

    if channel == 5:
        if state == 0:
            state = 1
            print("state reset by event on pin 5")
            GPIO.output(20,1)
            GPIO.output(21,1)
            time.sleep(2)
            GPIO.output(20,0)
            GPIO.output(21,0)
            

if __name__ == '__main__'     
    '''
    start this script with cron : sudo crontab -e 
    for example every hour
    0 * * * * python /this_script.py > /dev/null 2>&1
    '''
    state = 1 
    GPIO.setmode(GPIO.BCM)     #set up GPIO using BCM numbering    
    GPIO.setup(5, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)

    GPIO.add_event_detect(5, GPIO.FALLING,
                          callback=interrupt_handler,
                          bouncetime=200)


    while (True):
        time.sleep(0)

