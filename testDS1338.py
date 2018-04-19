#!/usr/bin/env python
#
# Test SDL_DS1307
# John C. Shovic, SwitchDoc Labs
# 07/10/2014
#
# Evaluation of the following RTC Clocks
#
#	rtc
#	DS1338
#	MCP79400
#	DS3231 
# 	PCF8563 
#

# imports

import sys
import time
import datetime

import DS1338

# Main Program

print ""
print "Test SDL_DS1307 Version 1.0 - SwitchDoc Labs"
print ""
print ""
print "Program Started at:" + time.strftime("%Y-%m-%d %H:%M:%S")

filename = time.strftime("%Y-%m-%d%H:%M:%SRTCTest") + ".txt"
starttime = datetime.datetime.utcnow()

rtc = DS1338.DS1338(1, 0x68)
# rtc.write_ctrl()
# rtc.write_now()

# Main Loop - sleeps 10 minutes, then reads and prints values of all clocks


while True:
    currenttime = datetime.datetime.utcnow()

    deltatime = currenttime - starttime

    print ""
    print "Raspberry Pi=\t" + time.strftime("%Y-%m-%d %H:%M:%S")

    print "rtc=\t\t%s" % rtc.read_datetime()
    print "Delta time" + str(deltatime)
    time.sleep(10.0)
