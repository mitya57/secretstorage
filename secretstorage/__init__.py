# SecretStorage module for Python
# Access passwords using the SecretService DBus API
# Author: Dmitry Shachnev, 2013-2018
# License: 3-clause BSD, see LICENSE file

"""This file provides quick access to all SecretStorage API. Please
refer to documentation of individual modules for API details.

It also provides some functions for compatibility with older
SecretStorage releases. Those functions are not recommended for use
in new software."""

import warnings
from jeepney.integrate.blocking import connect_and_authenticate
from secretstorage.collection import Collection, create_collection, \
 get_all_collections, get_default_collection, get_any_collection, \
 get_collection_by_alias, search_items
from secretstorage.item import Item
from secretstorage.exceptions import SecretStorageException, \
 SecretServiceNotAvailableException, LockedException, \
 ItemNotFoundException

__version_tuple__ = (3, 0, 1)
__version__ = '.'.join(map(str, __version_tuple__))

def dbus_init(*args, **kwargs):
	"""Returns a new connection to the session bus, instance of
	:class:`jeepney.DBusConnection` instance. This connection can
	then be passed to various SecretStorage functions, such as
	:func:`~secretstorage.collection.get_default_collection`.

	.. versionchanged:: 3.0
	   Before the port to Jeepney, this function returned an
	   instance of :class:`dbus.SessionBus` class.
	   Also, passing any arguments to this function is now deprecated.
	"""
	if args or kwargs:
		warnings.warn("Passing any arguments to dbus_init() is"
		              " deprecated.", DeprecationWarning)
	try:
		return connect_and_authenticate()
	except KeyError as ex:
		# os.environ['DBUS_SESSION_BUS_ADDRESS'] may raise it
		reason = "Environment variable {} is unset".format(ex.args[0])
		raise SecretServiceNotAvailableException(reason) from ex
