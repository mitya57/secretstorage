# Tests for SecretStorage
# Author: Dmitry Shachnev, 2018
# License: BSD

import unittest

from secretstorage import dbus_init, get_any_collection
from secretstorage.util import BUS_NAME
from secretstorage.exceptions import LockedException


@unittest.skipIf(BUS_NAME == "org.freedesktop.secrets",
                 "This test should only be run with the mocked server.")
class LockingUnlockingTest(unittest.TestCase):
	@classmethod
	def setUpClass(cls):
		cls.connection = dbus_init()
		cls.collection = get_any_collection(cls.connection)

	def test_lock_unlock(self):
		self.collection.lock()
		self.assertRaises(LockedException, self.collection.ensure_not_locked)
		self.collection.unlock()
		self.collection.ensure_not_locked()
