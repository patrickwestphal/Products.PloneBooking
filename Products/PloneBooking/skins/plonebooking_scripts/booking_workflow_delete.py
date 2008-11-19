## -*- coding: utf-8 -*-
## Copyright (C)200x Ingeniweb - all rights reserved
## No publication or distribution without authorization.

## Script (Python) "booking_workflow_delete"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=state_change
##title=Delete the booking and redirect to booked object
##

from Products.CMFPlone.utils import transaction_note
from DateTime import DateTime

# get the object
booking = state_change.object
booking_id = booking.getId()
booking_center = booking.getBookingCenter()
booked_object = booking.getBookableObject()
transaction_note('Deleted %s from %s' % (booking_id, booking.absolute_url()))

from Products.CMFCore.utils import getToolByName

booking_tool = getToolByName(booking, 'portal_booking')
booking_tool.cancelBooking(booking)

# raise the object deleted method and pass
# the folder you want to return to
raiseError = context.REQUEST.get_header("raiseError", True)

if raiseError == True:
    raise state_change.ObjectDeleted(booked_object)    

request = context.REQUEST
response = request.RESPONSE
response.setStatus(200)
response.write("")

