#!/usr/bin/env python
import requests
from util_funct import get_json_data_from_file, log_error
from util_dbase import write_to_dbase

def get_atmo():
    '''
    token like :
    {
    'Token_ARA':'d54eefdrce645682f71b445715d0'
    }
    '''
    global debug_print

    data_json = get_json_data_from_file("credential.txt")
    air_ra_url = 'http://api.atmo-aura.fr/communes/38185/indices?api_token='
    api_token = data_json['Token_ARA']
    url = "%s%s" % (air_ra_url, api_token)
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        log_error("api.atmo-aura.fr unreachable ...")
        return 0
    data = r.json()
    value_atmo = float(data['indices']['data'][1]['valeur'])
    value_atmo_int = int(value_atmo)
    qual_atmo = str(data['indices']['data'][1]['qualificatif'])
    if debug_print:
        print int(value_atmo)
        print qual_atmo
    jsony_body = [
        {
            "measurement": "IQA_Val",
            "tags": {
                "Location": 38000
            },
            "fields": {
                "value": value_atmo_int
            }
        },
        {
            "measurement": "IQA_Qual",
            "tags": {
                "Location": 38000
            },
            "fields": {
                "value":  qual_atmo
            }
        }
    ]
    return jsony_body


if __name__ == "__main__":
    '''
    start this script with cron : sudo crontab -e 
    for example every hour
    0 * * * * python /this_script.py > /dev/null 2>&1
    '''
    debug_print = False

    jsony_body = get_atmo()
    if jsony_body != 0:
        if debug_print:
            print jsony_body
        else:
            write_to_dbase(jsony_body)
