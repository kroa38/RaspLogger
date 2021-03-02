#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os.path
from influxdb import InfluxDBClient
from util_funct import get_json_data_from_file, log_event, log_error


def write_to_dbase(jsony_body, db_name):
    """
    :param json array,database name
    :return:
    """
    currentpathdir = os.path.dirname(os.path.realpath(__file__))
    cred_file = os.path.join(currentpathdir, "credential.txt")
    try:
        data_json = get_json_data_from_file(cred_file)
    except:
        print("**********************************")
        print("* Error : no file credential.txt *")
        print("**********************************")
        return
    db_user = data_json['DATABASE_USER_ADMIN']
    db_password = data_json['DATABASE_PASSWORD_ADMIN']
    client = InfluxDBClient('localhost', 8086, db_user, db_password, db_name)
    dbs = client.get_list_database()
    d = next((d for d in dbs if d['name'] == db_name), None)
    if d is None:
        client.create_database(db_name)
        if db_name == 'sysinfo':
            client.create_retention_policy('autogen', '7d', '1', db_name, False, '7d')
        else:
            client.create_retention_policy('autogen', '0s', '1', db_name, False, '31d')

            # grant privilege for grafana user
        db_user = data_json['DATABASE_USER_READER']
        client.grant_privilege('read', db_name, db_user)

    result = client.write_points(jsony_body)
    if not result:
        log_error("Database write error")


def init_dbase():
    """
    :param none
    :return: none
    """
    print("**********************************")
    print("* INIT DBASE USERS               *")
    print("**********************************")
    currentpathdir = os.path.dirname(os.path.realpath(__file__))
    cred_file = os.path.join(currentpathdir, "credential.txt")
    try:
        data_json = get_json_data_from_file(cred_file)
    except:
        print("**********************************")
        print("* Error : no file credential.txt *")
        print("**********************************")
        return

    client = InfluxDBClient('localhost', 8086)
    print("**********************************")
    print("* CREATE INFLUXDB GRAFANA USER   *")
    print("**********************************")
    # create a user for grafana	
    db_user = data_json['DATABASE_USER_READER']
    db_password = data_json['DATABASE_PASSWORD_READER']
    client.create_user(db_user, db_password, admin=False)

    print("**********************************")
    print("* CREATE INFLUXDB ADMIN USER     *")
    print("**********************************")
    # create admin user with read/write privilege	
    db_user = data_json['DATABASE_USER_ADMIN']
    db_password = data_json['DATABASE_PASSWORD_ADMIN']
    client.create_user(db_user, db_password, admin=True)


if __name__ == "__main__":
    '''
    start this script for creating the databases
    option "auth-enabled = false" must be declared into  /etc/influxdb/influxdb.conf
    '''
    init_dbase()
