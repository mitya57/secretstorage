# SecretStorage module for Python
# Access passwords using the SecretService DBus API
# Author: Dmitry Shachnev, 2013-2018
# License: 3-clause BSD, see LICENSE file

"""SecretStorage item contains a *secret*, some *attributes* and a
*label* visible to user. Editing all these properties and reading the
secret is possible only when the :doc:`collection <collection>` storing
the item is unlocked. The collection can be unlocked using collection's
:meth:`~secretstorage.collection.Collection.unlock` method."""

import warnings
from secretstorage.defines import SS_PREFIX
from secretstorage.exceptions import LockedException
from secretstorage.util import DBusAddressWrapper, \
 open_session, format_secret, unlock_objects
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

ITEM_IFACE = SS_PREFIX + 'Item'

class Item(object):
	"""Represents a secret item."""

	def __init__(self, connection, item_path, session=None):
		self.item_path = item_path
		self._item = DBusAddressWrapper(item_path, ITEM_IFACE, connection)
		self._item.get_property('Label')
		self.session = session
		self.connection = connection

	def __eq__(self, other):
		return self.item_path == other.item_path

	def is_locked(self):
		"""Returns :const:`True` if item is locked, otherwise
		:const:`False`."""
		return bool(self._item.get_property('Locked'))

	def ensure_not_locked(self):
		"""If collection is locked, raises
		:exc:`~secretstorage.exceptions.LockedException`."""
		if self.is_locked():
			raise LockedException('Item is locked!')

	def unlock(self):
		"""Requests unlocking the item. Usually, this means that the
		whole collection containing this item will be unlocked.

		Returns a boolean representing whether the prompt has been
		dismissed; that means :const:`False` on successful unlocking
		and :const:`True` if it has been dismissed.

		.. versionadded:: 2.1.2

		.. versionchanged:: 3.0
		   No longer accepts the ``callback`` argument.
		"""
		return unlock_objects(self.connection, [self.item_path])

	def get_attributes(self):
		"""Returns item attributes (dictionary)."""
		attrs = self._item.get_property('Attributes')
		return dict(attrs)

	def set_attributes(self, attributes):
		"""Sets item attributes to `attributes` (dictionary)."""
		self._item.set_property('Attributes', 'a{ss}', attributes)

	def get_label(self):
		"""Returns item label (unicode string)."""
		return self._item.get_property('Label')

	def set_label(self, label):
		"""Sets item label to `label`."""
		self.ensure_not_locked()
		self._item.set_property('Label', 's', label)

	def delete(self):
		"""Deletes the item."""
		self.ensure_not_locked()
		return self._item.call('Delete')

	def get_secret(self):
		"""Returns item secret (bytestring)."""
		self.ensure_not_locked()
		if not self.session:
			self.session = open_session(self.connection)
		secret, = self._item.call('GetSecret', 'o', self.session.object_path)
		if not self.session.encrypted:
			return bytes(secret[2])
		aes = algorithms.AES(self.session.aes_key)
		aes_iv = bytes(secret[1])
		decryptor = Cipher(aes, modes.CBC(aes_iv), default_backend()).decryptor()
		encrypted_secret = bytes(secret[2])
		padded_secret = decryptor.update(encrypted_secret) + decryptor.finalize()
		return bytes(padded_secret[:-padded_secret[-1]])

	def get_secret_content_type(self):
		"""Returns content type of item secret (string)."""
		self.ensure_not_locked()
		if not self.session:
			self.session = open_session(self.connection)
		secret, = self._item.call('GetSecret', 'o', self.session.object_path)
		return str(secret[3])

	def set_secret(self, secret, content_type='text/plain'):
		"""Sets item secret to `secret`. If `content_type` is given,
		also sets the content type of the secret (``text/plain`` by
		default)."""
		self.ensure_not_locked()
		if not self.session:
			self.session = open_session(self.connection)
		secret = format_secret(self.session, secret, content_type)
		self._item.call('SetSecret', '(oayays)', secret)

	def get_created(self):
		"""Returns UNIX timestamp (integer) representing the time
		when the item was created.

		.. versionadded:: 1.1"""
		return self._item.get_property('Created')

	def get_modified(self):
		"""Returns UNIX timestamp (integer) representing the time
		when the item was last modified."""
		return self._item.get_property('Modified')

	def to_tuple(self):
		"""Returns (*attributes*, *secret*) tuple representing the
		item.

		.. deprecated:: 3.0
		   Use ``get_attributes()`` and ``get_secret()`` instead.
		"""
		warnings.warn("Item.to_tuple() is deprecated. Use"
		              " Item.get_attributes() and Item.get_secret()"
		              " instead.", DeprecationWarning)
		self.ensure_not_locked()
		return self.get_attributes(), self.get_secret()
