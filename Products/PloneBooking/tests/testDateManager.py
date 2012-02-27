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
PloneBooking base test

$Id: testDateManager.py,v 1.7 2006/02/16 11:30:40 cbosse Exp $
"""

from DateTime import DateTime


import unittest2 as unittest

from Products.PloneBooking.testing import PRODUCTS_PLONEBOOKING_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, setRoles, login


class TestDateManager(unittest.TestCase):
    layer = PRODUCTS_PLONEBOOKING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.btool = self.portal.portal_booking

    def test_date_range_from_week(self):
        """Test method getDateRangeFromWeek
        """
        # Test week 7 in 2004
        start_date, end_date = self.btool.getDateRangeFromWeek(start_week=7,
            start_year=2004)
        self.assertEquals(DateTime(start_date.year(), start_date.month(),
            start_date.day()), DateTime(2004,2,9))
        self.assertEquals(end_date, DateTime(2004,2,15,23,59,59))

        # Test week 4 in 2005
        start_date, end_date = self.btool.getDateRangeFromWeek(start_week=4,
            start_year=2005)
        self.assertEquals(start_date, DateTime(2005,1,24,0,0,0))
        self.assertEquals(end_date, DateTime(2005,1,30,23,59,59))

        # Test week 7 to week 10 in 2004
        start_date, end_date = self.btool.getDateRangeFromWeek(start_week=7,
            start_year=2004, end_week=10)
        self.assertEquals(start_date, DateTime(2004,2,9))
        self.assertEquals(end_date, DateTime(2004,3,7,23,59,59))

    def test_date_range_from_month(self):
        """Test method getDateRangeFromMonth
        """
        # Test february 2004
        start_date, end_date = self.btool.getDateRangeFromMonth(start_month=2,
            start_year=2004)
        self.assertEquals(start_date, DateTime(2004,2,1))
        self.assertEquals(end_date, DateTime(2004,2,29,23,59,59))

        # Test february to march 2004
        start_date, end_date = self.btool.getDateRangeFromMonth(start_month=2,
            start_year=2004, end_month=3)
        self.assertEquals(start_date, DateTime(2004,2,1))
        self.assertEquals(end_date, DateTime(2004,3,31,23,59,59))

    def test_date_range_from_year(self):
        """Test method getDateRangeFromYear
        """
        # Test year 2004
        start_date, end_date = self.btool.getDateRangeFromYear(start_year=2004)
        self.assertEquals(start_date, DateTime(2004,1,1))
        self.assertEquals(end_date, DateTime(2005,1,1))

        # Test years 2004-2005
        start_date, end_date = self.btool.getDateRangeFromYear(
            start_year=2004, end_year=2005)
        self.assertEquals(start_date, DateTime(2004,1,1))
        self.assertEquals(end_date, DateTime(2006,1,1))

    def test_week_day_number_of_month(self):
        """test method weekDayNumberOfMonth
        """
        date = DateTime('2005/08/01')
        self.assertEquals(1, self.btool.weekDayNumberOfMonth(date))

        date = DateTime('2005/08/08')
        self.assertEquals(2, self.btool.weekDayNumberOfMonth(date))

        date = DateTime('2005/08/29')
        self.assertEquals(5, self.btool.weekDayNumberOfMonth(date))
