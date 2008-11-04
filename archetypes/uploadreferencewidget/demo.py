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

from Products.Archetypes.public import registerType
from Products.Archetypes.public import Schema
from Products.Archetypes.public import BaseSchema
from Products.Archetypes.public import BaseContent
from Products.Archetypes.public import ReferenceField
from archetypes.uploadreferencewidget.widget import UploadReferenceWidget

URWSchema = BaseSchema.copy() + Schema((

    ReferenceField(
        name='ref1',
        allowed_types=('File', 'Image'),
        relationship='rel1',
        required=True,
        widget=UploadReferenceWidget(
            label='Single Reference',
            description='This is the first field. It can reference a '
                        'single item. This field uses the site root as '
                        'the the startup directory.',
            startup_directory='/',
        ),
    ),

    ReferenceField(
        name='ref2',
        multiValued=True,
        allowed_types=('File', 'Image'),
        relationship='rel2',
        widget=UploadReferenceWidget(
            label='Multiple References',
            description='This is the second field. It can reference '
                        'multiple items. This field uses the current '
                        'folder as the startup directory.',
            startup_directory='',
        ),
    ),

    ReferenceField(
        name='ref3',
        allowed_types=('File', 'Image'),
        relationship='rel3',
        schemata='invalid',
        widget=UploadReferenceWidget(
            label='Invalid Path',
            description='This is the third field. It can reference a '
                        'single item. This field uses an invalid path '
                        'the the startup directory.',
            startup_directory='/non_existent',
        ),
    ),

))


class UploadReferenceWidgetDemo(BaseContent):
    """Demo content-type for testing UploadReferenceWidget."""
    schema = URWSchema


registerType(UploadReferenceWidgetDemo)
