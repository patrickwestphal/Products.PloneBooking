## -*- coding: utf-8 -*-
## Copyright (C)200x Ingeniweb - all rights reserved
## No publication or distribution without authorization.

## Script (Python) "booking_workflow_notification"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=notified_obj
##title=Workflow notification
##

from Products.CMFCore.utils import getToolByName

# Get review state
wf_tool = getToolByName(context, 'portal_workflow')
obj_review_state = wf_tool.getInfoFor(notified_obj, 'review_state')
mship = context.portal_membership

try:
    mhost = context.MailHost
except:
    # no mailhost found
    mhost = None

# the message format, %s will be filled in from data
message_template = """
From: %s
To: %s
Subject: %s - %s

%s

URL: %s
"""


if mhost:
    if 'booked' == obj_review_state:
        # object has been booked, contact the user
        receiver = notified_obj.getEmail()
        sender = context.email_from_address
        subject = 'Confirmation de reservation'
        body = 'Votre reservation du %s au %s a bien été enregistrée.'
        body = body % (notified_obj.startDate, notified_obj.endDate)
        url=notified_obj.absolute_url()

    if 'pending' == obj_review_state:
        # a booking is pending, contact the admin
        receiver = context.email_from_address
        sender = notified_obj.getEmail()
        subject = 'Demande de reservation'
        body = 'Cet item a été réservé par %s ; à vous de le confirmer en le rendant "public".' %(notified_obj.Creator())
        url=notified_obj.absolute_url()

    if 'canceled' == obj_review_state:
        # a booking has been canceled, contact the user
        receiver = notified_obj.getEmail()
        sender = context.email_from_address
        subject = 'Annulation de reservation '
        body = 'La reservation de cet item par %s a été annulée.'  %(notified_obj.Creator())
        url=''

    msg = message_template % (
             sender,
             receiver,
             subject,
             notified_obj.TitleOrId(),
             body,
             url
          )
    try:
        mhost.send(msg)
    except:
        # send mail failed
        pass
