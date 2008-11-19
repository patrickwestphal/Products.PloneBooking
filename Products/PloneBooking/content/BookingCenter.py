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
    PloneBooking: Booking Center
"""

__version__ = "$Revision: 1.9 $"
__author__  = 'malmzi2007'
__docformat__ = 'restructuredtext'

from zope.interface import implements

# Zope imports
from AccessControl import ClassSecurityInfo
from AccessControl import Unauthorized
from DateTime import DateTime

# CMF imports
from Products.CMFCore import permissions
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import normalizeString
from Products.CMFCore import utils

# Archetypes imports
try:
    from Products.LinguaPlone.public import *
except ImportError:
    # No multilingual support
    from Products.Archetypes.public import *


from Products.ATContentTypes.content.folder import (
    ATFolder,
    ATFolderSchema)

from Products.PloneBooking.content.vocabulary import (
    REQUIRED_FILTERS,
    CALENDAR_VIEWS,
    VIEW_MODES,
    LISTING_VIEWS,
    GLOBAL_BOOKING_REVIEW_MODES,
    CALENDAR_REFRESH_MODES)
from Products.PloneBooking.config import PROJECTNAME, I18N_DOMAIN
from Products.PloneBooking.interfaces import IBookingCenter
from Products.PloneBooking import BookingPermissions

DISPLAY_SCHEMATA = 'display'

BookingCenterSchema = ATFolderSchema.copy() + Schema((
    LinesField(
        'types',
        required=True,
        widget=LinesWidget(
            label='Types',
            description='You can define here a list of bookable object types (1 by line)',
            description_msgid='help_bookingcenter_types',
            label_msgid='label_bookingcenter_types',
            i18n_domain= I18N_DOMAIN,
            ),
        ),
    LinesField(
        'categories',
        required=False,
        widget=LinesWidget(
            label='Categories',
            description=' ',
            description_msgid='help_bookingcenter_categories',
            label_msgid='label_bookingcenter_categories',
            i18n_domain=I18N_DOMAIN,
            ),
        ),
    LinesField(
        'bookableObjectStates',
        default=('published',),
        widget=LinesWidget(
            label='Bookable object allowed states for book',
            description='Define here the workflow states of bookable objects you can book. If a bookable object is in a workflow\
                         state that is not in this list, it will not appear in available bookable objects.',
            label_msgid='label_bookable_object_states',
            description_msgid='help_bookable_object_states',
            i18n_domain=I18N_DOMAIN,
            ),
        ),
    LinesField(
        'requiredFilters',
        vocabulary=REQUIRED_FILTERS,
        widget=MultiSelectionWidget(
            default=tuple(),
            format='select',
            label='Required filters',
            description='',
            label_msgid='label_required_filters',
            description_msgid='',
            i18n_domain=I18N_DOMAIN,
            ),
        ),
    StringField(
        'calendarRefreshMode',
        default="auto",
        vocabulary=CALENDAR_REFRESH_MODES,
        widget=SelectionWidget(
            default=False,
            label='Refresh mode',
            description='',
            label_msgid='label_refresh_mode',
            description_msgid='',
            i18n_domain=I18N_DOMAIN,
            ),
        ),
    StringField(
        'bookingReviewMode',
        default='review',
        vocabulary=GLOBAL_BOOKING_REVIEW_MODES,
        widget=SelectionWidget(
            label='Booking review mode',
            description='',
            label_msgid='label_booking_review_mode',
            description_msgid='',
            i18n_domain=I18N_DOMAIN,
            ),
        ),
    StringField(
        'defaultViewMode',
        schemata=DISPLAY_SCHEMATA,
        required=True,
        default='calendar',
        vocabulary=VIEW_MODES,
        widget=SelectionWidget(
            format='radio',
            label='Default view mode',
            label_msgid='label_bookingcenter_default_view_mode',
            i18n_domain=I18N_DOMAIN,
            ),
        ),
    LinesField(
        'availableViewModes',
        schemata=DISPLAY_SCHEMATA,
        required=True,
        default=('listing', 'calendar'),
        vocabulary=VIEW_MODES,
        widget=MultiSelectionWidget(
            format='select',
            label='Available view modes',
            label_msgid='label_bookingcenter_available_view_modes',
            i18n_domain=I18N_DOMAIN,
            ),
        ),
    StringField(
        'defaultListingView',
        schemata=DISPLAY_SCHEMATA,
        required=True,
        default='day',
        vocabulary=LISTING_VIEWS,
        widget=SelectionWidget(
            format='select',
            label='Default listing view',
            label_msgid='label_bookingcenter_default_listing_view',
            i18n_domain=I18N_DOMAIN,
            ),
        ),
    LinesField(
        'availableListingViews',
        schemata=DISPLAY_SCHEMATA,
        required=True,
        default=('day', 'week', 'month', 'year'),
        vocabulary=LISTING_VIEWS,
        widget=MultiSelectionWidget(
            format='select',
            label='Available listing views',
            label_msgid='label_bookingcenter_available_listing_views',
            i18n_domain=I18N_DOMAIN,
            ),
        ),
    StringField(
        'defaultCalendarView',
        schemata=DISPLAY_SCHEMATA,
        required=True,
        default='day',
        vocabulary=CALENDAR_VIEWS,
        widget=SelectionWidget(
            format='select',
            label='Default calendar view',
            label_msgid='label_bookingcenter_default_calendar_view',
            i18n_domain=I18N_DOMAIN,
            ),
        ),
    LinesField(
        'availableCalendarViews',
        schemata=DISPLAY_SCHEMATA,
        required=True,
        default=('day', 'week', 'month'),
        vocabulary=CALENDAR_VIEWS,
        widget=MultiSelectionWidget(
            format='select',
            label='Available calendar views',
            label_msgid='label_bookingcenter_available_calendar_views',
            i18n_domain=I18N_DOMAIN,
            ),
        ),
    IntegerField(
        'calendarStartingHour',
        schemata=DISPLAY_SCHEMATA,
        required=True,
        default=8,
        widget=IntegerWidget(
            label='Starting hour',
            description='This is used in day and week calendar views',
            label_msgid='label_bookingcenter_calendar_starting_hour',
            description_msgid='help_bookingcenter_calendar_starting_hour',
            i18n_domain=I18N_DOMAIN,
            ),
        ),
    IntegerField(
        'calendarEndingHour',
        schemata=DISPLAY_SCHEMATA,
        required=True,
        default=19,
        widget=IntegerWidget(
            label='Ending hour',
            description='This is used in day and week calendar views',
            label_msgid='label_bookingcenter_calendar_ending_hour',
            description_msgid='help_bookingcenter_calendar_ending_hour',
            i18n_domain=I18N_DOMAIN,
            ),
        ),
    ))


BookingCenterSchema['description'].schemata = 'default'

# Put display schemata after default schemata
BookingCenterSchema.moveField('types', after='description')
BookingCenterSchema.moveField('defaultViewMode', after='types')

class BookingCenter(ATFolder):
    """
      Booking Center contains all Bookable Object and Bookings
    """
    implements(IBookingCenter)

    _at_rename_after_creation = True
    schema = BookingCenterSchema

    security = ClassSecurityInfo()

    security.declarePublic('getTypeDisplayList')
    def getTypeDisplayList(self, ):
        """Returns all types as a DisplayList"""

        return DisplayList([(normalizeString(x, encoding=self.getCharset()), x) for x in self.getTypes()])

    security.declarePublic('getCategoryDisplayList')
    def getCategoryDisplayList(self, ):
        """Returns all categories as a DisplayList"""

        return DisplayList([(normalizeString(x, encoding=self.getCharset()), x) for x in self.getCategories()])

    security.declarePublic('getBookingCenter')
    def getBookingCenter(self):
        """Returns booking center himself"""

        utool = getToolByName(self, 'portal_url')
        return self.restrictedTraverse(utool.getRelativeContentURL(self))

    security.declareProtected(permissions.View, 'getBookings')
    def getBookings(self, start_date=None, end_date=None, **kwargs):
        """Get booking objects in a interval of time (start_date, end_date).

        @param start_date: start date of scan. This is a DateTime
        @param end_date: end date of scan. This is a DateTime
        """

        return [x.getObject() for x in self.getBookingBrains(start_date, end_date, **kwargs)]

    security.declareProtected(permissions.View, 'getBookingBrains')
    def getBookingBrains(self, start_date=None, end_date=None,  **kwargs):
        """Get booking brains in a interval of time (start_date, end_date).

        @param start_date: start date of scan. This is a DateTime
        @param end_date: end date of scan. This is a DateTime
        """

        # Initialize
        ctool = getToolByName(self, 'portal_catalog')
        btool = getToolByName(self, 'portal_booking')
        center_obj = self.getBookingCenter()
        center_path = '/'.join(center_obj.getPhysicalPath())
        query_args = {}
        start_ts = None
        end_ts = None

        try:
            start_date = btool.ts2zdt(int(start_date))
            end_date = btool.ts2zdt(int(end_date))
        except:
            pass

        if start_date is not None:
            start_ts = btool.zdt2ts(start_date)
        if end_date is not None:
            end_ts = btool.zdt2ts(end_date)

        # Add default query args
        query_args['path'] = center_path
        query_args['portal_type'] = 'Booking'
        query_args['sort_on'] = 'start'

        # Add query args specific to start date and end date
        start_end_ranges = []
        if start_date is not None:
            # Start date between booking start and end date
            start_end_ranges.append((start_date, 'max', start_date, 'min'))
        if end_date is not None:
            # End date between booking start and end date
            start_end_ranges.append((end_date, 'max', end_date, 'min'))
        # Booking in start date and end date
        start_end_ranges.append((start_date, 'min', end_date, 'max'))

        # Update query_args
        if kwargs:
            query_args.update(kwargs)

        # Get brains
        brains = []
        brain_rids = []
        for sdate, srange, edate, erange in start_end_ranges:
            query_args_copy = query_args.copy()
            if sdate is not None:
                query_args_copy['start'] = {'query' : sdate, 'range' : srange}

            if edate is not None:
                query_args_copy['end'] = {'query' : edate, 'range' : erange}

            new_brains = ctool.searchResults(**query_args_copy)
            for brain in new_brains:
                brain_rid = brain.getRID()

                if brain_rid in brain_rids:
                    continue

                brain_rids.append(brain_rid)
                brain_start_dt = DateTime(brain.start)
                brain_start_ts = btool.zdt2ts(brain_start_dt)
                if brain_start_ts == end_ts:
                    continue
                brain_end_dt = DateTime(brain.end)
                brain_end_ts = btool.zdt2ts(brain_end_dt)
                if brain_end_ts == start_ts:
                    continue
                brains.append(brain)
        return brains

    def _getBookingStructure(self, booking_brain, default_title):
        """Build dictionnary with needed information :
        id, title, description, refs, url, start, end, creator, review_state"""

        booking_info = {}
        booking_info['id'] = booking_brain.getId
        title = booking_brain.Title
        booking_info['title'] = title
        if not title:
            booking_info['title'] = default_title
        booking_info['description'] = booking_brain.Description
        booking_info['bookedObjectUID'] = booking_brain.getBookedObjectUID
        booking_info['url'] = booking_brain.getURL()
        booking_info['start'] = DateTime(booking_brain.start)
        booking_info['end'] = DateTime(booking_brain.end)
        booking_info['creator'] = booking_brain.Creator
        booking_info['review_state'] = booking_brain.review_state
        return booking_info

    security.declareProtected(permissions.View, 'groupBookingsByIntervalOfMinutes')
    def groupBookingsByIntervalOfMinutes(self, start_date, end_date, interval=30, **kwargs):
        """Group bookings by interval of minutes.
        A brain can exist in several intervals.
        Returns tuple : (group_keys, booking_groups).
        Group key is : (year, month, day, interval).
        if interval equals 30, Interval of 0 means : 0-30
        if interval equals 30, Interval of 30 means : 30-60

        @param start_date: start date of scan. This is a DateTime
        @param end_date: end date of scan. This is a DateTime
        @param interval: interval in minutes. It must be a multiple or a divider of 60
        """

        # Interval must be a multiple or a divider of 60. Check it
        if (interval < 60 and (60/interval)*interval != 60) or \
           (interval > 60 and (interval/60)*interval != 60):
            raise ValueError, "Interval must be a multiple or a divider of 60"

        # Interval can't be greater than 3600 minutes (a day)
        if interval > 3600:
            raise ValueError, "Interval can't be greater than 3600 minutes"

        # Initialize
        btool = getToolByName(self, 'portal_booking')
        default_title = btool.getBookingDefaultTitle()
        group_keys = btool.getIntervalOfMinutesGroupKeys(start_date, end_date, interval)
        booking_groups = {}
        booking_brains = self.getBookingBrains(start_date, end_date, **kwargs)

        # Store brains in booking groups
        for brain in booking_brains:
            # Get brain group keys
            brain_start_date = DateTime(brain.start)
            brain_end_date = DateTime(brain.end)
            if start_date.greaterThanEqualTo(brain_start_date):
                brain_start_date = start_date
            if brain_end_date.greaterThanEqualTo(end_date):
                brain_end_date = end_date
            brain_group_keys = btool.getIntervalOfMinutesGroupKeys(brain_start_date, brain_end_date, interval)

            # Wrap booking
            booking_info = self._getBookingStructure(brain, default_title)

            # Append to booking groups
            for key in brain_group_keys:
                value = booking_info.copy()
                if not booking_groups.has_key(key):
                    booking_groups[key] = []
                booking_info['group_by'] = key
                booking_groups[key].append(booking_info)

        return group_keys, booking_groups

    security.declareProtected(permissions.View, 'groupBookingsByDay')
    def groupBookingsByDay(self, start_date, end_date, **kwargs):
        """Group bookings by day.
        A brain can exist in several days.
        Returns tuple : (group_keys, booking_groups).
        Group key is : (year, month, day)

        @param start_date: start date of scan. This is a DateTime
        @param end_date: end date of scan. This is a DateTime
        """

        # Initialize
        btool = getToolByName(self, 'portal_booking')
        default_title = btool.getBookingDefaultTitle()
        group_keys = btool.getDayGroupKeys(start_date, end_date)
        booking_groups = {}
        booking_brains = self.getBookingBrains(start_date, end_date, **kwargs)

        # Store brains in booking groups
        for brain in booking_brains:
            # Get brain group keys
            brain_start_date = DateTime(brain.start)
            brain_end_date = DateTime(brain.end)
            if start_date.greaterThanEqualTo(brain_start_date):
                brain_start_date = start_date
            if brain_end_date.greaterThanEqualTo(end_date):
                brain_end_date = end_date
            brain_group_keys = btool.getDayGroupKeys(brain_start_date, brain_end_date)

            # Wrap booking
            booking_info = self._getBookingStructure(brain, default_title)

            # Append to booking groups
            for key in brain_group_keys:
                value = booking_info.copy()
                if not booking_groups.has_key(key):
                    booking_groups[key] = []
                booking_info['group_by'] = key
                booking_groups[key].append(booking_info)

        return group_keys, booking_groups

    security.declareProtected(permissions.View, 'groupBookingsByWeek')
    def groupBookingsByWeek(self, start_date, end_date, **kwargs):
        """Group bookings by week.
        A brain can exist in several weeks.
        Returns tuple : (group_keys, booking_groups).
        Group key is : (year, week)

        @param start_date: start date of scan. This is a DateTime
        @param end_date: end date of scan. This is a DateTime
        """

        # Initialize
        btool = getToolByName(self, 'portal_booking')
        default_title = btool.getBookingDefaultTitle()
        group_keys = btool.getWeekGroupKeys(start_date, end_date)
        booking_groups = {}
        booking_brains = self.getBookingBrains(start_date, end_date, **kwargs)

        # Store brains in booking groups
        for brain in booking_brains:
            # Get brain group keys
            brain_start_date = DateTime(brain.start)
            brain_end_date = DateTime(brain.end)
            if start_date.greaterThanEqualTo(brain_start_date):
                brain_start_date = start_date
            if brain_end_date.greaterThanEqualTo(end_date):
                brain_end_date = end_date
            brain_group_keys = btool.getWeekGroupKeys(brain_start_date, brain_end_date)

            # Wrap booking
            booking_info = self._getBookingStructure(brain, default_title)

            # Append to booking groups
            for key in brain_group_keys:
                value = booking_info.copy()
                if not booking_groups.has_key(key):
                    booking_groups[key] = []
                booking_info['group_by'] = key
                booking_groups[key].append(booking_info)

        return group_keys, booking_groups

    security.declareProtected(permissions.View, 'groupBookingsByMonth')
    def groupBookingsByMonth(self, start_date, end_date, **kwargs):
        """Group bookings by month.
        A brain can exist in several months.
        Returns tuple : (group_keys, booking_groups).
        Group key is : (year, month)

        @param start_date: start date of scan. This is a DateTime
        @param end_date: end date of scan. This is a DateTime
        """

        # Initialize
        btool = getToolByName(self, 'portal_booking')
        default_title = btool.getBookingDefaultTitle()
        group_keys = btool.getMonthGroupKeys(start_date, end_date)
        booking_groups = {}
        booking_brains = self.getBookingBrains(start_date, end_date, **kwargs)

        # Store brains in booking groups
        for brain in booking_brains:
            # Get brain group keys
            brain_start_date = DateTime(brain.start)
            brain_end_date = DateTime(brain.end)
            if start_date.greaterThanEqualTo(brain_start_date):
                brain_start_date = start_date
            if brain_end_date.greaterThanEqualTo(end_date):
                brain_end_date = end_date
            brain_group_keys = btool.getMonthGroupKeys(brain_start_date, brain_end_date)

            # Wrap booking
            booking_info = self._getBookingStructure(brain, default_title)

            # Append to booking groups
            for key in brain_group_keys:
                value = booking_info.copy()
                if not booking_groups.has_key(key):
                    booking_groups[key] = []
                booking_info['group_by'] = key
                booking_groups[key].append(booking_info)

        return group_keys, booking_groups

    security.declareProtected(permissions.View, 'groupBookingsByYear')
    def groupBookingsByYear(self, start_date, end_date, **kwargs):
        """Group bookings by year.
        A brain can exist in several years.
        Returns tuple : (group_keys, booking_groups).
        Group key is : year

        @param start_date: start date of scan. This is a DateTime
        @param end_date: end date of scan. This is a DateTime
        """

        # Initialize
        btool = getToolByName(self, 'portal_booking')
        default_title = btool.getBookingDefaultTitle()
        group_keys = btool.getYearGroupKeys(start_date, end_date)
        booking_groups = {}
        booking_brains = self.getBookingBrains(start_date, end_date, **kwargs)

        # Store brains in booking groups
        for brain in booking_brains:
            # Get brain group keys
            brain_start_date = DateTime(brain.start)
            brain_end_date = DateTime(brain.end)
            if start_date.greaterThanEqualTo(brain_start_date):
                brain_start_date = start_date
            if brain_end_date.greaterThanEqualTo(end_date):
                brain_end_date = end_date
            brain_group_keys = btool.getYearGroupKeys(start_date, end_date)

            # Wrap booking
            booking_info = self._getBookingStructure(brain, default_title)

            # Append to booking groups
            for key in brain_group_keys:
                value = booking_info.copy()
                if not booking_groups.has_key(key):
                    booking_groups[key] = []
                booking_info['group_by'] = key
                booking_groups[key].append(booking_info)

        return group_keys, booking_groups

    def canBook(self):
        """Check for published bookable objects"""

        brains = self.getBookableObjectBrains(review_state='published')

        if not brains:
            return False

        return True

    security.declareProtected(permissions.View, 'getBookableObjectBrains')
    def getBookableObjectBrains(self, **kwargs):
        """Returns all bookable object brains
        """

        # Initialize defaults
        ctool = getToolByName(self, 'portal_catalog')
        center_obj = self.getBookingCenter()
        center_path = '/'.join(center_obj.getPhysicalPath())
        query_args = {}
        query_args['path'] = center_path
        query_args['portal_type'] = 'BookableObject'

        # Update query args
        if kwargs:
            query_args.update(kwargs)

        return ctool.searchResults(**query_args)

    security.declareProtected(permissions.View, 'getBookableObjects')
    def getBookableObjects(self, **kwargs):
        """Returns all bookable objects
        """
        objects = [x.getObject() for x in self.getBookableObjectBrains(**kwargs)]
        objects.sort(lambda x,y: cmp(x.Title(), y.Title()))
        return objects

    security.declareProtected(permissions.View, 'getBookableObjectCategories')
    def getBookableObjectCategories(self, **kwargs):
        """Returns the categories used in bookable objects"""

        brains = self.getBookableObjectBrains(**kwargs)
        brain_categories = [x.getCategory for x in brains]
        categ_vocab = self.getCategoryDisplayList()
        categories = [x for x in categ_vocab.keys() if x in brain_categories]
        categories.sort()
        return categories

    security.declareProtected(permissions.View, 'getBookableObjectTypes')
    def getBookableObjectTypes(self, **kwargs):
        """Returns the types used in bookable objects"""

        brains = self.getBookableObjectBrains(**kwargs)
        brain_types = [x.getType for x in brains]
        type_vocab = self.getTypeDisplayList()
        types = [x for x in type_vocab.keys() if x in brain_types]
        types.sort()
        return types


registerType(BookingCenter, PROJECTNAME)