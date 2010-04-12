Upload Reference Widget
=======================

  The Upload Reference Widget aims to be the primary mechanism for uploading a
  file when creating a content item that uses the file. Instead of embedding
  the file into the content item, this widget uploads the file as a separate
  item and automatically populates a reference in the content item. Now Plone
  can reuse image and file assets in a more user-friendly way.


The problem
-----------

  One of the biggest issues we have seen re-using file assets in the Plone
  CMS is that once a file is uploaded as an attribute of content; you can not
  easily reuse it. Take this scenerio for instance:

    - You create a 'News Item' in '/news/foo.html' and upload an image,
      'logo.jpg', that shows a picture of a corporate logo. To address this
      image you must goto a URL like, 'http://host/news/foo.html/logo.jpg'.

    - Two weeks later you create another 'News Item' in '/news/bar.html' and
      you dont want to re-upload the corporate logo. You simply want to reuse
      the existing corporate logo. Where do you find it?

    - We could browse content and goto '/news/foo.html' and inside the
      'News Item' see the 'logo.jpg'. While this is possible. It is not
      probable that someone has created a container where images are being
      uploaded. Specifically the default Plone 'News Item' implementation
      does not work this way.


The suggested solution
----------------------

  Create a new 'UploadReferenceWidget'. What this will do is be an alternative
  widget that can work in-place of a ReferenceWidget; and should retain all
  the functionality of a Reference Field/Widget. But enable someone to upload
  a 'File'. The policy on the Field/Widget could dictate that the file gets put
  into a certain folder. Take this scenerio for instance:

    - We know that all content in 'http://host/corporate/news' is commercial
      news.

    - When user is creating a 'News Item' and uploads 'logo2.jpg' into the
      Upload Reference Widget called 'image' that we will ask the policy
      Where does this image, 'logo2.jpg' go? The policy could put it in
      /images/logos.

    - The policy would have to do everything. The Widget wouldn't help
      anything. The file would be put into the '/images/logos' folder and
      then in the 'News Item' image attribute would be the reference id to
      the '/images/logos/logo2.jpg'.


Implementation details
----------------------

  The new widget has two main features:

  - Upload a new file: create a new object and make a reference to it

  - Select an existing object: make a reference to it

  When uploading a new file, the widget checks for the mimetype and create
  an instance of the appropriate content-type: File or Image. This content
  is created in the 'startup_directory' property defined in the widget.


Example usage
-------------

  Take a look in the 'demo.py' file for a simple example usage of this widget.

  The browse and select functionality is provided by
  'archetypes.referencebrowserwidget', which means you can use any of its
  current features.

  Check the "complete reference of available
  options":http://tinyurl.com/referencebrowserwidget-options online.

  It contains the list of default property values and explains its meanings.


