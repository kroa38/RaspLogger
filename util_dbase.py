#!/usr/bin/env python
from influxdb import InfluxDBClient
from util_funct import log_event,log_error

def write_to_dbase(jsony_body,db_name):
    """
    :param json array,database name
    :return:
    """
    currentpathdir = os.path.dirname(os.path.realpath(__file__))
    cred_file = os.path.join(currentpathdir, "credential.txt")
    data_json = get_json_data_from_file(cred_file)
    db_user = data_json['DATABASE_USER']
    db_password = data_json['DATABASE_PASSWORD']
    client = InfluxDBClient('localhost', 8086, db_user, db_password, db_name)
    dbs = client.get_list_database()
    d = next((d for d in dbs if d['name'] == db_name), None)
    if d is None:
        log_event("Create database : %s " % db_name )
        client.create_database(db_name)
    result = client.write_points(jsony_body)
    if not result:
        log_error("Database write error")

