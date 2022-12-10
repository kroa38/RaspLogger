#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
This module add some function to monitor the memomry of Raspberry
The collected info are sent to a database
"""

from util_dbase import write_to_dbase
import psutil

def memory_info():
    """

    :return: json data
    """
    global debug_print

    if debug_print:
        print("**** Memory Info ****")
    mem_total = psutil.virtual_memory().total
    mem_free = psutil.virtual_memory().free
    mem_available = psutil.virtual_memory().available


    json_body = [
        {"measurement": "MemTotal", "fields": {"value": mem_total}},
        {"measurement": "MemFree", "fields": {"value": mem_free}},
        {"measurement": "MemAvailable", "fields": {"value": mem_available}}
    ]

    return json_body

if __name__ == "__main__":
    '''
    start this script with cron : sudo crontab -e
    for example every day
    0 * * * * python /this_script.py > /dev/null 2>&1
    '''
    debug_print = True

    json_body = memory_info()

    if debug_print:
        print(json_body)
    else:
        write_to_dbase(json_body, "memory_info")
