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
"""PloneBooking tests

$Id: PloneBookingTestCase.py,v 1.8 2006/02/16 11:31:53 cbosse Exp $
"""

__author__ = ''
__docformat__ = 'restructuredtext'

# Python imports
import time

# Zope imports
from Testing import ZopeTestCase
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Acquisition import aq_base

# CMF imports
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName

# Products imports
from Products.PloneBooking.Extensions.Install import install as installPloneBooking

# Plone imports
from Products.CMFPlone.tests import PloneTestCase


portal_name = PloneTestCase.portal_name
portal_owner = PloneTestCase.portal_owner
portal_member = 'portal_member'
portal_member2 = 'portal_member2'

class PloneBookingTestCase(PloneTestCase.PloneTestCase):
    """ PloneBooking test case based on a plone site"""

    def afterSetUp(self):
        # Tools shortcuts
        self.ttool = getToolByName(self.portal, 'portal_types')
        self.wftool = getToolByName(self.portal, 'portal_workflow')
        self.mbtool = getToolByName(self.portal, 'portal_membership')
        self.btool = getToolByName(self.portal, 'portal_booking')
        self.member_folder = self.mbtool.getHomeFolder(portal_member)
        # Add role reviewer to portal_member in member_folder
        self.member_folder.manage_addLocalRoles(portal_member, roles = ['Reviewer',])
    
    def createEmptyBookableObject(self, container, content_id = 'booking', wf_action=None):
        # return an empty bookable object
        container.invokeFactory(type_name='BookableObject', id=content_id)
        self.failUnless(content_id in container.objectIds())
        self.bookable_object = getattr(container, content_id)
        self.assertEqual(self.bookable_object.title, '')
        self.assertEqual(self.bookable_object.getId(), content_id)
        
        if wf_action is not None:
            self.wftool.doActionFor(self.bookable_object, wf_action)
        
        return self.bookable_object
    
    def createEmptyBooking(self, container, content_id = 'booking'):
        # return empty booking
        container.invokeFactory(type_name='Booking', id=content_id)
        self.failUnless(content_id in container.objectIds())
        self.booking = getattr(container, content_id)
        self.assertEqual(self.booking.title, '')
        self.assertEqual(self.booking.getId(), content_id)
        return self.booking
    
    def createEmptyBookingCenter(self, container, content_id='booking_center', ):
        # return an empty booking center
        container.invokeFactory(type_name='BookingCenter', id=content_id)
        self.failUnless(content_id in container.objectIds())
        self.booking_center = getattr(container, content_id)
        self.assertEqual(self.booking_center.Title(), '')
        self.assertEqual(self.booking_center.getId(), content_id)
        return self.booking_center
    
    def createBookingStructure(self, container, center_id = 'booking_center', 
                               object_id = 'bookable_object', booking_id = 'booking', ):
        # Content creation
        #create empty booking center
        self.booking_center = self.createEmptyBookingCenter(container, content_id=center_id)
        self.bookable_object = self.createEmptyBookableObject(self.booking_center, content_id=object_id)
        self.wftool.doActionFor(self.bookable_object, 'publish')
        self.booking = self.createEmptyBooking(self.bookable_object, content_id=booking_id)
        
    def doBooking(self, booking, bookable_object, start_date, end_date, ):
        """
          Booking a bookable object
        """
        booking.edit(startDate=start_date, endDate=end_date)
        self.failUnless(booking.getStartDate() == start_date, 
                        "Value is %s" % booking.getStartDate())
        self.failUnless(booking.getEndDate() == end_date, 
                        "Value is %s" % booking.getEndDate())
        # let's book an object
        booking.addReference(bookable_object, "is_booking")
        
        #raise NameError, "%s %s %s"%(bookable_object.UID(), booking.getBookedObject(bookable_object.UID()).UID(), booking.getBookedObject(booking.getBookedObjectUIDs()[0]).UID())
        
        self.failUnless(booking.getStartDate() == start_date, 
                        "Value is %s" % booking.getStartDate())
        self.failUnless(booking.getEndDate() == end_date, 
                        "Value is %s" % booking.getEndDate())
        self.failUnless((bookable_object.UID() == booking.getBookedObjectUID()), 
                        "Uid of bookable obj (%s) not in  %s" % (bookable_object.UID(), booking.getBookedObjectUID()))
        
        

    def beforeTearDown(self):
        # logout
        noSecurityManager()
    
    def loginAsPortalMember(self):
        '''Use if you need to manipulate an object as member.'''
        uf = self.portal.acl_users
        user = uf.getUserById(portal_member).__of__(uf)
        newSecurityManager(None, user)
        
    def loginAsPortalMember2(self):
        '''Use if you need to manipulate an object as member.'''
        uf = self.portal.acl_users
        user = uf.getUserById(portal_member2).__of__(uf)
        newSecurityManager(None, user)
        
    def loginAsPortalOwner(self):
        '''Use if you need to manipulate an object as portal owner.'''
        uf = self.app.acl_users
        user = uf.getUserById(portal_owner).__of__(uf)
        newSecurityManager(None, user)

def setupPloneBooking(app, quiet=0):
    get_transaction().begin()
    _start = time.time()
    portal = app.portal
    
    if not quiet: ZopeTestCase._print('Installing PloneBooking ... ')

    # login as manager
    user = app.acl_users.getUserById(portal_owner).__of__(app.acl_users)
    newSecurityManager(None, user)
    
    # add PloneBooking
    if hasattr(aq_base(portal), 'portal_booking'):
        ZopeTestCase._print('PloneBooking already installed ... ')
    else:
        installPloneBooking(portal)
    
    # Create portal member
    portal.portal_registration.addMember(portal_member, 'azerty', ['Member'])
    portal.portal_registration.addMember(portal_member2, 'azerty', ['Member'])
    
    # Log out
    noSecurityManager()
    get_transaction().commit()
    if not quiet: ZopeTestCase._print('done (%.3fs)\n' % (time.time()-_start,))

app = ZopeTestCase.app()
setupPloneBooking(app)
ZopeTestCase.close(app)
