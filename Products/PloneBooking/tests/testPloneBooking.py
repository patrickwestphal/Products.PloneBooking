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

$Id: testPloneBooking.py,v 1.14 2006/02/16 11:30:40 cbosse Exp $
"""
import unittest2 as unittest

from Products.PloneBooking.testing import PRODUCTS_PLONEBOOKING_INTEGRATION_TESTING
from plone.app.testing import TEST_USER_ID, TEST_USER_NAME, setRoles, login


#Zope imports
from DateTime import DateTime

from Products.CMFCore.utils import getToolByName


class TestPloneBooking(unittest.TestCase):
    """test case for testing main PloneBooking functions"""
    layer = PRODUCTS_PLONEBOOKING_INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.btool = self.portal.portal_booking
        self.request = self.layer['request']
        self.wftool = self.portal.portal_workflow
        self.booking_center_id = 'booking_center'
        self.booking_center2_id = 'booking_center_two'
        self.bookable_obj_id = 'bookable_object'
        self.bookable_obj2_id = 'bookable_object_two'
        self.booking_id = 'booking'
        self.booking2_id = 'booking_two'

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        login(self.portal, TEST_USER_NAME)

        # set up empty content
        self.portal.invokeFactory(type_name='BookingCenter',
            id=self.booking_center_id)
        bc = self.portal[self.booking_center_id]
        bc.invokeFactory(type_name='BookableObject', id=self.bookable_obj_id)
        bo = bc[self.bookable_obj_id]
        self.wftool.doActionFor(bo, 'publish')
        bo.invokeFactory(type_name='Booking', id=self.booking_id)

        self.portal.invokeFactory(type_name='BookingCenter',
            id=self.booking_center2_id)
        bc2 = self.portal[self.booking_center2_id]
        bc2.invokeFactory(type_name='BookableObject',
            id=self.bookable_obj2_id)
        bo2 = bc2[self.bookable_obj2_id]
        self.wftool.doActionFor(bo2, 'publish')
        bo2.invokeFactory(type_name='Booking', id=self.booking2_id)

    def test_created_empty_booking_center(self):
        bc_id = self.booking_center_id
        self.failUnless(bc_id in self.portal.objectIds())
        self.assertEqual(self.portal[bc_id].Title(), '')
        self.assertEqual(self.portal[bc_id].getId(), bc_id)

    def test_edit_booking_center(self):
        title = 'A dummy Booking Center'
        description = 'A dummy description'
        bc = self.portal[self.booking_center_id]
        bc.edit(title=title, description=description)
        self.failUnless(bc.Title() == title,
            'Value is %s' % bc.Title())
        self.failUnless(bc.Description() == description,
            'Value is %s' % bc.Description())

    def test_created_bookable_object(self):
        bc = self.portal[self.booking_center_id]
        self.failUnless(self.bookable_obj_id in bc.objectIds())
        bookable_object = getattr(bc, self.bookable_obj_id)
        self.assertEqual(bookable_object.title, '')
        self.assertEqual(bookable_object.getId(), self.bookable_obj_id)

    def test_edit_bookable_object(self, ):
        title = 'A dummy Bookable Object'
        description = 'A dummy description'
        category = 'Dummy Category'

        bo = self.portal[self.booking_center_id][self.bookable_obj_id]
        bo.edit(title=title, description=description, category=category)
        self.failUnless(bo.Title() == title,
            'Value is %s' % bo.Title())
        self.failUnless(bo.Description() == description,
            'Value is %s' % bo.Description())
        self.failUnless(bo.getCategory() == category,
            'Value is %s' % bo.getCategory())

    def test_created_booking(self):
        bo = self.portal[self.booking_center_id][self.bookable_obj_id]
        self.failUnless(self.booking_id in bo.objectIds())
        booking = getattr(bo, self.booking_id)
        self.assertEqual(booking.title, '')
        self.assertEqual(booking.getId(), self.booking_id)

    def test_edit_booking(self, ):
        title = 'A dummy title'
        description = 'A dummy description'
        name = 'dummy name'
        phone = '0666996699'
        mail = 'dummy@dummy.com'
        booked_objects = ''
        start_date = DateTime()
        end_date = DateTime()

        booking = self.portal[self.booking_center_id]\
                [self.bookable_obj_id][self.booking_id]
        booking.edit(
            title=title,
            description=description,
            fullName=name,
            phone=phone,
            mail=mail,
            startDate=start_date,
            endDate=end_date,
        )

        self.failUnless(booking.Title()==title,
            'Value is %s' % booking.Title())
        self.failUnless(booking.Description()==description,
            'Value is %s' % booking.Description())
        self.failUnless(booking.getFullName()==name,
            'Value is %s' % booking.getFullName())
        self.failUnless(booking.getPhone()==phone,
            'Value is %s' % booking.getPhone())
        # self.failUnless(booking.getEmail()==mail,
        #     'Value is %s' % booking.getEmail())
        self.failUnless(booking.start() == start_date,
            'Value is %s' % booking.getStartDate())
        self.failUnless(booking.end() == end_date,
            'Value is %s' % booking.getEndDate())

    def test_do_booking(self):
        """
        Book an object from start_date to end_date
        """
        start_date = DateTime()
        end_date = DateTime()

        bo = self.portal[self.booking_center_id][self.bookable_obj_id]
        booking = bo[self.booking_id]

        booking.edit(startDate=start_date, endDate=end_date)
        self.failUnless(booking.getStartDate() == start_date,
            'Value is %s' % booking.getStartDate())
        self.failUnless(booking.getEndDate() == end_date,
            'Value is %s' % booking.getEndDate())
        # let's book an object
        booking.addReference(bo, 'is_booking')
        #raise NameError, '%s %s %s' % (bookable_object.UID(),
        #   booking.getBookedObject(bookable_object.UID()).UID(),
        #   booking.getBookedObject(booking.getBookedObjectUIDs()[0]).UID())

        self.failUnless(booking.getStartDate() == start_date,
            'Value is %s' % booking.getStartDate())
        self.failUnless(booking.getEndDate() == end_date,
            'Value is %s' % booking.getEndDate())
        self.failUnless(bo.UID() == booking.getBookedObjectUID(),
            'Uid of bookable obj (%s) not in  %s' % (bo.UID(),
            booking.getBookedObjectUID()))

    # test booking interface step by step
    def test_get_booked_object(self):
        start_date = DateTime()
        end_date = DateTime()

        bo = self.portal[self.booking_center_id][self.bookable_obj_id]
        booking = bo[self.booking_id]

        booking.edit(startDate=start_date, endDate=end_date)
        self.failUnless(booking.getBookedObject().UID() == bo.UID(),
            'Value is %s' % booking.getBookedObject().UID())

    def test_has_booked_object(self):
        bo = self.portal[self.booking_center_id][self.bookable_obj_id]
        bo_uid = bo.UID()
        booking = bo[self.booking_id]

        # defines some bookind date
        start_date = DateTime('1981/02/08')
        end_date = DateTime('1981/02/10')
        # no object must be booked in the booking
        self.failUnless(booking.hasBookedObject(start_date, end_date) == False,
            'WTF ?! Object is booked and it should not !')

        # book an object
        booking.edit(startDate=start_date, endDate=end_date)
        self.failUnless(booking.getBookedObject().UID() == bo.UID(),
            'Value is %s' % booking.getBookedObject().UID())

        #remove this there is a problem with doBooking
        booking.addReference(bo, 'is_booking')

        # object should be booked
        self.failUnless(booking.hasBookedObject(start_date, end_date) == True,
            'Object is not booked between %s and %s' %
            (booking.getStartDate(), booking.getEndDate()))

        # test another date where object is partially booked
        #start_date = DateTime(year = '1981', month = '02', day = '10', )
        #end_date = DateTime(year = '1981', month = '02', day = '11', )

        #desired end date is inside booked period
        start_date = DateTime('1981/02/07')
        end_date = DateTime('1981/02/10')
        self.failUnless(booking.hasBookedObject(start_date, end_date) == True,
            'Gosh ! Object is not booked between %s and %s' %
            (booking.getStartDate(), booking.getEndDate()))

        # desired start date is inside booked period
        start_date = DateTime('1981/02/09')
        end_date = DateTime('1981/02/12')
        self.failUnless(booking.hasBookedObject(start_date, end_date) == True,
            'Gosh ! Object is not booked between %s and %s' %
            (booking.getStartDate(), booking.getEndDate()))

        # desired period includes the booked period
        start_date = DateTime('1981/02/07')
        end_date = DateTime('1981/02/12')
        self.failUnless(booking.hasBookedObject(start_date, end_date) == True,
            'Gosh ! Object is not booked between %s and %s' %
            (booking.getStartDate(), booking.getEndDate()))


        # test other date where the object is not booked
        #start_date = DateTime(year = '1981', month = '02', day = '09', )
        #end_date = DateTime(year = '1981', month = '02', day = '12', )
        start_date = DateTime('1981/03/09')
        end_date = DateTime('1981/03/12')
        self.failUnless(booking.hasBookedObject(start_date, end_date) == False,
            'Gosh ! Object is booked !')

    def test_created_booking_center2(self):
        self.failUnless(self.booking_center2_id in self.portal.objectIds())
        booking_center = getattr(self.portal, self.booking_center2_id)
        self.assertEqual(booking_center.Title(), '')
        self.assertEqual(booking_center.getId(), self.booking_center2_id)

    def test_created_bookable_object2(self):
        bc2 = getattr(self.portal, self.booking_center2_id)
        self.failUnless(self.bookable_obj2_id in bc2.objectIds())
        bookable_object = getattr(bc2, self.bookable_obj2_id)
        self.assertEqual(bookable_object.getId(), self.bookable_obj2_id)
        self.assertEqual(bookable_object.Title(), '')

    def test_created_booking2(self):
        bc2 = getattr(self.portal, self.booking_center2_id)
        bo2 = getattr(bc2, self.bookable_obj2_id)
        self.failUnless(self.booking2_id in bo2.objectIds())
        booking = getattr(bo2, self.booking2_id)
        self.assertEqual(booking.title, '')
        self.assertEqual(booking.getId(), self.booking2_id)

    def test_edit_booking2(self):
        title = 'Another dummy title'
        description = 'Another dummy description'
        name = 'another dummy name'
        phone = '666996698'
        mail_address = 'toto@toto.com'
        start_date = DateTime()
        end_date = DateTime()

        bc2 = getattr(self.portal, self.booking_center2_id)
        bo2 = getattr(bc2, self.bookable_obj2_id)
        booking = getattr(bo2, self.booking2_id)
        # Edit content
        booking.edit(title=title, description=description, fullName=name,
            phone=phone, mail=mail_address, startDate=start_date,
            endDate=end_date)

        # test if everything is ok
        self.failUnless(booking.Title()==title,
            'Value is %s' % booking.Title())
        self.failUnless(booking.Description()==description,
            'Value is %s' % booking.Description())
        self.failUnless(booking.getFullName()==name,
            'Value is %s' % booking.getFullName())
        self.failUnless(booking.getPhone()==phone,
            'Value is %s' % booking.getPhone())
        # self.failUnless(booking.getEmail()==mail_address,
        #     'Value is %s' % booking.getEmail())
        self.failUnless(booking.start()==start_date,
            'Value is %s' % booking.getStartDate())
        self.failUnless(booking.end()==end_date,
            'Value is %s' % booking.getEndDate())

    def test_booking2(self,):
        booking_center = getattr(self.portal, self.booking_center2_id)
        bookable_object = getattr(booking_center, self.bookable_obj2_id)
        booking = getattr(bookable_object, self.booking2_id)
        start_date = DateTime('2005/02/08')
        end_date = DateTime('2005/02/14')
        booking.edit(title='Resa1', description='pas de description',
            fullName='Toto', phone='88666666', mail='toto@toto.com',
            startDate=start_date, endDate=end_date, wf_action='booked')

        #no error start and end are both earlier
        start_date = DateTime('2005/01/08')
        end_date = DateTime('2005/01/14')
        brains = booking_center.getBookingBrains(start_date=start_date,
            end_date=end_date)
        self.failUnless(len(brains) == 0,
            '%s is already booked. Brains Count : %s ' % (
                bookable_object.title_or_id(), len(brains)))

        #no error start and end are both later
        start_date = DateTime('2006/01/08')
        end_date = DateTime('2006/01/14')
        brains = booking_center.getBookingBrains(start_date=start_date,
            end_date=end_date)
        self.failUnless(len(brains) == 0,
            '%s is already booked. Brains Count : %s ' % (
                bookable_object.title_or_id(), len(brains)))

        # desired end date is inside booked period
        start_date = DateTime('2005/02/07')
        end_date = DateTime('2005/02/12')
        brains = booking_center.getBookingBrains(start_date=start_date,
            end_date=end_date)
        self.failUnless(len(brains) == 1,
            '%s is already booked. Brains Count : %s ' % (
                bookable_object.title_or_id(), len(brains)))

        # desired start date is inside booked period
        start_date = DateTime('2005/02/09')
        end_date = DateTime('2005/02/15')
        brains = booking_center.getBookingBrains(start_date=start_date,
            end_date=end_date)
        self.failUnless(len(brains) == 1,
            '%s is already booked. Brains Count : %s ' % (
                bookable_object.title_or_id(), len(brains)))

        # desired period includes the booked period
        start_date = DateTime('2005/02/07')
        end_date = DateTime('2005/02/15')
        brains = booking_center.getBookingBrains(start_date=start_date,
            end_date=end_date)
        self.failUnless(len(brains) == 1,
            '%s is already booked. Brains Count : %s ' % (
                bookable_object.title_or_id(), len(brains)))

        # booked period includes desired period
        start_date = DateTime('2005/02/09')
        end_date = DateTime('2005/02/12')
        brains = booking_center.getBookingBrains(start_date=start_date,
            end_date=end_date)
        self.failUnless(len(brains) == 1,
            '%s is already booked. Brains Count : %s ' % (bookable_object.title_or_id(), len(brains)))

    def test_get_xth_day_of_month(self,):
        bc2 = getattr(self.portal, self.booking_center2_id)
        bo2 = getattr(bc2, self.bookable_obj2_id)
        booking = getattr(bo2, self.booking2_id)
        title = 'A dummy title'
        description = 'A dummy description'
        name = 'dummy name'
        phone = '0666996699'
        mail = 'dummy@dummy.com'

        # normal test: should be every second monday of the month until
        # final_date
        start_date = DateTime('2005/08/29 09:00:00 GMT+2') #it is a monday
        end_date = DateTime('2005/09/01 18:00:00 GMT+2')
        final_date = DateTime('2005/10/29 09:00:00 GMT+2')
        periodicity_variable = 2
        result = booking.getXthDayOfMonth(start_date, end_date, final_date,
            periodicity_variable)

        # last start_date must not be later than final_date
        last_start_date = result[-1][0]
        self.failUnless(last_start_date<=final_date,
            '%s must be <= to %s' %(last_start_date, final_date))

        expected_result = [
            (DateTime('2005/09/12 09:00:00 GMT+2'),
                DateTime('2005/09/15 18:00:00 GMT+2')),
            (DateTime('2005/10/10 09:00:00 GMT+2'),
                DateTime('2005/10/13 18:00:00 GMT+2'))
        ]
        self.assertEquals(result, expected_result)

        # special test: should be every fifth monday of the month until
        # final_date
        # this is tricky because every month hasn't a fifth monday :p
        start_date = DateTime('2005/08/29 09:00:00 GMT+2') #it is a monday
        end_date = DateTime('2005/09/01 18:00:00 GMT+2')
        final_date = DateTime('2006/10/29 09:00:00 GMT+2')
        periodicity_variable = 5
        result = booking.getXthDayOfMonth(start_date, end_date, final_date,
            periodicity_variable)

        # last start_date must not be later than final_date
        last_start_date = result[-1][0]
        self.failUnless(last_start_date<=final_date,
            '%s must be <= to %s'%(last_start_date, final_date))

        expected_result = [
            (DateTime('2005/10/31 09:00:00 GMT+1'),
                DateTime('2005/11/03 18:00:00 GMT+1')),
            (DateTime('2006/01/30 09:00:00 GMT+1'),
                DateTime('2006/02/02 18:00:00 GMT+1')),
            (DateTime('2006/05/29 09:00:00 GMT+2'),
                DateTime('2006/06/01 18:00:00 GMT+2')),
            (DateTime('2006/07/31 09:00:00 GMT+2'),
                DateTime('2006/08/03 18:00:00 GMT+2')),
        ]
        self.assertEquals(result, expected_result)

        # special test: peridodicity_variable = 0
        start_date = DateTime('2005/08/29 09:00:00 GMT+2') #it is a monday
        end_date = DateTime('2005/09/01 18:00:00 GMT+2')
        final_date = DateTime('2006/10/29 09:00:00 GMT+2')
        periodicity_variable = 0
        result = booking.getXthDayOfMonth(start_date, end_date, final_date,
            periodicity_variable)
        expected_result = []
        self.assertEqual(result, expected_result)

    def test_create_periodic_bookings_type1(self,):
        booking_center_id = 'booking_center_id_xyz'
        bookable_obj_id = 'bookable_object_xyz'
        booking_id = 'booking_xyz'

        # create booking center
        self.portal.invokeFactory(type_name='BookingCenter',
            id=booking_center_id)
        booking_center = getattr(self.portal, booking_center_id)
        # create bookable object
        booking_center.invokeFactory(type_name='BookableObject',
            id=bookable_obj_id)
        bookable_object = getattr(booking_center, bookable_obj_id)
        self.wftool.doActionFor(bookable_object, 'publish')
        # create booking
        bookable_object.invokeFactory(type_name='Booking', id=booking_id)
        booking = getattr(bookable_object, booking_id)

        title = 'A dummy title'
        description = 'A dummy description'
        name = 'dummy name'
        phone = '0666996699'
        mail = 'dummy@dummy.com'
        startDate = DateTime('2005/08/29 09:00')
        endDate = DateTime('2005/08/29 10:00')
        end_periodicity = DateTime('2005/08/29 09:00')

        booking.edit(title=title, description=description, fullName=name,
            phone=phone, mail=mail, startDate=startDate, endDate=endDate)

        self.failUnless(not booking.isPeriodicBooking())

        # Activate Periodicity but end periodicity < start date
        periodicity_end_date = DateTime('2004/08/29 09:00')
        infos = booking.getPeriodicityInfos(periodicity_type=1,
            periodicity_end_date=periodicity_end_date)
        result = booking.createPeriodicBookings(periodicity_type=1,
            periodicity_end_date=periodicity_end_date)
        self.assertEquals(1, len(bookable_object.objectIds()))
        self.assertEquals(1, len(booking.getAllPeriodicBookingBrains()))
        self.failUnless(not booking.isPeriodicBooking())

        # test periodicity type 1, will create 4 bookings
        periodicity_end_date = DateTime('2005/09/29 09:00')
        infos = booking.getPeriodicityInfos(periodicity_type=1,
            periodicity_end_date=periodicity_end_date)
        result = booking.createPeriodicBookings(periodicity_type=1,
            periodicity_end_date=periodicity_end_date)
        self.assertEquals(5, len(bookable_object.objectIds()))
        self.assertEquals(5, len(booking.getAllPeriodicBookingBrains()))
        self.failUnless(booking.isPeriodicBooking())

    def test_create_periodic_bookings_type2(self,):
        booking_center_id = 'booking_center_id_wxy'
        bookable_obj_id = 'bookable_object_wxy'
        booking_id = 'booking_wxy'

        # create booking center
        self.portal.invokeFactory(type_name='BookingCenter',
            id=booking_center_id)
        booking_center = getattr(self.portal, booking_center_id)
        # create bookable object
        booking_center.invokeFactory(type_name='BookableObject',
            id=bookable_obj_id)
        bookable_object = getattr(booking_center, bookable_obj_id)
        self.wftool.doActionFor(bookable_object, 'publish')
        # create booking
        bookable_object.invokeFactory(type_name='Booking', id=booking_id)
        booking = getattr(bookable_object, booking_id)

        title = 'A dummy title'
        description = 'A dummy description'
        name = 'dummy name'
        phone = '0666996699'
        mail = 'dummy@dummy.com'
        startDate = DateTime('2005/08/29 09:00')
        endDate = DateTime('2005/08/29 10:00')
        booking.edit(title=title, description=description, fullName=name,
            phone=phone, mail=mail, startDate=startDate, endDate=endDate)

        self.failUnless(not booking.isPeriodicBooking())
        # test periodicity type 2, will create 4 bookings
        periodicity_end_date  = DateTime('2005/10/29 09:00')
        infos = booking.getPeriodicityInfos(periodicity_type=2,
            periodicity_end_date=periodicity_end_date, week_interval=2)
        result = booking.createPeriodicBookings(periodicity_type=2,
            periodicity_end_date=periodicity_end_date, week_interval=2)
        self.assertEquals(5, len(bookable_object.objectIds()))
        self.assertEquals(5, len(booking.getAllPeriodicBookingBrains()))
        self.failUnless(booking.isPeriodicBooking())

    def test_create_periodic_bookings_type3(self):
        booking_center_id = 'booking_center_id_vwx'
        bookable_obj_id = 'bookable_object_vwx'
        booking_id = 'booking_vwx'

        # create booking center
        self.portal.invokeFactory(type_name='BookingCenter',
            id=booking_center_id)
        booking_center = getattr(self.portal, booking_center_id)
        # create bookable object
        booking_center.invokeFactory(type_name='BookableObject',
            id=bookable_obj_id)
        bookable_object = getattr(booking_center, bookable_obj_id)
        self.wftool.doActionFor(bookable_object, 'publish')
        # create booking
        bookable_object.invokeFactory(type_name='Booking', id=booking_id)
        booking = getattr(bookable_object, booking_id)

        title = 'A dummy title'
        description = 'A dummy description'
        name = 'dummy name'
        phone = '0666996699'
        mail = 'dummy@dummy.com'
        startDate = DateTime('2005/08/12 09:00')
        endDate = DateTime('2005/08/13 10:00')
        booking.edit(title=title, description=description, fullName=name,
            phone=phone, mail=mail, startDate=startDate, endDate=endDate)

        self.failUnless(not booking.isPeriodicBooking())
        # test periodicity type 3, start and end date are not the same day,
        # will create 4 bookings
        periodicity_end_date = DateTime('2005/12/29 09:00')
        infos = booking.getPeriodicityInfos(periodicity_type=3,
            periodicity_end_date=periodicity_end_date)
        booking.edit(startDate=startDate, endDate=endDate)
        result = booking.createPeriodicBookings(periodicity_type=3,
            periodicity_end_date=periodicity_end_date)
        self.assertEquals(5, len(bookable_object.objectIds()))
        self.assertEquals(5, len(booking.getAllPeriodicBookingBrains()))
        self.failUnless(booking.isPeriodicBooking())

        # test periodicity type 3 with same day for start and end date, will
        # create 4 bookings
        start_date = DateTime('2005/08/14 09:00')
        end_date = DateTime('2005/08/14 12:00')
        booking.edit(startDate=start_date, endDate=end_date)
        infos = booking.getPeriodicityInfos(periodicity_type=3,
            periodicity_end_date=periodicity_end_date)
        result = booking.createPeriodicBookings(periodicity_type=3,
            periodicity_end_date=periodicity_end_date)
        self.assertEquals(9, len(bookable_object.objectIds()))
        self.assertEquals(9, len(booking.getAllPeriodicBookingBrains()))
        self.failUnless(booking.isPeriodicBooking())

    def test_get_interval_of_minutes_group_keys(self):
        # Interval of 30 minutes
        interval = 30
        # Calendar begins at 8h and finish at 12h 2005/11/15
        start_dt = DateTime(2005,11,15,8,0,0)
        end_dt = DateTime(2005,11,15,12,0,0)
        expected = [(2005, 11, 15, x*interval) for x in range(16, 24)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt,
            interval)
        self.assertEquals(result, expected)

        # Booking : 2005/11/15 9h15-9h25
        start_dt = DateTime(2005,11,15,9,15,0)
        end_dt = DateTime(2005,11,15,9,25,0)
        expected = [(2005, 11, 15, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt,
            interval)
        self.assertEquals(result, expected)

        # Booking : 2005/11/15 9h00-9h30
        start_dt = DateTime(2005,11,15,9,00,0)
        end_dt = DateTime(2005,11,15,9,30,0)
        expected = [(2005, 11, 15, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt,
            interval)
        self.assertEquals(result, expected)

        # Booking : 2005/11/15 9h00-9h35
        start_dt = DateTime(2005,11,15,9,00,0)
        end_dt = DateTime(2005,11,15,9,35,0)
        expected = [(2005, 11, 15, 540), (2005, 11, 15, 570)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt,
            interval)
        self.assertEquals(result, expected)

        # Booking : 2005/11/15 8h55-9h30
        start_dt = DateTime(2005,11,15,8,55,0)
        end_dt = DateTime(2005,11,15,9,30,0)
        expected = [(2005, 11, 15, 510), (2005, 11, 15, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt,
            interval)
        self.assertEquals(result, expected)

        # Booking : 2005/11/15 8h30-9h30
        start_dt = DateTime(2005,11,15,8,30,0)
        end_dt = DateTime(2005,11,15,9,30,0)
        expected = [(2005, 11, 15, 510), (2005, 11, 15, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt,
            interval)
        self.assertEquals(result, expected)

        # Interval of 60 minutes
        interval = 60
        # Calendar begins at 22h 2005/11/14 and finish at 2h 2005/11/15
        start_dt = DateTime(2005,11,14,22,0,0)
        end_dt = DateTime(2005,11,15,2,0,0)
        expected = [(2005, 11, 14, x*interval) for x in range(22, 24)]
        expected.extend([(2005, 11, 15, x*interval) for x in range(0, 2)])
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt,
            interval)
        self.assertEquals(result, expected)

        # Booking : 2005/11/14 9h15-9h45
        start_dt = DateTime(2005,11,14,9,15,0)
        end_dt = DateTime(2005,11,14,9,45,0)
        expected = [(2005, 11, 14, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt,
            interval)
        self.assertEquals(result, expected)

        # Booking : 2005/11/14 9h00-10h00
        start_dt = DateTime(2005,11,14,9,0,0)
        end_dt = DateTime(2005,11,14,10,0,0)
        expected = [(2005, 11, 14, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt,
            interval)
        self.assertEquals(result, expected)

    def test_get_day_group_keys(self):
        # Booking : 2005/11/14 9h00-10h00
        start_dt = DateTime(2005,11,14,9,0,0)
        end_dt = DateTime(2005,11,14,10,0,0)
        expected = [(2005, 11, 14)]
        result = self.btool.getDayGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)

        # Booking : 2005/11/14 0h00-24h00
        start_dt = DateTime(2005,11,14,0,0,0)
        end_dt = DateTime(2005,11,15,0,0,0)
        expected = [(2005, 11, 14)]
        result = self.btool.getDayGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)

        # Booking : 2005/11/14 0h00-24h00
        start_dt = DateTime(2005,11,14,23,59,59)
        end_dt = DateTime(2005,11,15,0,0,30)
        expected = [(2005, 11, 14), (2005, 11, 15)]
        result = self.btool.getDayGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)

    def test_get_week_group_keys(self):
        # Booking : 2005/11/8 9h00 - 2005/11/9 18h00
        start_dt = DateTime(2005,11,8,9,0,0)
        end_dt = DateTime(2005,11,9,18,0,0)
        expected = [(2005, 45)]
        result = self.btool.getWeekGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)

        # Booking : 2005/11/7 0h00 - 2005/11/14 0h00
        start_dt = DateTime(2005,11,7,0,0,0)
        end_dt = DateTime(2005,11,14,0,0,0)
        expected = [(2005, 45)]
        result = self.btool.getWeekGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)

        # Booking : 2005/11/13 23h59:59 - 2005/11/14 0h00:01
        start_dt = DateTime(2005,11,13,23,59,59)
        end_dt = DateTime(2005,11,14,0,0,1)
        expected = [(2005, 45), (2005, 46)]
        result = self.btool.getWeekGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)

    def test_get_month_group_keys(self):
        # Booking : 2005/11/7 9h00 - 2005/11/9 18h00
        start_dt = DateTime(2005,11,7,9,0,0)
        end_dt = DateTime(2005,11,9,18,0,0)
        expected = [(2005, 11)]
        result = self.btool.getMonthGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)

        # Booking : 2005/11/1 0h00 - 2005/12/1 0h00
        start_dt = DateTime(2005,11,1,0,0,0)
        end_dt = DateTime(2005,12,1,0,0,0)
        expected = [(2005, 11)]
        result = self.btool.getMonthGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)

        # Booking : 2005/10/31 23h59:59 - 2005/11/01 0h00:01
        start_dt = DateTime(2005,10,31,23,59,59)
        end_dt = DateTime(2005,11,1,0,0,1)
        expected = [(2005, 10), (2005, 11)]
        result = self.btool.getMonthGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)

    def test_get_year_group_keys(self):
        # Booking : 2005/11/7 9h00 - 2005/11/9 18h00
        start_dt = DateTime(2005,11,7,9,0,0)
        end_dt = DateTime(2005,11,9,18,0,0)
        expected = [(2005)]
        result = self.btool.getYearGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)

        # Booking : 2005/1/1 0h00 - 2006/1/1 0h00
        start_dt = DateTime(2005,1,1,0,0,0)
        end_dt = DateTime(2006,1,1,0,0,0)
        expected = [(2005)]
        result = self.btool.getYearGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)

        # Booking : 2005/12/31 23h59:59 - 2006/1/1 0h00:01
        start_dt = DateTime(2005,12,31,23,59,59)
        end_dt = DateTime(2006,1,1,0,0,1)
        expected = [(2005), (2006)]
        result = self.btool.getYearGroupKeys(start_dt, end_dt)
        self.assertEquals(result, expected)

    def test_get_booking_brains(self):
        booking_center_id = 'booking_center_id_uvw'
        bookable_obj_id = 'bookable_object_uvw'
        booking_id = 'booking_uvw'

        # create booking center
        self.portal.invokeFactory(type_name='BookingCenter',
            id=booking_center_id)
        booking_center = getattr(self.portal, booking_center_id)
        # create bookable object
        booking_center.invokeFactory(type_name='BookableObject',
            id=bookable_obj_id)
        bookable_object = getattr(booking_center, bookable_obj_id)
        self.wftool.doActionFor(bookable_object, 'publish')
        # create booking
        bookable_object.invokeFactory(type_name='Booking', id=booking_id)
        booking = getattr(bookable_object, booking_id)

        # Booking in 2005/11/15 9:00 9:30
        start_date = DateTime(2005,11,15,9,0,0)
        end_date = DateTime(2005,11,15,9,30,0)
        booking.edit(startDate=start_date, endDate=end_date)
        brains = booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 1)

        # Test in 2005/11/15 9:05 9:25
        start_date = DateTime(2005,11,15,9,5,0)
        end_date = DateTime(2005,11,15,9,25,0)
        brains = booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 1)

        # Test in 2005/11/15 8:55 9:25
        start_date = DateTime(2005,11,15,8,55,0)
        end_date = DateTime(2005,11,15,9,25,0)
        brains = booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 1)

        # Test in 2005/11/15 9:05 9:35
        start_date = DateTime(2005,11,15,9,5,0)
        end_date = DateTime(2005,11,15,9,35,0)
        brains = booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 1)

        # Test in 2005/11/15 8:55 9:35
        start_date = DateTime(2005,11,15,8,55,0)
        end_date = DateTime(2005,11,15,9,35,0)
        brains = booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 1)

        # Test in 2005/11/15 8:30 9:00
        start_date = DateTime(2005,11,15,8,30,0)
        end_date = DateTime(2005,11,15,9,0,0)
        brains = booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 0)

        # Test in 2005/11/15 9:30 10:00
        start_date = DateTime(2005,11,15,9,30,0)
        end_date = DateTime(2005,11,15,10,0,0)
        brains = booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 0)
