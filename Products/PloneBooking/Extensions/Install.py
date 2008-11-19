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
    PloneBooking: Installation script
"""

__version__ = "$Revision: 1.16 $"
__author__  = ''
__docformat__ = 'restructuredtext'

from Products.Archetypes import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin

from Products.CMFCore.utils import getToolByName

from Products.ExternalMethod.ExternalMethod import ExternalMethod
from Products.PloneBooking import BookingPermissions
from Products.PloneBooking.BookingTool import BookingTool
from Products.PloneBooking.config import GLOBALS, PROJECTNAME, SKINS_DIR
from Products.PloneBooking.BookingPermissions import *

from StringIO import StringIO

# List of worflows asssociations :
# workflow_id
# list of types using this workflow
# create workflow ?
# is the workflow a default one ?
plonebooking_workflows = (
    ('folder_workflow', ('BookingCenter', ), False, False, ),
    ('booking_workflow', ('Booking', ), True, False, ),
    ('bookable_object_workflow', ('BookableObject', ), True, False, ),
)

def addWorkflow(self, out):
    
    workflowTool = getToolByName(self, 'portal_workflow')
    for name, types, create, default in plonebooking_workflows:
        if create and name not in workflowTool.objectIds():
            installFunc = ExternalMethod('temp', 'temp', PROJECTNAME + '.' + name,
                                         'create' + name.capitalize())
            workflow = installFunc(name)
            workflowTool._setObject(name, workflow)   
        if types:
            workflowTool.setChainForPortalTypes(types, name)
        if default:
            workflowTool.setDefaultChain(name)
    out.write("Workflow added")

def DEPRECATED_install(self):
    out = StringIO()
    
    # Install types
    typeInfo = listTypes(PROJECTNAME)
    installTypes(self, out,
                 typeInfo,
                 PROJECTNAME)

    # Install tools
    add_tool = self.manage_addProduct[PROJECTNAME].manage_addTool
    if not self.objectIds(spec=BookingTool.meta_type):
        add_tool(BookingTool.meta_type)
    
    # Install skin
    install_subskin(self, out, GLOBALS)
    
    # Install permissions
    self.manage_permission(BookingPermissions.AddBooking, ('Member', 'Owner', 'Manager'), 1)
    
    # Add portal types to use portal factory
    pftool = getToolByName(self, 'portal_factory')
    pftool.manage_setPortalFactoryTypes(listOfTypeIds=('Booking', 'BookableObject'))
    
    # Install workflows
    #addWorkflow(self, out)
    
    # Add action icons
    addActionIcon(self,
                  category='plone',
                  action_id='book',
                  icon_expr='booking.gif',
                  title="Book an object",
                  priority=0)
    
    # Hide Booking from the navtree
    ntp = getToolByName(self, 'portal_properties').navtree_properties
    bl = list(ntp.getProperty('metaTypesNotToList', ()))
    if 'Booking' not in bl:
        bl.append('Booking')
        ntp._p_changed = 1
        ntp.metaTypesNotToList = bl
    
    out.write('Installation completed.\n')
    return out.getvalue()


def addActionIcon(self, category, action_id, icon_expr, title=None, priority=0):
    # Add the action icon if and only if it's not already here
    ai=getToolByName(self, 'portal_actionicons')
    if ai.queryActionInfo( category, action_id ):
      ai.updateActionIcon(category, action_id, icon_expr, title, priority)
    else:
      ai.addActionIcon(category, action_id, icon_expr, title, priority)




def DEPRECATED_uninstall(self):
    out = StringIO()
    
    # uninstall workflows
    wf_tool = getToolByName(self, 'portal_workflow')
    
    for workflow_id, types, create, default in plonebooking_workflows:
        if create and workflow_id in wf_tool.objectIds():
            wf_tool._delObject(workflow_id)
            
    #wf_tool.setDefaultChain('plone_workflow')
    out.write('Workflow uninstalled.\n')
    out.write('Uninstallation completed.\n')
    return out.getvalue()
