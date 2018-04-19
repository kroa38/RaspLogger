#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
import json             # lib pour fichiers json
from cloudscope import log_error, log_event, get_json_data_from_file, check_internet, email_ip_addr
import os

def main(str_arg):
    """  
    cette fonction retourne un paramètre en fonction l'argument passé en entrée
    elle est utilisé par l'arduino pour lire sa config en terme
    d'echantillonnage de la teleinfo et de mise à l'heure de la rtc via internet
    :itype : string
    :rtype : string

    """
    currentpathdir = os.path.dirname(os.path.realpath(__file__))
    jsonfilename = os.path.join(currentpathdir, "config.json")


    if str_arg == "sampling_interval":
        jsondata = get_json_data_from_file(jsonfilename)
        data = jsondata['arduino_config']['sampling_interval']
        log_event("sampling_interval set to : " + str(data))
        print str(data)
        exit()
    if str_arg == "adjust_rtc":
        jsondata = get_json_data_from_file(jsonfilename)
        data = jsondata['arduino_config']['adjust_rtc']
        log_event("RTC adjusted everyday at : " + str(data) + "h")
        print str(data)
        exit()
    if str_arg == "check_internet":
        if check_internet()=="1":
            email_ip_addr()
        exit()
    else:
        print "0"
        log_error("Bad argument passed to config.py")
        exit()


if __name__ == '__main__':

    main(sys.argv[1])
    #main("check_internet")


