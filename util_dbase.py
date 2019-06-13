#!/usr/bin/env python
import os.path
from influxdb import InfluxDBClient
from util_funct import get_json_data_from_file,log_event,log_error

def write_to_dbase(jsony_body,db_name):
    """
    :param json array,database name
    :return:
    """
    currentpathdir = os.path.dirname(os.path.realpath(__file__))
    cred_file = os.path.join(currentpathdir, "credential.txt")
    data_json = get_json_data_from_file(cred_file)
    db_user = data_json['DATABASE_USER_ADMIN']
    db_password = data_json['DATABASE_PASSWORD_ADMIN']
    client = InfluxDBClient('localhost', 8086, db_user, db_password, db_name)
    dbs = client.get_list_database()
    d = next((d for d in dbs if d['name'] == db_name), None)
    if d is None:
        log_event("Create database : %s " % db_name )
        client.create_database(db_name)
    result = client.write_points(jsony_body)
    if not result:
        log_error("Database write error")

def init_dbase():
    """
    :param none
    :return: none
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
    client = InfluxDBClient('localhost', 8086)
	
    client.create_database('linky')
    client.create_database('air_quality')
    client.create_database('ibeacon')
    client.create_database('sysinfo')
	
    db_user = data_json['DATABASE_USER_ADMIN']
    db_password = data_json['DATABASE_PASSWORD_ADMIN']	
    client.create_user(db_user,db_password,admin=True)
	
    db_user = data_json['DATABASE_USER_READER']
    db_password = data_json['DATABASE_PASSWORD_READER']	
    client.create_user(db_user,db_password,admin=False)	
    client.grant_privilege('read','ibeacon',db_user)
    client.grant_privilege('read','linky',db_user)
    client.grant_privilege('read','air_quality',db_user)
    client.grant_privilege('read','sysinfo',db_user)
    client.create_retention_policy('sysinfo_ret','7d','0','sysinfo',False,'7d')
if __name__ == "__main__":
    '''
    start this script for creating the databases
    option "auth-enabled = false" must be declared into  /etc/influxdb/influxdb.conf
    '''
    init_dbase()
