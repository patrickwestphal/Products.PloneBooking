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

$Id: testSecurity.py,v 1.4 2006/02/16 11:30:40 cbosse Exp $
"""

from DateTime import DateTime

import unittest2 as unittest

from Products.CMFCore.utils import getToolByName
from Products.PloneBooking.testing import PRODUCTS_PLONEBOOKING_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, setRoles, login

from Products.PloneBooking import BookingPermissions


class TestSecurity(unittest.TestCase):
    layer = PRODUCTS_PLONEBOOKING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.mbtool = getToolByName(self.portal, 'portal_membership')
        setRoles(self.portal, TEST_USER_ID, ['Member'])
        login(self.portal, TEST_USER_NAME)

    def test_check_permissions(self):
        """Check permissions
        """
        self.failUnless(
            not self.mbtool.checkPermission(
                BookingPermissions.AddBookingCenter, self.portal))
        self.failUnless(
            not self.mbtool.checkPermission(
                BookingPermissions.AddBookableObject, self.portal))
        self.failUnless(
            self.mbtool.checkPermission(
                BookingPermissions.AddBooking, self.portal))
