.. image:: https://github.com/mitya57/secretstorage/workflows/tests/badge.svg
   :target: https://github.com/mitya57/secretstorage/actions
   :alt: GitHub Actions status
.. image:: https://codecov.io/gh/mitya57/secretstorage/branch/master/graph/badge.svg
   :target: https://codecov.io/gh/mitya57/secretstorage
   :alt: Coverage status
.. image:: https://readthedocs.org/projects/secretstorage/badge/?version=latest
   :target: https://secretstorage.readthedocs.io/en/latest/
   :alt: ReadTheDocs status

Module description
==================

This module provides a way for securely storing passwords and other secrets.

It uses D-Bus `Secret Service`_ API that is supported by GNOME Keyring,
KWallet (since version 5.97) and KeePassXC.

The main classes provided are ``secretstorage.Item``, representing a secret
item (that has a *label*, a *secret* and some *attributes*) and
``secretstorage.Collection``, a place items are stored in.

SecretStorage supports most of the functions provided by Secret Service,
including creating and deleting items and collections, editing items,
locking and unlocking collections.

The documentation can be found on `secretstorage.readthedocs.io`_.

.. _`Secret Service`: https://specifications.freedesktop.org/secret-service/
.. _`secretstorage.readthedocs.io`: https://secretstorage.readthedocs.io/en/latest/

Building the module
===================

SecretStorage requires Python ≥ 3.10 and these packages to work:

* Jeepney_
* `python-cryptography`_

To build SecretStorage, use this command::

   python3 -m build

If you have Sphinx_ installed, you can also build the documentation::

   python3 -m sphinx docs build/sphinx/html

.. _Jeepney: https://pypi.org/project/jeepney/
.. _`python-cryptography`: https://pypi.org/project/cryptography/
.. _Sphinx: https://www.sphinx-doc.org/en/master/

Testing the module
==================

First, make sure that you have the Secret Service daemon installed.
The `GNOME Keyring`_ is the reference server-side implementation for the
Secret Service specification.

.. _`GNOME Keyring`: https://download.gnome.org/sources/gnome-keyring/

Then, start the daemon and unlock the ``default`` collection, if needed.
The testsuite will fail to run if the ``default`` collection exists and is
locked. If it does not exist, the testsuite can also use the temporary
``session`` collection, as provided by the GNOME Keyring.

Then, run the Python unittest module::

   python3 -m unittest discover -s tests

If you want to run the tests in an isolated or headless environment, run
this command in a D-Bus session::

   dbus-run-session -- python3 -m unittest discover -s tests

Get the code
============

SecretStorage is available under BSD license. The source code can be found
on GitHub_.

.. _GitHub: https://github.com/mitya57/secretstorage
