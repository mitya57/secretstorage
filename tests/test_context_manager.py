# Tests for SecretStorage
# Author: Dmitry Shachnev, 2019
# License: 3-clause BSD, see LICENSE file

# This file tests the secretstorage.create_connection() context manager.

import unittest
from secretstorage import create_connection, get_any_collection


class ContextManagerTest(unittest.TestCase):
	"""A test case that tests the :class:`secretstorage.create_connection`
	context manager."""

	def test_create_connection(self) -> None:
		with create_connection() as connection:
			collection = get_any_collection(connection)
			self.assertIsNotNone(collection)
			label = collection.get_label()
			self.assertIsNotNone(label)
