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
"""Common imports and declarations

common includes a set of basic things that every test needs.

$$
"""

__author__ = ''
__docformat__ = 'restructuredtext'

# enable nice names for True and False from newer python versions
try:
    dummy = True
except NameError: # python 2.1
    True  = 1
    False = 0

import time

def Xprint(s):
    """print helper

    print data via print is not possible, you have to use
    ZopeTestCase._print or this function
    """
    ZopeTestCase._print(str(s)+'\n')

def dcEdit(obj):
    """dublin core edit (inplace)
    """
    obj.setTitle('Test Title')
    obj.setDescription('Test description')
    # XXX more

from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager

###
# general test suits including products
###
from Testing import ZopeTestCase
ZopeTestCase.installProduct('CMFCore', 1)
ZopeTestCase.installProduct('CMFDefault', 1)
ZopeTestCase.installProduct('CMFCalendar', 1)
ZopeTestCase.installProduct('CMFTopic', 1)
ZopeTestCase.installProduct('DCWorkflow', 1)
ZopeTestCase.installProduct('CMFActionIcons', 1)
ZopeTestCase.installProduct('CMFQuickInstallerTool', 1)
ZopeTestCase.installProduct('CMFFormController', 1)
ZopeTestCase.installProduct('GroupUserFolder', 1)
ZopeTestCase.installProduct('ZCTextIndex', 1)
ZopeTestCase.installProduct('CMFPlone', 1)
ZopeTestCase.installProduct('MailHost', 1)
ZopeTestCase.installProduct('PageTemplates', 1)
ZopeTestCase.installProduct('PythonScripts', 1)
ZopeTestCase.installProduct('ExternalMethod', 1)
ZopeTestCase.installProduct('ZCatalog', 1)
ZopeTestCase.installProduct('Archetypes', 1)
ZopeTestCase.installProduct('PortalTransforms', 1)
ZopeTestCase.installProduct('PloneBooking', 1)


###
# from archetypes
###

from Products.Archetypes.public import *
from Products.Archetypes.config import PKG_NAME
from Products.Archetypes.tests import ArchetypesTestCase
from Products.Archetypes.tests.test_baseschema import BaseSchemaTest
from Products.Archetypes.interfaces.layer import ILayerContainer
from Products.Archetypes.Storage import AttributeStorage, MetadataStorage
from Products.Archetypes import listTypes
from Products.Archetypes.Widget import IdWidget, StringWidget, BooleanWidget, \
     KeywordWidget, TextAreaWidget, CalendarWidget, SelectionWidget
from Products.Archetypes.utils import DisplayList
from Products.CMFCore  import CMFCorePermissions
from Products.Archetypes.ExtensibleMetadata import FLOOR_DATE,CEILING_DATE
from Globals import package_home
from Products.PloneBooking.config import GLOBALS
from DateTime import DateTime
from Products.CMFCore.utils import getToolByName

# import Interface for interface testing
try:
    import Interface
except ImportError:
    # set dummy functions and exceptions for older zope versions
    def verifyClass(iface, candidate, tentative=0):
        return True
    def verifyObject(iface, candidate, tentative=0):
        return True
    def getImplementsOfInstances(object):
        return ()
    def getImplements(object):
        return ()
    def flattenInterfaces(interfaces, remove_duplicates=1):
        return ()
    class BrokenImplementation(Exception): pass
    class DoesNotImplement(Exception): pass
    class BrokenMethodImplementation(Exception): pass
else:
    from Interface.Implements import getImplementsOfInstances, \
         getImplements, flattenInterfaces
    from Interface.Verify import verifyClass, verifyObject
    from Interface.Exceptions import BrokenImplementation, DoesNotImplement
    from Interface.Exceptions import BrokenMethodImplementation

###
# PloneBooking tests
###

from PloneBookingTestCase import PloneBookingTestCase
from Products.PloneBooking.interfaces.interfaces import IBooking
from Products.PloneBooking import BookingPermissions
