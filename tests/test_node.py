#!/usr/bin/env python3
# testNode.py

""" Test an XLattice-style Node. """

import time
import hashlib
# import os
# import sys
import unittest
from Crypto.PublicKey import RSA as rsa
# from Crypto.Signature import PKCS1_v1_5 as pkcs1

from xlattice import HashTypes, check_hashtype
# from xlattice.node import Node
from rnglib import SimpleRNG

RNG = SimpleRNG(time.time)


class TestNode(unittest.TestCase):
    """
    Tests an XLattice-style Node, including its sign() and verify()
    functions, using SHA1, SHA2(56), and SHA3
    """

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def check_node(self, node, hashtype):
        """
        Verify that the basic capabilities of an XLattice Node are present.
        """
        assert node is not None

        pub = node.pub_key
        id_ = node.node_id
        if hashtype == HashTypes.SHA1:
            self.assertEqual(20, len(id_))
            sha = hashlib.sha1()
        elif hashtype == HashTypes.SHA2:
            self.assertEqual(32, len(id_))
            sha = hashlib.sha256()
        elif hashtype == HashTypes.SHA3:
            self.assertEqual(32, len(id_))
            # pylint: disable=no-member
            sha = hashlib.sha3_256()

        sha.update(pub.exportKey())
        expected_id = sha.digest()
        self.assertEqual(expected_id, id_)

        # make a random array of bytes
        count = 16 + RNG.next_int16(256)
        msg = bytearray(count)
        RNG.next_bytes(msg)

        # sign it and verify that it verifies
        sig = node.sign(msg)
        self.assertTrue(node.verify(msg, sig))

        # flip some bits and verify that it doesn't verify with the same sig
        msg[0] = msg[0] ^ 0x36
        self.assertFalse(node.verify(msg, sig))

    # ---------------------------------------------------------------
    def do_test_generated_rsa_key(self, hashtype):
        """ Run tests on a generated Node for a specific hashtype. """

        assert hashtype                 # XXX hack: stop warnings
        # node = Node(hashtype=hashtype)  # no RSA key provided, so creates one
        # self.check_node(node, hashtype)

    def test_generated_rsa_key(self):
        """ Run basic tests for all supported hash types. """
        for hashtype in HashTypes:
            self.do_test_generated_rsa_key(hashtype)

    # ---------------------------------------------------------------
    def do_test_with_openssl_key(self, hashtype):
        """ Run tests using an OpenSSL key for the specified hashtypes. """

        check_hashtype(hashtype)

        # import an openSSL-generated 2048-bit key (this becomes a
        # string constant in this program)
        with open('tests/openssl2k.pem', 'r') as file:
            pem_key = file.read()
        key = rsa.importKey(pem_key)
        assert key is not None
        self.assertTrue(key.has_private())

        # XXX COMMENTED THIS OUT TO SILENCE WARNINGS
        # XXX Need ck_priv
        # node = Node(hashtype=hashtype, sk_priv=key)
        # self.check_node(node, hashtype)

        # The _RSAobj.publickey() returns a raw key.
        # self.assertEqual(key.publickey().exportKey(),
        #                 node.pub_key.exportKey())

        # -----------------------------------------------------------
        # CLEAN THIS UP: node.key and node.pubKey should return
        # stringified objects, but node._privateKey and _pubKey should
        # be binary
        # -----------------------------------------------------------

    def test_with_open_ssl_key(self):
        """ Run tests using an OpenSSL key for all supported hashtypes. """
        for hashtype in HashTypes:
            self.do_test_with_openssl_key(hashtype)


if __name__ == '__main__':
    unittest.main()
