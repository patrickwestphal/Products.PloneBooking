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

#Zope imports
from DateTime import DateTime

from common import *
from Products.CMFCore.utils import getToolByName

tests = []
class TestPloneBooking(PloneBookingTestCase):

    def testCreateBookingCenter(self, ):
        """
        """
        self.loginAsPortalMember()
        self.booking_center = self.createEmptyBookingCenter(self.member_folder)

    def testEditBookingCenter(self, ):
        """
        Editing Booking Center
        """

        self.loginAsPortalMember()
        self.createEmptyBookingCenter(self.member_folder)
        title = "A dummy Booking Center"
        description = "A dummy description"

        # Edit content
        self.booking_center.edit(title = title, description = description)
        # test if everything is ok
        self.failUnless(self.booking_center.Title() == title,
                        "Value is %s" % self.booking_center.Title())
        self.failUnless(self.booking_center.Description() == description,
                        "Value is %s" % self.booking_center.Description())

    def testCreateBookableObject(self, ):
        """
        """
        self.loginAsPortalMember()
        self.createEmptyBookingCenter(self.member_folder)
        self.createEmptyBookableObject(self.booking_center)

    def testEditBookableObject(self, ):
        """
        Editing Bookable Object
        """
        self.loginAsPortalMember()
        self.createEmptyBookingCenter(self.member_folder)
        self.createEmptyBookableObject(self.booking_center)
        title = "A dummy Bookable Object"
        description = "A dummy description"
        category = 'Dummy Category'


        # Edit content
        self.bookable_object.edit(title = title,
                                  description = description,
                                  category= category)
        # test if everything is ok
        self.failUnless(self.bookable_object.Title() == title,
                        "Value is %s" % self.bookable_object.Title())
        self.failUnless(self.bookable_object.Description() == description,
                        "Value is %s" % self.bookable_object.Description())
        self.failUnless(self.bookable_object.getCategory() == category,
                        "Value is %s" % self.bookable_object.getCategory())

    def testCreateBooking(self, ):
        """
        """
        self.loginAsPortalMember()
        self.booking_center = self.createEmptyBookingCenter(self.member_folder)

        self.bookable_object = self.createEmptyBookableObject(self.booking_center, wf_action='publish')
        self.booking = self.createEmptyBooking(self.bookable_object)

    def testEditBooking(self, ):
        """
        Editing Booking
        """
        self.loginAsPortalMember()
        self.createEmptyBookingCenter(self.member_folder)
        self.createEmptyBookableObject(self.booking_center, wf_action='publish')
        self.createEmptyBooking(self.bookable_object)
        title = 'A dummy title'
        description = 'A dummy description'
        name = 'dummy name'
        phone = '0666996699'
        mail = 'dummy@dummy.com'
        bookedObjects = ''
        startDate = DateTime()
        endDate = DateTime()

        # Edit content
        self.booking.edit(title = title,
                          description = description,
                          fullName = name,
                          phone = phone,
                          mail = mail,
                          startDate = startDate,
                          endDate = endDate,
                         )

        # test if everything is ok
        self.failUnless(self.booking.Title() == title,
                        "Value is %s" % self.booking.Title())
        self.failUnless(self.booking.Description() == description,
                        "Value is %s" % self.booking.Description())
        self.failUnless(self.booking.getFullName() == name,
                        "Value is %s" % self.booking.getFullName())
        self.failUnless(self.booking.getPhone() == phone,
                        "Value is %s" % self.booking.getPhone())

        # no booked objects

        self.failUnless(self.booking.start() == startDate,
                        "Value is %s" % self.booking.getStartDate())
        self.failUnless(self.booking.end() == endDate,
                        "Value is %s" % self.booking.getEndDate())

    def testBookingStructure(self, ):
        """
          Create booking center, object and booking
        """
        self.loginAsPortalMember()
        self.createBookingStructure(self.member_folder)

    def testDoBooking(self, ):
        """
          Book an object from startDate to endDate
        """
        self.loginAsPortalMember()
        self.createBookingStructure(self.member_folder)
        self.doBooking(booking = self.booking,
                       bookable_object = self.bookable_object,
                       start_date = DateTime(),
                       end_date = DateTime(),
                      )


    # test booking interface step by step
    def testGetBookedObject(self, ):
        """
        """
        self.loginAsPortalMember()
        # a structure with a an object that is booked
        self.createBookingStructure(self.member_folder)
        self.doBooking(booking = self.booking,
                       bookable_object = self.bookable_object,
                       start_date = DateTime(),
                       end_date = DateTime(),
                      )
        self.failUnless(self.booking.getBookedObject().UID() == self.bookable_object.UID(),
                        "Value is %s" % self.booking.getBookedObject().UID())


    def testHasBookedObject(self, ):
        """
        """
        self.loginAsPortalMember()
        self.createBookingStructure(self.member_folder)
        object_uid = self.bookable_object.UID()
        # defines some bookind date
        start_date = DateTime('1981/02/08')
        end_date = DateTime('1981/02/10')
        #end_date = DateTime(year = '1981', month = '02', day = '10', )
        # no object must be booked in the booking
        self.failUnless( self.booking.hasBookedObject(start_date, end_date) == False,
                        "WTF ?! Object is booked and it should not !")

        # book an object
        self.doBooking(booking = self.booking,
                       bookable_object = self.bookable_object,
                       start_date = start_date,
                       end_date = end_date,
                      )

        #remove this there is a problem with doBooking
        self.booking.addReference(self.bookable_object, "is_booking")

        # object should be booked
        self.failUnless( self.booking.hasBookedObject(start_date, end_date) == True,
                        "Object is not booked between %s and %s" %
                          (self.booking.getStartDate(), self.booking.getEndDate())
                       )

        # test another date where object is partially booked

        #start_date = DateTime(year = '1981', month = '02', day = '10', )
        #end_date = DateTime(year = '1981', month = '02', day = '11', )

        #desired end date is inside booked period
        start_date = DateTime('1981/02/07')
        end_date = DateTime('1981/02/10')
        self.failUnless(self.booking.hasBookedObject(start_date, end_date) == True,
                        "Gosh ! Object is not booked between %s and %s" %
                        (self.booking.getStartDate(), self.booking.getEndDate()))

        # desired start date is inside booked period
        start_date = DateTime('1981/02/09')
        end_date = DateTime('1981/02/12')
        self.failUnless(self.booking.hasBookedObject(start_date, end_date) == True,
                        "Gosh ! Object is not booked between %s and %s" %
                        (self.booking.getStartDate(), self.booking.getEndDate()))

        # desired period includes the booked period
        start_date = DateTime('1981/02/07')
        end_date = DateTime('1981/02/12')
        self.failUnless(self.booking.hasBookedObject(start_date, end_date) == True,
                        "Gosh ! Object is not booked between %s and %s" %
                        (self.booking.getStartDate(), self.booking.getEndDate()))


        # test other date where the object is not booked
        #start_date = DateTime(year = '1981', month = '02', day = '09', )
        #end_date = DateTime(year = '1981', month = '02', day = '12', )
        start_date = DateTime('1981/03/09')
        end_date = DateTime('1981/03/12')
        self.failUnless( self.booking.hasBookedObject(start_date, end_date) == False,
                        "Gosh ! Object is booked !")


    def createBookingCenter2(self, container, content_id='content_id', title=''):
        """
        """
        # return an booking center
        container.invokeFactory(type_name='BookingCenter', id=content_id)
        self.failUnless(content_id in container.objectIds())
        booking_center = getattr(container, content_id)
        self.assertEqual(booking_center.Title(), '')
        self.assertEqual(booking_center.getId(), content_id)
        return booking_center


    def createBookableObject2(self, container, content_id = 'bookable_obj', title='', wf_action=None):
        # return an bookable object
        container.invokeFactory(type_name='BookableObject', id=content_id)
        self.failUnless(content_id in container.objectIds())
        bookable_object = getattr(container, content_id)
        self.assertEqual(bookable_object.getId(), content_id)
        self.assertEqual(bookable_object.Title(), '')

        if wf_action is not None:
            self.wftool.doActionFor(bookable_object, wf_action)

        return bookable_object

    def createBooking2(self, container, content_id='booking', title='', description='', name='', phone='', mail='toto@toto.com', bookable_objects=(), start_date=DateTime(), end_date=DateTime(), wf_action=None):
        """
        """

        container.invokeFactory(type_name='Booking', id=content_id)
        self.failUnless(content_id in container.objectIds())
        booking = getattr(container, content_id)
        self.assertEqual(booking.title, '')
        self.assertEqual(booking.getId(), content_id)
        # Edit content
        booking.edit(title = title,
                     description = description,
                     fullName = name,
                     phone = phone,
                     mail = mail,
                     startDate = start_date,
                     endDate = end_date,
                    )

        # test if everything is ok
        self.failUnless(booking.Title() == title,
                        "Value is %s" % booking.Title())
        self.failUnless(booking.Description() == description,
                        "Value is %s" % booking.Description())
        self.failUnless(booking.getFullName() == name,
                        "Value is %s" % booking.getFullName())
        self.failUnless(booking.getPhone() == phone,
                        "Value is %s" % booking.getPhone())
        self.failUnless(booking.start() == start_date,
                        "Value is %s" % booking.getStartDate())
        self.failUnless(booking.end() == end_date,
                        "Value is %s" % booking.getEndDate())
        return booking

    def testBookingCreation2(self,):
        """
        """
        self.loginAsPortalMember()
        booking_center = self.createBookingCenter2(self.member_folder)
        bookable_object = self.createBookableObject2(booking_center, wf_action='publish')
        start_date = DateTime('2005/02/08')
        end_date = DateTime('2005/02/14')
        booking = self.createBooking2(bookable_object, title='Resa1', description='pas de description', name='Toto', phone='88666666', mail='toto@toto.com', start_date=start_date, end_date=end_date, wf_action='booked')


        #no error start and end are both earlier
        start_date = DateTime('2005/01/08')
        end_date = DateTime('2005/01/14')
        brains = booking_center.getBookingBrains(start_date=start_date, end_date=end_date)
        self.failUnless(len(brains) == 0,
                        "%s is already booked. Brains Count : %s " % (bookable_object.title_or_id(), len(brains)))

        #no error start and end are both later
        start_date = DateTime('2006/01/08')
        end_date = DateTime('2006/01/14')
        brains = booking_center.getBookingBrains(start_date=start_date, end_date=end_date)
        self.failUnless(len(brains) == 0,
                        "%s is already booked. Brains Count : %s " % (bookable_object.title_or_id(), len(brains)))

        # desired end date is inside booked period
        start_date = DateTime('2005/02/07')
        end_date = DateTime('2005/02/12')
        brains = booking_center.getBookingBrains(start_date=start_date, end_date=end_date)
        self.failUnless(len(brains) == 1,
                        "%s is already booked. Brains Count : %s " % (bookable_object.title_or_id(), len(brains)))

        # desired start date is inside booked period
        start_date = DateTime('2005/02/09')
        end_date = DateTime('2005/02/15')
        brains = booking_center.getBookingBrains(start_date=start_date, end_date=end_date)
        self.failUnless(len(brains) == 1,
                        "%s is already booked. Brains Count : %s " % (bookable_object.title_or_id(), len(brains)))

        # desired period includes the booked period
        start_date = DateTime('2005/02/07')
        end_date = DateTime('2005/02/15')
        brains = booking_center.getBookingBrains(start_date=start_date, end_date=end_date)
        self.failUnless(len(brains) == 1,
                        "%s is already booked. Brains Count : %s " % (bookable_object.title_or_id(), len(brains)))

        # booked period includes desired period
        start_date = DateTime('2005/02/09')
        end_date = DateTime('2005/02/12')
        brains = booking_center.getBookingBrains(start_date=start_date, end_date=end_date)
        self.failUnless(len(brains) == 1,
                        "%s is already booked. Brains Count : %s " % (bookable_object.title_or_id(), len(brains)))

    def testGetXthDayOfMonth(self,):
        """
        """
        self.loginAsPortalOwner()
        self.createEmptyBookingCenter(self.member_folder)
        self.createEmptyBookableObject(self.booking_center, wf_action='publish')
        self.createEmptyBooking(self.bookable_object)
        title = 'A dummy title'
        description = 'A dummy description'
        name = 'dummy name'
        phone = '0666996699'
        mail = 'dummy@dummy.com'

        #normal test: should be every second monday of the month until final_date
        start_date = DateTime('2005/08/29 09:00:00 GMT+2') #it is a monday
        end_date = DateTime('2005/09/01 18:00:00 GMT+2')
        final_date = DateTime('2005/10/29 09:00:00 GMT+2')
        periodicity_variable = 2
        result = self.booking.getXthDayOfMonth(start_date, end_date, final_date, periodicity_variable)

        # last start_date must not be later than final_date
        last_start_date = result[-1][0]
        self.failUnless(last_start_date <= final_date, '%s must be <= to %s'%(last_start_date, final_date))

        expected_result = [(DateTime('2005/09/12 09:00:00 GMT+2'), DateTime('2005/09/15 18:00:00 GMT+2')), (DateTime('2005/10/10 09:00:00 GMT+2'), DateTime('2005/10/13 18:00:00 GMT+2'))]
        self.assertEquals(result, expected_result)

        #special test: should be every fifth monday of the month until final_date
        # this is tricky because every month hasn't a fifth monday :p
        start_date = DateTime('2005/08/29 09:00:00 GMT+2') #it is a monday
        end_date = DateTime('2005/09/01 18:00:00 GMT+2')
        final_date = DateTime('2006/10/29 09:00:00 GMT+2')
        periodicity_variable = 5
        result = self.booking.getXthDayOfMonth(start_date, end_date, final_date, periodicity_variable)

        # last start_date must not be later than final_date
        last_start_date = result[-1][0]
        self.failUnless(last_start_date <= final_date, '%s must be <= to %s'%(last_start_date, final_date))

        expected_result = [
                            (DateTime('2005/10/31 09:00:00 GMT+1'),
                             DateTime('2005/11/03 18:00:00 GMT+1')
                            ),
                            (DateTime('2006/01/30 09:00:00 GMT+1'),
                             DateTime('2006/02/02 18:00:00 GMT+1')
                            ),
                            (DateTime('2006/05/29 09:00:00 GMT+2'),
                             DateTime('2006/06/01 18:00:00 GMT+2')
                            ),
                            (DateTime('2006/07/31 09:00:00 GMT+2'),
                             DateTime('2006/08/03 18:00:00 GMT+2')
                            ),
                           ]
        self.assertEquals(result, expected_result)

        #special test: peridodicity_variable = 0
        start_date = DateTime('2005/08/29 09:00:00 GMT+2') #it is a monday
        end_date = DateTime('2005/09/01 18:00:00 GMT+2')
        final_date = DateTime('2006/10/29 09:00:00 GMT+2')
        periodicity_variable = 0
        result = self.booking.getXthDayOfMonth(start_date, end_date, final_date, periodicity_variable)
        expected_result = []
        self.assertEqual(result, expected_result)

    def testCreatePeriodicBookingsType1(self,):
        """
        """
        self.loginAsPortalOwner()
        self.createEmptyBookingCenter(self.member_folder)
        self.createEmptyBookableObject(self.booking_center, wf_action='publish')
        self.createEmptyBooking(self.bookable_object)
        title = 'A dummy title'
        description = 'A dummy description'
        name = 'dummy name'
        phone = '0666996699'
        mail = 'dummy@dummy.com'
        startDate = DateTime('2005/08/29 09:00')
        endDate = DateTime('2005/08/29 10:00')
        end_periodicity = DateTime('2005/08/29 09:00')
        self.booking.edit(title = title,
                          description = description,
                          fullName = name,
                          phone = phone,
                          mail = mail,
                          startDate = startDate,
                          endDate = endDate,
                          )

        self.failUnless(not self.booking.isPeriodicBooking())
        # Activate Periodicity but end periodicity < start date
        periodicity_end_date = DateTime('2004/08/29 09:00')
        infos = self.booking.getPeriodicityInfos(periodicity_type=1, periodicity_end_date=periodicity_end_date)
        result = self.booking.createPeriodicBookings(periodicity_type=1, periodicity_end_date=periodicity_end_date)
        self.assertEquals(1, len(self.bookable_object.objectIds()))
        self.assertEquals(1, len(self.booking.getAllPeriodicBookingBrains()))
        self.failUnless(not self.booking.isPeriodicBooking())

        # test periodicity type 1, will create 4 bookings
        periodicity_end_date = DateTime('2005/09/29 09:00')
        infos = self.booking.getPeriodicityInfos(periodicity_type=1, periodicity_end_date=periodicity_end_date)
        result = self.booking.createPeriodicBookings(periodicity_type=1, periodicity_end_date=periodicity_end_date)
        self.assertEquals(5, len(self.bookable_object.objectIds()))
        self.assertEquals(5, len(self.booking.getAllPeriodicBookingBrains()))
        self.failUnless(self.booking.isPeriodicBooking())

        self.logout()

    def testCreatePeriodicBookingsType2(self,):
        """
        """
        self.loginAsPortalOwner()
        self.createEmptyBookingCenter(self.member_folder)
        self.createEmptyBookableObject(self.booking_center, wf_action='publish')
        self.createEmptyBooking(self.bookable_object)
        title = 'A dummy title'
        description = 'A dummy description'
        name = 'dummy name'
        phone = '0666996699'
        mail = 'dummy@dummy.com'
        startDate = DateTime('2005/08/29 09:00')
        endDate = DateTime('2005/08/29 10:00')
        self.booking.edit(title = title,
                          description = description,
                          fullName = name,
                          phone = phone,
                          mail = mail,
                          startDate = startDate,
                          endDate = endDate,
                          )
        
        self.failUnless(not self.booking.isPeriodicBooking())
        # test periodicity type 2, will create 4 bookings
        periodicity_end_date  = DateTime('2005/10/29 09:00')
        infos = self.booking.getPeriodicityInfos(periodicity_type=2, periodicity_end_date=periodicity_end_date, week_interval=2)
        result = self.booking.createPeriodicBookings(periodicity_type=2, periodicity_end_date=periodicity_end_date, week_interval=2)
        self.assertEquals(5, len(self.bookable_object.objectIds()))
        self.assertEquals(5, len(self.booking.getAllPeriodicBookingBrains()))
        self.failUnless(self.booking.isPeriodicBooking())

        self.logout()

    def testCreatePeriodicBookingsType3(self,):
        """
        """
        self.loginAsPortalOwner()
        self.createEmptyBookingCenter(self.member_folder)
        self.createEmptyBookableObject(self.booking_center, wf_action='publish')
        self.createEmptyBooking(self.bookable_object)
        title = 'A dummy title'
        description = 'A dummy description'
        name = 'dummy name'
        phone = '0666996699'
        mail = 'dummy@dummy.com'
        startDate = DateTime('2005/08/12 09:00')
        endDate = DateTime('2005/08/13 10:00')
        self.booking.edit(title = title,
                          description = description,
                          fullName = name,
                          phone = phone,
                          mail = mail,
                          startDate = startDate,
                          endDate = endDate,
                          )

        self.failUnless(not self.booking.isPeriodicBooking())
        # test periodicity type 3, start and end date are not the same day, will create 4 bookings
        periodicity_end_date = DateTime('2005/12/29 09:00')
        infos = self.booking.getPeriodicityInfos(periodicity_type=3, periodicity_end_date=periodicity_end_date)
        self.booking.edit(startDate=startDate, endDate=endDate)
        result = self.booking.createPeriodicBookings(periodicity_type=3, periodicity_end_date=periodicity_end_date)
        self.assertEquals(5, len(self.bookable_object.objectIds()))
        self.assertEquals(5, len(self.booking.getAllPeriodicBookingBrains()))
        self.failUnless(self.booking.isPeriodicBooking())        

        # test periodicity type 3 with same day for start and end date, will create 4 bookings
        start_date = DateTime('2005/08/14 09:00')
        end_date = DateTime('2005/08/14 12:00')
        self.booking.edit(startDate=start_date, endDate=end_date)
        infos = self.booking.getPeriodicityInfos(periodicity_type=3, periodicity_end_date=periodicity_end_date)
        result = self.booking.createPeriodicBookings(periodicity_type=3, periodicity_end_date=periodicity_end_date)
        self.assertEquals(9, len(self.bookable_object.objectIds()))
        self.assertEquals(9, len(self.booking.getAllPeriodicBookingBrains()))
        self.failUnless(self.booking.isPeriodicBooking())
        
        self.logout()
    
    def testGetIntervalOfMinutesGroupKeys(self):
        """
        """
        
        # Interval of 30 minutes
        interval = 30
        # Calendar begins at 8h and finish at 12h 2005/11/15
        start_dt = DateTime(2005,11,15,8,0,0)
        end_dt = DateTime(2005,11,15,12,0,0)
        expected = [(2005, 11, 15, x*interval) for x in range(16, 24)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)
        
        # Booking : 2005/11/15 9h15-9h25
        start_dt = DateTime(2005,11,15,9,15,0)
        end_dt = DateTime(2005,11,15,9,25,0)
        expected = [(2005, 11, 15, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)
        
        # Booking : 2005/11/15 9h00-9h30
        start_dt = DateTime(2005,11,15,9,00,0)
        end_dt = DateTime(2005,11,15,9,30,0)
        expected = [(2005, 11, 15, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)
        
        # Booking : 2005/11/15 9h00-9h35
        start_dt = DateTime(2005,11,15,9,00,0)
        end_dt = DateTime(2005,11,15,9,35,0)
        expected = [(2005, 11, 15, 540), (2005, 11, 15, 570)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)
        
        # Booking : 2005/11/15 8h55-9h30
        start_dt = DateTime(2005,11,15,8,55,0)
        end_dt = DateTime(2005,11,15,9,30,0)
        expected = [(2005, 11, 15, 510), (2005, 11, 15, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)
        
        # Booking : 2005/11/15 8h30-9h30
        start_dt = DateTime(2005,11,15,8,30,0)
        end_dt = DateTime(2005,11,15,9,30,0)
        expected = [(2005, 11, 15, 510), (2005, 11, 15, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)
        
        # Interval of 60 minutes
        interval = 60
        # Calendar begins at 22h 2005/11/14 and finish at 2h 2005/11/15
        start_dt = DateTime(2005,11,14,22,0,0)
        end_dt = DateTime(2005,11,15,2,0,0)
        expected = [(2005, 11, 14, x*interval) for x in range(22, 24)]
        expected.extend([(2005, 11, 15, x*interval) for x in range(0, 2)])
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)
        
        # Booking : 2005/11/14 9h15-9h45
        start_dt = DateTime(2005,11,14,9,15,0)
        end_dt = DateTime(2005,11,14,9,45,0)
        expected = [(2005, 11, 14, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)
        
        # Booking : 2005/11/14 9h00-10h00
        start_dt = DateTime(2005,11,14,9,0,0)
        end_dt = DateTime(2005,11,14,10,0,0)
        expected = [(2005, 11, 14, 540)]
        result = self.btool.getIntervalOfMinutesGroupKeys(start_dt, end_dt, interval)
        self.assertEquals(result, expected)
        
    def testGetDayGroupKeys(self):
        """
        """    
        
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
    
    def testGetWeekGroupKeys(self):
        """
        """
        
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
        
    def testGetMonthGroupKeys(self):
        """
        """
        
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
    
    def testGetYearGroupKeys(self):
        """
        """
        
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
        
    def testGetBookingBrains(self):
        """
        """
        
        self.loginAsPortalOwner()
        self.createEmptyBookingCenter(self.member_folder)
        self.createEmptyBookableObject(self.booking_center, wf_action='publish')
        self.createEmptyBooking(self.bookable_object)

        # Booking in 2005/11/15 9:00 9:30
        start_date = DateTime(2005,11,15,9,0,0)
        end_date = DateTime(2005,11,15,9,30,0)
        self.booking.edit(startDate=start_date, endDate=end_date)
        brains = self.booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 1)
        
        # Test in 2005/11/15 9:05 9:25
        start_date = DateTime(2005,11,15,9,5,0)
        end_date = DateTime(2005,11,15,9,25,0)
        brains = self.booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 1)
        
        # Test in 2005/11/15 8:55 9:25
        start_date = DateTime(2005,11,15,8,55,0)
        end_date = DateTime(2005,11,15,9,25,0)
        brains = self.booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 1)
        
        # Test in 2005/11/15 9:05 9:35
        start_date = DateTime(2005,11,15,9,5,0)
        end_date = DateTime(2005,11,15,9,35,0)
        brains = self.booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 1)
        
        # Test in 2005/11/15 8:55 9:35
        start_date = DateTime(2005,11,15,8,55,0)
        end_date = DateTime(2005,11,15,9,35,0)
        brains = self.booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 1)
        
        # Test in 2005/11/15 8:30 9:00
        start_date = DateTime(2005,11,15,8,30,0)
        end_date = DateTime(2005,11,15,9,0,0)
        brains = self.booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 0)
        
        # Test in 2005/11/15 9:30 10:00
        start_date = DateTime(2005,11,15,9,30,0)
        end_date = DateTime(2005,11,15,10,0,0)
        brains = self.booking_center.getBookingBrains(start_date, end_date)
        self.assertEquals(len(brains), 0)
    
tests.append(TestPloneBooking)

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

