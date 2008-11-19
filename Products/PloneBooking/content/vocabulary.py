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
    PloneBooking: Vocabulary
"""

__version__ = "$Revision: 1.4 $"
__author__  = ''
__docformat__ = 'restructuredtext'

from Products.Archetypes.utils import DisplayList

CALENDAR_REFRESH_MODES = DisplayList((
    ('auto', 'Automatic', 'label_refresh_auto'),
    ('manual', 'Manual', 'label_refresh_manual'),
))

REQUIRED_FILTERS = DisplayList((
    ('type', 'Type', 'label_type'),
    ('category', 'Category', 'label_category'),
    ('resource', 'Resource', 'label_resource')))

CALENDAR_VIEWS = DisplayList((
    ('day', 'Day', 'label_day'),
    ('week', 'Week', 'label_week'),
    ('month', 'Month', 'label_month')))

LISTING_VIEWS = DisplayList((
    ('day', 'Day', 'label_day'),
    ('week', 'Week', 'label_week'),
    ('month', 'Month', 'label_month'),
    ('year', 'Year', 'label_year')))

VIEW_MODES = DisplayList((
    ('listing', 'Listing', 'label_listing'),
    ('calendar', 'Calendar', 'label_calendar')))

BOOKING_REVIEW_MODES = DisplayList((
    ('default', 'Default (in booking center)', 'label_default_booking_review_mode'),
    ('review', 'Review bookings', 'label_review_bookings'),
    ('publish', 'Publish automatically bookings', 'label_publish_automatically_bookings')))

GLOBAL_BOOKING_REVIEW_MODES = DisplayList((
    ('review', 'Review bookings', 'label_review_bookings'),
    ('publish', 'Publish automatically bookings', 'label_publish_automatically_bookings')))