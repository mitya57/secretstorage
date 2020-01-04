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

	def setUp(self) -> None:
		self.connection = secretstorage.dbus_init()
		self.collection = secretstorage.get_any_collection(self.connection)

	def tearDown(self) -> None:
		self.connection.close()

	def test_double_deleting(self) -> None:
		item = self.collection.create_item('MyItem',
			{'application': 'secretstorage-test'}, b'pa$$word')
		item.delete()
		self.assertRaises(ItemNotFoundException, item.delete)

	def test_non_existing_item(self) -> None:
		self.assertRaises(ItemNotFoundException, secretstorage.Item,
			self.connection, '/not/existing/path')

	def test_non_existing_collection(self) -> None:
		self.assertRaises(ItemNotFoundException,
			secretstorage.get_collection_by_alias,
			self.connection, 'non-existing-alias')
