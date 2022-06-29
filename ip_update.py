#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import os.path  # lib pour test fichiers
from util_funct import get_json_data_from_file, log_error,log_event


def opendns():
    """
    Update opendns with the current global ip address
    """
    global debug_print
    currentpathdir = os.path.dirname(os.path.realpath(__file__))
    cred_file = os.path.join(currentpathdir, "credential.txt")
    data_json = get_json_data_from_file(cred_file)
    opendns_url = '@updates.dnsomatic.com/nic/update?hostname='
    opendns_name = data_json['Token_OPENDNS_NAME']
    opendns_password = data_json['Token_OPENDNS_PASSWORD']
    opendns_domain = data_json['Token_OPENDNS_DOMAIN']
    opendns_wildcard = '&wildcard=NOCHG&mx=NOCHG&backmx=NOCHG'

    url = "https://%s:%s%s%s%s" % (opendns_name, opendns_password,opendns_url
                                   , opendns_domain,opendns_wildcard)
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        log_error("Fail to update OpenDNS %s" % r.text)
        exit()
        if debug_print:
            print("Failed to update OpenDNS.", r.text)
    else:
        if debug_print:
            print("Successfully updated IP:", r.text)
            log_event("update OpenDNS ok: %s" % r.text)

def duckdns():
    """
    Update duckdns.org with the current global ip address
    """
    global debug_print
    currentpathdir = os.path.dirname(os.path.realpath(__file__))
    cred_file = os.path.join(currentpathdir, "credential.txt")
    data_json = get_json_data_from_file(cred_file)
    duck_url = 'https://www.duckdns.org/update?domains='
    api_token = data_json['Token_DUCK']
    url = "%s%s&ip=" % (duck_url, api_token)
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        log_error("Fail to update DuckDns: %s" % r.text)
        if debug_print:
            print("Failed to update DuckDns: ", r.text)
    else:
        log_event("update DuckDNS ok: %s" % r.text)
        if debug_print:
            print("DuckDns updated: ", r.text)


if __name__ == "__main__":
    '''
    start this script with cron : sudo crontab -e 
    for example every hour
    0 * * * * python /this_script.py > /dev/null 2>&1
    '''
    debug_print = True
    opendns()
    duckdns()


