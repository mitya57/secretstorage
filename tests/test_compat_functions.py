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

class CompatFunctionsTest(unittest.TestCase):
	"""A test case that tests compatibility functions, based on old
	SecretStorage test."""

	@classmethod
	def setUpClass(cls):
		cls.item_id = secretstorage.create_item('Test item',
			ATTRIBUTES, PASSWORD)

	def test_get_items(self):
		attrs, secret = secretstorage.get_items(ATTRIBUTES)[-1]
		self.assertEqual(attrs['application'], 'secretstorage-test')
		self.assertEqual(secret, PASSWORD)

	def test_get_items_ids(self):
		item_id = secretstorage.get_items_ids(ATTRIBUTES)[-1]
		self.assertEqual(item_id, self.item_id)

	def test_get_item(self):
		attrs, secret = secretstorage.get_item(self.item_id)
		self.assertEqual(attrs['application'], 'secretstorage-test')
		self.assertEqual(secret, PASSWORD)

	def test_get_item_attributes(self):
		attrs = secretstorage.get_item_attributes(self.item_id)
		self.assertEqual(attrs['application'], 'secretstorage-test')
		self.assertEqual(attrs['attribute'], rand)

	@classmethod
	def tearDownClass(cls):
		secretstorage.delete_item(cls.item_id)

if __name__ == '__main__':
	unittest.main()
