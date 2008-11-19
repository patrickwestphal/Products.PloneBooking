## Controller Python Script "booking_manage"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=ids=[]
##title= Manage booking
##

from Products.CMFCore.utils import getToolByName
request = context.REQUEST
response = request.RESPONSE
wtool = getToolByName(context, 'portal_workflow')
booked_obj = context.getBookedObject()
wf_action = None
redirect_to_booked_obj = False

if request.has_key('form.button.Retract'):
		wf_action = 'cancel'
elif request.has_key('form.button.RetractAll'):
		wf_action = 'cancel'
		ids = [x.getId for x in	context.getAllPeriodicBookingBrains()]
		redirect_to_booked_obj = True
elif request.has_key('form.button.Book'):
		wf_action = 'book'
elif request.has_key('form.button.BookAll'):
		wf_action = 'book'
		ids = [x.getId for x in	context.getAllPeriodicBookingBrains()]

if wf_action is not None:
		for booking_id in ids:
				booking_obj = getattr(booked_obj, booking_id)
				try:
						wtool.doActionFor(booking_obj, wf_action)
				except:
						pass

state.setNextAction('redirect_to:string:%s' % context.absolute_url())
if redirect_to_booked_obj:
		state.setNextAction('redirect_to:string:%s' % booked_obj.absolute_url())

message='Your changes have been saved.'
return state.set(status='success', portal_status_message=message)