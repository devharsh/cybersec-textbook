import sys, pickle; sys.path.insert(0,".build")
from nbbuild import md, code
C=pickle.load(open(".build/_ch02_cells.pkl","rb")); A=C.append

A(md(r'''## 2.6 Block Cipher Modes of Operation

A block cipher encrypts exactly one block. A *mode of operation* specifies how to use the cipher
repeatedly to encrypt a message longer than one block, and this seemingly mechanical choice has
enormous security consequences.

The naive approach is **Electronic Codebook (ECB)** mode: split the plaintext into blocks and encrypt
each independently with the same key. ECB is simple and parallelizable, and it is also broken, because
identical plaintext blocks produce identical ciphertext blocks. The result leaks the structure of the
data. The famous demonstration encrypts a bitmap image of the Linux penguin in ECB mode: the outline
of the penguin remains plainly visible in the ciphertext, because regions of identical color encrypt to
identical patterns. **Never use ECB for data with any structure**, which is essentially all real data.

Secure modes break this pattern by chaining or randomizing each block. **Cipher Block Chaining (CBC)**
XORs each plaintext block with the previous ciphertext block before encrypting, and uses a random
*initialization vector (IV)* for the first block, so identical plaintexts encrypt differently each
time. CBC requires padding and is sequential for encryption. **Cipher Feedback (CFB)** and **Output
Feedback (OFB)** turn a block cipher into a stream cipher. **Counter (CTR)** mode encrypts an
incrementing counter to produce a keystream that is XORed with the plaintext; it is parallelizable,
needs no padding, and is widely preferred, but it is fatally insecure if a counter/nonce value is ever
reused with the same key.

Crucially, all of the modes above provide *confidentiality only*. They do not detect tampering: an
attacker can flip bits in the ciphertext and cause predictable changes in the decrypted plaintext. This
gap is closed by **Galois/Counter Mode (GCM)**, an *authenticated encryption* mode that combines CTR-mode
confidentiality with a built-in authentication tag, so any modification is detected on decryption.
AES-GCM and the stream-cipher construction ChaCha20-Poly1305 are the modern defaults; they belong to
the AEAD family discussed in Section 2.8. The code cell below makes ECB's failure visible by encrypting
a simple patterned image in ECB and CBC modes.
'''))

A(code(r'''# Chapter 2 -- ECB vs CBC: why ECB leaks structure (self-contained)
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

# Build a simple structured image (large blocks of constant color)
H = W = 128
img = np.zeros((H, W), dtype=np.uint8)
img[20:108, 20:60] = 200          # a bright rectangle
img[40:90, 70:108] = 120          # a mid-gray rectangle
raw = img.tobytes()

key, iv = os.urandom(16), os.urandom(16)

def aes_encrypt(data, mode):
    padder = padding.PKCS7(128).padder()
    padded = padder.update(data) + padder.finalize()
    enc = Cipher(algorithms.AES(key), mode).encryptor()
    return enc.update(padded) + enc.finalize()

ecb = aes_encrypt(raw, modes.ECB())[:H*W]
cbc = aes_encrypt(raw, modes.CBC(iv))[:H*W]
ecb_img = np.frombuffer(ecb, dtype=np.uint8).reshape(H, W)
cbc_img = np.frombuffer(cbc, dtype=np.uint8).reshape(H, W)

fig, ax = plt.subplots(1, 3, figsize=(11, 4))
for a, im, t in zip(ax, [img, ecb_img, cbc_img],
                    ["Original", "AES-ECB (structure leaks!)", "AES-CBC (looks random)"]):
    a.imshow(im, cmap="gray"); a.set_title(t); a.axis("off")
plt.tight_layout(); plt.savefig("ch02_ecb_vs_cbc.png", dpi=110)
print("Saved ch02_ecb_vs_cbc.png")
print("Note how the ECB ciphertext preserves the rectangles, while CBC does not.")''' ))

A(md(r'''## 2.7 Cryptographic Hash Functions

A **cryptographic hash function** takes an input of any size and produces a fixed-size output called a
*digest* or *hash*. Examples include SHA-256 (a 256-bit digest from the SHA-2 family) and SHA-3.
Hashes are everywhere: they verify file integrity, index data, store passwords (with the extra steps in
Section 2.9), underpin digital signatures, and form the backbone of blockchains. A function suitable for
cryptography must satisfy three security properties.

**Preimage resistance** (one-wayness): given a digest h, it is computationally infeasible to find any
input m such that hash(m) = h. You cannot run the function backward. **Second-preimage resistance**:
given a specific input m1, it is infeasible to find a different input m2 with the same digest.
**Collision resistance**: it is infeasible to find *any* two distinct inputs with the same digest.
Collisions must exist mathematically, because infinitely many inputs map to finitely many digests, but
a good hash makes finding them infeasible. A related requirement is the *avalanche effect*: changing a
single input bit should change roughly half the output bits, so digests of similar inputs look totally
unrelated.

The security of collision resistance is bounded by the **birthday paradox**: because of the
probabilistic ease of finding *some* matching pair, an attacker needs only about 2 to the n/2 work to
find a collision in an n-bit hash, not 2 to the n. This is why a 256-bit hash offers only about 128
bits of collision security, and why digest sizes are chosen generously. History shows the stakes: MD5
and SHA-1 were once standard but are now broken for collision resistance (researchers produced real
SHA-1 collisions in 2017), so neither may be used where collision resistance matters, such as
certificates or signatures. Use SHA-256 or stronger today.

Most classical hashes (MD5, SHA-1, SHA-2) are built with the **Merkle-Damgard construction**, which
processes the message in fixed-size blocks through a compression function. This design has a quirk, the
*length-extension attack*, in which an attacker who knows hash(m) can compute hash(m || extra) without
knowing m, which is why naive `hash(secret || message)` must never be used as a MAC; HMAC (Section 2.8)
fixes this. SHA-3 uses a different *sponge* construction that is immune to length extension. A related
structure, the **Merkle tree**, hashes data in a tree so that any single item can be verified against a
small root hash, a technique central to Git, certificate transparency, and blockchains. The code cell
demonstrates the avalanche effect and a simple integrity check.
'''))

A(code(r'''# Chapter 2 -- Hash functions: avalanche effect and integrity check
import hashlib

def sha256(s): return hashlib.sha256(s.encode()).hexdigest()

a = sha256("The quick brown fox")
b = sha256("The quick brown fox.")   # one extra character
print("SHA-256('...fox') :", a)
print("SHA-256('...fox.'):", b)
# Hamming distance between the two digests (in bits)
xa, xb = int(a,16), int(b,16)
print("Bits changed by a 1-char edit:", bin(xa ^ xb).count("1"), "of 256  (avalanche)\\n")

# Integrity verification: detect tampering
message = "Transfer $100 to Alice"
digest  = sha256(message)
received = "Transfer $900 to Alice"   # attacker altered the amount
print("Stored digest   :", digest)
print("Recomputed match:", sha256(received) == digest, "=> tampering detected")

# Compare digest sizes / algorithms
for algo in ["md5", "sha1", "sha256", "sha3_256"]:
    h = hashlib.new(algo); h.update(b"hello")
    print(f"  {algo:9s} ({h.digest_size*8:3d} bits): {h.hexdigest()[:32]}...")''' ))
print("part C total:", len(C))
pickle.dump(C, open(".build/_ch02_cells.pkl","wb"))
