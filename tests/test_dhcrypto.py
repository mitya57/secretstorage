# Tests for SecretStorage
# Author: Dmitry Shachnev, 2014
# License: BSD

# This file tests the dhcrypto module.

import unittest
from secretstorage.dhcrypto import long_to_bytes

class ConversionTest(unittest.TestCase):
	"""A test case that tests conversion functions
	between bytes and long."""

	def test_long_to_bytes(self):
		self.assertEqual(long_to_bytes(1), b'\x01')
		self.assertEqual(long_to_bytes(258), b'\x01\x02')
		self.assertEqual(long_to_bytes(1 << 64), b'\x01' + b'\x00' * 8)

if __name__ == '__main__':
	unittest.main()
