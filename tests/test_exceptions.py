# Tests for SecretStorage
# Author: Dmitry Shachnev, 2013-2018
# License: 3-clause BSD, see LICENSE file

# Various exception tests

import unittest
import secretstorage
from secretstorage.exceptions import ItemNotFoundException

class ExceptionsTest(unittest.TestCase):
	"""A test case that ensures that all SecretStorage exceptions
	are raised correctly."""

	@classmethod
	def setUpClass(cls):
		cls.connection = secretstorage.dbus_init()
		cls.collection = secretstorage.get_any_collection(cls.connection)

	def test_double_deleting(self):
		item = self.collection.create_item('MyItem',
			{'application': 'secretstorage-test'}, b'pa$$word')
		item.delete()
		self.assertRaises(ItemNotFoundException, item.delete)

	def test_non_existing_item(self):
		self.assertRaises(ItemNotFoundException, secretstorage.Item,
			self.connection, '/not/existing/path')

	def test_non_existing_collection(self):
		self.assertRaises(ItemNotFoundException,
			secretstorage.get_collection_by_alias,
			self.connection, 'non-existing-alias')

if __name__ == '__main__':
	unittest.main()
