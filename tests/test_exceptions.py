# Tests for SecretStorage
# Author: Dmitry Shachnev, 2013
# License: BSD

# Various exception tests

import unittest
import secretstorage
from secretstorage.exceptions import ItemNotFoundException

class ExceptionsTest(unittest.TestCase):
	"""A test case that ensures that all SecretStorage exceptions
	are raised correctly."""

	@classmethod
	def setUpClass(cls):
		cls.bus = secretstorage.dbus_init(main_loop=False)
		cls.collection = secretstorage.Collection(cls.bus)

	def test_double_deleting(self):
		item = self.collection.create_item('MyItem',
			{'application': 'secretstorage-test'}, b'pa$$word')
		item.delete()
		self.assertRaises(ItemNotFoundException, item.delete)

	def test_non_existing_item(self):
		self.assertRaises(ItemNotFoundException, secretstorage.Item,
			self.bus, '/not/existing/path')

	def test_non_existing_collection(self):
		self.assertRaises(ItemNotFoundException,
			secretstorage.get_collection_by_alias,
			self.bus, 'non-existing-alias')

if __name__ == '__main__':
	unittest.main()
