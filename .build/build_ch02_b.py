import sys, pickle; sys.path.insert(0,".build")
from nbbuild import md, code
C=pickle.load(open(".build/_ch02_cells.pkl","rb")); A=C.append

A(md(r'''## 2.3 Perfect Secrecy and the One-Time Pad

In 1949 Claude Shannon placed cryptography on a rigorous mathematical footing by defining **perfect
secrecy**. A cipher is perfectly secret if observing the ciphertext gives an adversary *no information
whatsoever* about the plaintext, beyond what they knew before. Formally, for every plaintext m and
every ciphertext c, the probability of m given c equals the probability of m: the ciphertext and
plaintext are statistically independent. An adversary with unlimited computing power learns nothing.

Remarkably, perfect secrecy is achievable, by the **one-time pad (OTP)**. The pad is a random key as
long as the message; encryption combines each plaintext bit with the corresponding key bit using
exclusive-or (XOR), and decryption XORs again with the same key. If the key is truly random, used only
once, kept secret, and at least as long as the message, the result is provably unbreakable. The
intuition is that for any observed ciphertext, *every* plaintext of that length is equally possible
under some key, so the ciphertext reveals nothing.

```{admonition} Going Deeper (graduate/research): why OTP is optimal and why we abandon it
:class: tip
Shannon proved a stronger negative result: perfect secrecy *requires* the key space to be at least as
large as the message space, so the key must be at least as long as the message. This is why perfect
secrecy does not scale: to send a gigabyte secretly you must first share a gigabyte of secret key,
which merely relocates the problem. Modern cryptography therefore trades Shannon's *information-theoretic*
security for *computational* security: ciphers like AES are not unbreakable in principle, but breaking
them is believed to require computational effort far beyond any feasible adversary. The formal goal
becomes *semantic security* (equivalently, indistinguishability under chosen-plaintext attack,
IND-CPA): no efficient adversary can distinguish the encryptions of two chosen messages with more than
negligible advantage. Block ciphers in a proper mode, seeded by a short key, approximate the OTP's
guarantee against bounded adversaries while keeping the key small.
```

The one-time pad also illustrates how cryptography fails in practice. The "one-time" requirement is
absolute: if the same pad encrypts two messages, XORing the two ciphertexts cancels the key and leaks
the XOR of the plaintexts, which is often enough to recover both. This exact mistake broke Soviet
traffic in the mid-twentieth century VENONA project, when pad pages were reused. The pattern, *key
reuse destroys security*, recurs throughout cryptography, from the OTP to stream ciphers to the nonce
reuse that breaks modern authenticated encryption.
'''))

A(md(r'''## 2.4 Randomness: True, Pseudo, and Cryptographically Secure

Every cryptographic guarantee in the previous section rested on one phrase: *truly random key*.
Randomness is the silent foundation of cryptography, and weak randomness is one of the most common and
catastrophic real-world failures. We must distinguish three notions.

**True randomness** comes from physical, unpredictable processes: electronic noise, radioactive decay,
or timing jitter. Operating systems gather such *entropy* and expose it (for example through Linux
`/dev/random` and the `getrandom` system call). True entropy is the gold standard but can be slow to
collect.

**Pseudo-randomness** is produced by deterministic algorithms, *pseudo-random number generators*
(PRNGs), that stretch a small seed into a long sequence that looks random by statistical tests. The
classic example is the **linear congruential generator (LCG)**, which computes each value from the
previous one as `x = (a*x + c) mod m`. LCGs are fast and fine for simulations and games, but they are
catastrophically insecure for cryptography: given a few outputs, an attacker can solve for the internal
state and predict all past and future values. General-purpose generators such as the Mersenne Twister
(Python's default `random` module) are likewise predictable and must never be used for keys, tokens, or
nonces.

**Cryptographically secure pseudo-random number generators (CSPRNGs)** are PRNGs with an additional
guarantee: even an adversary who sees a long run of output cannot predict the next bit with advantage
better than chance, and cannot recover the internal state. In Python, `secrets` and
`random.SystemRandom` (backed by `os.urandom`) are CSPRNGs; the plain `random` module is not. The
practical rule is simple and worth memorizing: **for anything security-sensitive, use a CSPRNG**.
Predictable randomness has broken real systems repeatedly, from a 2008 Debian OpenSSL bug that
shrank the key space to a few thousand possibilities, to cryptocurrency wallets drained because their
keys were generated with weak entropy.
'''))

A(code(r'''# Chapter 2 -- Randomness: predictable PRNG vs CSPRNG
import secrets

# A linear congruential generator (predictable!) -- glibc-style constants
class LCG:
    def __init__(self, seed): self.state = seed
    def next(self):
        self.state = (1103515245 * self.state + 12345) & 0x7fffffff
        return self.state

lcg = LCG(seed=42)
outputs = [lcg.next() for _ in range(5)]
print("LCG outputs   :", outputs)
# An attacker who knows the constants reproduces the stream exactly:
attacker = LCG(seed=42)
print("Attacker copy :", [attacker.next() for _ in range(5)])
print("=> A deterministic PRNG with a known/recovered seed is fully predictable.\\n")

# CSPRNG: unpredictable, suitable for keys and tokens
print("Secure 256-bit key   :", secrets.token_hex(32))
print("Secure URL-safe token:", secrets.token_urlsafe(24))
print("Secure dice roll 1-6 :", 1 + secrets.randbelow(6))
print("\\nRule: use `secrets` / os.urandom for keys, nonces, tokens; never `random` for security.")''' ))

A(md(r'''## 2.5 Symmetric Encryption: Stream and Block Ciphers

**Symmetric cryptography** uses a single shared secret key for both encryption and decryption. It is
fast and efficient, making it the workhorse for encrypting bulk data, but it raises the *key
distribution problem*: the two parties must somehow share the secret key over a secure channel before
they can communicate, a problem solved later by public-key methods. Symmetric ciphers come in two
families.

**Stream ciphers** encrypt data one bit or byte at a time by generating a pseudo-random *keystream*
from the key and XORing it with the plaintext, much like a practical approximation of the one-time pad
with a short key. They are fast and well suited to streaming data, but they are fragile: reusing a
keystream is fatal, exactly as with the OTP. Modern stream ciphers such as **ChaCha20** are widely used,
notably in TLS and in mobile devices, and the older RC4 is now deprecated because of fatal biases.

**Block ciphers** encrypt fixed-size blocks of bits at a time, typically 128 bits, transforming a
whole block under the key. The dominant block cipher is the **Advanced Encryption Standard (AES)**,
selected by the U.S. National Institute of Standards and Technology in 2001 (the Rijndael algorithm by
Daemen and Rijmen) to replace the aging Data Encryption Standard (DES). DES had a 56-bit key that
modern hardware brute-forces in hours; AES supports 128, 192, and 256-bit keys and remains secure.

Internally, AES is a *substitution-permutation network* that applies several *rounds* (10, 12, or 14
depending on key size) of four operations to a 4-by-4 byte state: SubBytes (a non-linear byte
substitution through an S-box, providing Shannon's *confusion*), ShiftRows and MixColumns (linear
mixing that spreads each byte's influence across the block, providing *diffusion*), and AddRoundKey
(XOR with a round key derived from the main key by the key schedule). Confusion obscures the
relationship between key and ciphertext; diffusion ensures that changing one plaintext bit changes
about half the ciphertext bits, the *avalanche effect*. You do not need to implement AES, modern CPUs
even have dedicated AES-NI instructions, but you must understand that a block cipher alone only encrypts
one block. To encrypt a real message of many blocks, we need a *mode of operation*, the subject of the
next section, and the choice of mode is where security is most often won or lost.
'''))
print("part B total:", len(C))
pickle.dump(C, open(".build/_ch02_cells.pkl","wb"))
