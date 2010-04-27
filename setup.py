from setuptools import setup, find_packages
import os

version = '2.2.3'

setup(name='Products.PloneBooking',
      version=version,
      description="A booking center for Plone",
      long_description = open(os.path.join("Products", "PloneBooking", "README.txt")).read() + "\n" +
                         open(os.path.join("Products", "PloneBooking", "CHANGES")).read(),
      # Get more strings from http://www.python.org/pypi?%3Aaction=list_classifiers
      classifiers=[
        "Framework :: Plone",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
        ],
      keywords='plone zope booking',
      author='Alter Way Solutions',
      author_email='support@ingeniweb.com',
      url='http://alterway.fr',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['Products'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
