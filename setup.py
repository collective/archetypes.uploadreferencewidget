import os
from setuptools import setup, find_packages


def read(*rnames):
    return open(os.path.join(os.path.dirname(__file__), *rnames)).read()

version = '0.2.1'


long_description = (
    read('README.txt')
    + '\n' +
    read('CHANGES.txt')
    + '\n' +
    read('docs', 'HISTORY.txt')
    )

setup(name='archetypes.uploadreferencewidget',
      version=version,
      description='A widget for Archetypes with support for both uploading '
                  'and referencing content.',
      long_description=long_description,
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
          'archetypes.referencebrowserwidget',
          'plone.namedfile'
      ],
      )
