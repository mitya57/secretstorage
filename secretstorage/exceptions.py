# SecretStorage module for Python
# Access passwords using the SecretService DBus API
# Author: Dmitry Shachnev, 2012
# License: BSD

"""All secretstorage functions may raise various exceptions when
something goes wrong. All exceptions derive from base
:exc:`SecretStorageException` class."""

class SecretStorageException(Exception):
	"""All exceptions derive from this class."""
	pass

class LockedException(SecretStorageException):
	"""Raised when an action cannot be performed because the collection
	is locked. Use :meth:`~secretstorage.collection.Collection.is_locked`
	to check if the collection is locked, and
	:meth:`~secretstorage.collection.Collection.unlock` to unlock it.
	"""
	pass

class ItemNotFoundException(SecretStorageException):
	"""Raised when an item does not exist or has been deleted. Example of
	handling:

	>>> try:
	...     item = secretstorage.Item(item_path)
	... except secretstorage.ItemNotFoundException:
	...     print('Item not found!')
	... 
	'Item not found!'

	Also, :func:`~secretstorage.collection.create_collection` may raise
	this exception when a prompt was dismissed during creating the
	collection.
	"""
	pass
