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
    PloneBooking: Schemas
"""

__version__ = "$Revision: 1.7 $"
__author__  = ''
__docformat__ = 'restructuredtext'

# CMF imports
from Products.CMFCore import permissions

# Archetypes imports
from Products.Archetypes.public import *

#PloneBooking imports
from Products.PloneBooking.config import I18N_DOMAIN
from Products.PloneBooking.content.vocabulary import \
    CALENDAR_VIEWS, \
    VIEW_MODES, \
    LISTING_VIEWS, \
    BOOKING_REVIEW_MODES, \
    GLOBAL_BOOKING_REVIEW_MODES

BookingSchema = BaseSchema.copy() + Schema((
    StringField(
        'fullName',
        required=True,
        default_method='getDefaultFullname',
        widget=StringWidget(
            label="Full name",
            label_msgid="label_booking_user_full_name",
            i18n_domain=I18N_DOMAIN,
            ),
        ),

    StringField(
        'phone',
        default_method='getDefaultPhone',
        required=True,
        widget=StringWidget(
            label="Phone",
            label_msgid="label_booking_user_phone",
            i18n_domain=I18N_DOMAIN,
            ),
        ),

    StringField(
        'email',
        required=True,
        default_method='getDefaultEmail',
        validators=('isEmail',),
        widget=StringWidget(
            label="Email",
            label_msgid="label_booking_user_email",
            i18n_domain=I18N_DOMAIN,
            ),
        ),

    DateTimeField(
        'startDate',
        required = True,
        accessor='start',
        default_method='getDefaultStartDate',
        languageIndependent=True,
        index='FieldIndex:brains',
        write_restricted_permission=permissions.ReviewPortalContent,
        widget=CalendarWidget(
            label="Booking start date",
            description=("Enter the starting date and time, or click "
                         "the calendar icon and select it. "),
            label_msgid="label_booking_start_date",
            description_msgid="help_booking_start_date",
            i18n_domain=I18N_DOMAIN,
            ),
        ),

    DateTimeField(
        'endDate',
        required = True,
        accessor='end',
        default_method='getDefaultEndDate',
        languageIndependent=True,
        write_restricted_permission=permissions.ReviewPortalContent,
        index='FieldIndex:brains',
        widget=CalendarWidget(
            label="Booking end date",
            description=("Enter the ending date and time, or click "
                         "the calendar icon and select it. "),
            label_msgid="label_booking_end_date",
            description_msgid="help_booking_end_date",
            i18n_domain=I18N_DOMAIN,
            ),
        ),

    StringField(
        'periodicityUID',
        default_method='getDefaultPeriodicityUID',
        languageIndependant=True,
        index='FieldIndex',
        widget=StringWidget(
            visible={'edit': 'invisible', 'view': 'invisible'},
            ),
        ),
  ))

field = BookingSchema['description']
BookingSchema.delField('description')
BookingSchema.addField(field)

BookingSchema['id'].widget.visible={'view' : 'hidden', 'edit' : 'hidden'}
BookingSchema['title'].required = False
BookingSchema['title'].widget.label='Booking title'
BookingSchema['title'].widget.label_msgid='label_booking_title'
BookingSchema['title'].widget.i18n_domain='plonebooking'

BookingSchema['description'].schemata = 'default'
BookingSchema['description'].widget.label='Comment'
BookingSchema['description'].widget.label_msgid='label_booking_description'
BookingSchema['description'].widget.i18n_domain='plonebooking'
BookingSchema['description'].widget.description=' '
BookingSchema['description'].widget.description_msgid='help_booking_description'

BookableObjectSchema = BaseSchema.copy() + Schema((
    StringField(
        'type',
        required=True,
        index='FieldIndex:brains',
        vocabulary='getTypeVocabulary',
        widget=SelectionWidget(
            format='select',
            label="Type",
            label_msgid="label_bookableobject_type",
            i18n_domain=I18N_DOMAIN,
            ),
        ),

    StringField(
        'category',
        index='FieldIndex:brains',
        vocabulary='getCategoryVocabulary',
        widget=SelectionWidget(
            format='select',
            label="Category",
            label_msgid="label_bookableobject_category",
            i18n_domain=I18N_DOMAIN,
            ),
        ),

    ComputedField(
        'bookedObjectUID',
        index='FieldIndex:brains',
        expression='context.getBookableObject().UID()',
        widget=ComputedWidget(
            visible={'view': 'invisible', 'edit' : 'invisible'},
            ),
        ),

    TextField(
        'text',
        default_content_type='text/html',
        default_output_type='text/html',
        allowable_content_types=('text/html',),
        widget=VisualWidget(
            label="Text",
            label_msgid="label_bookableobject_text",
            i18n_domain=I18N_DOMAIN,
            ),
        ),


    StringField(
        'bookingReviewMode',
        vocabulary=BOOKING_REVIEW_MODES,
        default='default',
        widget=SelectionWidget(
            label='Booking review mode',
            description='',
            label_msgid='label_booking_review_mode',
            description_msgid='',
            i18n_domain=I18N_DOMAIN,
            ),
        ),
  ))

BookableObjectSchema['title'].widget.label = 'Bookable object title'
BookableObjectSchema['title'].widget.label_msgid = 'label_bookableobject_title'
BookableObjectSchema['title'].widget.i18n_domain = 'plonebooking'

BookableObjectSchema['description'].schemata = 'default'