# -*- coding: utf-8 -*-
## PloneBooking: Online Booking Tool to allow booking on any kind of ressource
## Copyright (C)2005 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
    DateManager: Date tools
"""

__version__ = "$Revision: 1.19 $"
__author__  = ''
__docformat__ = 'restructuredtext'

# Python imports
import os
import calendar
import time
try :
    import datetime
except:
    raise ImportError('Module datetime not found, make sure you have Python 2.3 or greater.')



# Zope imports
import Globals
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from DateTime import DateTime


# CMF imports
from Products.CMFCore import permissions

# Products imports
from Products.PloneBooking.config import I18N_DOMAIN

class DateManager:
    """
    Tool for managing date
    """

    security = ClassSecurityInfo()

    def getDateRangeFromWeek(self, start_week, start_year, end_week=None, end_year=None):
        """Returns tuple of DateTime.
        Compute this tuple from weeks.
        A week begins monday and ends sunday.
        """

        if end_week is None:
            end_week = start_week

        if end_year is None:
            end_year = start_year

        # Get first day of start year
        date_first_day = DateTime(start_year, 1, 1)
        day_minus = (date_first_day.dow() -1) % 7
        day_plus = 0
        start_day = (start_week * 7) - 6 - day_minus
        start_date = DateTime(start_year, start_day)

        if start_date.week() != start_week:
            day_plus = 7
            start_date = start_date + day_plus

        # Get first day of end year
        date_first_day = DateTime(end_year, 1, 1)
        day_minus = (date_first_day.dow() -1) % 7
        end_day = (end_week * 7) - day_minus + day_plus
        end_date = DateTime(end_year, end_day)

        # Finished at 23:59:59
        end_date = DateTime(end_date.year(),
                      end_date.month(),
                      end_date.day(),
                      23, 59, 59)

        return (start_date, end_date)

    def buildWeekDays(self, week, year):
        """ Return a list of timestamp from the beginning of the week to its end
            week : int
            year : int
        """
        week_range = self.getDateRangeFromWeek(week, year)
        week_start_date = week_range[0]
        week_end_date = week_range[1]

        # build the days (timestamp)
        ts_delta = 24*60*60 # a day in seconds
        ts_start = self.getTsFromDatetime(self.zdt2dt(week_start_date))
        ts_end = self.setTsTime(self.getTsFromDatetime(self.zdt2dt(week_end_date)), 0, 0)
        days = self.buildPeriodList(ts_start, ts_end, ts_delta)
        return days

    def buildWeekTable(self, week, year, starting_hour=8, starting_minute=0, ending_hour=19, ending_minute=0, delta=3600):
        """ Return a list of list. Length of list is the hour count
            and sublists length are the number of day in a week.
            [ [day1_hour1, day2_hour1, ...], [day1_hour2, day2_hour2, ...] ]
        """
        days = self.buildWeekDays(week, year)

        week_table = []
        #init
        ts_start = self.setTsTime(days[0], starting_hour, starting_minute)
        ts_end = self.setTsTime(days[0], ending_hour, ending_minute)
        hours = self.buildPeriodList(ts_start, ts_end, delta)
        for hour in hours:
            week_table.append([])
        for day in days:
            ts_start = self.setTsTime(day, starting_hour, starting_minute)
            ts_end = self.setTsTime(day, ending_hour, ending_minute)
            hours = self.buildPeriodList(ts_start, ts_end, delta)

            for hour in hours:
                index = hours.index(hour)
                week_table[index].append(hour)
        return week_table

    def getDateRangeFromMonth(self, start_month, start_year, end_month=None, end_year=None):
        """Returns tuple of DateTime.
        Compute this tuple from months."""

        if end_month is None:
            end_month = start_month

        if end_year is None:
            end_year = start_year

        start_date = DateTime(start_year, start_month, 1)
        end_day = calendar.monthrange(end_year, end_month)[1]
        end_date = DateTime(end_year, end_month, end_day)

        # Finished at 23:59:59
        end_date = DateTime(end_date.year(),
                      end_date.month(),
                      end_date.day(),
                      23, 59, 59)

        return (start_date, end_date)

    def getDateRangeFromYear(self, start_year, end_year=None):
        """Returns tuple of DateTime.
        Compute this tuple from years."""

        if end_year is None:
            end_year = start_year

        start_date = DateTime(start_year, 1, 1)
        end_date = DateTime(end_year + 1, 1, 1)
        return (start_date, end_date)

    def getDateRangeFromDate(self, start_date, end_date=None):
        """Returns tuple of DateTime.
        Compute this tuple from dates."""

        if end_date is None:
            end_date = start_date

        start_date = DateTime(start_date.year(),
                      start_date.month(),
                      start_date.day(),
                      0, 0, 0)

        # Finished at 23:59:59
        end_date = DateTime(end_date.year(),
                      end_date.month(),
                      end_date.day(),
                      23, 59, 59)

        return (start_date, end_date)

    security.declarePublic('getFormatedDate')
    def getFormatedDate(self, date, with_year=1):
        """Get translated date"""

        domain = I18N_DOMAIN
        date_format_msgid = 'date_format_without_year'
            
        day = date.day()
        weekday = (date.dow() - 1) % 7
        month = date.month()
        weekdayname_msgid = 'calendar_weekday_%d' % weekday
        monthname_msgid = 'calendar_month_%d' % month

        mapping= {
            'day':      str(day),
            'weekdayname':  self.translate(domain=domain, msgid=weekdayname_msgid),
            'monthname':    self.translate(domain=domain, msgid=monthname_msgid),
            }

        if with_year:
            year = date.year()
            date_format_msgid = 'date_format'
            mapping['year'] = str(year)

        return self.translate(
            domain= domain,
            msgid= date_format_msgid,
            mapping= mapping
            )

    security.declareProtected('View', 'getFormatedLongDate')
    def getFormatedLongDate(self, date):
        """Get translated date with hour and minutes.
        Use UTC date"""
        
        local_date = date
        #local_zone = date.localZone()
        #local_date = date.toZone(local_zone)
        domain = I18N_DOMAIN
        date_format_msgid = 'date_long_format'
        mapping= {
            'day': '%02d' % local_date.day(),
            'month': '%02d' % local_date.month(),
            'year':  '%04d' % local_date.year(),
            'hour': '%02d:%02d' % (local_date.h_24(), local_date.minute()),
            }

        return self.translate(
            domain= domain,
            msgid= date_format_msgid,
            mapping= mapping
            )

    def getFormatedWeekDate(self, week, year):
        """ Get translated week date
        """

        domain = I18N_DOMAIN
        date_format_msgid = 'week_date_format'

        return self.translate(
            domain= domain,
            msgid= date_format_msgid,
            mapping= {
                'week': str(week),
                'year': str(year),
                }
            )


    def getFormatedMonthDate(self, month, year):
        """ Get translated month date
        """

        domain = I18N_DOMAIN
        date_format_msgid = 'month_date_format'
        monthname_msgid = 'calendar_month_%d' % month

        return self.translate(
            domain= domain,
            msgid= date_format_msgid,
            mapping= {
                'monthname':    self.translate(domain=domain, msgid=monthname_msgid),
                'year':         str(year),
                }
            )

    def getFormatedYearDate(self, year):
        """ Get translated year date
        """

        domain = I18N_DOMAIN
        date_format_msgid = 'year_date_format'

        return self.translate(
            domain= domain,
            msgid= date_format_msgid,
            mapping= {
                'year':         str(year),
                }
            )

    def getWeekFromDelta(self, week, year, delta=0):
        """ Return tuple week, year
        """

        # Get DateTime from week and year
        start_date, end_date = self.getDateRangeFromWeek(start_week=week, start_year=year)

        new_date = start_date + (7 * delta)

        return int(new_date.week()), int(new_date.year())

    def getMonthFromDelta(self, month, year, delta=0):
        """ Return tuple month, year
        """

        new_month = ((month + delta - 1) % 12) + 1
        new_year = year + (((month + delta) - 1) / 12)

        return new_month, new_year



    ##############
    ##Date Utils##
    ##############


    security.declareProtected(permissions.View, "getTsFromDatetime")
    def getTsFromDatetime(self, dt):
        """ Return the timestamp corresponding to the datetime"""
        return self.dt2ts(dt)

    security.declareProtected(permissions.View, "getTsFromDatetime")
    def getTsFromZDateTime(self, zdt):
        """ Return the timestamp corresponding to the (Zope) DateTime"""
        return self.zdt2ts(zdt)

    security.declareProtected(permissions.View, "getTsFromDatetime")
    def getZDateTimeFromts(self, ts):
        """ Return the Zope DateTime corresponding to the epoch timestamp"""
        return self.ts2zdt(int(ts))

    security.declareProtected(permissions.View, "getDatetimeFromTs")
    def getDatetimeFromTs(self, ts):
        """ Return the corresponding datetime from this timestamp """
        return self.ts2dt(int(ts))


    security.declareProtected(permissions.View, "addDays")
    def addDays(self, ts, days=1):
        """ Add a day count to timestamp
        """
        return int(ts) + (days*24*60*60)

    security.declareProtected(permissions.View, "addWeeks")
    def addWeeks(self, ts, weeks=1):
        """ Add a week count to timestamp
        """
        return self.addDays(ts, days=7*weeks)

    security.declareProtected(permissions.View, "deltaMonths")
    def deltaMonths(self, ts, months=0):
        """
        Add or remove months from delta
        """
        
        # Get current month and current year
        dt = self.ts2dt(ts)
        month = dt.month
        year = dt.year
        
        # Compute months from year zero
        months_from_year_zero = year * 12 + month + months
        
        # Compute new month and new year
        # Don't work with date before christ
        new_month = (months_from_year_zero - 1)%12 + 1
        new_year = (months_from_year_zero - 1)/12
        return self.dt2ts(datetime.datetime(new_year, new_month, 1, 0, 0))
        

    security.declareProtected(permissions.View, "addMonths")
    def addMonths(self, ts, months=1):
        """
        Add a month count to timestamp
        Go to the first day of the n next months
        """
        return self.deltaMonths(ts, months)
    
    security.declareProtected(permissions.View, "addYears")
    def addYears(self, ts, years=1):
        """
        Add a year count to timestamp
        """
        
        # Get current month and current year
        dt = self.ts2dt(ts)
        month = dt.month
        year = dt.year + years
        day = dt.day
        
        return self.dt2ts(datetime.datetime(year, month, day, 0, 0))

    security.declareProtected(permissions.View, "substractYears")
    def substractYears(self, ts, years=1):
        """Substract a year count from timestamp
        """
        
        # Get current month and current year
        dt = self.ts2dt(ts)
        month = dt.month
        year = dt.year - years
        day = dt.day
        
        return self.dt2ts(datetime.datetime(year, month, day, 0, 0))
    
    security.declareProtected(permissions.View, "substractMonths")
    def substractMonths(self, ts, months=1):
        """Substract a month count from timestamp
        Go to the first day of the n previous months
        """
        return self.deltaMonths(ts, -months)

    security.declareProtected(permissions.View, "substractWeeks")
    def substractWeeks(self, ts, weeks=1):
        """ Substract a week count from timestamp
        """
        return self.substractDays(ts, days=7*weeks)


    security.declareProtected(permissions.View, "substractDays")
    def substractDays(self, ts, days=1):
        """ Substract a day count to timestamp
        """
        return int(ts) - (days*24*60*60)

    security.declareProtected(permissions.View, "getTodayTs")
    def getTodayTs(self, ):
        """ Return today's timestamp
        """
        dt = datetime.datetime.now().replace(hour=0,minute=0,second=0)
        return self.dt2ts(dt)

    security.declareProtected(permissions.View, "setTsTime")
    def setTsTime(self, ts, hour=0, minute=0):
        """ Set hour and minute for a given datetime
        """
        dt = self.ts2dt(ts)
        dt = dt.replace(hour=hour,minute=minute,second=0)
        return self.dt2ts(dt)

    def buildPeriodList(self, ts_start, ts_end, ts_delta):
        """ Return a list of timestamp from ts_start to ts_end using ts_delta
        """
        return map(lambda x: x, range(ts_start, ts_end + 1, ts_delta))

    def buildMonthCalendar(self, year, month):
        """
        year: interger. The year of the calendar
        month: integer. Month number
        return a list of day number list : [ [0,0,1,2,3,4,5], [6,7,8 ...] ...]
        """
        calendar.setfirstweekday(calendar.MONDAY)
        return calendar.monthcalendar(year, month)

    def getTimeFromTs(self, ts):
        """ Return time from given timestamp
        """
        return self.ts2dt(ts).time()

    def getFirstValidDay(self, line):
        """ Return the first non 0 day number of a month_calendar line
        """
        for number in line:
            if number != 0:
                return number

    ##############
    ##Converters##
    ##############

    security.declarePrivate('dt2ts')
    def dt2ts(self, dt):
        """ Convert a datetime to an epoch timestamp """
        return int(time.mktime(dt.timetuple()))

    security.declarePrivate('ds2dt')
    def ts2dt(self, ts):
        """ Convert this epoch timestamp to a datetime
        """
        return datetime.datetime.fromtimestamp(int(ts))

    security.declarePrivate('ts2zdt')
    def ts2zdt(self, ts):
        """ Convert this epoch timestamp to a Zope DateTime
        """
        dt = self.ts2dt(ts)
        return DateTime(dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

    security.declarePrivate('zdt2dt')
    def zdt2dt(self, zdt):
        """ Convert a Zope DateTime to a datetime
        """
        return datetime.datetime(zdt.year(), zdt.month(), zdt.day(), zdt.hour(), zdt.minute(), int(zdt.second()))

    security.declarePrivate('zdt2ts')
    def zdt2ts(self, zdt):
        """ Convert a Zope DateTime to an epoch timestamp
        """
        dt = self.zdt2dt(zdt)
        return int(time.mktime(dt.timetuple()))

    #############################################
    # Get week day number of month
    # for example the third tuesday of the month
    #############################################

    security.declarePublic('weekDayNumberOfMonth')
    def weekDayNumberOfMonth(self, date):
        """
        Get week day number of the month
        for example the third tuesday of the month
        """
        day_month_number = date.day()
        day_week_number = date.dow()
        x = 1
        while day_month_number > 7:
            x += 1
            day_month_number -= 7

        return x



InitializeClass(DateManager)
