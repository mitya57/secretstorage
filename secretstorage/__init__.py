# SecretStorage module for Python
# Access passwords using the SecretService DBus API
# Author: Dmitry Shachnev, 2013
# License: BSD

import dbus
from secretstorage.collection import Collection
from secretstorage.item import Item

__version__ = '0.8'

# The functions below are provided for compatibility with old
# SecretStorage versions (<= 0.2).

def _dbus_init(async=False):
	if async:
		from dbus.mainloop.glib import DBusGMainLoop
		DBusGMainLoop(set_as_default=True)
	return dbus.SessionBus()

def get_items(search_attributes, unlock_all=True):
	"""Returns tuples for all items in the default collection matching
	`search_attributes`."""
	bus = _dbus_init(async=unlock_all)
	collection = Collection(bus)
	if unlock_all and collection.is_locked():
		collection.unlock()
	search_results = collection.search_items(search_attributes)
	return [item.to_tuple() for item in search_results]

def get_items_ids(search_attributes):
	"""Returns item id for all items in the default collection matching
	`search_attributes`."""
	bus = _dbus_init()
	collection = Collection(bus)
	search_results = collection.search_items(search_attributes)
	return [item._item_id() for item in search_results]

def get_item_attributes(item_id):
	"""Returns item attributes for item with given id."""
	bus = _dbus_init()
	item = Item(bus, item_id)
	return item.get_attributes()

def get_item_object(item_id, unlock=True):
	"""Returns the item with given id and unlocks it if `unlock` is
	`True`."""
	bus = _dbus_init(async=unlock)
	item = Item(bus, item_id)
	collection_path = item.item_path.rsplit('/', 1)[0]
	collection = Collection(bus, collection_path)
	if unlock and collection.is_locked():
		collection.unlock()
	return item

def get_item(item_id, unlock=True):
	"""Returns tuple representing the item with given id."""
	return get_item_object(item_id, unlock).to_tuple()

def delete_item(item_id, unlock=True):
	"""Deletes the item with given id."""
	return get_item_object(item_id, unlock).delete()

def create_item(label, attributes, secret, unlock=True):
	"""Creates an item with given `label`, `attributes` and `secret` in
	the default collection. Returns id of the created item."""
	bus = _dbus_init(async=unlock)
	collection = Collection(bus)
	if unlock and collection.is_locked():
		collection.unlock()
	item = collection.create_item(label, attributes, secret)
	return item._item_id()
