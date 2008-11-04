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

from ZPublisher.HTTPRequest import FileUpload


class FakeRequest:
    """Dummy request object.
    """
    def __init__(self):
        self.other = {}
        self.form = {}


class FakeFileUpload(FileUpload):
    """Dummy upload object.
    """
    __allow_access_to_unprotected_subobjects__ = 1
    headers = {}
    filename = 'dummy.gif'

    def __init__(self, filename=None, headers=None, file=None):
        self.file = file
        if filename is not None:
            self.filename = filename
        if headers is not None:
            self.headers = headers

    def seek(self, *args):
        return self.file.seek(*args)

    def tell(self, *args):
        return self.file.tell(*args)

    def read(self, *args):
        return self.file.read(*args)
