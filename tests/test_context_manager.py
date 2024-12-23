# Tests for SecretStorage
# Author: Dmitry Shachnev, 2019
# License: 3-clause BSD, see LICENSE file

# This file tests using secretstorage.dbus_init() function
# together with contextlib.closing context manager.

import unittest
from contextlib import closing

from secretstorage import check_service_availability, dbus_init
from secretstorage.collection import get_any_collection


class ContextManagerTest(unittest.TestCase):
    """``dbus_init()`` should work fine with ``contextlib.closing``
    context manager."""

    def test_closing_context_manager(self) -> None:
        with closing(dbus_init()) as connection:
            self.assertTrue(check_service_availability(connection))
            collection = get_any_collection(connection)
            self.assertIsNotNone(collection)
            label = collection.get_label()
            self.assertIsNotNone(label)
