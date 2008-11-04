#
# archetypes.uploadreferencewidget
# Copyright(C), 2008, Enfold Systems, Inc. - ALL RIGHTS RESERVED
#
# This software is licensed under the Terms and Conditions
# contained within the "LICENSE.txt" file that accompanied
# this software.  Any inquiries concerning the scope or
# enforceability of the license should be addressed to:
#
# Enfold Systems, Inc.
# 4617 Montrose Blvd., Suite C215
# Houston, Texas 77006 USA
# p. +1 713.942.2377 | f. +1 832.201.8856
# www.enfoldsystems.com
# info@enfoldsystems.com
#

"""Base class for integration tests, based on ZopeTestCase and PloneTestCase.

Note that importing this module has various side-effects: it registers a set of
products with Zope, and it sets up a sandbox Plone site with the appropriate
products installed.
"""

import os
import doctest
from Testing import ZopeTestCase

# Import PloneTestCase - this registers more products with Zope as a side effect
from Products.PloneTestCase import PloneTestCase

from archetypes.uploadreferencewidget.config import PRODUCT_DIR


# Set up a Plone site, and install our custom widget product
PloneTestCase.setupPloneSite(products=['archetypes.referencebrowserwidget', 
    'archetypes.uploadreferencewidget'])

OPTIONFLAGS = (doctest.REPORT_ONLY_FIRST_FAILURE |
               doctest.ELLIPSIS |
               doctest.NORMALIZE_WHITESPACE)


class IntegrationTestCase(PloneTestCase.PloneTestCase):
    """Base class for the UploadReferenceWidget product integration tests.

    This may provide specific set-up and tear-down operations, or provide
    convenience methods.
    """

    def _setup(self):
        PloneTestCase.PloneTestCase._setup(self)
        self.IMG = open(os.path.join(PRODUCT_DIR, 'tests', 'enfold.gif'))
        self.PDF = open(os.path.join(PRODUCT_DIR, 'tests', 'enfold.pdf'))

    def createMemberarea(self, name):
        # Bypass PTC's creation of a home folder for the default user
        pass


class FunctionalTestCase(IntegrationTestCase, PloneTestCase.FunctionalTestCase):
    pass
