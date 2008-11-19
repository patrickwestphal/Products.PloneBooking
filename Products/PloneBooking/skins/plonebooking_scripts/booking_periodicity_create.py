## -*- coding: utf-8 -*-
## Copyright (C)200x Ingeniweb - all rights reserved
## No publication or distribution without authorization.

## Script (Python) "booking_periodicity_create"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=uid, periodicity_type, periodicity_end_date, periodicity_variable
##title=
from Products.CMFCore.utils import getToolByName

at_tool = getToolByName(context, 'archetype_tool')
obj = at_tool.getObject(uid)

# end date validation
try:
    end_date = DateTime(periodicity_end_date[:16])
except:
    return '<div class="portalMessage">The periodicity end date is not valid</div>'

if obj is None:
    return '<div class="portalMessage">No object found.</div>'

result = ""

if periodicity_variable:
    result = obj.createPeriodicBookings(int(periodicity_type), end_date, week_interval=int(periodicity_variable))
else:
    result = obj.createPeriodicBookings(int(periodicity_type), end_date)
    
return '<div class="portalMessage">%s</div>' % result

