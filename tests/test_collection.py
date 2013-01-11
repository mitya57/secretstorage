# Tests for SecretStorage
# Author: Dmitry Shachnev, 2013
# License: BSD

# This file tests the secretstorage.Collection class.

import unittest
from secretstorage import dbus_init, Collection

class CollectionTest(unittest.TestCase):
	"""A test case that tests that all common methods of Collection
	class work and do not crash."""

	@classmethod
	def setUpClass(cls):
		bus = dbus_init(main_loop=False)
		cls.collection = Collection(bus)

	def test_all_items(self):
		for item in self.collection.get_all_items():
			item.get_label()

	def test_label(self):
		old_label = self.collection.get_label()
		self.collection.set_label('Hello!')
		self.assertEqual(self.collection.get_label(), 'Hello!')
		self.collection.set_label(old_label)
		self.assertEqual(self.collection.get_label(), old_label)

if __name__ == '__main__':
	unittest.main()
