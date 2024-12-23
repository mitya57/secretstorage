#!/usr/bin/env python

import os.path
import subprocess
import sys
import unittest

tests_dir = os.path.dirname(__file__)
sys.path.insert(0, os.path.dirname(tests_dir))

import secretstorage  # noqa

if __name__ == '__main__':
    major, minor, patch = sys.version_info[:3]
    print('Running with Python %d.%d.%d (SecretStorage from %s)' %
          (major, minor, patch, os.path.dirname(secretstorage.__file__)))
    mock = None
    if len(sys.argv) > 1 and os.path.isfile(sys.argv[1]):
        mock = subprocess.Popen(('/usr/bin/python3', sys.argv[1],),
                                stdout=subprocess.PIPE,
                                universal_newlines=True)
        assert mock.stdout is not None  # for mypy
        bus_name = mock.stdout.readline().rstrip()
        secretstorage.util.BUS_NAME = bus_name
        print('Bus name set to %r' % secretstorage.util.BUS_NAME)
    loader = unittest.TestLoader()
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(loader.discover(tests_dir))
    if mock is not None:
        mock.terminate()
    sys.exit(not result.wasSuccessful())
