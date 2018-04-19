#!/usr/bin/python
# -*- coding: utf-8 -*-

import calendar
from datetime import datetime
from time import localtime, strftime


class TimeFunc:

    def __init__(self):
        pass

    @staticmethod
    def epoch_to_iso8601(epochtime):
        """
        convert the unix epoch time into a iso8601 formatted date
        epoch_to_iso8601(1341866722) return   '2012-07-09T22:45:22'
        In : Int
        Out : String
        """
        return datetime.fromtimestamp(epochtime).isoformat()

    @staticmethod
    def iso8601_to_epoch(datestring):
        """
        iso8601_to_epoch - convert the iso8601 date into the unix epoch time
        In : String
        Out :
        """
        return calendar.timegm(datetime.strptime(datestring, "%Y-%m-%dT%H:%M:%S").timetuple())

    @staticmethod
    def iso8601_to_year():
        """
        iso8601_to_epoch - convert the iso8601 date into the unix epoch time
        In : String
        Out :
        """
        datestring = int(datetime.now().strftime("%Y"))
        print datestring
        datestring = int(datetime.now().strftime("%m"))
        print datestring
        datestring = int(datetime.now().strftime("%d"))
        print datestring
        datestring = datetime.now().strftime("%d-%m-%Y")
        print datestring
        datestring = datetime.now().strftime("%H:%M")
        print datestring
        datestring = int(datetime.now().strftime("%M"))
        print datestring
        datestring = datetime.now().strftime("%A")
        print datestring
        datestring = int(datetime.now().strftime("%w"))
        print datestring
        datestring = int(datetime.now().strftime("%W"))
        print datestring
        '''return calendar.timegm(datetime.strptime(datestring, "%Y").timetuple())'''

    @staticmethod
    def epoch_to_hour(epochtime):
        """
        return the hour from epoch time
        in : Int
        Out Int
        """
        return int(strftime("%H", localtime(epochtime)))

    @staticmethod
    def epoch_to_date(epochtime):
        """
        return the hour from epoch time
        in : Int
        Out string
        """
        return strftime("%d-%m-%Y", localtime(epochtime))

    @staticmethod
    def epoch_to_year(epochtime):
        """
        return the year from epoch time
        in : Int
        Out Int
        """
        return int(strftime("%Y", localtime(epochtime)))

    @staticmethod
    def epoch_to_month(epochtime):
        """
        return the year from epoch time
        in : Int
        Out Int
        """
        return int(strftime("%m", localtime(epochtime)))

    @staticmethod
    def epoch_to_day(epochtime):
        """
        return the year from epoch time
        in : Int
        Out Int
        """
        return int(strftime("%d", localtime(epochtime)))

    @staticmethod
    def epoch_to_hourminute(epochtime):
        """
        return the hour from epoch time
        in : Int
        Out string
        """
        return strftime("%H:%M", localtime(epochtime))

    @staticmethod
    def epoch_to_minute(epochtime):
        """
        return the minutes from epoch time
        in : Int
        Out Int
        """
        return int(strftime("%M", localtime(epochtime)))

    @staticmethod
    def epoch_to_weekday_name(epochtime):
        """
        return the day of week from epoch time
        ex : 1431959458 return : Monday
        in : Int
        Out String
        """
        wdn = TimeFunc.epoch_to_weekday_number(epochtime)

        if wdn == 1:
            return 'lundi'
        if wdn == 2:
            return 'mardi'
        if wdn == 3:
            return 'mercredi'
        if wdn == 4:
            return 'jeudi'
        if wdn == 5:
            return 'vendredi'
        if wdn == 6:
            return 'samedi'
        if wdn == 7:
            return 'dimanche'

    @staticmethod
    def epoch_to_week_number(epochtime):
        """
        return the current week (1 ...54)
        ex : 1432203683 return : 21
        in : Int
        Out :Int
        """
        weeknumber = int(datetime.fromtimestamp(epochtime).strftime("%W")) + 1

        return weeknumber

    @staticmethod
    def epoch_to_weekday_number(epochtime):
        """
        return the day of week from epoch time
        1 =
        ex : 1431959458 return : 1
        in : Int
        Out int
        """
        dayt = int(datetime.fromtimestamp(epochtime).strftime("%w"))
        if dayt == 0:
            dayt = 7
        return dayt