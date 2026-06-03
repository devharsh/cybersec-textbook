import sys, json, uuid; sys.path.insert(0,".build")
from nbbuild import md
path="chapters/02_cryptography/chapter02.ipynb"
nb=json.load(open(path)); cells=nb["cells"]
def find(prefix):
    for i,c in enumerate(cells):
        if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith(prefix):
            return i
    return None
def append_to(prefix, text):
    i=find(prefix); cells[i]["source"]=(("".join(cells[i]["source"])).rstrip()+text+"\n").splitlines(keepends=True)

append_to("## 2.4", r'''

Where does true entropy actually come from? Operating systems harvest unpredictability from physical
events, the precise timing of interrupts, keystrokes, mouse movement, and disk activity, and many modern
CPUs include a hardware random-number generator (Intel's RDRAND, for example) seeded by thermal noise.
This entropy is collected into a pool that seeds a CSPRNG. A long-standing point of confusion on Linux is
the difference between `/dev/random` and `/dev/urandom`: historically the former could block waiting for
"fresh" entropy while the latter would not, but on modern kernels, once the pool has been initialized
once, both are cryptographically secure, and the recommended interface is the `getrandom` system call.
The real-world failures are sobering. Embedded devices and virtual machines often boot with little
entropy and have generated predictable keys at scale; a famous 2012 study found large numbers of TLS and
SSH keys sharing factors because devices generated them before gathering enough randomness. The
operational takeaways are to ensure adequate entropy at first boot, to prefer the OS CSPRNG over any
home-grown generator, and to be especially careful in virtualized and embedded environments.''')

append_to("## 2.6", r'''

A practical note ties these modes to engineering reality. CTR and GCM are *parallelizable* and require no
padding, which suits high-throughput systems and is one reason AES-GCM dominates TLS; CBC is sequential
and needs padding, which historically exposed it to padding-oracle attacks. All modes that take an IV or
nonce demand care: the IV for CBC must be unpredictable, while the nonce for CTR and GCM must be unique
but need not be secret, and confusing these requirements has broken real systems. The single most
important operational rule across every mode is the one stated for the one-time pad and repeated for GCM:
the combination of key and nonce must never repeat. When this discipline is hard to guarantee, for
example across distributed servers, prefer a nonce-misuse-resistant mode such as AES-GCM-SIV, which
degrades gracefully if a nonce is accidentally reused.''')

append_to("## 2.10", r'''

Two cautions make RSA safe in practice, and both are frequent exam and audit topics. First, **textbook
RSA is insecure** and must never be used directly. Because plain RSA is deterministic, identical messages
encrypt identically (leaking equality), small messages with a small public exponent can be recovered by
simply taking an integer root (m^e may be less than n, so no modular reduction occurs), and the
multiplicative homomorphism enables chosen-ciphertext manipulation. Secure padding fixes these: **OAEP**
randomizes and structures the plaintext before encryption, and **PSS** does so for signatures, which is
why every real library applies them. Second, RSA has been undone by *parameter* mistakes rather than by
factoring: reusing a modulus across users, choosing primes that are too close together, using a tiny
private exponent, or, as Section 2.4 noted, generating primes with poor randomness so that two keys share
a common factor that a simple GCD computation reveals. These lessons reinforce the chapter's refrain:
even a sound algorithm fails when its preconditions, randomness, padding, and parameter hygiene, are
violated.''')

append_to("## 2.12", r'''

A little geometry demystifies elliptic-curve "addition." Over the real numbers, to add two points P and Q
on the curve you draw the line through them, find the third point where that line intersects the curve,
and reflect it across the x-axis; to "double" a point you use the tangent line instead. Cryptography uses
the same rule over a finite field rather than the reals, which scrambles the geometry into something that
looks random while preserving the group structure that makes the math work. Scalar multiplication, adding
G to itself k times to get kG, is fast (using double-and-add), but inverting it to recover k from kG and G
is the hard elliptic-curve discrete-log problem. Because the best known attacks on well-chosen curves are
fully exponential, key sizes stay small: 256-bit curves for roughly 128-bit security. Practitioners must
still avoid pitfalls, using vetted curves (the rigidity of Curve25519 was designed to remove the suspicion
that surrounds some parameter choices), validating that received points actually lie on the curve to
prevent invalid-curve attacks, and using constant-time implementations to resist timing side channels.''')

# New section 2.19 practical guidance before "## Why This Matters"
wi=find("## Why This Matters")
guidance=md(r'''## 2.19 Practical Guidance: Choosing and Using Cryptography

After surveying primitives, attacks, key management, and applications, a practitioner needs a compact set
of rules for making real decisions, which this section provides as the chapter's actionable conclusion.

The first and most important rule is **do not roll your own cryptography**. Implementing ciphers,
protocols, or even padding from scratch is how subtle, fatal bugs enter systems; use well-maintained,
widely reviewed libraries (such as libsodium, the cloud providers' key-management services, or a
language's vetted standard library) and use their high-level "easy" interfaces, which make the safe
choice the default. The second rule is **prefer authenticated encryption** (AEAD) for confidentiality so
that integrity comes for free; never deploy a mode that provides confidentiality alone. The third is to
choose modern algorithms with adequate parameters, summarized below as sensible defaults for new systems
as of the mid-2020s.

| Need | Recommended default | Avoid |
|---|---|---|
| Symmetric encryption | AES-256-GCM or ChaCha20-Poly1305 (AEAD) | ECB; unauthenticated CBC; DES/3DES; RC4 |
| Hashing | SHA-256, SHA-3, or BLAKE2 | MD5, SHA-1 |
| Password storage | Argon2id (or scrypt/bcrypt) with unique salt | plain or fast-hashed passwords |
| Key exchange | X25519 / ECDHE (ephemeral, forward secret) | static DH; non-ephemeral exchange |
| Public-key encryption/signatures | RSA-3072+ with OAEP/PSS, or Ed25519/ECDSA | textbook RSA; short keys |
| Random values | OS CSPRNG (`secrets`, `getrandom`) | `random`, LCGs, time-seeded RNGs |
| Long-term/quantum exposure | hybrid classical + ML-KEM/ML-DSA | classical-only for decades-long secrets |

Two further disciplines distinguish mature programs. **Crypto-agility** is designing systems so
algorithms can be replaced without re-architecting, which the looming post-quantum migration makes
urgent; hard-coding a single cipher or key size is now considered a design flaw. **Compliance and
validation** matter in regulated environments: standards such as FIPS 140-3 certify cryptographic
modules, and frameworks discussed in later chapters often mandate specific algorithms and key lengths.
Finally, remember that cryptography is a means, not an end. It enforces confidentiality, integrity, and
authentication, but it cannot secure a compromised endpoint, fix a flawed protocol, or compensate for
poor key management. Used correctly, within a system designed with the principles of Chapter 1, it is the
strongest tool we have; used carelessly, it provides a false sense of security that can be worse than
none at all.''')
guidance.setdefault("id", uuid.uuid4().hex[:12])
cells[wi:wi]=[guidance]

for c in cells: c.setdefault("id", uuid.uuid4().hex[:12])
json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="markdown")
codew=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="code")
print(f"chapter02: {len(cells)} cells, {mdw} md words (~{mdw/500:.1f} pg), +{codew} code words, total~{mdw+codew}")
