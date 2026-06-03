import sys, pickle; sys.path.insert(0,".build")
from nbbuild import md, code
C=pickle.load(open(".build/_ch02_cells.pkl","rb")); A=C.append

A(md(r'''## 2.8 Message Authentication Codes and Authenticated Encryption

Encryption hides data but, as we saw, most modes do not detect tampering. **Integrity** and
**authentication** are provided by a **message authentication code (MAC)**: a short tag computed from
the message and a shared secret key. The sender transmits the message and tag; the receiver recomputes
the tag with the same key and accepts only if it matches. Because the attacker lacks the key, they
cannot forge a valid tag for a modified message. A MAC thus proves both that the message is unchanged
(integrity) and that it came from someone holding the key (authentication), though, unlike a signature,
it does not provide non-repudiation, since either party could have produced the tag.

The standard MAC is **HMAC** (hash-based MAC), which wraps a hash function in a specific keyed
construction, `HMAC(K, m) = H((K xor opad) || H((K xor ipad) || m))`. This nested design makes HMAC
secure even when built on a Merkle-Damgard hash, immunizing it against the length-extension attack that
dooms naive `H(K || m)`. HMAC-SHA256 is ubiquitous in APIs, tokens, and protocols.

Combining encryption and a MAC correctly is subtle, and doing it by hand invites mistakes (the order
matters; *encrypt-then-MAC* is the safe composition). The modern solution is **authenticated encryption
with associated data (AEAD)**, which provides confidentiality, integrity, and authentication in a single
primitive, and also authenticates *associated data* (such as packet headers) that must be visible but
unmodified. The two dominant AEAD constructions are **AES-GCM** and **ChaCha20-Poly1305**; both are used
in TLS 1.3. The non-negotiable rule for AEAD is *never reuse a nonce with the same key*: nonce reuse in
GCM not only leaks plaintext relationships but can expose the authentication key itself, enabling
forgeries. When in doubt, prefer a misuse-resistant AEAD or a library that manages nonces for you.

```{admonition} Going Deeper (graduate/research): security definitions
:class: tip
The relevant security notion for authenticated encryption is *indistinguishability under chosen-
ciphertext attack* (IND-CCA) combined with *ciphertext integrity* (INT-CTXT); together these imply
authenticated-encryption security (AE). A scheme that is IND-CPA only (like raw CBC) succumbs to
chosen-ciphertext attacks such as the *padding oracle* attack, where the error behavior of a decryptor
leaks one plaintext byte at a time. The padding-oracle attack (Vaudenay, 2002) broke many real CBC
deployments and is the practical reason the field moved decisively to AEAD. The lesson is definitional:
choosing the right *security goal* (AE/IND-CCA, not merely confidentiality) is as important as choosing
a strong cipher.
```
'''))

A(md(r'''## 2.9 Key Derivation and Password Storage

Two recurring problems require turning weak or raw key material into strong cryptographic keys: deriving
keys from human passwords, and storing passwords for authentication. Both are solved by **key derivation
functions (KDFs)**, but with an important twist.

Passwords are low-entropy: people choose predictable strings, and the space of likely passwords is
small enough to enumerate. If a site stored passwords in plaintext, a database breach would expose them
all; if it stored a fast hash like SHA-256, an attacker with the stolen hashes could try billions of
guesses per second on a GPU and crack most of them, especially with precomputed *rainbow tables*. The
defenses are *salting* and *key stretching*. A **salt** is a unique random value stored alongside each
hash; it ensures identical passwords produce different stored values and defeats precomputed tables.
**Key stretching** deliberately makes the function slow and resource-intensive, so each guess costs the
attacker dearly while remaining tolerable for a single legitimate login.

Password-hashing KDFs implement these ideas. **PBKDF2** applies a hash thousands or millions of times;
it is widely supported but only CPU-hard, so GPUs and custom hardware accelerate attacks. **bcrypt** is
deliberately slow and somewhat memory-using. **scrypt** and, the current best practice, **Argon2** (the
2015 Password Hashing Competition winner) are *memory-hard*: they require large amounts of memory,
which neutralizes the parallelism advantage of GPUs and ASICs. For deriving an encryption key from a
shared secret that is already high-entropy (for instance the output of a key exchange), a fast KDF such
as **HKDF** is appropriate; HKDF is not for passwords. The practical guidance: never store passwords
reversibly or with a plain fast hash; use Argon2id (or scrypt/bcrypt) with a unique salt and tuned cost
parameters. The code cell contrasts an insecure approach with a correct one.
'''))

A(code(r'''# Chapter 2 -- Password storage: the wrong way and a better way
import hashlib, os, hmac

password = "correct horse battery staple"

# WRONG: a single fast hash, no salt -> vulnerable to rainbow tables and fast GPU cracking
bad = hashlib.sha256(password.encode()).hexdigest()
print("INSECURE sha256(pw):", bad)

# BETTER: unique salt + key stretching (PBKDF2 shown for portability; prefer Argon2id in production)
salt = os.urandom(16)
iterations = 200_000
derived = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, iterations)
print("Salt (hex)         :", salt.hex())
print("PBKDF2 derived hash:", derived.hex())

# Verification at login: recompute with the stored salt and compare in constant time
def verify(candidate, salt, iterations, stored):
    test = hashlib.pbkdf2_hmac("sha256", candidate.encode(), salt, iterations)
    return hmac.compare_digest(test, stored)   # constant-time compare avoids timing leaks

print("Login correct pw   :", verify(password, salt, iterations, derived))
print("Login wrong   pw   :", verify("guess", salt, iterations, derived))
print("\\nProduction note: prefer argon2-cffi (Argon2id), which is memory-hard.")''' ))

A(md(r'''## 2.10 Public-Key Cryptography and RSA

Symmetric cryptography has an inescapable bootstrapping problem: the parties must already share a secret
key. In 1976 Whitfield Diffie and Martin Hellman published the idea of **public-key (asymmetric)
cryptography**, which dissolves this problem. Each party holds a mathematically linked *key pair*: a
**public key** that may be freely published, and a **private key** kept secret. Anyone can encrypt a
message with the recipient's public key, but only the holder of the matching private key can decrypt it.
Conversely, the private key can *sign* data in a way that anyone can verify with the public key, giving
authentication and non-repudiation. Public-key cryptography rests on *trapdoor* mathematical problems:
operations easy to perform but infeasible to reverse without secret information.

The first and still most recognizable public-key system is **RSA** (Rivest, Shamir, Adleman, 1977). Its
security rests on the difficulty of *factoring* the product of two large primes. Key generation chooses
two large secret primes p and q, computes the modulus n = p*q and Euler's totient phi = (p-1)(q-1),
selects a public exponent e coprime to phi (commonly 65537), and computes the private exponent d as the
modular inverse of e modulo phi. The public key is (n, e); the private key is d. Encryption of a message
m is c = m^e mod n, and decryption is m = c^d mod n. The correctness follows from Euler's theorem; the
security follows from the belief that recovering d from the public (n, e) requires factoring n, which is
infeasible for sufficiently large n (today at least 2048 bits, with 3072 or more recommended for
long-term use). In practice RSA is never used on raw messages; secure padding (OAEP for encryption, PSS
for signatures) is essential, and "textbook RSA" without padding is insecure. The code cell illustrates
RSA on tiny numbers for understanding, then with a real library.
'''))

A(code(r'''# Chapter 2 -- RSA from first principles (tiny, for learning) and with a real library
# --- Educational toy RSA (DO NOT use small numbers in practice) ---
def egcd(a, b):
    if b == 0: return (a, 1, 0)
    g, x, y = egcd(b, a % b)
    return (g, y, x - (a // b) * y)
def modinv(a, m):
    g, x, _ = egcd(a, m)
    return x % m

p, q = 61, 53
n = p * q
phi = (p - 1) * (q - 1)
e = 17
d = modinv(e, phi)
print(f"p={p} q={q}  n={n}  phi={phi}  e={e}  d={d}")
m = 42
c = pow(m, e, n)            # encryption: c = m^e mod n
m2 = pow(c, d, n)           # decryption: m = c^d mod n
print(f"message={m}  cipher={c}  decrypted={m2}  ok={m==m2}\\n")

# --- Real RSA with OAEP padding and PSS signatures ---
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
priv = rsa.generate_private_key(public_exponent=65537, key_size=2048)
pub = priv.public_key()
msg = b"Public-key cryptography solves key distribution."
ct = pub.encrypt(msg, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),
                                   algorithm=hashes.SHA256(), label=None))
pt = priv.decrypt(ct, padding.OAEP(mgf=padding.MGF1(hashes.SHA256()),
                                   algorithm=hashes.SHA256(), label=None))
print("Decrypted matches original:", pt == msg)
sig = priv.sign(msg, padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                 salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
print("Signature length (bytes):", len(sig), "(verifiable with the public key)")''' ))
print("part D total:", len(C))
pickle.dump(C, open(".build/_ch02_cells.pkl","wb"))
