# SecretStorage module for Python
# Access passwords using the SecretService DBus API
# Author: Dmitry Shachnev, 2013
# License: BSD

# This file contains implementation of secretstorage.Item class.

import dbus
from secretstorage.defines import SECRETS, SS_PREFIX
from secretstorage.exceptions import LockedException
from secretstorage.util import open_session, format_secret, to_unicode

ITEM_IFACE = SS_PREFIX + 'Item'

class Item(object):
	"""Represents a secret item."""

	def __init__(self, bus, item_path, session=None):
		item_obj = bus.get_object(SECRETS, item_path)
		self.session = session
		self.bus = bus
		self.item_iface = dbus.Interface(item_obj, ITEM_IFACE)
		self.item_props_iface = dbus.Interface(item_obj,
			dbus.PROPERTIES_IFACE)

	def is_locked(self):
		"""Returns True if item is locked, otherwise False."""
		return bool(self.item_props_iface.Get(ITEM_IFACE, 'Locked'))

	def ensure_not_locked(self):
		"""If collection is locked, raises `LockedException`."""
		if self.is_locked():
			raise LockedException('Item is locked!')

	def get_attributes(self):
		"""Returns item attributes (dictionary)."""
		attrs = self.item_props_iface.Get(ITEM_IFACE, 'Attributes')
		return dict([(to_unicode(key), to_unicode(value))
			for key, value in attrs.items()])

	def set_attributes(self, attributes):
		"""Sets item attributes to `attributes` (dictionary)."""
		self.item_props_iface.Set(ITEM_IFACE, 'Attributes', attributes)

	def get_label(self):
		"""Returns item label (unicode string)."""
		label = self.item_props_iface.Get(ITEM_IFACE, 'Label')
		return to_unicode(label)

	def set_label(self, label):
		"""Sets item label to `label`."""
		self.ensure_not_locked()
		self.item_props_iface.Set(ITEM_IFACE, 'Label', label)

	def delete(self):
		"""Deletes the item."""
		self.ensure_not_locked()
		return self.item_iface.Delete()

	def get_secret(self):
		"""Returns item secret (`bytes`)."""
		self.ensure_not_locked()
		if not self.session:
			self.session = open_session(self.bus)
		secret = self.item_iface.GetSecret(self.session)
		return bytes(bytearray(secret[2]))

	def set_secret(self, secret):
		"""Sets item secret to `secret`."""
		self.ensure_not_locked()
		if not self.session:
			self.session = open_session(self.bus)
		secret = format_secret(secret, self.session)
		self.item_iface.SetSecret(secret)
