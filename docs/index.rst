=======================================
Welcome to SecretStorage documentation!
=======================================

This module provides a way for securely storing passwords and other
secrets.

It uses D-Bus-based FreeDesktop.org `Secret Service`_ standard that is,
for example, supported by `GNOME Keyring`_ (since version 2.30) and by
KWallet_ (since 4.8).

It allows one to create new secret items, delete and search for
passwords matching given attributes. It also supports graphical prompts
when unlocking is needed.

.. _`Secret Service`: http://standards.freedesktop.org/secret-service/
.. _`GNOME Keyring`: http://live.gnome.org/GnomeKeyring
.. _KWallet: http://userbase.kde.org/KDE_Wallet_Manager

Examples of using SecretStorage
===============================

Creating a new item in the default collection:

>>> import secretstorage
>>> import dbus
>>> bus = dbus.SessionBus()
>>> collection = secretstorage.Collection(bus)
>>> attributes = {'application': 'myapp', 'another attribute':
...     'another value'}
>>> item = collection.create_item('My first item', attributes,
...     b'pa$$word')

Getting item's label, attributes and secret:

>>> item = collection.create_item('My first item', attributes, b'pa$$word')
>>> item.get_label()
'My first item'
>>> item.get_attributes()
{'another attribute': 'another value', 'application': 'myapp'}
>>> item.get_secret()
b'pa$$word'

Locking and unlocking collections:

>>> import secretstorage
>>> import dbus
>>> from dbus.mainloop.glib import DBusGMainLoop
>>> DBusGMainLoop(set_as_default=True)
>>> bus = dbus.SessionBus()
>>> collection = secretstorage.Collection(bus)
>>> collection.is_locked()
False
>>> collection.lock()
>>> collection.is_locked()
True
>>> collection.unlock()

Asynchronously unlocking the collection (the GLib main loop is used
here, Qt loop is also supported):

>>> from gi.repository import GObject
>>> loop = GObject.MainLoop()
>>> def callback(dismissed, unlocked):
...     print(dismissed, unlocked)
...     loop.quit()
... 
>>> collection.unlock(callback); loop.run()
False [dbus.ObjectPath('/org/freedesktop/secrets/aliases/default')]

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
