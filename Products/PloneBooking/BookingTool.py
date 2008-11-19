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
    PloneBooking Tool
"""

__version__ = "$Revision: 1.25 $"
__author__  = ''
__docformat__ = 'restructuredtext'

# Python imports
import re
import os
import math
from types import StringType

# Zope imports
import Globals
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SpecialUsers import emergency_user
        
#from OFS.PropertyManager import PropertyManager
from DateTime import DateTime

# CMF imports
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore import permissions
from Products.CMFCore.ActionInformation import ActionInformation
from Products.CMFCore.Expression import Expression
from Products.CMFCore.utils import UniqueObject
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.public import Vocabulary

# PloneBooking imports
from Products.PloneBooking.BookingPermissions import AddBooking
from Products.PloneBooking.DateManager import DateManager
from Products.generator import i18n
from Products.PloneBooking.content.vocabulary import CALENDAR_VIEWS, VIEW_MODES, LISTING_VIEWS
from Products.PloneBooking.config import I18N_DOMAIN

# Constants
ESCAPE_CHARS_RE = r'[\t\r\n\"\']'
ESCAPE_CHARS = re.compile(ESCAPE_CHARS_RE)

class BookingTool(DateManager, UniqueObject, SimpleItem, ActionProviderBase):
    """
    Tool for PloneBooking
    """

    plone_tool = 1
    id = 'portal_booking'
    title = "Misc utilities for PloneBooking application"
    meta_type = "BookingTool"
    
    __implements__ = (ActionProviderBase.__implements__,
                      SimpleItem.__implements__, )

    
    manage_options = (ActionProviderBase.manage_options + SimpleItem.manage_options)
    security = ClassSecurityInfo()

    security.declarePublic('isBooked')
    def isBooked(self, b_start, b_end, start, end):
        """
        b_start: timestamp. Beginning date of booking
        b_end: timestamp. Ending date of booking
        start: timestamp. Beginning date of tested period
        end: timestamp. Ending date of tested period
     
        return is_booked: boolean
        """
        is_booked = False
    
        if b_start < start:
            if b_end > start:
                is_booked = True
        else:
            if b_end < end or b_start < end:
                is_booked = True
    
        return is_booked

    security.declarePublic('filterBookingBrains')
    def filterBookingBrains(self, booking_brains, start_date, end_date):
        """Returns brains  booked in interval of start date and end date
        """
        
        result = []
        for brain in booking_brains:
            booking_start_date = brain['start']
            booking_end_date = brain['end']
            is_booked = self.isBooked(booking_start_date, booking_end_date, start_date, end_date)
            if is_booked:
                result.append(brain)
        return result

    security.declarePublic('getPeriodicBookingBrains')
    def getAllPeriodicBookingBrains(self, booking_uid):
        """Returns periodic brains for a booking.
        """
        
        atool = getToolByName(self, 'archetype_tool')
        obj = atool.getObject(booking_uid)
        return obj.getAllPeriodicBookingBrains()
        
    security.declarePublic('cancelBooking')
    def cancelBooking(self, booking):
        """
          Delete the booking
        """

        request = self.REQUEST
        booking_id = booking.getId()
        booked_object = booking.getBookedObject()

        # Use manager role to change permissions
        current_user = getSecurityManager().getUser()
        newSecurityManager(request, emergency_user)
        
        # delete booking
        booked_object.manage_delObjects([booking_id,])
        
        # Restore current user permission
        newSecurityManager(request, current_user)
    
    security.declarePublic('getBookingDefaultTitle')    
    def getBookingDefaultTitle(self):
        """Returns booking default title.
        It is used when no title is defined on booking"""
        
        msg_id = "label_booking"
        msg_default = "Booking"
        return i18n.translate(I18N_DOMAIN, msg_id, context=self, default=msg_default)
        
    security.declarePublic('buildFilter')
    def buildFilter(self, **kwargs):
        """Returns a dictionnary using kwargs.
        Removes None values."""
        
        result = {}
        for key, value in kwargs.items():
            if value is not None:
                result[key] = value
        return result
    
    security.declarePublic('getIntervalOfMinutesGroupKeys')
    def getIntervalOfMinutesGroupKeys(self, start_date, end_date, interval):
        """"""
        
        group_keys = []
        interval_in_seconds = interval * 60.0
        
        # Round start date and end date to interval
        start_ts = self.zdt2ts(start_date)
        start_ts_from_zero = self.zdt2ts(DateTime(start_date.year(), start_date.month(), start_date.day()))
        new_start_ts = start_ts_from_zero + math.floor((start_ts - start_ts_from_zero) / interval_in_seconds ) * interval_in_seconds
        new_start_dt = self.ts2zdt(new_start_ts)
        end_ts = self.zdt2ts(end_date)
        end_ts_from_zero = self.zdt2ts(DateTime(end_date.year(), end_date.month(), end_date.day()))
        new_end_ts = end_ts_from_zero + math.ceil((end_ts - end_ts_from_zero) / interval_in_seconds) * interval_in_seconds
        nb_intervals = int((new_end_ts - new_start_ts) / interval_in_seconds)
        
        for i in range(0, nb_intervals):
            key_date = new_start_dt + (i * (interval_in_seconds / 86400.0))
            key_interval = (key_date.hour() * 60 + key_date.minute())
            group_keys.append((key_date.year(), key_date.month(), key_date.day(), key_interval))
        return group_keys
    
    security.declarePublic('getDayGroupKeys')
    def getDayGroupKeys(self, start_date, end_date):
        """"""
        
        group_keys = []
        interval_in_seconds = 86400.0
        
        # Round start date and end date to day
        new_start_ts = self.zdt2ts(DateTime(start_date.year(), start_date.month(), start_date.day()))
        new_start_dt = self.ts2zdt(new_start_ts)
        end_ts = self.zdt2ts(end_date)
        end_ts_from_zero = self.zdt2ts(DateTime(end_date.year(), end_date.month(), end_date.day()))
        new_end_ts = end_ts_from_zero + math.ceil((end_ts - end_ts_from_zero) / interval_in_seconds) * interval_in_seconds
        nb_days = int((new_end_ts - new_start_ts) / interval_in_seconds)
        
        for i in range(0, nb_days):
            key_date = new_start_dt + i
            group_keys.append((key_date.year(), key_date.month(), key_date.day()))
        return group_keys
    
    security.declarePublic('getWeekGroupKeys')
    def getWeekGroupKeys(self, start_date, end_date):
        """"""
        
        group_keys = []
        interval_in_seconds = 7 * 86400.0
        
        # Assume monday is the first day of the week
        # and sunday is the last day of the week
        new_start_dt = DateTime(start_date.year(), start_date.month(), start_date.day()) - (start_date.dow() - 1) % 7 # Get the monday before start_date
        new_start_ts = self.zdt2ts(new_start_dt)
        end_ts = self.zdt2ts(end_date)
        end_ts_from_zero = self.zdt2ts((DateTime(end_date.year(), end_date.month(), end_date.day())  - (end_date.dow() - 1) % 7))
        new_end_ts = end_ts
        if end_ts != end_ts_from_zero:
            new_end_ts += interval_in_seconds
     
        nb_weeks = int((new_end_ts - new_start_ts) / interval_in_seconds)
     
        for i in range(0, nb_weeks):
            key_date = new_start_dt + (i * 7)
            group_keys.append((key_date.year(), key_date.week()))
        return group_keys
    
    security.declarePublic('getMonthGroupKeys')
    def getMonthGroupKeys(self, start_date, end_date):
        """"""
        
        group_keys = []
        
        end_ts = self.zdt2ts(end_date)
        end_ts_from_zero = self.zdt2ts(DateTime(end_date.year(), end_date.month(), 1))
        end_year = end_date.year()
        end_month = end_date.month()
        if end_ts == end_ts_from_zero:
            if end_month == 1:
                end_month = 12
                end_year -= 1
            else:
                end_month -= 1
        
        # Round start date and end date to month
        start_months = (start_date.year() * 12 + start_date.month())
        end_months = (end_year * 12 + end_month)
        nb_months = end_months - start_months + 1
        
        for i in range(0, nb_months):
            new_month = (start_months + i - 1)%12 + 1
            new_year = (start_months + i - 1)/12
            group_keys.append((new_year, new_month))
        return group_keys
    
    security.declarePublic('getYearGroupKeys')
    def getYearGroupKeys(self, start_date, end_date):
        """"""
        
        group_keys = []
        
        end_ts = self.zdt2ts(end_date)
        end_ts_from_zero = self.zdt2ts(DateTime(end_date.year(), 1, 1))
        end_year = end_date.year()
        
        if end_ts == end_ts_from_zero:
            end_year -= 1
        new_start_dt, new_end_dt = self.getDateRangeFromYear(start_date.year(), end_year)
        first_year = new_start_dt.year()
        nb_years = new_end_dt.year() - first_year
        
        for i in range(0, nb_years):
            group_keys.append(first_year + i)
        return group_keys
    
    
    security.declarePublic('getViewModeDisplayList')
    def getViewModeDisplayList(self):
        """Returns view mode display list"""
        
        return VIEW_MODES
    
    security.declarePublic('getListingViewDisplayList')
    def getListingViewDisplayList(self):
        """Returns listing view display list"""
        
        return LISTING_VIEWS

    security.declarePublic('getCalendarViewDisplayList')
    def getCalendarViewDisplayList(self):
        """Returns listing view display list"""
        
        return CALENDAR_VIEWS
    
    security.declarePublic('getViewModeVocabulary')
    def getViewModeVocabulary(self):
        """Returns view mode vocabulary"""
        
        dl = self.getViewModeDisplayList()
        return Vocabulary(dl, self, I18N_DOMAIN)
    
    security.declarePublic('getListingViewVocabulary')
    def getListingViewVocabulary(self):
        """Returns listing view vocabulary"""
        
        dl = self.getListingViewDisplayList()
        return Vocabulary(dl, self, I18N_DOMAIN)

    security.declarePublic('getCalendarViewVocabulary')
    def getCalendarViewVocabulary(self):
        """Returns listing view vocabulary"""
        
        dl = self.getCalendarViewDisplayList()
        return Vocabulary(dl, self, I18N_DOMAIN)
    
    def escapeText(self, text):
        """Escape chars on text. It can be very useful to use text in javascript
        
        @param text: text to escape
        """
    
        # If matching escapable char call this function
        def escape(match):
            """Escape chars"""
    
            char = match.group(0)
    
            # Special chars already escaped. Apply double escape
            if char== '\n':
                return '\\n'
            elif char== '\r':
                return '\\n'
            elif char== '\t':
                return '\\t'
    
            return '\\%s' % char
    
        # Text must be an encoded string
        if type(text) != StringType and type(text) != type(u''):
            raise ValueError, "You can just escape strings: %s" % str(text)
        
        # Escape text
        return ESCAPE_CHARS.sub(escape, text)
    
InitializeClass(BookingTool)
