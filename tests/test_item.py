# Tests for SecretStorage
# Author: Dmitry Shachnev, 2013
# License: BSD

# This file tests the secretstorage.Collection class.

import unittest
import time
from secretstorage import dbus_init, search_items, get_any_collection

ATTRIBUTES = {'application': 'secretstorage-test', 'attribute': 'qwerty'}
NEW_ATTRIBUTES = {'application': 'secretstorage-test',
	'newattribute': 'asdfgh'}

class ItemTest(unittest.TestCase):
	"""A test case that tests that all common methods of Item
	class work and do not crash."""

	@classmethod
	def setUpClass(cls):
		cls.bus = dbus_init(main_loop=False)
		cls.collection = get_any_collection(cls.bus)
		cls.created_timestamp = time.time()
		cls.item = cls.collection.create_item('My item', ATTRIBUTES,
			b'pa$$word')
		cls.other_item = cls.collection.create_item('My item',
			ATTRIBUTES, '', content_type='data/null')

	def test_equal(self):
		self.assertEqual(self.item, self.item)
		self.assertNotEqual(self.item, self.other_item)
		self.assertEqual(self.other_item, self.other_item)

	def test_searchable(self):
		search_results = self.collection.search_items(ATTRIBUTES)
		self.assertIn(self.item, search_results)
		search_results = search_items(self.bus, ATTRIBUTES)
		self.assertIn(self.item, search_results)

	def test_item_in_all_items(self):
		all_items = self.collection.get_all_items()
		self.assertIn(self.item, all_items)

	def test_attributes(self):
		attributes = self.item.get_attributes()
		for key in ATTRIBUTES:
			self.assertEqual(ATTRIBUTES[key], attributes[key])
		self.item.set_attributes(NEW_ATTRIBUTES)
		attributes = self.item.get_attributes()
		for key in NEW_ATTRIBUTES:
			self.assertEqual(NEW_ATTRIBUTES[key], attributes[key])
		self.item.set_attributes(ATTRIBUTES)

	def test_label(self):
		self.assertEqual(self.item.get_label(), 'My item')
		self.item.set_label('Hello!')
		self.assertEqual(self.item.get_label(), 'Hello!')

	def test_secret(self):
		self.assertEqual(self.item.get_secret(), b'pa$$word')
		self.item.set_secret(b'newpa$$word')
		self.assertIsInstance(self.item.get_secret(), bytes)
		self.assertEqual(self.item.get_secret(), b'newpa$$word')
		self.assertEqual(self.other_item.get_secret(), b'')

	def test_secret_content_type(self):
		self.assertEqual(self.item.get_secret_content_type(), 'text/plain')
		# The check below fails in gnome-keyring because it doesn't really
		# support content types.
		#self.assertEqual(self.other_item.get_secret_content_type(), 'data/null')

	def test_modified(self):
		now = time.time()
		modified = self.item.get_modified()
		self.assertAlmostEqual(now, modified, places=-1)

	def test_created(self):
		created = self.item.get_created()
		self.assertAlmostEqual(self.created_timestamp, created, places=-1)

	@classmethod
	def tearDownClass(cls):
		cls.item.delete()
		cls.other_item.delete()

if __name__ == '__main__':
	unittest.main()
