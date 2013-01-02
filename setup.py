#!/usr/bin/python

from distutils.core import setup
from sphinx.setup_command import BuildDoc

version = '0.8'

long_description = \
'''This module provides a way for securely storing passwords and other secrets.

It uses DBus Secret Service API that is supported by GNOME Keyring (>= 2.30) and
KSecretsService.

It allows one to create new passwords, delete and search for passwords matching
given attributes. It also supports graphical prompts when unlocking is needed.'''

classifiers = ['Development Status :: 4 - Beta',
	'License :: OSI Approved :: BSD License',
	'Operating System :: POSIX',
	'Programming Language :: Python',
	'Programming Language :: Python :: 2',
	'Programming Language :: Python :: 2.6',
	'Programming Language :: Python :: 2.7',
	'Programming Language :: Python :: 3',
	'Programming Language :: Python :: 3.1',
	'Programming Language :: Python :: 3.2',
	'Programming Language :: Python :: 3.3',
	'Topic :: Security',
	'Topic :: Software Development :: Libraries :: Python Modules'
]

setup(name='SecretStorage',
	version=version,
	description='Secure storing of passwords and another secrets',
	long_description=long_description,
	author='Dmitry Shachnev',
	author_email='mitya57@gmail.com',
	url='http://launchpad.net/python-secretstorage',
	packages=['secretstorage'],
	platforms='Linux',
	license='BSD',
	classifiers=classifiers,
	cmdclass={'build_sphinx': BuildDoc},
	requires=['dbus']
)
