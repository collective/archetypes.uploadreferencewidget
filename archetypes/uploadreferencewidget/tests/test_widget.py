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

from Testing import ZopeTestCase
from Products.CMFPlone.utils import _createObjectByType

from StringIO import StringIO
from Products.PloneTestCase import PloneTestCase
from archetypes.uploadreferencewidget.tests import URWTestCase
from archetypes.uploadreferencewidget.widget import UploadReferenceWidget

from archetypes.uploadreferencewidget.tests.utils import FakeRequest
from archetypes.uploadreferencewidget.tests.utils import FakeFileUpload


class IntegrationTests(URWTestCase.IntegrationTestCase):

    def afterSetUp(self):
        self.doc = _createObjectByType('Document', self.portal, id='doc')
        self.image = _createObjectByType('Image', self.portal, id='image')
        self.field = self.doc.getField('relatedItems')
        self.field.isMetadata = False
        self.setRoles('Manager')
        self.request = FakeRequest()

    def uploadContentToPath(self, obj, path, destination):
        field = obj.getField('relatedItems')
        fileupload = FakeFileUpload(filename='enfold.pdf', file=self.PDF)
        field.widget = UploadReferenceWidget(startup_directory=path)
        form = {
            'relatedItems_option': 'upload',
            'relatedItems_file': [fileupload],
        }
        self.request.form.update(form)
        obj.processForm(REQUEST=self.request)
        expected = destination.objectValues('ATFile')
        result = obj.getRefs('relatesTo')
        self.assertEqual(expected, result)

    def testSelectExistingContentProcessWidget(self):
        self.field.widget = UploadReferenceWidget()
        form = {
            'relatedItems': [self.image.UID()],
            'relatedItems_option': 'select',
        }
        expected = [self.image.UID()], {}
        result = self.field.widget.process_form(self.doc, self.field, form,
                                                validating=False)
        self.assertEqual(expected, result)

    def testValidateUploadWithoutSelectAFileInARequiredField(self):
        fileupload = FakeFileUpload(filename='', file=StringIO())
        self.field.widget = UploadReferenceWidget()
        self.field.required = True
        self.field.multiValued = False

        # First force a validation error, as we don't pass anything:
        form = {
            'relatedItems': '',
            'relatedItems_option': 'upload',
            'relatedItems_file': [fileupload],
        }
        value, errors = self.field.widget.process_form(self.doc, self.field,
                                                       form, validating=False)
        result = self.field.validate(value, self.doc, errors)
        self.failUnless('required' in result)

        # Then pass something as the field previous value, no error this time:
        form = {
            'relatedItems': 'something',
            'relatedItems_option': 'upload',
            'relatedItems_file': [fileupload],
        }
        value, errors = self.field.widget.process_form(self.doc, self.field,
                                                       form, validating=False)
        result = self.field.validate(value, self.doc, errors)
        self.assertEqual(result, None)

        # Finally, upload a valid file. Again, no error:
        fileupload = FakeFileUpload(filename='foo.txt', file=StringIO('foo'))
        form = {
            'relatedItems': '',
            'relatedItems_option': 'upload',
            'relatedItems_file': [fileupload],
        }
        value, errors = self.field.widget.process_form(self.doc, self.field,
                                                       form, validating=False)
        result = self.field.validate(value, self.doc, errors)
        self.assertEqual(result, None)

    def testSelectMultipleExistingContentProcessWidget(self):
        video = _createObjectByType('File', self.portal, id='video')
        self.field.widget = UploadReferenceWidget()
        form = {
            'relatedItems': [self.image.UID(), video.UID()],
            'relatedItems_option': 'select',
        }
        expected = [self.image.UID(), video.UID()], {}
        result = self.field.widget.process_form(self.doc, self.field, form,
                                                validating=False)
        self.assertEqual(expected, result)

    def testSelectExistingContentCreateReference(self):
        self.field.widget = UploadReferenceWidget()
        form = {
            'relatedItems': [self.image.UID()],
            'relatedItems_option': 'select',
        }
        self.request.form.update(form)
        self.doc.processForm(REQUEST=self.request)
        expected = [self.image]
        result = self.doc.getRefs('relatesTo')
        self.assertEqual(expected, result)

    def testSelectMultipleExistingContentCreateReferences(self):
        video = _createObjectByType('File', self.portal, id='video')
        self.field.widget = UploadReferenceWidget()
        form = {
            'relatedItems': [self.image.UID(), video.UID()],
            'relatedItems_option': 'select',
        }
        self.request.form.update(form)
        self.doc.processForm(REQUEST=self.request)
        expected = [self.image, video]
        result = self.doc.getRefs('relatesTo')
        self.assertEqual(expected, result)

    def testUploadImageCreateObjectAndReference(self):
        fileupload = FakeFileUpload(filename='enfold.gif', file=self.IMG)
        self.field.widget = UploadReferenceWidget(startup_directory='test')
        self.portal.invokeFactory('Folder', id='test')
        form = {
            'relatedItems_option': 'upload',
            'relatedItems_file': [fileupload],
        }
        self.request.form.update(form)
        self.doc.processForm(REQUEST=self.request)
        expected = self.portal.test.objectValues('ATImage')
        result = self.doc.getRefs('relatesTo')
        self.assertEqual(expected, result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].getContentType(), 'image/gif')

    def testUploadFileCreateObjectAndReference(self):
        fileupload = FakeFileUpload(filename='enfold.pdf', file=self.PDF)
        self.field.widget = UploadReferenceWidget(startup_directory='test')
        self.portal.invokeFactory('Folder', id='test')
        form = {
            'relatedItems_option': 'upload',
            'relatedItems_file': [fileupload],
        }
        self.request.form.update(form)
        self.doc.processForm(REQUEST=self.request)
        expected = self.portal.test.objectValues('ATFile')
        result = self.doc.getRefs('relatesTo')
        self.assertEqual(expected, result)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].getContentType(), 'application/pdf')

    def testUploadKeepCurrentReferencesForMultiValuedField(self):
        fileupload = FakeFileUpload(filename='enfold.pdf', file=self.PDF)
        self.field.widget = UploadReferenceWidget(startup_directory='test')
        self.portal.invokeFactory('Folder', id='test')
        form = {
            'relatedItems': [self.image.UID()],
            'relatedItems_option': 'upload',
            'relatedItems_file': [fileupload],
        }
        self.request.form.update(form)
        self.doc.processForm(REQUEST=self.request)
        expected = self.portal.test.objectValues() + [self.image]
        result = self.doc.getRefs('relatesTo')
        self.assertEqual(len(expected), 2)
        self.assertEqual(expected, result)

    def testUploadKeepCurrentReferencesForMultiValuedFieldWithMultipleUploads(self):
        fileupload1 = FakeFileUpload(filename='enfold.pdf', file=self.PDF)
        fileupload2 = FakeFileUpload(filename='enfold.gif', file=self.IMG)
        self.field.widget = UploadReferenceWidget(startup_directory='test')
        self.portal.invokeFactory('Folder', id='test')
        form = {
            'relatedItems': [self.image.UID()],
            'relatedItems_option': 'upload',
            'relatedItems_file': [fileupload1, fileupload2],
        }
        self.request.form.update(form)
        self.doc.processForm(REQUEST=self.request)
        expected = self.portal.test.objectValues() + [self.image]
        result = self.doc.getRefs('relatesTo')
        self.assertEqual(len(expected), 3)
        self.assertEqual(expected, result)

    def testUploadReplaceCurrentReferencesForSingleValuedField(self):
        fileupload = FakeFileUpload(filename='enfold.pdf', file=self.PDF)
        self.field.multiValued = False
        self.field.widget = UploadReferenceWidget(startup_directory='test')
        self.portal.invokeFactory('Folder', id='test')
        form = {
            'relatedItems': self.image.UID(),
            'relatedItems_option': 'upload',
            'relatedItems_file': [fileupload],
        }
        self.request.form.update(form)
        self.doc.processForm(REQUEST=self.request)
        expected = self.portal.test.objectValues()
        result = self.doc.getRefs('relatesTo')
        self.assertEqual(expected, result)

    def testUploadKeepReferenceWhenUploadingWithoutAValueForMultiValuedField(self):
        fileupload = FakeFileUpload(filename='', file=StringIO())
        self.field.widget = UploadReferenceWidget(startup_directory='test')
        self.portal.invokeFactory('Folder', id='test')
        form = {
            'relatedItems': [self.image.UID()],
            'relatedItems_option': 'upload',
            'relatedItems_file': [fileupload],
        }
        self.request.form.update(form)
        self.doc.processForm(REQUEST=self.request)
        self.assertEqual(self.portal.test.objectValues(), [])
        expected = [self.image]
        result = self.doc.getRefs('relatesTo')
        self.assertEqual(expected, result)

    def testUploadKeepReferenceWhenUploadingWithoutAValueForSingleValuedField(self):
        fileupload = FakeFileUpload(filename='', file=StringIO())
        self.field.multiValued = False
        self.field.widget = UploadReferenceWidget(startup_directory='test')
        self.portal.invokeFactory('Folder', id='test')
        form = {
            'relatedItems': self.image.UID(),
            'relatedItems_option': 'upload',
            'relatedItems_file': [fileupload],
        }
        self.request.form.update(form)
        self.doc.processForm(REQUEST=self.request)
        self.assertEqual(self.portal.test.objectValues(), [])
        expected = [self.image]
        result = self.doc.getRefs('relatesTo')
        self.assertEqual(expected, result)

    def testUploadCreateObjectOnCurrentForCurrentPathNonFolderish(self):
        folder1 = _createObjectByType('Folder', self.portal, id='folder1')
        folder2 = _createObjectByType('Folder', folder1, id='folder2')
        new = _createObjectByType('Document', folder2, id='new')
        self.uploadContentToPath(new, '', folder2)

    def testUploadCreateObjectOnSelfForCurrentPathFolderish(self):
        folder1 = _createObjectByType('Folder', self.portal, id='folder1')
        folder2 = _createObjectByType('Folder', folder1, id='folder2')
        new = _createObjectByType('Folder', folder2, id='new')
        self.uploadContentToPath(new, '', new)

    def testUploadCreateObjectOnRootForRootPathNonFolderish(self):
        folder1 = _createObjectByType('Folder', self.portal, id='folder1')
        folder2 = _createObjectByType('Folder', folder1, id='folder2')
        new = _createObjectByType('Document', folder2, id='new')
        self.uploadContentToPath(new, '/', self.portal)

    def testUploadCreateObjectOnRootForRootPathFolderish(self):
        folder1 = _createObjectByType('Folder', self.portal, id='folder1')
        folder2 = _createObjectByType('Folder', folder1, id='folder2')
        new = _createObjectByType('Folder', folder2, id='new')
        self.uploadContentToPath(new, '/', self.portal)

    def testUploadCreateObjectOnAbsoluteForAbsolutePathNonFolderish(self):
        folder1 = _createObjectByType('Folder', self.portal, id='folder1')
        folder2 = _createObjectByType('Folder', folder1, id='folder2')
        new = _createObjectByType('Document', self.portal, id='new')
        self.uploadContentToPath(new, '/folder1/folder2', folder2)

    def testUploadCreateObjectOnAbsoluteForAbsolutePathFolderish(self):
        folder1 = _createObjectByType('Folder', self.portal, id='folder1')
        folder2 = _createObjectByType('Folder', folder1, id='folder2')
        new = _createObjectByType('Folder', self.portal, id='new')
        self.uploadContentToPath(new, '/folder1/folder2', folder2)

    def testUploadCreateObjectOnRelativeForRelativePathNonFolderish(self):
        folder1 = _createObjectByType('Folder', self.portal, id='folder1')
        folder2 = _createObjectByType('Folder', folder1, id='folder2')
        new = _createObjectByType('Document', folder1, id='new')
        self.uploadContentToPath(new, 'folder2', folder2)

    def testUploadCreateObjectOnParentForInvalidRelativePathNonFolderish(self):
        folder1 = _createObjectByType('Folder', self.portal, id='folder1')
        folder2 = _createObjectByType('Folder', folder1, id='folder2')
        new = _createObjectByType('Document', folder1, id='new')
        self.uploadContentToPath(new, 'invalid', folder1)

    def testUploadCreateObjectOnSelfForInvalidRelativePathFolderish(self):
        folder1 = _createObjectByType('Folder', self.portal, id='folder1')
        folder2 = _createObjectByType('Folder', folder1, id='folder2')
        new = _createObjectByType('Folder', folder1, id='new')
        self.uploadContentToPath(new, 'invalid', new)

    def testUploadCreateObjectOnParentForInvalidAbsolutePathNonFolderish(self):
        folder1 = _createObjectByType('Folder', self.portal, id='folder1')
        folder2 = _createObjectByType('Folder', folder1, id='folder2')
        new = _createObjectByType('Document', folder1, id='new')
        self.uploadContentToPath(new, '/invalid', folder1)

    def testUploadCreateObjectOnSelfForInvalidAbsolutePathFolderish(self):
        folder1 = _createObjectByType('Folder', self.portal, id='folder1')
        folder2 = _createObjectByType('Folder', folder1, id='folder2')
        new = _createObjectByType('Folder', folder1, id='new')
        self.uploadContentToPath(new, '/invalid', new)


def test_suite():
    from unittest import TestSuite, makeSuite
    suite = TestSuite()
    suite.addTest(makeSuite(IntegrationTests))
    suite.addTest(ZopeTestCase.FunctionalDocFileSuite(
        'widget.txt',
        optionflags=URWTestCase.OPTIONFLAGS,
        package='archetypes.uploadreferencewidget.tests',
        test_class=URWTestCase.FunctionalTestCase))
    return suite
