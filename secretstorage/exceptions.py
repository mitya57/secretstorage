# SecretStorage module for Python
# Access passwords using the SecretService DBus API
# Author: Dmitry Shachnev, 2012
# License: BSD

class SecretStorageException(Exception):
	pass

class LockedException(SecretStorageException):
	pass

class ItemNotFoundException(SecretStorageException):
	pass
