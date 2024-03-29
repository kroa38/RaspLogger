#!/usr/bin/python3
# -*- coding: utf-8 -*-

import requests
import os.path
from util_funct import get_json_data_from_file, log_error, log_event
from util_dbase import write_to_dbase
from math import ceil


def get_atmo_new():
    """
    new version of atmo aura
    https://api.atmo-aura.fr/documentation
    """
    global debug_print
    ig = 0
    currentpathdir = os.path.dirname(os.path.realpath(__file__))
    cred_file = os.path.join(currentpathdir, "credential.txt")
    data_json = get_json_data_from_file(cred_file)
    detail_communal = "https://api.atmo-aura.fr/api/v1/communes/38485/indices/atmo?commune_insee=38485&date_echeance="
    api_token = data_json['Token_ARA']
    url = "%s%s%s" % (detail_communal, 'now', "&api_token=")
    url = "%s%s" % (url, api_token)
    print(url)
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        log_error("api.atmo-aura.fr unreachable ...")
        return 0
    else:
        if debug_print:
            log_event("air_quality update ok")
    retval = r.json()
    print (retval)

    ig = 0
    for indice in range(5):
        if debug_print:
            print(retval['data'][0]['sous_indices'][indice]['polluant_nom'])
            print(retval['data'][0]['sous_indices'][indice]['concentration'])
            print("indice=", retval['data'][0]['sous_indices'][indice]['indice'])
            print("--------------------")
        if  retval['data'][0]['sous_indices'][indice]['indice'] > ig:
            ig = retval['data'][0]['sous_indices'][indice]['indice']

    if debug_print:
        print('Indice global')
        print("indice=", ig)
        print("--------------------")

    my_body = [
        {
            "measurement": "Qualificatif",
            "tags": {
                "Location": 38170
            },
            "fields": {
                "value": ig
            }
        },
        {
            "measurement": retval['data'][0]['sous_indices'][0]['polluant_nom'],
            "tags": {
                "Location": 38170
            },
            "fields": {
                "value": ceil(retval['data'][0]['sous_indices'][0]['concentration'])
            }
        },
        {
            "measurement": retval['data'][0]['sous_indices'][1]['polluant_nom'],
            "tags": {
                "Location": 38170
            },
            "fields": {
                "value": ceil(retval['data'][0]['sous_indices'][1]['concentration'])
            }
        }, {
            "measurement": retval['data'][0]['sous_indices'][2]['polluant_nom'],
            "tags": {
                "Location": 38170
            },
            "fields": {
                "value": ceil(retval['data'][0]['sous_indices'][2]['concentration'])
            }
        },
        {
            "measurement": retval['data'][0]['sous_indices'][3]['polluant_nom'],
            "tags": {
                "Location": 38170
            },
            "fields": {
                "value": ceil(retval['data'][0]['sous_indices'][3]['concentration'])
            }
        }, {
            "measurement": retval['data'][0]['sous_indices'][4]['polluant_nom'],
            "tags": {
                "Location": 38170
            },
            "fields": {
                "value": ceil(retval['data'][0]['sous_indices'][4]['concentration'])
            }
        }

    ]
    return my_body


def get_atmo():
    """
    token like :
    {
    'Token_ARA':'d54eefdrce645682f71b445715d0'
    }
    """
    global debug_print

    currentpathdir = os.path.dirname(os.path.realpath(__file__))
    cred_file = os.path.join(currentpathdir, "credential.txt")
    data_json = get_json_data_from_file(cred_file)
    air_ra_url = 'http://api.atmo-aura.fr/communes/38185/indices?api_token='
    api_token = data_json['Token_ARA']
    url = "%s%s" % (air_ra_url, api_token)
    r = requests.get(url)
    if r.status_code != requests.codes.ok:
        log_error("api.atmo-aura.fr unreachable ...")
        return 0
    else:
        if debug_print:
            log_event("air_quality update ok")
    data = r.json()
    value_atmo = float(data['indices']['data'][0]['valeur'])
    value_atmo_int = round(value_atmo)

    if value_atmo_int < 10:
        qual_atmo = "Très bon"
    elif 10 < value_atmo_int <= 40:
        qual_atmo = "Bon"
    elif 40 < value_atmo_int <= 50:
        qual_atmo = "Moyen"
    elif 50 < value_atmo_int <= 80:
        qual_atmo = "Médiocre"
    elif 80 < value_atmo_int <= 90:
        qual_atmo = "Mauvais"
    else:
        qual_atmo = "Très Mauvais"

    if debug_print:
        print(int(value_atmo))
        print(qual_atmo)

    my_body = [
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
                "value": qual_atmo
            }
        }
    ]
    return my_body


if __name__ == "__main__":
    '''
    start this script with cron : sudo crontab -e 
    for example every hour
    0 * * * * python3 /this_script.py > /dev/null 2>&1
    '''
    debug_print = True

    my_json_body = get_atmo_new()
    if my_json_body != 0:
        if debug_print:
            print(my_json_body)
        else:
            write_to_dbase(my_json_body, "air_quality_new")
