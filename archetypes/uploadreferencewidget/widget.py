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

import mimetypes
from Acquisition import aq_parent
from OFS.interfaces import IFolder
from AccessControl import ClassSecurityInfo
from zope.component import queryUtility
from Products.CMFCore.utils import getToolByName
from Products.Archetypes.Registry import registerWidget
from archetypes.referencebrowserwidget.widget import ReferenceBrowserWidget

import pkg_resources
try:
    from z3c.blobfile.interfaces import IBlobFile, IBlobImage
    HAVE_BLOBS = True
except ImportError:
    HAVE_BLOBS = False

try:
    pkg_resources.get_distribution('plone.dexterity')
except pkg_resources.DistributionNotFound:
    HAS_DEXTERITY = False
    pass
else:
    HAS_DEXTERITY = True
    from plone.i18n.normalizer.interfaces import IURLNormalizer
    from plone.dexterity.utils import createContent, addContentToContainer

    if HAVE_BLOBS:
        from plone.namedfile import NamedBlobImage as Image
        from plone.namedfile import NamedBlobFile as File
    else:
        from plone.namedfile import NamedImage as Image
        from plone.namedfile import NamedFile as File

try:
    from plone.uuid.interfaces import IUUID
    HAS_UUID = True
except ImportError:
    HAS_UUID = False


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

            # Define the destination folder
            root = instance
            foldername = self.getStartupDirectory(instance, field)
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
                    mimetype = mimetypes.guess_type(filename)[0] or ""
                    if mimetype.startswith('image'):
                        content = 'Image'

                    # if HAS_DEXTERITY and FTI_von content = IDexteritykram:
                    # Create the new content
                    if HAS_DEXTERITY:
                        util = queryUtility(IURLNormalizer)
                        obj_id = util.normalize(filename)
                        filename = filename.decode('utf-8')
                        obj = createContent(content, id=obj_id, title=filename)
                        obj = addContentToContainer(folder, obj)
                        fileobj.seek(0)
                        data = fileobj.read()
                        headers = fileobj.headers
                        contentType = 'application/octet-stream'
                        if headers:
                            contentType = headers.get('Content-Type', contentType)
                        obj.filename = filename
                        if content == 'File':
                            obj.file = File(data, contentType=contentType, filename=filename)
                        else:
                            obj.image = Image(data, contentType=contentType, filename=filename)
                    else:
                        # Create Content with Archtypes
                        old_id = folder.generateUniqueId(content)
                        new_id = folder.invokeFactory(content, id=old_id, title=filename)
                        obj = getattr(folder, new_id)
                        obj._renameAfterCreation()
                        obj.unmarkCreationFlag()
                        obj.update_data(fileobj, mimetype)
                    obj.reindexObject()

                    if HAS_UUID:
                        result.append(IUUID(obj, None))
                    else:
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
