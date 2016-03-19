# Crypto Implementation Nodes

## Private Key Generation

Use

	openssl genrsa -out openssl2k.pem 2048

to generate a 2Kbit private key and write it to the file names.

## OIDs

Current roadblock is the lack of an OID for SHA3_256 aka Keccak-256.

Per sp800-78-3.pdf, section 3.2.3, the object identifier for SHA-1 is

    id-sha1 ::= {iso(1) identified-organization(3) oiw(14) secsig(3) algorithms(2) 26}

**LATER NODE:** This is the ITU's unwieldy way of writing what the IETF calls
1.3.14.3.2.26..  See http://www.alvestrand.no/objectid/ and
http://www.itu.int/ITU-T/asn1/  The ITU website points you to www.oid-info.com,
a searchable OID repository.  This contains nothing matching keccak or sha3
or sha-3 or sha3_256.  It yields many matches on sha1, including this one, as
the 42nd match.

Section 3.2.1, Table 3-4, in the same document has for the signature algorithm
"RSA with SHA-1 and PKCS #1 v1.5 padding" the object identifier

    sha1WithRSAEncryption ::=
        {iso(1) member-body(2) us(840) rsadsi(113549) pkcs(1) pkcs-1(1) 5}

In the RFC, there is only one space after the '::='; there is no carriage
return in either of these OIDs.

These are encoded as ASN.1 DER object identifiers.  The first is also declared
in RFC 3370, section 2.1, page 3 in the .txt version of the RFC, published in
August 2002.  Section 3.2 of RSA 3370 on page 6 sets out the second OID above.
These are also included in the summary, section 7, ASN.1 Module, in that RFC.

docs.python.org/3.4/whatsnew/changelog.html says that they have added an sha3
module based on the Keccak reference implementation and that hashlib now
has four additional hash algorithms sha3_{224,256,384,612} (in my notation).
This is in response to http://bugs.python.org/issue16113 which has the title
"Add SHA-3 (Keccak) support" and was dated 2012-10-03.

This new module by Christian Helmes may be better than the python-sha3 by
Bjorn Edstrom that I got from github.com.

[The Python bug report](http://bugs.python.org/issue16166)
follows on from this.

## A Pycrypt Problem?

PKCS1-V1_5 is defined by RFC 3447.  The encryption operation is described
in section 7.2.1, which makes no mention of the OID.  The inputs are the
RSA public key (n,e) and the message.  The output is ciphertext.  The
decryption operation (section 7.2.2) has the private key and ciphertext
as input; the output is the message, an opaque sequence of octets.

The pycrypt implementation appears to have a message consisting of a
sequence of parts, with the OID as the first part.

However, it is possible that this is actually a result of the use of
ASN1.DER encoding... Yes.
[stackoverflow](See stackoverflow.com/questions/3713774 c-sharp-how-to-calculate-asn-1-der-encoding-of-a-particular-hash-algorithm).
This is exceedngly clear and makes it obvious that the problem is the
DigestInfo sequence, which includes the digestAlgorithm, which is another
seqence, the algorithm's OID and its parameter list (which is empty).  So
the problem is the PKCS1-V1_5 wrapper around the digital signature.

The core problem is that the signature formatter is dependent upon a
cumbersome standardization process.  PKCS1-V1_5 knows only about
the sha-1 variants (sha256, sha512, and so forth).  There isn't an
OID for sha3_256 / Keccak256 and without that progress is not possible.

Possibilities: (a) use a private OID or (b) proceed without the PKCS1-V1_5
wrapping.  The former is possible; there are free numbers, just are there
free ipv4 addresses like 10/8.  Private OIDs begin with 1.3.6.1.4.1
(iso.org.doc.internet.private.enterprise); these are in fact the most
common OIDs seen in the wild, according to Wikipedia's Object_identifier
article.

**LATER NODE:** the ASN.1 encoding for an SHA1 digest has one oddity.  The
  first two bytes of the OID, 1.3.14.3.2.26, are combined into 40*val1 + val2,
  which is 0x2b (decimal 3).  This gives a byte sequence

	SEQUENCE            30
	  LENGTH            21
	  SEQUENCE          30
	    LENGTh          09
	    OID             06                  # ALGORITHM
	      LEN           05
	      value         2b 0e 03 02 1a      # first byte = 40*1 + 3
	    PARAMETERS      05 00               # NULL
	    OCTET STRING    04
	      LEN           20
	      HASH          that many bytes

See
[A Layman's Guide to a Subset of ASN.1, BER, and DER](luca.ntop.org/Teaching/Appunti/asn1.html)
in addition to
[stackoverflow](stackoverflow.com/questions/3713774).

An instance of the type (b) approach would be to pass the digital signature
as a fieldz message.  The digital signature proper would be the sha3_256
hash of the message encrypted using a 2048-bit or better RSA private key.

Alter the Node spec to add a usingPKCS1 parameter defaulting to True.
Then we have a pkcs1Signer = pkcs1.new(self._privateKey) that is used
to sign the message if usingPKCS1; otherwise we use an sha3_256_signer
which returns a bytearray containing a lenBytes fieldz instance, that is,
if LEN is the length of the RSA-encrypted hash, than the digital signature
consists of

	varInt LEN

followed by LEN bytes of data, with no padding.

So we need to add to pzog.xlattice.crypto a class Signer with methods
sign() and verify(), and a subclass SHA3_256Signer.  This crypto module
can and should import the necessary bits from fieldz.

## Pysha3 0.2.1 (my notes 2012-11-02)

This is Christian Helmes's wrapper and patch to hashlib to support SHA3.  It
can be had through pypi.python.org/pypi/pysha3/0.2.1#downloads.

The 'home' site, https://bitbucket.org/tiran/pykeccak carries a warning:
"**Don't use SHA-3 for HMAC!** HMAC hasn't been specified for SHA-3 yet
and no test vectors are available, too."

I installed pysha3-0.2.1 on PaloAlto.  The tests.py script succeeds.

If this module is to be used it needs to be imported in such a way as
not to conflict with the Python 3.4 version of hashlib.

	import sys
	import hashlib
	if sys.version_info < (3,4):
	    import sha3
	# get eg 256-bit instance
	d = hashlib.new("sha3_256")     # or d = hashlib.sha3_256()

## Integrating pysah3-0.2.1 into Pycrypto

Using a private OID as described above and pycrypto-2.6/lib/Crypto/Hash/SHA.py
as a model:
