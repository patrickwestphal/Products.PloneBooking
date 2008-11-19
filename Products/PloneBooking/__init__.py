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
    PloneBooking: Module
"""

__version__ = "$Revision: 1.6 $"
__author__  = ''
__docformat__ = 'restructuredtext'

# Python imports
import sys
from Globals import package_home

from zope.i18nmessageid import MessageFactory

# CMF imports
from Products.CMFCore import utils
from Products.CMFCore import permissions
from Products.CMFCore.DirectoryView import registerDirectory

# Archetypes import
from Products.Archetypes.public import listTypes, process_types

# Products imports
from Products.PloneBooking.interfaces import (IBookingCenter, 
                                              IBooking, 
                                              IBookableObject)
from Products.PloneBooking.config import PROJECTNAME, SKINS_DIR, GLOBALS
from Products.PloneBooking.config import I18N_DOMAIN
from Products.PloneBooking import BookingPermissions
from Products.PloneBooking import content
from Products.PloneBooking.BookingTool import BookingTool


PloneBookingFactory = MessageFactory(I18N_DOMAIN)


registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):
    types_list = listTypes(PROJECTNAME)
    
    content_types, constructors, ftis = process_types(
        types_list,
        PROJECTNAME)
        
    bookingcenter_content_types = []
    bookingcenter_constructors  = []
    booking_content_types = []
    booking_constructors  = []
    bookableobject_content_types = []
    bookableobject_constructors  = []
    other_content_types = []
    other_constructors  = []

    for i in range(len(types_list)):
        at_type = types_list[i]
        klass = at_type['klass']
        
        if IBookingCenter.implementedBy(klass):
            bookingcenter_content_types.append(content_types[i])
            bookingcenter_constructors.append(constructors[i])
        elif IBooking.implementedBy(klass):
            booking_content_types.append(content_types[i])
            booking_constructors.append(constructors[i])
        elif IBookableObject.implementedBy(klass):
            bookableobject_content_types.append(content_types[i])
            bookableobject_constructors.append(constructors[i])
        else:
            other_content_types.append(content_types[i])
            other_constructors.append(constructors[i])
            
    # others
    utils.ContentInit(
        PROJECTNAME + ' Content',
        content_types = tuple(other_content_types),
        permission = permissions.AddPortalContent,
        extra_constructors = tuple(other_constructors),
        fti = ftis,
        ).initialize(context)

    # booking center
    utils.ContentInit(
        PROJECTNAME + ' BookingCenter',
        content_types = tuple(bookingcenter_content_types),
        permission = BookingPermissions.AddBookingCenter,
        extra_constructors = tuple(bookingcenter_constructors),
        fti = ftis,
        ).initialize(context)
    
    # booking
    utils.ContentInit(
        PROJECTNAME + ' Booking',
        content_types = tuple(booking_content_types),
        permission = BookingPermissions.AddBooking,
        extra_constructors = tuple(booking_constructors),
        fti = ftis,
        ).initialize(context)
        
    # bookable object
    utils.ContentInit(
        PROJECTNAME + ' BookableObject',
        content_types = tuple(bookableobject_content_types),
        permission = BookingPermissions.AddBookableObject,
        extra_constructors = tuple(bookableobject_constructors),
        fti = ftis,
        ).initialize(context)
    
    # Add tool
    utils.ToolInit(
        PROJECTNAME + ' Tool',
        tools=(BookingTool,),
        icon='tool.gif').initialize(context)
