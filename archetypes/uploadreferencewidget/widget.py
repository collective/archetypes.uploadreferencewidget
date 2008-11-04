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

from Acquisition import aq_parent
from OFS.interfaces import IFolder
from AccessControl import ClassSecurityInfo
from ZPublisher.HTTPRequest import FileUpload
from Products.CMFCore.utils import getToolByName
from Products.CMFPlone.utils import _createObjectByType
from Products.Archetypes.Registry import registerWidget
from Products.Archetypes.Registry import registerPropertyType
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget


class UploadReferenceWidget(ReferenceBrowserWidget):

    _properties = ReferenceBrowserWidget._properties.copy()
    _properties.update({
        'macro': 'uploadreference',
        'helper_js': (
            'uploadreference.js',
            'referencebrowser.js',
            'select_lists.js',
        ),
    })

    security = ClassSecurityInfo()

    security.declarePublic('process_form')
    def process_form(self, instance, field, form, empty_marker=None,
                     emptyReturnsMarker=False, validating=True):
        """A custom implementation for the widget form processing."""
        if validating:
            # At the validation phase, only return the existing UID field
            # value or the filename of the new FileUpload object
            value = form.get(field.getName())
            if value:
                return value, {}

            value = empty_marker
            files_list = form.get('%s_file' % field.getName(), [])
            if files_list:
                obj = files_list[0]
                value = getattr(obj, 'filename', getattr(obj, 'name', ''))
            return value, {}

        option = form.get('%s_option' % field.getName(), empty_marker)
        value = form.get(field.getName(), empty_marker)

        # In this case, just do the trivial
        if option == 'select':
            if value is empty_marker:
                return empty_marker
            if emptyReturnsMarker and value == '':
                return empty_marker
            return value, {}

        # In this case, we need to create new object(s) and get its UID(s)
        if option == 'upload':
            result = []
            files_list = form.get('%s_file' % field.getName(), [])
            portal = getToolByName(instance, 'portal_url').getPortalObject()
            mt_tool = getToolByName(portal, 'mimetypes_registry')

            # Define the destination folder
            root = instance
            foldername = self.startup_directory
            if foldername.startswith('/'):
                root = portal
                foldername = foldername[1:]
            try:
                folder = root.restrictedTraverse(foldername)
            except (KeyError, AttributeError):
                # If the startup_directory doesn't exists, fallback to
                # the current instance if folderish, or its parent
                if IFolder.providedBy(instance):
                    folder = instance
                else:
                    folder = aq_parent(instance)

            for fileobj in files_list:
                # Normalize the filename
                filename = getattr(fileobj, 'filename', '')
                filename = filename.split('\\')[-1]

                if filename:
                    # Guess the mimetype & define the content-type class
                    content = 'File'
                    mimetype = str(mt_tool.classify(fileobj.read(1024)))
                    if mimetype.startswith('image'):
                        content = 'Image'

                    # Create the new content
                    old_id = folder.generateUniqueId(content)
                    new_id = folder.invokeFactory(content, id=old_id, title=filename)
                    obj = getattr(folder, new_id)
                    obj._renameAfterCreation()
                    obj.unmarkCreationFlag()
                    obj.update_data(fileobj, mimetype)

                    result.append(obj.UID())

            if field.multiValued:
                # Multi valued, append the old value
                result.extend(value)
            elif result:
                # Non multi valued, with a valid upload, return it
                result = result[0]
            else:
                # Non multi valued, with an invalid upload, return the old value
                result = value

            return result, {}

        return empty_marker


registerWidget(
    UploadReferenceWidget,
    title='Upload Reference Widget',
    description='A widget that allows you to upload a content '
                'and create a reference to it.',
    used_for=('Products.Archetypes.Field.ReferenceField',)
)
