#!/usr/bin/env python
from influxdb import InfluxDBClient
from util_funct import log_event,log_error

def write_to_dbase(jsony_body,db_name):
    """
    :param json array,database name
    :return:
    """

    client = InfluxDBClient('localhost', 8086, 'root', 'root', db_name)
    dbs = client.get_list_database()
    d = next((d for d in dbs if d['name'] == db_name), None)
    if d is None:
        log_event("Create database : %s " % db_name )
        client.create_database(db_name)
    result = client.write_points(jsony_body)
    if not result:
        log_error("Database write error")

