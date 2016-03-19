# ~/dev/py/pzog/pzog/xlattice/node.py

import os
from Crypto.Hash import SHA as sha
from Crypto.PublicKey import RSA as rsa
#from Crypto.Signature       import PKCS1_PSS    as pkcs1
from Crypto.Signature import PKCS1_v1_5 as pkcs1
from pzog.xlattice import SHA3_256
import u


class AbstractNode(object):

    def __init__(self, usingSHA1=False, pubKey=None, nodeID=None):
        self._usingSHA1 = usingSHA1
        if nodeID is None:
            if pubKey:
                # DEBUG
                print("AbstractNode: public key is %s" % str(pubKey))
                print("              class is %s" % pubKey.__class__)
                # END
                if usingSHA1:
                    h = sha.new()
                else:
                    h = SHA3_256.new()
                h.update(pubKey.exportKey())
                nodeID = h.digest()    # a binary value
            else:
                raise ValueError('cannot calculate nodeID without pubKey')

        self._nodeID = nodeID
        self._pubKey = pubKey

    @property
    def nodeID(self): return self._nodeID

    @property
    def pubKey(self): return self._pubKey


class Node(AbstractNode):
    """
    """

    def __init__(self, usingSHA1=False, privateKey=None):
        # making this the default value doesn't work: it always
        # generates the same key
        if privateKey is None:
            privateKey = rsa.generate(2048, os.urandom)
        nodeID, pubKey = Node.getIDAndPubKeyForNode(
            usingSHA1, self, privateKey)
        AbstractNode.__init__(self, usingSHA1, pubKey, nodeID)

        assert(isinstance(usingSHA1, bool))

        if not privateKey:
            raise ValueError('INTERNAL ERROR: undefined private key')
        self._privateKey = privateKey

        # each of these needs some sort of map or maps, or we will have to do
        # a linear search
        self._peers = []
        self._overlays = []    #
        self._connections = []    # with peers? with clients?

    def createFromKey(self, s):
        # XXX STUB: given the serialization of a node, create one
        # despite the name, this should also handle peer lists, etc
        # XXX WE ALSO NEED a serialization function
        pass

    @staticmethod
    def getIDAndPubKeyForNode(usingSHA1, node, rsaPrivateKey):

        (nodeID, pubKey) = (None, None)
        pubKey = rsaPrivateKey.publickey()

#       # DEBUG
#       print "GET_ID: private key is %s" % str(rsaPrivateKey.__class__)
#       print "    has_private = %s" % rsaPrivateKey.has_private()
#       print "GET_ID: public key is  %s" % str(pubKey.__class__)
#       print "    has_private = %s" % pubKey.has_private()
#       # END

        # generate the nodeID from the public key
        if usingSHA1:
            h = sha.new()
        else:
            h = SHA3_256.new()
        h.update(pubKey.exportKey())
        nodeID = h.digest()
        return (nodeID,                 # nodeID = 160/256 bit BINARY value
                pubKey)                 # from private key

    @property
    def key(self):
        return self._privateKey

    # these work with
    def sign(self, msg):
        if self._usingSHA1:
            h = sha.new()
        else:
            h = SHA3_256.new()
        h.update(msg)
        d = h.digest()
        return self._privateKey.sign(d, msg)

    def verify(self, msg, signature):
        if self._usingSHA1:
            h = sha.new()
        else:
            h = SHA3_256.new()
        h.update(msg)
        d = h.digest()
        return self._pubKey.verify(d, signature)


class Peer(AbstractNode):
    """ a Peer is a Node seen from the outside """

    def __init__(self, usingSHA1=False, nodeID=None, pubKey=None):
        AbstractNode.__init__(self, usingSHA1, nodeID, pubKey)
