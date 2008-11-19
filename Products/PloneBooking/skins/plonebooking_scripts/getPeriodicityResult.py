## -*- coding: utf-8 -*-
## Copyright (C)200x Ingeniweb - all rights reserved
## No publication or distribution without authorization.

## Script (Python) "getPeriodicityResult"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=uid, periodicity_type, periodicity_end_date, periodicity_variable=None
##title=
from Products.CMFCore.utils import getToolByName
periodicity_extras = {}
periodicity_type = int(periodicity_type)
# ###############
# Form validation
# ###############

# Define charset of result to make sure translation are really encoded in the correct charset
ptool = getToolByName(context, 'portal_properties')
charset = ptool.site_properties.default_charset
context.REQUEST.RESPONSE.setHeader('Content-Type','text/html; charset=%s' % charset)

# periodicity validation
if periodicity_type == 2:
    message = context.translate(msgid="message_give_number_for_periodicity", default="You must give a number for the periodicity.", domain="plonebooking")
    html_message = '<div class="portalMessage">%s</div>' % message
    if periodicity_variable:
        try:
            result = int(periodicity_variable)
            periodicity_extras['week_interval'] = result
        except:
            return html_message
    else:
        return html_message

# end date validation
try:
    end_date = DateTime(periodicity_end_date[:16])
except:
    message = context.translate(msgid="message_periodicity_end_date_not_valid", default="The periodicity end date is not valid.", domain="plonebooking")
    html_message = '<div class="portalMessage">%s</div>' % message
    return html_message

# generate HTML code
atool = getToolByName(context, 'archetype_tool')
obj = context#atool.getObject(uid)

if obj is None:
    message = context.translate(msgid="message_object_not_found", default="No object found.", domain="plonebooking")
    html_message = '<div class="portalMessage">%s</div>' % message
    return html_message

return context.booking_periodicity_result(periodicity_type=periodicity_type, periodicity_end_date=end_date, periodicity_extras=periodicity_extras, here_uid=uid)
                                                
