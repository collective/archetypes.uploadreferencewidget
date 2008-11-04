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

from inspect import getargs
from Products.Archetypes.utils import mapply
from Products.Archetypes.Widget import TypesWidget
from Products.Archetypes.BaseObject import BaseObject

# If the process_form method has less than three default values,
# then we need to patch it
PATCH_PROCESS_FORM = False

args = getargs(TypesWidget.process_form.im_func.func_code)[0]
if 'validating' not in args:
    PATCH_PROCESS_FORM = True

try:
    from Products.Archetypes.interfaces import IMultiPageSchema
    MULTI_PAGE = True
except ImportError:
    # BBB: Archetypes 1.4.x
    class IMultiPageSchema:
        def providedBy(self):
            pass
    MULTI_PAGE = False

_marker = []

def patched_processForm(self, data=1, metadata=None, REQUEST=None, values=None):
    request = REQUEST or self.REQUEST
    if values:
        form = values
    else:
        form = request.form
    fieldset = form.get('fieldset', None)
    schema = self.Schema()
    schemata = self.Schemata()
    fields = []

    if MULTI_PAGE and not IMultiPageSchema.providedBy(self):
        fields = schema.fields()
    elif fieldset is not None:
        fields = schemata[fieldset].fields()
    else:
        if data:
            fields += schema.filterFields(isMetadata=0)
        if metadata:
            fields += schema.filterFields(isMetadata=1)

    form_keys = form.keys()

    for field in fields:
        ## Delegate to the widget for processing of the form
        ## element.  This means that if the widget needs _n_
        ## fields under a naming convention it can handle this
        ## internally.  The calling API is process_form(instance,
        ## field, form) where instance should rarely be needed,
        ## field is the field object and form is the dict. of
        ## kv_pairs from the REQUEST
        ##
        ## The product of the widgets processing should be:
        ##   (value, **kwargs) which will be passed to the mutator
        ##   or None which will simply pass

        if not field.writeable(self):
            # If the field has no 'w' in mode, or the user doesn't
            # have the required permission, or the mutator doesn't
            # exist just bail out.
            continue

        try:
            # Pass validating=False to inform the widget that we
            # aren't in the validation phase, IOW, the returned
            # data will be forwarded to the storage
            result = field.widget.process_form(self, field, form,
                                               empty_marker=_marker,
                                               validating=False)
        except TypeError:
            # Support for old-style process_form methods
            result = field.widget.process_form(self, field, form,
                                               empty_marker=_marker)

        if result is _marker or result is None:
            continue

        # Set things by calling the mutator
        mutator = field.getMutator(self)
        __traceback_info__ = (self, field, mutator)
        result[1]['field'] = field.__name__
        mapply(mutator, result[0], **result[1])

    self.reindexObject()

if PATCH_PROCESS_FORM:
    BaseObject._processForm = patched_processForm
