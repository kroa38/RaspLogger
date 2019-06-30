#!/usr/bin/python
import RPi.GPIO as GPIO
import time
from util_funct import check_internet, tweet_message
from util_dbase import write_to_dbase

def interrupt_handler(channel):
    """  Interrupt based GPIO handler
         write to dbase  event
         send a tweet
    """
    json_body = [{
            "measurement": "Door",
            "tags": {"Location": "Main Input"},
            "fields": {"value": 1}    }]
    if check_internet()==True:
        tweet_message("Hop Hop..")
    write_to_dbase(json_body,"gpio")


if __name__ == "__main__":
    ''' detect gpio 5

    '''
    state = 1
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)     #set up GPIO using BCM numbering
    GPIO.setup(5, GPIO.IN)     #, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(20, GPIO.OUT)
    GPIO.setup(21, GPIO.OUT)
    GPIO.add_event_detect(5, GPIO.FALLING,
                          callback=interrupt_handler,
                          bouncetime=200)


    while (True):
        time.sleep(5)

