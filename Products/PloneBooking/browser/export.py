# -*- coding: utf-8 -*-
## PloneBooking: Online Booking Tool to allow booking on any kind of ressource
## Copyright (C) 2008 Ingeniweb

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
"""

import csv
import cStringIO

from zope.component import getUtility
from zope.interface import implements
#from zope.i18n import translate

from DateTime import DateTime
from Products.Five import BrowserView

from Products.CMFCore.utils import getToolByName

# from Products.Five.browser.pagetemplatefile import ZopeTwoPageTemplateFile
from Products.PloneBooking.interfaces import IBookingExporter
from Products.PloneBooking import PloneBookingFactory as _

from zope.i18n.interfaces import ITranslationDomain, INegotiator

class BookingExporter:
    """
        Basic implementation of a Booking exporter.
        You can orverride this implementation by using some
        ZCML in an overrides.zcml
    """
    
    implements(IBookingExporter)
    
    def getFields(self):
        """
            Return the labels of all the fields for this export
        """
        return [
            _("label_booking_user_full_name", "Full Name"),
            _("label_booking_user_phone", "Phone"),
            _("label_booking_user_email", "Email"),
            _("label_booking_start_date", "Booking start date"),
            _("label_booking_end_date", "Booking end date"),
        ]
        
    def getValues(self, brains):
        """
            Return a list of values associated with this brain.
        """
        results = []
        for brain in brains:
            ## wake up the object: perhaps there is another way to do that
            ## but I don't think it's very efficient to put all the data
            ## of the booking in the catalog metadata...
            booking = brain.getObject()
            results.append(
                (
                    booking.getFullName(),
                    booking.getPhone(),
                    booking.getEmail(),
                    booking.getStartDate(),
                    booking.getEndDate(),
                )
            )

        return results
    
    def getPortalType(self):
        """
            Return the portal to use for the request
        """
        return "Booking"
    
    def getEncoding(self):
        """
            Get the encoding that will be used for the CSV export
        """
        return "utf-8"

class Export(BrowserView):
    """
        Export the bookables of a selected ressource (ressource type given
        in the context)
    """
    # implements(IBookingExporter)
    
    def __init__(self, context, request):
        BrowserView.__init__(self, context, request)
        self.exporter = getUtility(IBookingExporter)
        self.catalog = getToolByName(self.context, "portal_catalog")
        
        if request.form.get("export_type") == "csv":
            self.__call__ = self.exportToCsv
        elif request.form.get("export_type") == "html":
            self.values = self.getValues()
            if len(self.values) < 1:
                self.context.plone_utils.addPortalMessage(
                    _(
                        'info_no_results',
                        "There is no booking matching your criteria."
                    ),
                    "info",
                )
        else:
            self.values = None

            
    def getBrains(self):
        """
            Get the brains associated with the export request
        """
        
        query = {
            ## TODO: perhaps replace this criterion with "provided_by" once the
            ## interface would appear in the catalog...
            "portal_type": self.exporter.getPortalType(),
            "path": "/".join(self.context.getPhysicalPath()),
            "start": {
                "query": self.start,
                "range": "min",
            },
            "end": {
                "query": self.end,
                "range": "max",
            },
        }

        brains = self.catalog(**query)
        return brains
        
    def getFields(self):
        """
            Return translated fields in a list of unicode
        """
        fields = getUtility(IBookingExporter).getFields()
        return [self.context.translate(field, domain=field.domain) for field in fields]
    
    def getValues(self):
        try:
            self.start = DateTime(int(self.context.request.form["ts_start"]))
            self.end = DateTime(int(self.context.request.form["ts_end"]))
        except KeyError:
            self.context.request.response.redirect(
                self.context.absolute_url() + "/export_form"
            )

        if self.start + 6000 < self.end:
            # in this case, the range is too big: we filter to have a range
            # that is less than 60 days.
            self.context.plone_utils.addPortalMessage(
                _(
                    'error_range_too_large',
                    "Please enter a range that fits into 2 monthes."
                ),
                "error",
            )
            self.context.request.response.redirect(
                self.context.absolute_url() + "/export_form"
            )

        return self.exporter.getValues(self.getBrains())
    
    def getEncoding(self):
        """
            Return the encoding of the CSV file
        """
        return getUtility(IBookingExporter).getEncoding()
    
    def exportToCsv(self):
        """
            Called only when the user select "CSV" export type
        """
        fields = self.getFields()
        values = self.getValues()
       
        stream = cStringIO.StringIO()
        writer = csv.writer(stream)
        encoding = self.getEncoding()

        writer.writerow([field.encode(encoding) for field in fields])
        writer.writerows(values)
        
        result = stream.getvalue()
        stream.close()
        response = self.context.request.response
        response.setHeader("Content-Type", "text/csv")
        response.setHeader("Content-Encoding", encoding)
        response.setHeader(
            "Content-Disposition",
            "attachment; filename=booking-%s-%s-%s.csv" % (
                self.context.getId(),
                self.start.strftime("%Y%m%d"),
                self.end.strftime("%Y%m%d"),
            )
        )
        return result

    def exportToHtml(self):
        """
            Called by the page template, return a list of list containing all the
            fields to display
        """
        
        return self.values
