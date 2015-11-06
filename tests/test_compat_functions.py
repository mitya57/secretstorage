# Tests for SecretStorage
# Author: Dmitry Shachnev, 2013
# License: BSD

# This file tests the compatibility functions in __init__.py.

import secretstorage
import random
import unittest

rand = str(random.randint(0, 1000))

ATTRIBUTES = {'application': 'secretstorage-test', 'attribute': rand}
PASSWORD = b'pa$$word'

def catch_deprecation_warnings(testcase, function_in):
	if not hasattr(testcase, 'assertWarns'):
		return function_in
	def function_out(*args, **kwargs):
		with testcase.assertWarns(DeprecationWarning):
			return function_in(*args, **kwargs)
	return function_out

class CompatFunctionsTest(unittest.TestCase):
	"""A test case that tests compatibility functions, based on old
	SecretStorage test."""

	def __init__(self, *args, **kwargs):
		unittest.TestCase.__init__(self, *args, **kwargs)
		self.create_item = catch_deprecation_warnings(self, secretstorage.create_item)
		self.get_items = catch_deprecation_warnings(self, secretstorage.get_items)
		self.get_items_ids = catch_deprecation_warnings(self, secretstorage.get_items_ids)
		self.get_item = catch_deprecation_warnings(self, secretstorage.get_item)
		self.get_item_attributes = catch_deprecation_warnings(self, secretstorage.get_item_attributes)
		self.delete_item = catch_deprecation_warnings(self, secretstorage.delete_item)

	def setUp(self):
		self.item_id = self.create_item('Test item', ATTRIBUTES, PASSWORD)

	def test_get_items(self):
		attrs, secret = self.get_items(ATTRIBUTES)[-1]
		self.assertEqual(attrs['application'], 'secretstorage-test')
		self.assertEqual(secret, PASSWORD)

	def test_get_items_ids(self):
		item_id = self.get_items_ids(ATTRIBUTES)[-1]
		self.assertEqual(item_id, self.item_id)

	def test_get_item(self):
		attrs, secret = self.get_item(self.item_id)
		self.assertEqual(attrs['application'], 'secretstorage-test')
		self.assertEqual(secret, PASSWORD)

	def test_get_item_attributes(self):
		attrs = self.get_item_attributes(self.item_id)
		self.assertEqual(attrs['application'], 'secretstorage-test')
		self.assertEqual(attrs['attribute'], rand)

	def tearDown(self):
		self.delete_item(self.item_id)

if __name__ == '__main__':
	unittest.main()
