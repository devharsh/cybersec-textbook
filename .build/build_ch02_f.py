import sys, pickle; sys.path.insert(0,".build")
from nbbuild import md, code, write_nb
C=pickle.load(open(".build/_ch02_cells.pkl","rb")); A=C.append

A(md(r'''## 2.15 Advanced and Emerging Cryptography

The cryptography above secures today's internet. A frontier of more powerful constructions is moving
from theory into practice, enabling computation on data that stays encrypted, and preparing for a future
in which quantum computers threaten the classical assumptions. This section surveys these topics at a
level that orients the reader; Chapter 17 develops their security implications further.

**Homomorphic encryption (HE)** allows computation directly on ciphertext, so that decrypting the result
yields the same answer as if the computation had been performed on the plaintext. *Partially* homomorphic
schemes support one operation indefinitely (textbook RSA is multiplicatively homomorphic, and the
Paillier cryptosystem is additively homomorphic, a property you can observe by adding ciphertexts).
*Fully homomorphic encryption (FHE)*, first realized by Craig Gentry in 2009, supports arbitrary
computation; it remains costly but is advancing rapidly and promises privacy-preserving cloud computing,
where a server processes your data without ever seeing it. **Functional encryption** generalizes
public-key encryption so that a specially issued key reveals only a specific *function* of the
plaintext (for example, only whether an encrypted record matches a query) and nothing more, with
attribute-based and identity-based encryption as important special cases.

**Oblivious computation** is a family of techniques for computing on data while hiding access patterns or
inputs. *Secure multi-party computation (MPC)* lets several parties jointly compute a function of their
private inputs while learning only the output, the classic illustration being two millionaires who learn
who is richer without revealing their wealth. *Oblivious transfer (OT)* is a primitive in which a receiver
obtains one of several items from a sender without the sender learning which, and it is a building block
for MPC. *Oblivious RAM (ORAM)* hides which memory locations a program accesses, defeating attacks that
infer secrets from access patterns, and *private information retrieval (PIR)* lets a user query a database
without revealing the query. *Zero-knowledge proofs*, in which one party proves a statement is true while
revealing nothing beyond its truth, are closely related and now central to privacy-preserving
blockchains.

**Steganography** differs in kind from all of the above: rather than making a message unreadable, it hides
the very *existence* of the message, for example by embedding data in the least-significant bits of an
image or audio file, where the change is imperceptible. Cryptography and steganography are complementary;
encrypting a message before hiding it provides both secrecy and concealment. Steganography is also a
defensive concern, since malware uses it for covert command-and-control and data exfiltration, a theme
revisited in the forensics and malware chapters. The small code cell demonstrates least-significant-bit
image steganography and additive homomorphism.

```{admonition} Going Deeper (graduate/research): the quantum threat and post-quantum cryptography
:class: tip
Large-scale quantum computers would break much of today's public-key cryptography. *Shor's algorithm*
solves integer factoring and discrete logarithms in polynomial time, which would defeat RSA, classical
Diffie-Hellman, and elliptic-curve cryptography entirely. *Grover's algorithm* gives only a quadratic
speedup against symmetric primitives, so doubling key and hash sizes (AES-256, SHA-384) restores their
security. The defensive response is **post-quantum cryptography (PQC)**: public-key algorithms based on
problems believed hard even for quantum computers, principally *lattice* problems, but also hash-based,
code-based, and multivariate constructions. In 2024 NIST standardized the first PQC algorithms,
including ML-KEM (the lattice-based key-encapsulation mechanism derived from CRYSTALS-Kyber), ML-DSA
(derived from CRYSTALS-Dilithium), and the hash-based signature SLH-DSA (derived from SPHINCS+). A
pressing operational concern is the *harvest-now, decrypt-later* attack, in which adversaries record
encrypted traffic today to decrypt once quantum computers mature, which makes migrating long-lived
secrets to PQC, often via *hybrid* classical-plus-PQC schemes, an urgent rather than hypothetical task.
```
'''))

A(code(r'''# Chapter 2 -- LSB image steganography and additive homomorphism (self-contained)
import numpy as np

# --- Least-significant-bit steganography ---
def hide(cover, message):
    bits = "".join(f"{b:08b}" for b in message.encode()) + "00000000"  # null terminator
    flat = cover.flatten().copy()
    for i, bit in enumerate(bits):
        flat[i] = (flat[i] & 0xFE) | int(bit)     # overwrite the least significant bit
    return flat.reshape(cover.shape)

def reveal(stego):
    flat = stego.flatten()
    bits, out = "", []
    for v in flat:
        bits += str(v & 1)
        if len(bits) == 8:
            if bits == "00000000": break
            out.append(int(bits, 2)); bits = ""
    return bytes(out).decode(errors="ignore")

cover = np.random.randint(0, 256, (64, 64), dtype=np.uint8)
stego = hide(cover, "meet at noon")
print("Hidden message recovered:", repr(reveal(stego)))
print("Max pixel change:", int(np.abs(cover.astype(int) - stego.astype(int)).max()), "(imperceptible)\\n")

# --- Additive homomorphism (toy Paillier-style intuition with simple modular adds) ---
# Demonstrate that some encryptions let you add underneath encryption.
# Here: textbook RSA is *multiplicatively* homomorphic: E(a)*E(b) = E(a*b)
def egcd(a,b):
    return (a,1,0) if b==0 else (lambda g,x,y:(g,y,x-(a//b)*y))(*egcd(b,a%b))
n, e = 3233, 17    # toy RSA modulus (61*53)
Ea, Eb = pow(7,e,n), pow(3,e,n)
print("E(7)*E(3) mod n decrypts to 7*3 = 21 ->", (Ea*Eb) % n, "is E(21); homomorphic property holds")''' ))

A(md(r'''## Why This Matters

Cryptography is the load-bearing wall of digital security. Every other chapter leans on it: secure
networking is TLS, secure authentication stores password hashes and verifies signatures, blockchains are
hash chains and signatures, and privacy engineering increasingly relies on the advanced primitives in
Section 2.15. Just as important is knowing cryptography's failure modes, weak randomness, key and nonce
reuse, broken hashes, missing authentication, padding oracles, downgrade attacks, because in practice
systems are almost never broken by defeating AES or RSA head-on; they are broken at the seams, where the
mathematics meets fallible engineering. A practitioner who understands both the guarantees and their
preconditions can choose, configure, and audit cryptographic systems correctly, which is exactly what
certifications from Security+ through CISSP test, and what real adversaries probe.
'''))

A(md(r'''## News in Focus: Heartbleed (2014)

In April 2014, researchers disclosed **Heartbleed**, a vulnerability in the widely used OpenSSL library
(tracked as CVE-2014-0160). The flaw was not in any cryptographic algorithm but in a memory-handling bug
in OpenSSL's implementation of the TLS heartbeat extension: a missing bounds check let an attacker request
more data than they had supplied, causing the server to return up to 64 kilobytes of adjacent memory per
request. That memory could contain private keys, session cookies, usernames, and passwords, and the
attack left no trace in normal logs.

Through this chapter's lens, Heartbleed is a textbook example of the gap between sound algorithms and
fragile implementations. TLS, RSA, and the ciphers involved were all secure; the breach came from a
buffer over-read in C code, the kind of memory-safety failure examined in the exploitation chapter. The
response illustrates cryptographic operations under stress: affected organizations had to patch OpenSSL,
*revoke and reissue* TLS certificates because private keys might have leaked, and force password resets at
scale, exactly the PKI revocation machinery described in Section 2.13. The episode also accelerated
interest in memory-safe languages and in funding for critical open-source infrastructure. These details
reflect public reporting from the time and may be refined by later analysis.
'''))

A(md(r'''## Review Questions

**Q1.** Kerckhoffs's principle states that a cryptosystem should be secure even if:
A. The key is short  B. Everything except the key is public  C. The algorithm is secret  D. No one attacks it

**Q2.** The one-time pad achieves perfect secrecy only if the key is:
A. 128 bits  B. Reused for efficiency  C. Truly random, secret, and as long as the message  D. A strong password

**Q3.** Why is ECB mode insecure for most data?
A. It is too slow  B. Identical plaintext blocks yield identical ciphertext blocks  C. It needs no key  D. It cannot decrypt

**Q4.** Which generator is safe for cryptographic keys?
A. A linear congruential generator  B. Python's default `random`  C. The Mersenne Twister  D. A CSPRNG such as `secrets`/os.urandom

**Q5.** The birthday paradox implies that finding a collision in an n-bit hash takes about:
A. 2^n work  B. 2^(n/2) work  C. n work  D. n^2 work

**Q6.** HMAC is preferred over `hash(key || message)` because the latter is vulnerable to:
A. Brute force  B. Length-extension attacks  C. Birthday attacks  D. Padding oracles

**Q7.** AES-GCM provides, beyond confidentiality:
A. Nothing extra  B. Compression  C. Integrity and authentication (AEAD)  D. Key exchange

**Q8.** RSA's security primarily rests on the hardness of:
A. Discrete logarithms  B. Factoring large integers  C. The elliptic-curve discrete log  D. Hashing

**Q9.** Forward secrecy ensures that:
A. Keys never expire  B. Past sessions stay secret even if the long-term key is later stolen
C. The future is encrypted  D. Certificates never need revocation

**Q10.** A 256-bit elliptic-curve key offers security roughly comparable to an RSA key of:
A. 256 bits  B. 512 bits  C. 1024 bits  D. 3072 bits

**Q11.** Which property is unique to digital signatures (versus a MAC)?
A. Integrity  B. Authentication  C. Non-repudiation  D. Confidentiality

**Q12.** For storing user passwords, the best practice is:
A. Plain SHA-256  B. Reversible encryption  C. A salted, memory-hard KDF such as Argon2id  D. Base64 encoding

**Q13.** In a TLS 1.3 handshake, the shared session keys are derived using:
A. ECB  B. (EC)DHE key exchange fed into HKDF  C. The server password  D. MD5

**Q14.** Shor's algorithm, on a large quantum computer, would break:
A. AES-256  B. SHA-3  C. RSA and elliptic-curve cryptography  D. Argon2

**Q15.** Steganography differs from encryption in that it:
A. Uses larger keys  B. Hides the existence of the message rather than its content
C. Is always unbreakable  D. Requires a certificate authority

**Q16.** Reusing a nonce with the same key in AES-GCM can:
A. Improve speed safely  B. Leak plaintext relationships and enable forgeries  C. Strengthen the key  D. Do nothing

---

### Answer Key

1: B 2: C 3: B 4: D 5: B 6: B 7: C 8: B 9: B 10: D 11: C 12: C 13: B 14: C 15: B 16: B
'''))

A(md(r'''## Hands-on Labs

**Lab 2.1 (beginner) - Break a cipher.** Use the Section 2.2 code to brute-force the Caesar challenge
strings, then take a longer monoalphabetic ciphertext and break it with frequency analysis. Write a short
explanation of which language features made the break possible.

**Lab 2.2 (beginner/intermediate) - Randomness matters.** Generate 1000 values from the toy LCG and from
`secrets`. Plot histograms and successive-pair scatter plots of each. Identify visible structure in the
LCG output and explain why it disqualifies the LCG for key generation.

**Lab 2.3 (intermediate) - Modes and integrity.** Encrypt the same image in ECB and CBC using the
Section 2.6 code and compare. Then flip one byte of a CBC ciphertext, decrypt, and observe the result;
repeat with AES-GCM and show that decryption fails (tamper detected). Explain the difference.

**Lab 2.4 (intermediate) - Password cracking economics.** Hash a small list of weak passwords with plain
SHA-256 and time how many guesses per second you can check; then do the same with PBKDF2 at 200,000
iterations and with Argon2id. Estimate how key stretching changes an attacker's cost per cracked password.

**Lab 2.5 (advanced/research) - Build a mini-PKI and a homomorphic tally.** (a) Create a self-signed root
CA, issue a server certificate, and validate the chain with a library. (b) Implement an additively
homomorphic voting tally using the Paillier cryptosystem (via a library): encrypt individual votes, sum
the ciphertexts, and decrypt only the total, confirming individual votes are never revealed. Discuss the
threat model and what the scheme does and does not protect.
'''))

A(md(r'''## References

1. Shannon, C. E. "Communication Theory of Secrecy Systems." *Bell System Technical Journal*, 28(4), 1949.
2. Diffie, W., and Hellman, M. "New Directions in Cryptography." *IEEE Transactions on Information
   Theory*, 22(6), 1976.
3. Rivest, R., Shamir, A., and Adleman, L. "A Method for Obtaining Digital Signatures and Public-Key
   Cryptosystems." *Communications of the ACM*, 21(2), 1978.
4. Nakov, S. *Practical Cryptography for Developers.* https://cryptobook.nakov.com
5. Boneh, D., and Shoup, V. *A Graduate Course in Applied Cryptography.* https://crypto.stanford.edu/~dabo/cryptobook/
6. Katz, J., and Lindell, Y. *Introduction to Modern Cryptography*, 3rd ed. CRC Press, 2020.
7. National Institute of Standards and Technology. *FIPS 197: Advanced Encryption Standard (AES)*, 2001.
8. National Institute of Standards and Technology. *FIPS 203 (ML-KEM), FIPS 204 (ML-DSA), FIPS 205
   (SLH-DSA): Post-Quantum Cryptography Standards*, 2024.
9. Gentry, C. "Fully Homomorphic Encryption Using Ideal Lattices." *STOC*, 2009.
10. Rescorla, E. *The Transport Layer Security (TLS) Protocol Version 1.3.* RFC 8446, IETF, 2018.
11. Vaudenay, S. "Security Flaws Induced by CBC Padding." *EUROCRYPT*, 2002.
'''))

import uuid
for c in C: c.setdefault("id", uuid.uuid4().hex[:12])
write_nb("chapters/02_cryptography/chapter02.ipynb", C)
