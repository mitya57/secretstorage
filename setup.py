#!/usr/bin/python

import os.path
try:
	from setuptools import setup
except ImportError:
	from distutils.core import setup

version = '3.0.0'

readme_file = open(os.path.join(os.path.dirname(__file__), 'README.rst'))
long_description = '\n' + readme_file.read()
readme_file.close()

classifiers = [
	'Development Status :: 5 - Production/Stable',
	'License :: OSI Approved :: BSD License',
	'Operating System :: POSIX',
	'Programming Language :: Python',
	'Programming Language :: Python :: 3 :: Only',
	'Programming Language :: Python :: 3.5',
	'Programming Language :: Python :: 3.6',
	'Topic :: Security',
	'Topic :: Software Development :: Libraries :: Python Modules'
]

setup(name='SecretStorage',
	version=version,
	description='Python bindings to FreeDesktop.org Secret Service API',
	long_description=long_description,
	author='Dmitry Shachnev',
	author_email='mitya57@gmail.com',
	url='https://github.com/mitya57/secretstorage',
	packages=['secretstorage'],
	platforms='Linux',
	license='BSD',
	classifiers=classifiers,
	python_requires='>=3.5',
	install_requires=['cryptography'],
	extras_require={
		'dbus-python': ['dbus-python'],
	},
	requires=['dbus', 'cryptography']
)
