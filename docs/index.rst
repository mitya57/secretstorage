=======================================
Welcome to SecretStorage documentation!
=======================================

This module provides a way for securely storing passwords and other
secrets.

It uses `D-Bus`_-based FreeDesktop.org `Secret Service`_ standard that is,
for example, supported by `GNOME Keyring`_ (since version 2.30),
KSecretsService_ and KeePassXC_.

It allows one to create new secret items, delete and search for
passwords matching given attributes. It also supports graphical prompts
when unlocking is needed.

.. _`D-Bus`: https://www.freedesktop.org/wiki/Software/dbus
.. _`Secret Service`: https://specifications.freedesktop.org/secret-service/
.. _`GNOME Keyring`: https://wiki.gnome.org/Projects/GnomeKeyring
.. _KSecretsService: https://community.kde.org/KDE_Utils/ksecretsservice
.. _KeePassXC: https://avaldes.co/2020/01/28/secret-service-keepassxc.html

SecretStorage code is hosted on GitHub_.

.. _GitHub: https://github.com/mitya57/secretstorage

Initializing D-Bus
==================

.. seealso::
   If you don't know how D-Bus works, please read `Introduction to D-Bus`_
   firstly.

   .. _`Introduction to D-Bus`: https://www.freedesktop.org/wiki/IntroductionToDBus

Before using SecretStorage, you need to initialize D-Bus. This can be done
using this function:

.. autofunction:: secretstorage.dbus_init

If you need to quickly check whether the Secret Service daemon is available
(either running or `activatable via D-Bus`_) without trying to call any its
methods, you can use the following function:

.. autofunction:: secretstorage.check_service_availability

.. _`activatable via D-Bus`: https://www.freedesktop.org/wiki/IntroductionToDBus/#activation

Examples of using SecretStorage
===============================

Creating a new item in the default collection:

>>> import secretstorage
>>> connection = secretstorage.dbus_init()
>>> collection = secretstorage.get_default_collection(connection)
>>> attributes = {'application': 'myapp', 'another attribute':
...     'another value'}
>>> item = collection.create_item('My first item', attributes,
...     b'pa$$word')

Getting item's label, attributes and secret:

>>> item.get_label()
'My first item'
>>> item.get_attributes()
{'another attribute': 'another value', 'application': 'myapp'}
>>> item.get_secret()
b'pa$$word'

Locking and unlocking collections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The current version of SecretStorage provides only the synchronous API for
locking and unlocking.
This means that if prompting the user for a password is needed, then
:meth:`~secretstorage.collection.Collection.unlock` call will block until
the password is entered.

>>> collection.lock()
>>> collection.is_locked()
True
>>> collection.unlock()
>>> collection.is_locked()
False

If you want to use the asynchronous API, please `file a bug`_ and describe
your use case.

.. _`file a bug`: https://github.com/mitya57/secretstorage/issues/new

Contents
========

.. toctree::
   :maxdepth: 2

   collection
   item
   util
   exceptions
   changelog

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
