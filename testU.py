#!/usr/bin/env python3

# testU.py
import time
import hashlib
import os
import sys
import unittest


class TestU (unittest.TestCase):
    """
    Tests an XLattice-style Node, including its sign() and verify()
    functions, using SHA1 and SHA3 (Keccak); for the latter I use a
    private OID.
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testURandom(self):
        stuff = os.urandom(256)
        print(("os.urandom() output is %s" % stuff.__class__))

        # XXX STUB XXX

if __name__ == '__main__':
    unittest.main()
