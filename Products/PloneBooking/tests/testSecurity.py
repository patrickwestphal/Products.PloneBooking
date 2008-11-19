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

#Zope imports
from DateTime import DateTime

from common import *
from Products.CMFCore.utils import getToolByName

tests = []
class TestSecurity(PloneBookingTestCase):

    def testCheckPermissions(self):
        """
        Check permissions
        """
        
        self.loginAsPortalMember()
        
        # Check roles on member folder
        permissions = (
            BookingPermissions.AddBookingCenter,
            BookingPermissions.AddBookableObject,
            )
        
        for permission in permissions:
            self.failUnless(not self.mbtool.checkPermission(permission ,self.portal))
            self.failUnless(self.mbtool.checkPermission(permission ,self.member_folder))
        
        permissions = (
            BookingPermissions.AddBooking,
            )
        
        for permission in permissions:
            self.failUnless(self.mbtool.checkPermission(permission ,self.portal))
        
        self.logout()
        
        
        
tests.append(TestSecurity)

if __name__ == '__main__':
    framework()
else:
    # While framework.py provides its own test_suite()
    # method the testrunner utility does not.
    import unittest
    def test_suite():
        suite = unittest.TestSuite()
        for test in tests:
            suite.addTest(unittest.makeSuite(test))
        return suite

