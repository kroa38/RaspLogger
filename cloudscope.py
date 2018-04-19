#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 17 16:40:25 2015

On the arduino install the packages :

    opkg update #updates the available packages list
    opkg install distribute #it contains the easy_install command line tool
    opkg install python-openssl #adds ssl support to python
    easy_install pip #installs pip

 install the following python package on the arduino

 pip install httplib2
 pip install google-api-python-client
 pip install gspread
 pip install plotly

 first of all :
 create a credential file with the get_credential.py

 This project need the files :
 credential_google.json		(file generated by 'get_credential.py')
 
 This project generate the files below
 
 error.log		(tracking errors)
 event.log		(tracking event)...
 
  No space left on device: '/usr/lib/python2.7/site-packages/pytz-2015.2.dist-info'
"""
import time  # lib pour gestion heure
import httplib2  # lib requette http
import base64
import gspread  # lib for google spreadsheet
import json  # lib pour fichiers json
import os.path  # lib pour test fichiers
import urllib2  # lib pour requettes internet

from apiclient.discovery import build
from apiclient.http import MediaFileUpload
from oauth2client.file import Storage
from apiclient import errors
from email.mime.text import MIMEText
from twitter import *

'''
DRIVE_SCOPE = 'https://www.googleapis.com/auth/drive '
GMAIL_SCOPE = 'https://mail.google.com/'
SHEET_SCOPE = 'https://spreadsheets.google.com/feeds'
'''


def oauth2_build(scope):
    """  query oauth2 to google
    :itype : string (scope name)
    :rtype : none
    """
    currentpathdir = os.path.dirname(os.path.realpath(__file__))
    jsonfilename = os.path.join(currentpathdir, "credential_google.json")

    storage = Storage(jsonfilename)
    credentials = storage.get()

    http_auth = httplib2.Http()
    credentials.refresh(http_auth)
    storage.put(credentials)

    http_auth = credentials.authorize(http_auth)

    if scope == 'https://www.googleapis.com/auth/drive':
        # print 'Drive scope Oauth'
        authorisation = build(serviceName='drive', version='v2', http=http_auth)
        return authorisation
    if scope == 'https://mail.google.com/':
        # print 'Gmail scope Oauth'
        authorisation = build(serviceName='gmail', version='v1', http=http_auth)
        return authorisation
    if scope == 'https://spreadsheets.google.com/feeds':
        # print 'Sheet scope Oauth'
        try:
            authorisation = gspread.authorize(credentials)
            # print 'Authorisation for SpreadSheets OK'
            return authorisation
        except gspread.AuthenticationError:
            log_error("Oauth Spreadsheet error")
            # print 'Authorisation failure'


def drive_insert_file(file_name, folder_id):
    """  envoie un fichier à google drive
    :itype : string (the file name)
    :itype : string (id of folder)
    :rtype : none
    """
    if os.path.isfile(file_name):

        drive_service = oauth2_build('https://www.googleapis.com/auth/drive')
        media_body = MediaFileUpload(file_name, mimetype='*/*', resumable=True)

        body = {
            'title': file_name,
            'mimeType': '*/*',
            'parents': [{"kind": "drive#filelink", "id": folder_id}]
        }

        try:
            filehandler = drive_service.files().insert(body=body, media_body=media_body).execute()
            file_id = filehandler['id']
            textmessage = 'File : %s uploaded .  ' % file_name + 'ID File is : %s' % file_id
            log_event(textmessage)
            # print textmessage
            return [file_id]
        except errors.HttpError, e:
            error = json.loads(e.content)
            error = error['error']['message']
            log_error("HttpError in function drive_insert_file() : " + error)
            # print 'An error occured: %s' % error
    else:
        log_error("file %s doesn't exist in function : drive_insert_file() : " % file_name)
        exit()


def drive_delete_file(file_id):
    """  delete a file in drive
    :itype : string (id of the file)
    :rtype : none
    """
    drive_service = oauth2_build('https://www.googleapis.com/auth/drive')

    try:
        drive_service.files().delete(fileId=file_id).execute()
        textmessage = 'File : %s deleted' % file_id
        log_event(textmessage)
    except errors.HttpError, e:
        error = json.loads(e.content)
        error = error['error']['message']
        log_error("HttpError in function : drive_delete_file() : " + error)
        exit()


def print_files_in_folder(folder_id):
    """  affiche les id des fichiers du répertoire
    :itype : string of the folder id
    :rtype : none
    """
    drive_service = oauth2_build('https://www.googleapis.com/auth/drive')
    page_token = None
    while True:
        try:
            param = {}
            if page_token:
                param['pageToken'] = page_token
            children = drive_service.children().list(folderId=folder_id, **param).execute()
            if not len(children['items']):
                log_error(
                    "No File in folder %s \r\t\t\t\t\tor bad folder_id in function :  print_files_in_folder() " % folder_id)
                break
            for child in children.get('items', []):
                print child['id']
            # file = service.files().get(fileId=child['id']).execute()
            #        print 'Title: %s' % file['title']
            page_token = children.get('nextPageToken')
            if not page_token:
                break
        except errors.HttpError, e:
            error = json.loads(e.content)
            error = error['error']['message']
            log_error("HttpError in function : print_files_in_folder() : " + error)
            break
    exit()


def gmaillistmessage():
    """  liste les messages de la boite mail
    :itype : none
    :rtype : print the ID
    """
    gmail_service = oauth2_build('https://mail.google.com/')
    try:
        threads = gmail_service.users().threads().list(userId='me').execute()
        if threads['threads']:
            for thread in threads['threads']:
                print 'Thread ID: %s' % (thread['id'])
    except errors.HttpError, e:
        error = json.loads(e.content)
        error = error['error']['message']
        log_error("HttpError in function  : gmaillistmessage() : " + error)
        exit()


def gmailsendmessage(message):
    """  envoie le message par email
    :itype : string text message
    :rtype : none
    """
    text_message = gmailcreatemessage(message)
    gmail_service = oauth2_build('https://mail.google.com/')

    try:
        message = (gmail_service.users().messages().send(userId='me', body=text_message)
                   .execute())
        # print 'Message Id: %s' % message['id']
        log_event("Email Message Id: %s sent" % message['id'])
    except errors.HttpError, e:
        error = json.loads(e.content)
        error = error['error']['message']
        log_error("HttpError in function : gmailsendmessage()" + error)
        exit()


def gmailcreatemessage(message_text):
    """  creation du message à envoyer pour email
    :itype : string text message
    :rtype : string  raw encoded
    """
    currentpathdir = os.path.dirname(os.path.realpath(__file__))
    jsonfilename = os.path.join(currentpathdir, "config.json")

    data_email = get_json_data_from_file(jsonfilename)
    message = MIMEText(message_text)
    message['to'] = data_email['dest_mail']
    message['from'] = data_email['source_mail']
    message['subject'] = "Yuno info"
    return {'raw': base64.b64encode(message.as_string())}


def get_json_data_from_file(file_name):
    """ Return the data object from the  json file in a python dictionnary.
    :itype : file name
    :rtype : dictionnary
    """
    try:
        json_data = open(file_name).read()
    except IOError:
        log_error("IOError in function function : get_json_data_from_file()")
        exit()
    else:
        python_data = json.loads(json_data)
        return python_data


def check_internet():
    """  test cnx internet
    :itype : None
    :rtype : int (1 = true 0 = false)
    """
    try:
        os.system("wget -q --delete-after www.google.fr")  # pour debloquer websense (quiet and delete after download.
        _ = urllib2.urlopen('http://www.google.fr/', timeout=4)
        log_event("Internet is UP")
        return "1"
    except urllib2.URLError:
        log_event("Internet is Down !")
        return "0"


def get_ip_adress():
    """"
    get the current ip address of WLAN and ETH1
    :itype none
    :rtype  string
    """
    wlan0_ip = str(os.popen("ifconfig wlan0 | grep 'inet' | cut -d: -f2 | awk '{ print $2}'").read()).strip()
    ip_string = "IP  = " + wlan0_ip
    # log_event(ip_string)
    return ip_string


def email_ip_addr():
    """"
    send by email the IP address
    :itype none
    :rtype  string
    """

    gmailsendmessage(get_ip_adress())


def tweet_ip_addr():
    """
    """
    currentpathdir = os.path.dirname(os.path.realpath(__file__))
    jsonfilename = os.path.join(currentpathdir, "credential_twitter.json")

    data_tweet = get_json_data_from_file(jsonfilename)

    token = data_tweet['token']
    token_secret = data_tweet['token_secret']
    consumer_key = data_tweet['consumer_key']
    consumer_secret = data_tweet['consumer_secret']

    t = Twitter(auth=OAuth(token, token_secret, consumer_key, consumer_secret))
    message = get_ip_adress()
    t.statuses.update(status=message)


def log_error(error_message):
    """ log to the file error.log the current error with the date
    :itype : string message
    :rtype : None
    """
    currentpathdir = os.path.dirname(os.path.realpath(__file__))
    logfile = os.path.join(currentpathdir, "error.log")

    now = str(time.strftime("%c"))
    f = open(logfile, "a")
    f.write(now + "    " + error_message + "\r\n")
    f.close()


def log_event(event_message):
    """ log to the file event.log the current event with the date
    :itype : string message
    :rtype : None
    """
    currentpathdir = os.path.dirname(os.path.realpath(__file__))
    logfile = os.path.join(currentpathdir, "event.log")

    now = str(time.strftime("%c"))
    f = open(logfile, "a")
    f.write(now + "    " + event_message + "\r\n")
    f.close()

# drive_delete_file("0B9Yp8cxBtjfea2xiU3VEblRsaE0")
# File_Id = drive_insert_file("teleinfo.log",test_folder)
# folder = get_json_data_from_file("config.json")
# folder = folder['test_folder']
# print_files_in_folder(folder)
# gmaillistmessage()
# gmailsendmessage("test de message")
# check_internet()
# print str(get_index())
# put_index(12355)
# print str(get_index())
