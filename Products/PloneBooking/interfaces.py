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
    PloneBooking: Interfaces
"""


# $Source: /isp/cvs/repository/zope/products/PloneBooking/interfaces/interfaces.py,v $
# $Id: interfaces.py,v 1.5 2006/04/07 13:49:33 cbosse Exp $
__version__ = "$Revision: 1.5 $"
__author__  = ''
__docformat__ = 'restructuredtext'

from zope.interface import Interface


"""
VOCABULARY:

  - Booking contains "referenced" on Bookable Objects

  - Bookable Object can be booked for a period
"""

class IBooking(Interface):
    """ This interface proposes methods to access to Booked Objects, and get the
        booking period.
    """
    #
    # Booked Objects
    #
    
    def getBookedObject(self, UID):
        """
        Parameters
            UID -> UID of attachment
            
        Return a Bookable object
        """
        
    def getBookedObjectRefs(self, ):
        """
        Return all booked objects referenced in Booking.
        """
        
    
    def getBookedObjectUIDs(self, ):
        """
        Return all Booked Objects uids referenced in Booking.
        """
    
    def isBookingObject(self, UID):
        """
        Parameters
            UID -> UID of bookable object
        
        Return true if the booking books the object with the given UID.
        """
        
    def isBookingObjects(self, uids_list):
        """
        Parameters
            uids_list -> uids_list of bookable object
        
        Return true if the booking books one of the object (from uid's list).
        """
    
    # Period
    #
    def hasBookedObject(self, UID, start_date, end_date):
        """
        Parameters
            UID -> uid of object
            start_date -> Date of booking's start
            end_date -> Date of booking's end
            
        Return true there are booked object during the given period.
        """
    
    def hasBookedObjects(self, uids_list, start_date, end_date):
        """
        Parameters 
            uids_list -> list of uids to test
            start_date -> Date of booking's start
            end_date -> Date of booking's end
        """
        
    
class IBookingCenter(Interface):
    """ This interface proposes methods to access contains of a Booking Center.
    """
    #
    # Booking
    #
    def getBookingCenter(self, ):
        """
        Return the Booking center itself
        """
    
    def getBookings(self, sort=''):
        """
        Return all Bookings contained in the BookingCenter.
        """
    
    def getBookingContainer(self,):
        """
        Return the booking container.
        """
    
    def getBookableObjectContainer(self,):
        """
        Return the bookable object container.
        """
    
    def getBookedObjects(self, ):
        """
        Return all booked object in container
        """
    

class IBookableObject(Interface):
    """ This interface proposes methods to know if an object is booked.
    """
    def isBooked(self,):
        """
        """

class IBookingExporter(Interface):
    """
        Utility methods to format and manipulate exports fields
    """
