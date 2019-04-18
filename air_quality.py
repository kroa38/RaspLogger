import requests
from influxdb import InfluxDBClient
'''

'''
def store_to_database(json_body):

    influx_database = 'testdb'
    client = InfluxDBClient('localhost', 8086, 'root', 'root', influx_database)
    dbs = client.get_list_database()
    d = next((d for d in dbs if d['name'] == influx_database), None)
    if d is None: # not found
        print ("create database ")
        client.create_database(influx_database)
    result = client.write_points(json_body)
    #if result == True:
    #    print("Write to Database Success")
    #else:
    #    print("Fail to write to database")

def get_atmo():

    air_ra_url = 'http://api.atmo-aura.fr/communes/38185/indices?'
    api_token = 'api_token=d64189535a0084eefdcce6f71b4715d0'
    url = "%s%s" % (air_ra_url, api_token)

    r = requests.get(url)
    data = r.json()

    value_atmo = float(data['indices']['data'][1]['valeur'])
    value_atmo_int = int(value_atmo)
    qual_atmo = str(data['indices']['data'][1]['qualificatif'])
    #print int(value_atmo)
    #print qual_atmo
    json_body = [
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
    return json_body


json_body = get_atmo()
#print json_body
store_to_database(json_body)


