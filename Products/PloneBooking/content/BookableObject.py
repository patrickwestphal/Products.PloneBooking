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
    PloneBooking: Bookable Object
"""

__version__ = "$Revision: 1.6 $"
__author__  = ''
__docformat__ = 'restructuredtext'

# Python imports
from types import DictionaryType

# Zope imports
from zope.interface import implements

from AccessControl import ClassSecurityInfo
from DateTime import DateTime
from Globals import InitializeClass

# CMF imports
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName

# Archetypes imports
try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *

#PloneBooking imports
from Products.PloneBooking.config import PROJECTNAME, I18N_DOMAIN
from Products.PloneBooking.content.schemata import BookableObjectSchema
from Products.PloneBooking.interfaces import IBookableObject


class BookableObject(BaseBTreeFolder):
    """
      Bookable Object is an object that can be booked ...
    """

    implements(IBookableObject)

    _at_rename_after_creation = True

    schema = BookableObjectSchema

    security = ClassSecurityInfo()

    # this works around a problem that makes empty folders
    # evaluate to false in boolean tests, like:
    # tal:condition="python: someFolder and someFolder.someMethod(...)"
    def __len__(self):
        return 1

    security.declarePrivate('setDefaults')
    def setDefaults(self):
        """Set field values to the default values
        """
        BaseBTreeFolder.setDefaults(self)

        # Add hook. Script in skin named bookableobject_defaults
        default_method = getattr(self, 'bookableobject_defaults',
            self.restrictedTraverse('@@defaultFieldValues', None))

        if default_method is not None:
            # Get dictionnary
            kwargs = default_method()

            if type(kwargs) is DictionaryType:
                self.edit(**kwargs)

    security.declarePublic('getBookableObject')
    def getBookableObject(self):
        """Returns bookable object himself"""

        utool = getToolByName(self, 'portal_url')
        return self.restrictedTraverse(utool.getRelativeContentURL(self))

    security.declarePrivate('getTypeVocabulary')
    def getTypeVocabulary(self, ):
        """ Get a type list for the bookable object.
        """

        center_obj = self.getBookingCenter()
        return Vocabulary(center_obj.getTypeDisplayList(), self, I18N_DOMAIN)

    security.declarePrivate('getCategoryVocabulary')
    def getCategoryVocabulary(self, ):
        """ Get a category list for the bookable object.
        """

        center_obj = self.getBookingCenter()
        new_items = []
        dl = center_obj.getCategoryDisplayList()

        # Append None value
        new_items.append(('', 'No category', 'label_no_category'))
        new_items.extend(dl.items())
        return Vocabulary(DisplayList(tuple(new_items)), self, I18N_DOMAIN)

    security.declareProtected(permissions.ModifyPortalContent, 'edit')
    def edit(self, **kwargs):
        """Alias for update()
        """
        self.update(**kwargs)

    security.declareProtected(permissions.View, 'CookedBody')
    def CookedBody(self, stx_level='ignored'):
        """CMF compatibility method
        """

        return self.getText()

registerType(BookableObject, PROJECTNAME)
