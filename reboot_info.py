#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This module log the reboot date of the Raspberry-pi
The info is stored into memory_info database
"""

from util_dbase import write_to_dbase
import psutil

def reboot_info():
    """
    :return: json data
    """
    global debug_print

    if debug_print:
        print("**** Reboot Info ****")

    json_body = [
        {"measurement": "Reboot", "fields": {"value": 1}}
    ]

    return json_body

if __name__ == "__main__":
    '''
    start this script with cron : sudo crontab -e
    for example every day
    0 * * * * python /this_script.py > /dev/null 2>&1
    '''
    debug_print = True

    json_body = reboot_info()

    if debug_print:
        print(json_body)
    else:
        write_to_dbase(json_body, "memory_info")
