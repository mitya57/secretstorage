#!/usr/bin/env python3

import secretstorage

with secretstorage.create_connection() as connection:
	items = secretstorage.search_items(connection, {'application': 'secretstorage-test'})

	for item in items:
		print('Deleting item with label %r.' % item.get_label())
		item.delete()
