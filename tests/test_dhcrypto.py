# Tests for SecretStorage
# Author: Dmitry Shachnev, 2014-2016
# License: 3-clause BSD, see LICENSE file

# This file tests the dhcrypto module.

import unittest

from secretstorage.dhcrypto import int_to_bytes


class ConversionTest(unittest.TestCase):
    """A test case that tests conversion functions
    between bytes and long."""

    def test_int_to_bytes(self) -> None:
        self.assertEqual(int_to_bytes(1), b'\x01')
        self.assertEqual(int_to_bytes(258), b'\x01\x02')
        self.assertEqual(int_to_bytes(1 << 64), b'\x01' + b'\x00' * 8)
