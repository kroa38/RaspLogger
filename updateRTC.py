#!/usr/bin/python3
# -*- coding: utf-8 -*-
#

import DS1338
from util_funct import check_internet, log_event, tweet_message

# Main Program
if __name__ == "__main__":

    rtc = DS1338.DS1338(1, 0x68)

    if check_internet():
        rtc.write_now()
        rtc.write_ctrl()
        log_event("rtc updated")
        tweet_message("rtc updated")
