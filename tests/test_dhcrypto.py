# Tests for SecretStorage
# Author: Dmitry Shachnev, 2014
# License: BSD

# This file tests the dhcrypto module.

import unittest
from secretstorage.dhcrypto import long_to_bytes, bytes_to_long

class ConversionTest(unittest.TestCase):
	"""A test case that tests conversion functions
	between bytes and long."""

	def test_long_to_bytes(self):
		self.assertEqual(long_to_bytes(1), b'\x01')
		self.assertEqual(long_to_bytes(258), b'\x01\x02')
		self.assertEqual(long_to_bytes(1 << 64), b'\x01' + b'\x00' * 8)

	def test_bytes_to_long(self):
		self.assertEqual(bytes_to_long(b'\x01'), 1)
		self.assertEqual(bytes_to_long(b'\x01\x02'), 258)
		self.assertEqual(bytes_to_long(b'\x01' + b'\x00' * 8), 1 << 64)

	def test_array_to_long(self):
		self.assertEqual(bytes_to_long([1] + [0] * 8), 1 << 64)
		self.assertEqual(bytes_to_long(bytearray([1] + [0] * 8)), 1 << 64)

if __name__ == '__main__':
	unittest.main()
