# Tests for SecretStorage
# Author: Dmitry Shachnev, 2018
# License: 3-clause BSD, see LICENSE file

import unittest

from secretstorage import dbus_init, Collection
from secretstorage.util import BUS_NAME
from secretstorage.exceptions import LockedException


@unittest.skipIf(BUS_NAME == "org.freedesktop.secrets",
                 "This test should only be run with the mocked server.")
class LockingUnlockingTest(unittest.TestCase):
	def setUp(self) -> None:
		self.connection = dbus_init()
		collection_path = "/org/freedesktop/secrets/collection/english"
		self.collection = Collection(self.connection, collection_path)

	def tearDown(self) -> None:
		self.connection.close()

	def test_lock_unlock(self) -> None:
		self.assertFalse(self.collection.is_locked())
		self.collection.lock()
		self.assertTrue(self.collection.is_locked())
		self.assertRaises(LockedException, self.collection.ensure_not_locked)
		item, = self.collection.search_items({"number": "1"})
		self.assertRaises(LockedException, item.ensure_not_locked)
		self.assertIs(self.collection.unlock(), False)
		self.assertFalse(self.collection.is_locked())
		self.collection.ensure_not_locked()
