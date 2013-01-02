# SecretStorage module for Python
# Access passwords using the SecretService DBus API
# Author: Dmitry Shachnev, 2013
# License: BSD

"""This module provides some utility functions, but these shouldn't
normally be used by external applications."""

import dbus
from secretstorage.defines import SECRETS, SS_PATH, SS_PREFIX

def open_session(bus):
	"""Returns a new Secret Service session."""
	service_obj = bus.get_object(SECRETS, SS_PATH)
	service_iface = dbus.Interface(service_obj, SS_PREFIX+'Service')
	return service_iface.OpenSession('plain', '', signature='sv')[1]

def format_secret(secret, session):
	"""Formats `secret` to make possible to pass it to the
	Secret Service API."""
	if not isinstance(secret, bytes):
		secret = secret.encode('utf-8')
	return dbus.Struct((session, '', dbus.ByteArray(secret), 'text/plain'))

def exec_prompt(bus, prompt, callback):
	"""Executes the given `prompt`, when complete calls `callback`
	function with two arguments: a boolean representing whether the
	operation was dismissed and a list of unlocked item paths. A main
	loop should be running and registered for this function to work."""
	prompt_obj = bus.get_object(SECRETS, prompt)
	prompt_iface = dbus.Interface(prompt_obj, SS_PREFIX+'Prompt')
	prompt_iface.Prompt('')
	def new_callback(dismissed, unlocked):
		if isinstance(unlocked, dbus.Array):
			unlocked = list(unlocked)
		callback(bool(dismissed), unlocked)
	prompt_iface.connect_to_signal('Completed', new_callback)

def exec_prompt_async_glib(bus, prompt):
	"""Like :func:`exec_prompt`, but asynchronous (uses loop from GLib
	API). Retuns (*dismissed*, *unlocked*) tuple."""
	from gi.repository import GObject
	loop = GObject.MainLoop()
	result = []
	def callback(dismissed, unlocked):
		result.append(dismissed)
		result.append(unlocked)
		loop.quit()
	exec_prompt(bus, prompt, callback)
	loop.run()
	return result[0], result[1]

def exec_prompt_async_qt(bus, prompt):
	"""Like :func:`exec_prompt`, but asynchronous (uses loop from PyQt4
	API). Retuns (*dismissed*, *unlocked*) tuple."""
	from PyQt4.QtCore import QCoreApplication
	app = QCoreApplication([])
	result = []
	def callback(dismissed, unlocked):
		result.append(dismissed)
		result.append(unlocked)
		loop.quit()
	exec_prompt(bus, prompt, callback)
	app.exec_()
	return result[0], result[1]

def to_unicode(string):
	"""Converts D-Bus string to unicode string."""
	try:
		# For Python 2
		return unicode(string)
	except NameError:
		# For Python 3
		return str(string)
