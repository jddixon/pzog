#!/usr/bin/env python

# testCrypto.py
import time
import unittest

from pzog.xlattice.crypto import createPrivateKey, getIDAndPubKeyForNode


class TestCrypto (unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def testCreatePrivateKey(self):
        key = createPrivateKey()
        assert key is not None
        # wierd but seems to be  correct
        self.assertEquals(2048 - 1, key.size())
        self.assertTrue(key.has_private())
        print key.exportKey()

        pubkey = key.publickey()
        print pubkey.exportKey()

if __name__ == '__main__':
    unittest.main()
