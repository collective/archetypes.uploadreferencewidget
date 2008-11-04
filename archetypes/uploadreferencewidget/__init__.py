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

from Products.CMFCore import utils
from Products.CMFCore.permissions import AddPortalContent
from Products.CMFCore.DirectoryView import registerDirectory

from Products.Archetypes.public import listTypes
from Products.Archetypes.public import process_types

from archetypes.uploadreferencewidget import config
from archetypes.uploadreferencewidget import demo

# This patch can be removed when the Archetypes 1.6/1.5.5/1.4.6
# versions are released
import patch

def initialize(context):

    content_types, constructors, ftis = process_types(
        listTypes(config.PROJECTNAME), config.PROJECTNAME)

    utils.ContentInit(
        config.PROJECTNAME + ' Content',
        content_types=content_types,
        permission=AddPortalContent,
        extra_constructors=constructors,
        fti=ftis,
    ).initialize(context)
