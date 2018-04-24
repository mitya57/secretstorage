#!/usr/bin/python

import os.path
from setuptools import setup

version = '3.0.1'

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme_file:
	long_description = readme_file.read()

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
	long_description_content_type='text/x-rst',
	author='Dmitry Shachnev',
	author_email='mitya57@gmail.com',
	url='https://github.com/mitya57/secretstorage',
	packages=['secretstorage'],
	platforms='Linux',
	license='BSD',
	classifiers=classifiers,
	python_requires='>=3.5',
	install_requires=['jeepney', 'cryptography'],
	requires=['jeepney', 'cryptography']
)
