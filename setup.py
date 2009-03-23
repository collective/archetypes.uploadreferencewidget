from setuptools import setup, find_packages
import os

def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = read('archetypes', 'uploadreferencewidget', 'VERSION.txt').strip()

setup(name='archetypes.uploadreferencewidget',
      version=version,
      description='A widget for Archetypes with support for both uploading '
                  'and referencing content.',
      long_description=read('archetypes', 'uploadreferencewidget', 'README.txt') +
                       read('docs', 'HISTORY.txt'),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='Relation Widget',
      author='Dorneles Tremea',
      author_email='dorneles@tremea.com',
      url='http://svn.plone.org/svn/archetypes/MoreFieldsAndWidgets/archetypes.uploadreferencewidget',
      license='LGPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['archetypes'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'archetypes.referencebrowserwidget'
      ],
      )
