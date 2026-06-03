import sys, pickle; sys.path.insert(0,".build")
from nbbuild import md, code
C=pickle.load(open(".build/_ch02_cells.pkl","rb")); A=C.append

A(md(r'''## 2.11 Diffie-Hellman Key Exchange

Public-key encryption lets two strangers communicate secretly, but asymmetric operations are slow, so in
practice we use them only to establish a shared symmetric key and then switch to fast symmetric
encryption. The original and most elegant mechanism for agreeing on a shared secret over a public channel
is the **Diffie-Hellman key exchange (DHKE)**. Its near-magical property is that two parties can derive a
common secret while an eavesdropper who sees every message exchanged still cannot compute it.

The classic construction works in modular arithmetic. The parties publicly agree on a large prime p and
a generator g. Alice picks a secret a and sends A = g^a mod p; Bob picks a secret b and sends B = g^b mod
p. Alice computes B^a mod p and Bob computes A^b mod p; both equal g^(ab) mod p, the shared secret. The
eavesdropper sees g, p, A, and B but cannot recover the secret without solving the **discrete logarithm
problem**, finding a from g^a mod p, which is infeasible for large p. The shared value is then fed through
a KDF to produce symmetric keys.

A vital caveat: plain Diffie-Hellman provides no authentication, so it is vulnerable to a
*man-in-the-middle* attack in which an active attacker performs separate exchanges with each party and
relays traffic. DH must therefore be combined with authentication (signatures or certificates), as TLS
does. A further refinement is *ephemeral* Diffie-Hellman (DHE, or ECDHE on elliptic curves), which uses
fresh random secrets for every session. This provides **forward secrecy**: even if a server's long-term
private key is later stolen, past recorded sessions remain secret, because the per-session DH secrets
were never stored. Forward secrecy is now a standard requirement and is mandatory in TLS 1.3.
'''))

A(code(r'''# Chapter 2 -- Diffie-Hellman shared-secret derivation (small numbers for clarity)
p = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD1  # a (small, demo) prime
g = 2
import secrets
a = secrets.randbelow(p - 2) + 2     # Alice's private secret
b = secrets.randbelow(p - 2) + 2     # Bob's private secret
A = pow(g, a, p)                     # Alice -> Bob (public)
B = pow(g, b, p)                     # Bob -> Alice (public)
alice_shared = pow(B, a, p)          # Alice computes B^a
bob_shared   = pow(A, b, p)          # Bob computes A^b
print("Alice and Bob agree:", alice_shared == bob_shared)
print("Shared secret (hex):", hex(alice_shared)[:50], "...")
print("An eavesdropper sees g, p, A, B but must solve discrete log to get the secret.")''' ))

A(md(r'''## 2.12 Elliptic-Curve Cryptography

RSA and classical Diffie-Hellman are secure only with large keys (2048 bits and up), which cost
bandwidth, storage, and computation, an increasing burden on mobile and embedded devices. **Elliptic-curve
cryptography (ECC)** provides the same security with dramatically smaller keys by basing its hard problem
on the algebra of points on an elliptic curve rather than on integer factoring or modular exponentiation.

An elliptic curve over a finite field is the set of points satisfying an equation such as y^2 = x^3 + ax +
b, together with a special "point at infinity." One can define an addition operation on these points with
the same group structure that makes Diffie-Hellman work. The security rests on the **elliptic-curve
discrete logarithm problem**: given a base point G and a multiple Q = kG (adding G to itself k times),
recovering the scalar k is infeasible. Because no sub-exponential algorithm is known for this problem
(unlike factoring), ECC keys can be much shorter: a 256-bit elliptic-curve key offers security comparable
to a 3072-bit RSA key. This efficiency is why ECC now dominates new deployments.

Practitioners rarely choose curve parameters themselves; they use vetted *named curves*. Common choices
include the NIST curves P-256, P-384, and P-521, and the modern, rigidly designed **Curve25519** (used
for key exchange as X25519) and its signature counterpart **Ed25519**, both prized for speed,
simplicity, and resistance to implementation pitfalls. The elliptic-curve forms of the standard
protocols, ECDH/ECDHE for key exchange and ECDSA/EdDSA for signatures, are the defaults in TLS 1.3,
SSH, Signal, and most cryptocurrencies (Bitcoin and Ethereum use the curve secp256k1). When you need
asymmetric cryptography today, ECC is usually the right starting point unless interoperability forces
RSA.
'''))

A(md(r'''## 2.13 Digital Signatures, Certificates, and PKI

A **digital signature** is the public-key analog of a handwritten signature, but far stronger. To sign,
the author hashes the message and transforms the hash with their *private* key; anyone can verify by
checking the signature against the message using the author's *public* key. A valid signature proves
three things at once: **integrity** (the message was not altered, or the hash would differ),
**authentication** (only the private-key holder could have produced it), and **non-repudiation** (the
signer cannot credibly deny it, since no one else has the private key). This last property, unique to
public-key methods, is why signatures underpin software distribution, legal documents, and blockchain
transactions. Standard signature algorithms are RSA-PSS, ECDSA, and EdDSA.

Signatures create a new problem, however: how do you know that a public key really belongs to the party
it claims to? If an attacker can substitute their own public key, they can impersonate anyone. The
answer is a **public-key infrastructure (PKI)**, a system of trust built on **digital certificates**. A
certificate is a data structure (in the X.509 format) that binds an identity (such as a domain name) to
a public key, and is itself *signed* by a trusted **certificate authority (CA)**. Your browser and
operating system ship with a list of trusted *root CAs*; a website presents a certificate signed by a CA
(possibly through a chain of intermediate CAs leading back to a trusted root), and your browser verifies
the chain of signatures up to a root it trusts. This delegated trust lets you authenticate a server you
have never met.

PKI is powerful but introduces its own risks and machinery: CAs can be compromised or coerced into
issuing fraudulent certificates, so mechanisms such as *certificate revocation* (CRLs and OCSP),
*Certificate Transparency* logs (public, append-only logs of issued certificates, often built on Merkle
trees), and short certificate lifetimes exist to detect and contain abuse. Certificate validation
failures, expired certificates, name mismatches, untrusted issuers, are among the most common security
warnings users see, and training users to click through them undermines the entire system.
'''))

A(md(r'''## 2.14 Putting It Together: The TLS Handshake

Transport Layer Security (TLS), the protocol behind the padlock in your browser and the "S" in HTTPS,
is the most important real-world application of everything in this chapter. It weaves together
asymmetric and symmetric cryptography, signatures, certificates, and key exchange to turn an insecure
network into a confidential, authenticated channel. The modern version, TLS 1.3 (2018), streamlined and
hardened the protocol, removing legacy ciphers and mandating forward secrecy.

At a high level, a TLS 1.3 handshake proceeds as follows. The client opens with a *ClientHello* that
offers its supported cipher suites and includes an ephemeral (EC)DH key share. The server replies with a
*ServerHello* containing its own key share, its **certificate**, and a **signature** over the handshake
that proves possession of the certificate's private key. Both sides now combine their ephemeral key
shares via (EC)DHE to derive a shared secret, run it through a KDF (HKDF) to produce symmetric session
keys, and switch to fast AEAD encryption (AES-GCM or ChaCha20-Poly1305) for all subsequent application
data. The ephemeral key exchange provides forward secrecy; the certificate and signature provide server
authentication and defeat the man-in-the-middle attack that plain DH would allow.

```{mermaid}
sequenceDiagram
    participant C as Client
    participant S as Server
    C->>S: ClientHello (cipher suites, ECDHE key share, random)
    S->>C: ServerHello (chosen suite, ECDHE key share, random)
    S->>C: Certificate (X.509, public key)
    S->>C: CertificateVerify (signature over handshake)
    S->>C: Finished (MAC over handshake)
    Note over C,S: Both derive shared secret via ECDHE, then HKDF -> session keys
    C->>S: Finished (MAC over handshake)
    Note over C,S: Encrypted application data (AES-GCM / ChaCha20-Poly1305)
```

Trace each arrow against the primitives in this chapter: key exchange (ECDHE), certificates and
signatures (PKI), key derivation (HKDF), and authenticated encryption (AEAD). TLS is a microcosm of
applied cryptography, and its history of attacks, BEAST, CRIME, POODLE, Heartbleed, and downgrade
attacks, is a catalog of how subtle the engineering is even when the underlying algorithms are sound.
'''))
print("part E total:", len(C))
pickle.dump(C, open(".build/_ch02_cells.pkl","wb"))
