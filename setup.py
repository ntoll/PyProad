#!/usr/bin/env python

from distutils.core import setup

setup(name='proad',
    version='0.0.1',
    description="Thin wrapper around Amazon's Product Advertising API",
    author='Nicholas Tollervey',
    author_email='ntoll@ntoll.org',
    url='http://fluidinfo.com',
    license='MIT',
    requires=['httplib2',],
    py_modules=['proad', ],
    long_description=open('README.rst').read(),
    classifiers=['Development Status :: 4 - Beta',
    'Environment :: Web Environment',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: OS Independent',
    'Programming Language :: Python',
    'Topic :: Internet :: WWW/HTTP',
    'Topic :: Software Development :: Libraries'])
