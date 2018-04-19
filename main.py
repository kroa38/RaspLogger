#!/usr/bin/python
# -*- coding: utf-8 -*-


import random
import os.path
import urllib2
import sys
from cloudscope import oauth2_build
from sqlcode import SqlBase
from timefunc import TimeFunc
from plotlyplot import PlotlyPlot


'''
DRIVE_SCOPE = 'https://www.googleapis.com/auth/drive '
GMAIL_SCOPE = 'https://mail.google.com/'
'''
index_hp = 5451113
index_hc = 5323021
epochdate = 1403482200

def worksheet():

    sheet_scope = 'https://spreadsheets.google.com/feeds'

    sheet_service = oauth2_build(sheet_scope)
    wks = sheet_service.open("teleinfo").sheet1
    for ligne in range(1, 10):
        data = float(ligne) * 3.48
        wks.update_cell(ligne, 6, data)
        print data
        # val = wks.acell('E1').value
        # print val
        # val = wks.cell(1,2).value
        # print val


def datalist_test():
    """
    For test only this method return a list  like [1256234,1546879,"HP","26.1","2012-07-09T22:45:22"]
    the global variable a defined at the beginning of the file
    in : void
    Out list  [Int, Int, String, Float, String]  [1451271, 1324002, 'HP', '26.1' , '2001-12-11T06:21:40']
    """

    global index_hc
    global index_hp
    global epochdate
    epochdate += 2001

    datetime_iso8601 = TimeFunc.epoch_to_iso8601(epochdate)
    heures = int(TimeFunc.epoch_to_hour(epochdate))
    minutes = int(TimeFunc.epoch_to_minute(epochdate))

    mode = "HP"
    # check between 15h38 and 17h38
    if (heures * 60 + minutes > 15 * 60 + 38) and (heures * 60 + minutes < 17 * 60 + 38):
        mode = "HC"
    # check between 21h08 and 23h59
    if (heures * 60 + minutes > 21 * 60 + 8) and (heures * 60 + minutes < 23 * 60 + 59):
        mode = "HC"
    # check between 00h00 and 03h08
    if (heures * 60 + minutes > 0) and (heures * 60 + minutes < 3 * 60 + 8):
        mode = "HC"

    if mode == "HP":
        index_hp += abs(random.randint(1, 100))  # increment HP during HP time
    if mode == "HC":
        index_hc += abs(random.randint(1, 100))  # increment HC during HC time

    temperature = abs(random.randint(20, 25))
    tfl = abs(random.randint(1, 9))/10.0
    temperature += tfl

    liste1 = [index_hp, index_hc, mode, temperature, datetime_iso8601]

    return liste1


'''
************************************************************************
************************************************************************
************************************************************************
'''
if __name__ == '__main__':

    test = 2
    plot = 1

    if test == 1:
        print "Test Mode"
        dbname = 'testdatabase.db'
        if os.path.isfile(dbname):
            os.remove(dbname)
            print "database erased"
        for x in range(0, 225):
            SqlBase.update(dbname, test, datalist_test())
        print "database updated"
        if plot:
            SqlBase.resetflagupload(dbname)
            PlotlyPlot.plot(dbname, test)
            print "Plotly updated"
    if test == 2:
        # dbname = '/root/python/yun_database.db'
        dbname = 'yun_database.db'
        # SqlBase.resetflagupload(dbname)
        PlotlyPlot.plot(dbname, 0)
    else:
        dbname = '/root/python/yun_database.db'
        SqlBase.update(dbname, test, sys.argv[1:])
        if plot:
            PlotlyPlot.plot(dbname, test)

