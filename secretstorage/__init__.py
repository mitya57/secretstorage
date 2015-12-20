# SecretStorage module for Python
# Access passwords using the SecretService DBus API
# Author: Dmitry Shachnev, 2013
# License: BSD

"""This file provides quick access to all SecretStorage API. Please
refer to documentation of individual modules for API details.

It also provides some functions for compatibility with older
SecretStorage releases. Those functions are not recommended for use
in new software."""

import dbus
from secretstorage.collection import Collection, create_collection, \
 get_all_collections, get_default_collection, get_any_collection, \
 get_collection_by_alias, search_items
from secretstorage.item import Item
from secretstorage.defines import DBUS_NOT_SUPPORTED, DBUS_EXEC_FAILED, \
 DBUS_NO_REPLY
from secretstorage.exceptions import SecretStorageException, \
 SecretServiceNotAvailableException, LockedException, \
 ItemNotFoundException
from os.path import join
from functools import wraps
from warnings import warn

__version_tuple__ = (2, 1, 3)
__version__ = '.'.join(map(str, __version_tuple__))

def dbus_init(main_loop=True, use_qt_loop=False):
	"""Returns new SessionBus_. If `main_loop` is :const:`True` and no
	D-Bus main loop is registered yet, registers a default main loop
	(PyQt5 main loop if `use_qt_loop` is :const:`True`, otherwise GLib
	main loop).

	.. _SessionBus: http://www.freedesktop.org/wiki/IntroductionToDBus/#buses

	.. note::
	   Qt uses GLib main loops on UNIX-like systems by default, so one
	   will rarely need to set `use_qt_loop` to :const:`True`.
	"""
	if main_loop and not dbus.get_default_main_loop():
		if use_qt_loop:
			from dbus.mainloop.pyqt5 import DBusQtMainLoop
			DBusQtMainLoop(set_as_default=True)
		else:
			from dbus.mainloop.glib import DBusGMainLoop
			DBusGMainLoop(set_as_default=True)
	try:
		return dbus.SessionBus()
	except dbus.exceptions.DBusException as e:
		if e.get_dbus_name() in (DBUS_NOT_SUPPORTED,
		DBUS_EXEC_FAILED, DBUS_NO_REPLY):
			raise SecretServiceNotAvailableException(
				e.get_dbus_message())
		raise

# The functions below are provided for compatibility with old
# SecretStorage versions (<= 0.2).

def _deprecated(function_in):
	@wraps(function_in)
	def function_out(*args, **kwargs):
		warn('Function %s is deprecated. Please use the documented API'
		     ' instead.' % function_in.__name__, DeprecationWarning,
		     stacklevel=2)
		return function_in(*args, **kwargs)
	return function_out

@_deprecated
def get_items(search_attributes, unlock_all=True):
	"""Returns tuples for all items in the default collection matching
	`search_attributes`."""
	bus = dbus_init()
	collection = get_any_collection(bus)
	if unlock_all and collection.is_locked():
		collection.unlock()
	search_results = collection.search_items(search_attributes)
	return [item.to_tuple() for item in search_results]

@_deprecated
def get_items_ids(search_attributes):
	"""Returns item id for all items in the default collection matching
	`search_attributes`."""
	bus = dbus_init()
	collection = get_any_collection(bus)
	search_results = collection.search_items(search_attributes)
	return [item._item_id() for item in search_results]

@_deprecated
def get_item_attributes(item_id):
	"""Returns item attributes for item with given id."""
	bus = dbus_init()
	collection = get_any_collection(bus)
	item = Item(bus, join(collection.collection_path, str(item_id)))
	return item.get_attributes()

@_deprecated
def get_item_object(item_id, unlock=True):
	"""Returns the item with given id and unlocks it if `unlock` is
	`True`."""
	bus = dbus_init()
	collection = get_any_collection(bus)
	item = Item(bus, join(collection.collection_path, str(item_id)))
	if unlock and collection.is_locked():
		collection.unlock()
	return item

@_deprecated
def get_item(item_id, unlock=True):
	"""Returns tuple representing the item with given id."""
	return get_item_object(item_id, unlock).to_tuple()

@_deprecated
def delete_item(item_id, unlock=True):
	"""Deletes the item with given id."""
	return get_item_object(item_id, unlock).delete()

@_deprecated
def create_item(label, attributes, secret, unlock=True):
	"""Creates an item with given `label`, `attributes` and `secret` in
	the default collection. Returns id of the created item."""
	bus = dbus_init()
	collection = get_any_collection(bus)
	if unlock and collection.is_locked():
		collection.unlock()
	item = collection.create_item(label, attributes, secret)
	return item._item_id()
