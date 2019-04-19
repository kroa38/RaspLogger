#!/usr/bin/env python
#

import DS1338
from util_funct import check_internet, log_event, tweet_message

# Main Program

rtc = DS1338.DS1338(1, 0x68)

if check_internet() == "1":
    rtc.write_now()
    rtc.write_ctrl()
    log_event("rtc updated")
    tweet_message("rtc updated")

