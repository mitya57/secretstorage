# SecretStorage module for Python
# Access passwords using the SecretService DBus API
# Author: Dmitry Shachnev, 2013
# License: BSD

# This file contains implementation of secretstorage.Item class.

import dbus
from secretstorage.defines import SECRETS, SS_PREFIX, SS_PATH
from secretstorage.exceptions import LockedException
from secretstorage.item import Item
from secretstorage.util import *

COLLECTION_IFACE = SS_PREFIX + 'Collection'
DEFAULT_COLLECTION = '/org/freedesktop/secrets/aliases/default'

class Collection(object):
	"""Represents a collection."""

	def __init__(self, bus, collection_path=DEFAULT_COLLECTION, session=None):
		collection_obj = bus.get_object(SECRETS, collection_path)
		self.bus = bus
		self.session = session
		self.collection_path = collection_path
		self.collection_iface = dbus.Interface(collection_obj,
			COLLECTION_IFACE)
		self.collection_props_iface = dbus.Interface(collection_obj,
			dbus.PROPERTIES_IFACE)

	def is_locked(self):
		"""Returns True if item is locked, otherwise False."""
		return bool(self.collection_props_iface.Get(
			COLLECTION_IFACE, 'Locked'))

	def ensure_not_locked(self):
		"""If collection is locked, raises `LockedException`."""
		if self.is_locked():
			raise LockedException('Item is locked!')

	def unlock(self, callback=None):
		"""Requests unlocking the keyring. If `callback` is specified,
		calls it when unlocking is complete (see `exec_prompt`
		description for details). Otherwise, uses async Glib loop."""
		service_obj = self.bus.get_object(SECRETS, SS_PATH)
		service_iface = dbus.Interface(service_obj, SS_PREFIX+'Service')
		prompt = service_iface.Unlock([self.collection_path], signature='ao')[1]
		if len(prompt) > 1:
			if callback:
				exec_prompt(self.bus, prompt, callback)
			else:
				exec_prompt_async_glib(self.bus, prompt)
		elif callback:
			# We still need to call it.
			callback([], [])

	def get_all_items(self):
		"""Returns a generator of all items in the collection."""
		for item_path in self.collection_props_iface.Get(
		COLLECTION_IFACE, 'Items'):
			yield Item(self.bus, item_path, self.session)

	def search_items(self, attributes):
		"""Returns a generator of items with the given attributes.
		`attributes` should be a dictionary."""
		locked, unlocked = self.collection_iface.SearchItems(
			COLLECTION_IFACE, attributes)
		for item in locked + unlocked:
			yield Item(self.bus, item_path, self.session)

	def get_label(self):
		"""Returns the collection label."""
		label = self.collection_props_iface.Get(COLLECTION_IFACE, 'Label')
		return to_unicode(label)

	def set_label(self, label):
		"""Sets collection label to `label`."""
		self.ensure_not_locked()
		self.collection_props_iface.Set(COLLECTION_IFACE, 'Label', label)

	def create_item(self, label, attributes, secret):
		"""Creates a new item with given `label` (unicode string),
		`attributes` (dictionary) and `secret` (bytestring).
		Returns the created item."""
		self.ensure_not_locked()
		if not self.session:
			self.session = open_session(self.bus)
		secret = format_secret(secret, self.session)
		properties = {
			SS_PREFIX+'Item.Label': label,
			SS_PREFIX+'Item.Attributes': attributes
		}
		new_item, prompt = self.collection_iface.CreateItem(properties,
			secret, True)
		return Item(self.bus, new_item, self.session)
