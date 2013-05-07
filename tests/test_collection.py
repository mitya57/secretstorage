# Tests for SecretStorage
# Author: Dmitry Shachnev, 2013
# License: BSD

# This file tests the secretstorage.Collection class.

import unittest
from secretstorage import dbus_init, Collection, get_all_collections

class CollectionTest(unittest.TestCase):
	"""A test case that tests that all common methods of Collection
	class work and do not crash."""

	@classmethod
	def setUpClass(cls):
		cls.bus = dbus_init(main_loop=False)
		cls.collection = Collection(cls.bus)

	def test_all_collections(self):
		labels = map(Collection.get_label, get_all_collections(self.bus))
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

if not hasattr(CollectionTest, 'assertIn'): # Python <= 2.6
	CollectionTest.assertIn = lambda self, a, b: self.assertTrue(a in b)

if __name__ == '__main__':
	unittest.main()
