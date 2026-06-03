import sys, json, uuid; sys.path.insert(0,".build")
from nbbuild import md
path="chapters/02_cryptography/chapter02.ipynb"
nb=json.load(open(path)); cells=nb["cells"]
def find(prefix):
    for i,c in enumerate(cells):
        if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith(prefix):
            return i
    return None

# Deepen 2.7 hashing: applications paragraph
i=find("## 2.7")
add27=r'''

Because they are fast, deterministic, and collision-resistant, hash functions appear far beyond
integrity checking, and recognizing these uses helps connect later chapters. They enable **deduplication
and content addressing** (Git names every object by its SHA hash, so identical content is stored once and
any tampering is detectable). They provide **commitment**: publishing the hash of a value lets you reveal
the value later and prove you had not changed it, the basis of many protocols. They drive **proof of
work** in blockchains, where miners search for inputs whose hash meets a difficulty target. They support
**password-adjacent** uses such as deriving lookup keys and HMAC-based one-time passwords. And the
**Merkle tree** structure, by letting any single leaf be verified against a tiny root hash with a short
"proof path," underpins Certificate Transparency, peer-to-peer file distribution, and the tamper-evident
ledgers of distributed systems. When you meet these mechanisms in later chapters, remember that a single
primitive, the cryptographic hash, is doing the heavy lifting.'''
cells[i]["source"]=(("".join(cells[i]["source"])).rstrip()+add27+"\n").splitlines(keepends=True)

# Deepen 2.13 PKI: certificate contents and chain validation
i=find("## 2.13")
add213=r'''

It helps to know what a certificate actually contains and how validation really proceeds, since
certificate errors are among the most common security decisions an ordinary user faces. An X.509
certificate carries the *subject* (the identity, such as a domain name, possibly with Subject
Alternative Names for multiple hosts), the *subject public key*, the *issuer* (the CA that signed it), a
*validity period* (not-before and not-after dates), a *serial number*, key-usage constraints, and the
CA's *digital signature* over all of the above. To validate a server's certificate, a client performs
several checks in sequence: it confirms the certificate has not expired, that the requested hostname
matches the subject or a SAN, that the certificate has not been revoked (via CRL or OCSP), and, crucially,
that the signature chain leads from the server's certificate, through any intermediate CA certificates,
up to a *root* certificate already in the client's trust store. Each link is verified by checking that
the issuer's public key validates the next certificate's signature. If any check fails, the connection
should be refused. This chain of trust is powerful but only as strong as its weakest CA, which is why
incidents in which a CA was tricked or breached into issuing fraudulent certificates (for example the
2011 DigiNotar compromise, which led to that CA's removal from trust stores) are treated as serious
ecosystem-wide events, and why Certificate Transparency now requires CAs to log every certificate they
issue to public, append-only Merkle-tree logs that domain owners can monitor.'''
cells[i]["source"]=(("".join(cells[i]["source"])).rstrip()+add213+"\n").splitlines(keepends=True)

# New section 2.18 Applied Cryptographic Systems before "## Why This Matters"
wi=find("## Why This Matters")
applied=md(r'''## 2.18 Applied Cryptographic Systems

The TLS handshake showed primitives combining into one protocol. To make the chapter's relevance
concrete, this section briefly surveys the other systems you use every day that are, underneath, the same
building blocks rearranged. Each is developed further in later chapters; the goal here is to see the
cryptography at work.

**Full-disk and file encryption** protect data at rest. Tools such as BitLocker, FileVault, and LUKS
encrypt entire volumes with a symmetric cipher (AES in a length-preserving mode such as XTS designed for
storage), while the disk key is itself protected by a key derived from the user's password and, ideally,
sealed in a TPM so that the disk cannot be decrypted on different hardware. This is why a stolen but
powered-off encrypted laptop usually protects its data, and why the *possession* property of the
Parkerian hexad, lost when the hardware is taken, still does not imply loss of *confidentiality*.

**Secure messaging** brought strong end-to-end encryption (E2EE) to billions of people. The Signal
protocol, used by Signal, WhatsApp, and others, combines an initial ECDH key agreement (X3DH) with the
**double ratchet**, which derives a fresh key for every message so that compromising one key exposes
neither past nor future messages, properties called forward secrecy and post-compromise security. E2EE
means the service provider itself cannot read message contents, which is also why it is a recurring point
of tension with law enforcement, revisited in the privacy and law chapter.

**Virtual private networks (VPNs)** create an encrypted tunnel across an untrusted network. IPsec and the
modern, compact WireGuard protocol authenticate the endpoints and then carry traffic under authenticated
encryption, applying the same key-exchange-then-symmetric pattern as TLS at the network layer. **Code
signing** uses digital signatures so that operating systems and app stores install only software whose
signature verifies against a trusted developer key, the defense whose subversion made the SolarWinds
supply-chain attack so damaging. **Cryptocurrencies** combine hash-linked Merkle-tree ledgers with
elliptic-curve signatures: ownership of funds is simply possession of a private key, which makes key
management (Section 2.16) a matter of real money and explains why lost or stolen keys translate directly
into lost or stolen value. Across all of these, notice the recurring grammar of applied cryptography:
agree on a key, encrypt with AEAD, authenticate with signatures or MACs, and manage keys carefully. Once
you see that grammar, unfamiliar secure systems become readable.''')
applied.setdefault("id", uuid.uuid4().hex[:12])
cells[wi:wi]=[applied]

for c in cells: c.setdefault("id", uuid.uuid4().hex[:12])
json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="markdown")
codew=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="code")
print(f"chapter02: {len(cells)} cells, {mdw} md words (~{mdw/500:.1f} pages), +{codew} code words")
