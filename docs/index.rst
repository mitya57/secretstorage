=======================================
Welcome to SecretStorage documentation!
=======================================

This module provides a way for securely storing passwords and other
secrets.

It uses `D-Bus`_-based FreeDesktop.org `Secret Service`_ standard that is,
for example, supported by `GNOME Keyring`_ (since version 2.30) and by
KSecretsService_.

It allows one to create new secret items, delete and search for
passwords matching given attributes. It also supports graphical prompts
when unlocking is needed.

.. _`D-Bus`: https://www.freedesktop.org/wiki/Software/dbus
.. _`Secret Service`: https://specifications.freedesktop.org/secret-service/
.. _`GNOME Keyring`: https://wiki.gnome.org/Projects/GnomeKeyring
.. _KSecretsService: https://techbase.kde.org/Projects/Utils/ksecretsservice

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

Examples of using SecretStorage
===============================

Creating a new item in the default collection:

>>> import secretstorage
>>> bus = secretstorage.dbus_init()
>>> collection = secretstorage.get_default_collection(bus)
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

Locking and unlocking collections:

>>> collection.lock()
>>> collection.is_locked()
True
>>> collection.unlock()
>>> collection.is_locked()
False

Asynchronously unlocking the collection (the GLib main loop is used
here, Qt loop is also supported):

>>> from gi.repository import GLib
>>> loop = GLib.MainLoop()
>>> def callback(dismissed, unlocked):
...     print('dismissed:', dismissed)
...     print('unlocked:', unlocked)
...     loop.quit()
... 
>>> collection.unlock(callback); loop.run()
dismissed: False
unlocked: [dbus.ObjectPath('/org/freedesktop/secrets/aliases/default')]

Contents
========

.. toctree::
   :maxdepth: 2

   collection
   item
   util
   exceptions

Indices and tables
==================

* :ref:`genindex`
* :ref:`search`
