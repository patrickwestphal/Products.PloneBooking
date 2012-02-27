from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.testing import z2
from zope.configuration import xmlconfig

import Products.PloneBooking

class ProductsPloneBooking(PloneSandboxLayer):
    """Test layer for Products.PloneBooking"""
    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configuration_context):
        """Set up Zope for testing"""
        xmlconfig.file(
                'configure.zcml',
                Products.PloneBooking,
                context=configuration_context
        )
        with z2.zopeApp() as app:
            z2.installProduct(app, 'Products.PloneBooking')

    def setUpPloneSite(self, portal):
        """Set up Plone for testing"""
        applyProfile(portal, 'Products.PloneBooking:default')


PRODUCTS_PLONEBOOKING_FIXTURE = ProductsPloneBooking()
PRODUCTS_PLONEBOOKING_INTEGRATION_TESTING = IntegrationTesting(
        bases=(PRODUCTS_PLONEBOOKING_FIXTURE,),
        name='ProductsPloneBooking:Integration',
)
