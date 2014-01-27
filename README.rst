Module description
==================

This module provides a way for securely storing passwords and other secrets.

It uses D-Bus `Secret Service`_ API that is supported by GNOME Keyring
(>= 2.30) and KSecretsService.

The main classes provided are ``secretstorage.Item``, representing a secret
item (that has a *label*, a *secret* and some *attributes*) and
``secretstorage.Collection``, a place items are stored in.

SecretStorage supports most of the functions provided by Secret Service,
including creating and deleting items and collections, editing items,
locking and unlocking collections (asynchronous unlocking is also supported).

The documentation can be found on `pythonhosted.org`_.

.. _`Secret Service`: http://standards.freedesktop.org/secret-service/
.. _`pythonhosted.org`: http://pythonhosted.org/SecretStorage/

Building the module
===================

.. note::
   SecretStorage supports all versions of Python since 2.6. Here we assume
   that your Python version is 3.x.

SecretStorage requires these packages to work:

* `dbus-python`_ (available in Debian-based distributions in `python3-dbus package`_);
* PyCrypto_ (available in Debian-based distributions in `python3-crypto package`_).

To build SecretStorage, use this command::

   python3 setup.py build

If you have Sphinx_ installed, you can also build the documentation::

   python3 setup.py build_sphinx

.. _`dbus-python`: http://www.freedesktop.org/wiki/Software/DBusBindings#dbus-python
.. _PyCrypto: https://www.dlitz.net/software/pycrypto/
.. _`python3-dbus package`: http://packages.debian.org/sid/python3-dbus
.. _`python3-crypto package`: http://packages.debian.org/sid/python3-crypto
.. _Sphinx: http://sphinx-doc.org/

Get the code
============

SecretStorage is available under BSD license. The source code can be found
on GitHub_.

.. _GitHub: https://github.com/mitya57/secretstorage
