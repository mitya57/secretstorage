#!/usr/bin/env python3

import secretstorage

bus = secretstorage.dbus_init()
items = secretstorage.search_items(bus, {'application': 'secretstorage-test'})

for item in items:
	print('Deleting item with label %r.' % item.get_label())
	item.delete()
