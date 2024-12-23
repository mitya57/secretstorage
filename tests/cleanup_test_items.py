#!/usr/bin/env python3

from contextlib import closing

import secretstorage

with closing(secretstorage.dbus_init()) as connection:
    items = secretstorage.search_items(
        connection, {'application': 'secretstorage-test'}
    )

    for item in items:
        print('Deleting item with label %r.' % item.get_label())
        item.delete()
