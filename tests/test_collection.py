# Tests for SecretStorage
# Author: Dmitry Shachnev, 2013-2018
# License: 3-clause BSD, see LICENSE file

# This file tests the secretstorage.Collection class.

import unittest
from secretstorage import dbus_init, get_any_collection, get_all_collections, Collection
from secretstorage.util import BUS_NAME

class CollectionTest(unittest.TestCase):
	"""A test case that tests that all common methods of Collection
	class work and do not crash."""

	@classmethod
	def setUpClass(cls):
		cls.connection = dbus_init()
		cls.collection = get_any_collection(cls.connection)

	def test_all_collections(self):
		labels = map(Collection.get_label, get_all_collections(self.connection))
		self.assertIn(self.collection.get_label(), labels)

	def test_all_items(self):
		for item in self.collection.get_all_items():
			item.get_label()

	def test_create_empty_item(self):
		item = self.collection.create_item('', {}, b'')
		item.delete()

	def test_label(self):
		old_label = self.collection.get_label()
		self.collection.set_label('Hello!')
		self.assertEqual(self.collection.get_label(), 'Hello!')
		self.collection.set_label(old_label)
		self.assertEqual(self.collection.get_label(), old_label)

	@unittest.skipIf(BUS_NAME == "org.freedesktop.secrets",
	                 "This test should only be run with the mocked server.")
	def test_deleting(self):
		collection_path = "/org/freedesktop/secrets/collection/spanish"
		collection = Collection(self.connection, collection_path)
		collection.unlock()
		collection.delete()


if __name__ == '__main__':
	unittest.main()
