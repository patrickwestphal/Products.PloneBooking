## -*- coding: utf-8 -*-
## Copyright (C)200x Ingeniweb - all rights reserved
## No publication or distribution without authorization.

## Controller Python Script "plonebooking_add"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=obj_uid=None, start_ts=None, end_ts=None, ajax=None
##title= Add new booking
##

from Products.CMFCore.utils import getToolByName

request  = context.REQUEST
response = request.RESPONSE

atool = getToolByName(context, 'archetype_tool')
btool = getToolByName(context, 'portal_booking')
ftool = getToolByName(context, 'portal_factory')

type_name = 'Booking'

query_args = {}
use_factory = ftool.getFactoryTypes().has_key(type_name)
bookable_obj = None

if obj_uid is None:
    bookable_obj = context.getBookableObject()
else:
    bookable_obj = atool.getObject(obj_uid)
booking_id = context.generateUniqueId(type_name)
start_date = end_date = None
date_format = '%Y/%m/%d %H:%M:%S'
if start_ts is not None:
    start_date = btool.getZDateTimeFromts(start_ts)
    query_args['startDate:date'] = start_date.strftime(date_format)
    query_args['start_ts'] = start_ts

if end_ts is not None:
    end_date = btool.getZDateTimeFromts(end_ts)
    query_args['endDate:date'] = end_date.strftime(date_format)
    query_args['end_ts'] = end_ts

if use_factory:
    booking_obj = bookable_obj.restrictedTraverse('portal_factory/%s/%s' % (type_name, booking_id))
else:
    bookable_obj.invokeFactory(type_name, booking_id)
    booking_obj = getattr(bookable_obj, booking_id)
    booking_obj.setStartDate(start_date)
    booking_obj.setEndDate(end_date)

if ajax:
    redirect_url = '%s/booking_ajax_form' % booking_obj.absolute_url()
else:
    redirect_url = '%s/base_edit' % booking_obj.absolute_url()
if query_args:
    query_string = '&'.join(['='.join((k, v,)) for k, v in query_args.items()])
    redirect_url = '%s?%s' % (redirect_url, query_string)

return response.redirect(redirect_url)