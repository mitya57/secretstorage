# Tests for SecretStorage
# Author: Dmitry Shachnev, 2013
# License: BSD

# This file tests the secretstorage.Collection class.

import unittest
import dbus
from secretstorage.collection import Collection
from secretstorage.item import Item

ATTRIBUTES = {'application': 'secretstorage-test', 'attribute': 'qwerty'}
NEW_ATTRIBUTES = {'application': 'secretstorage-test',
	'newattribute': 'asdfgh'}

class ItemTest(unittest.TestCase):
	"""A test case that tests that all common methods of Item
	class work and do not crash."""

	def setUp(self):
		bus = dbus.SessionBus()
		collection = Collection(bus)
		self.item = collection.create_item('My item', ATTRIBUTES,
			b'pa$$word')

	def test_attributes(self):
		attributes = self.item.get_attributes()
		for key in ATTRIBUTES:
			self.assertEqual(ATTRIBUTES[key], attributes[key])
		self.item.set_attributes(NEW_ATTRIBUTES)
		attributes = self.item.get_attributes()
		for key in NEW_ATTRIBUTES:
			self.assertEqual(NEW_ATTRIBUTES[key], attributes[key])

	def test_label(self):
		self.assertEqual(self.item.get_label(), 'My item')
		self.item.set_label('Hello!')
		self.assertEqual(self.item.get_label(), 'Hello!')

	def test_secret(self):
		self.assertEqual(self.item.get_secret(), b'pa$$word')
		self.item.set_secret(b'newpa$$word')
		self.assertEqual(self.item.get_secret(), b'newpa$$word')

	def tearDown(self):
		self.item.delete()

if __name__ == '__main__':
	unittest.main()
