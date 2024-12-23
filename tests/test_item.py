# Tests for SecretStorage
# Author: Dmitry Shachnev, 2013-2018
# License: 3-clause BSD, see LICENSE file

# This file tests the secretstorage.Collection class.

import time
import unittest

from secretstorage import dbus_init, get_any_collection, search_items

ATTRIBUTES = {'application': 'secretstorage-test', 'attribute': 'qwerty'}
NEW_ATTRIBUTES = {'application': 'secretstorage-test',
                  'newattribute': 'asdfgh'}


class ItemTest(unittest.TestCase):
    """A test case that tests that all common methods of Item
    class work and do not crash."""

    def setUp(self) -> None:
        self.connection = dbus_init()
        self.collection = get_any_collection(self.connection)
        self.created_timestamp = time.time()
        self.item = self.collection.create_item(
            'My item', ATTRIBUTES,
            b'pa$$word')
        self.other_item = self.collection.create_item(
            'My item',
            ATTRIBUTES, b'', content_type='data/null')

    def tearDown(self) -> None:
        self.item.delete()
        self.other_item.delete()
        self.connection.close()

    def test_equal(self) -> None:
        self.assertEqual(self.item, self.item)
        self.assertNotEqual(self.item, self.other_item)
        self.assertEqual(self.other_item, self.other_item)

    def test_searchable(self) -> None:
        search_results = self.collection.search_items(ATTRIBUTES)
        self.assertIn(self.item, search_results)
        search_results = search_items(self.connection, ATTRIBUTES)
        self.assertIn(self.item, search_results)

    def test_item_in_all_items(self) -> None:
        all_items = self.collection.get_all_items()
        self.assertIn(self.item, all_items)

    def test_attributes(self) -> None:
        attributes = self.item.get_attributes()
        for key in ATTRIBUTES:
            self.assertEqual(ATTRIBUTES[key], attributes[key])
        self.item.set_attributes(NEW_ATTRIBUTES)
        attributes = self.item.get_attributes()
        for key in NEW_ATTRIBUTES:
            self.assertEqual(NEW_ATTRIBUTES[key], attributes[key])
        self.item.set_attributes(ATTRIBUTES)

    def test_label(self) -> None:
        self.assertEqual(self.item.get_label(), 'My item')
        self.item.set_label('Hello!')
        self.assertEqual(self.item.get_label(), 'Hello!')

    def test_secret(self) -> None:
        self.assertEqual(self.item.get_secret(), b'pa$$word')
        self.item.set_secret(b'newpa$$word')
        self.assertIsInstance(self.item.get_secret(), bytes)
        self.assertEqual(self.item.get_secret(), b'newpa$$word')
        self.assertEqual(self.other_item.get_secret(), b'')

    def test_secret_wrong_type(self) -> None:
        # string passwords are encoded as bytes
        self.item.set_secret('test тест')  # type: ignore
        self.assertEqual(self.item.get_secret(),
                         'test тест'.encode())
        # other types are not allowed
        with self.assertRaises(TypeError):
            self.item.set_secret(None)  # type: ignore

    def test_secret_content_type(self) -> None:
        self.assertEqual(self.item.get_secret_content_type(), 'text/plain')
        # The check below fails in gnome-keyring because it doesn't really
        # support content types.
        # self.assertEqual(self.other_item.get_secret_content_type(), 'data/null')

    def test_modified(self) -> None:
        now = time.time()
        modified = self.item.get_modified()
        self.assertAlmostEqual(now, modified, places=-1)

    def test_created(self) -> None:
        created = self.item.get_created()
        self.assertAlmostEqual(self.created_timestamp, created, places=-1)

    def test_unlock(self) -> None:
        self.item.unlock()
