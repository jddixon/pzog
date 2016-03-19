# ~/dev/py/pzog/pzog/xlattice/crypto.py

import hashlib
import os
import Crypto.PublicKey.RSA as rsa
import Crypto.Util.number as rng


def createPrivateKey():
    # http://stackoverflow.com/questions/4232389/signing-and-verifying-i
    #        data-using-pycrypto-rsa
    # generate a 2 Kbit value
    key = rsa.generate(2048, os.urandom)
    # DEBUG
    print("HAVE GENERATED A PRIVATE KEY")
    # END
    return key              # a binary key


def getIDAndPubKeyForNode(node, rsaPrivateKey):

    (nodeID, pubKey) = (None, None)

    # generate the public key from the private key; will be in PEM format
    pubKey = rsaPrivateKey.publickey().exportKey()

    # DEBUG
    print("public key is %s" % str(pubKey))
    # END

    # generate the nodeID from the public key
    digest = hashlib.sha1()
    digest.update(pubKey)
    nodeID = digest.hexdigest()     # in string form

    return (nodeID,                 # nodeID = 160 bit value
            pubKey)                 # RSA public key, from private key #GEEP


def getRSAPublicKeyFromPrivate(rsaPrivateKey):
    # XXX STUB XXX
    return None
