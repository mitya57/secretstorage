#!/usr/bin/python

import os.path
from distutils.core import setup

version = '1.1.0'

readme_file = open(os.path.join(os.path.dirname(__file__), 'README'))
long_description = '\n' + readme_file.read()
readme_file.close()

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

cmdclass = {}
try:
	from sphinx.setup_command import BuildDoc
except:
	pass
else:
	cmdclass['build_sphinx'] = BuildDoc

setup(name='SecretStorage',
	version=version,
	description='Secure storing of passwords and other secrets',
	long_description=long_description,
	author='Dmitry Shachnev',
	author_email='mitya57@gmail.com',
	url='http://launchpad.net/python-secretstorage',
	packages=['secretstorage'],
	platforms='Linux',
	license='BSD',
	classifiers=classifiers,
	cmdclass=cmdclass,
	requires=['dbus']
)
