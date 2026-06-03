import sys; sys.path.insert(0,".build")
from nbbuild import md, code
import pickle
C=[]; A=C.append

A(md(r'''# Chapter 2: Cryptography

> "Cryptography is the essential building block of independence for organizations on the Internet,
> just like armies are the essential building blocks of states." -- Julian Assange, paraphrasing a
> common sentiment in the cypherpunk movement

---

## Learning Objectives

After completing this chapter, you will be able to:

1. Define the goals of cryptography (confidentiality, integrity, authentication, non-repudiation) and
   state Kerckhoffs's principle.
2. Break classical ciphers using frequency analysis and explain why they fail.
3. Explain perfect secrecy and the one-time pad, and why perfect secrecy is impractical at scale.
4. Distinguish true randomness, pseudo-randomness, and cryptographically secure pseudo-randomness, and
   identify the danger of weak generators.
5. Describe symmetric encryption, contrast stream and block ciphers, and explain the AES structure.
6. Compare the block-cipher modes of operation (ECB, CBC, CFB, OFB, CTR, GCM) and justify why ECB is
   insecure.
7. Explain cryptographic hash functions, their security properties, and constructions such as
   Merkle-Damgard and Merkle trees.
8. Explain message authentication codes (HMAC), authenticated encryption (AEAD), key derivation
   functions, and secure password storage.
9. Describe public-key cryptography: RSA, Diffie-Hellman key exchange, and elliptic-curve cryptography.
10. Explain digital signatures, public-key infrastructure, certificates, and the TLS handshake.
11. Describe advanced and forward-looking topics: homomorphic encryption, functional encryption,
    oblivious computation, steganography, and post-quantum cryptography.

## Key Terms

- **Plaintext / ciphertext**: the readable message and its encrypted form.
- **Cipher**: an algorithm for encryption and decryption.
- **Key**: the secret parameter that controls a cipher's output.
- **Symmetric cryptography**: encryption and decryption use the same shared secret key.
- **Asymmetric (public-key) cryptography**: a mathematically linked key pair, public and private.
- **Kerckhoffs's principle**: a cryptosystem must be secure even if everything except the key is public.
- **Cryptanalysis**: the study of breaking cryptographic systems.
- **Hash function**: a one-way function mapping arbitrary input to a fixed-size digest.
- **MAC**: message authentication code, a keyed tag proving integrity and authenticity.
- **AEAD**: authenticated encryption with associated data; confidentiality plus integrity in one step.
- **KDF**: key derivation function, deriving keys from passwords or other key material.
- **PKI**: public-key infrastructure, the system of certificate authorities and certificates that binds
  public keys to identities.
'''))

A(md(r'''```{admonition} Camp Note: what cryptography really is
:class: note
Imagine passing a note in class. Anyone who intercepts it can read it, unless you and your friend
agreed in advance on a secret way to scramble the letters. Cryptography is the mathematics of doing
this so well that even someone with a supercomputer and the full description of your scrambling method,
but not your secret key, cannot read the note. The rest of this chapter turns that intuition into
precise, testable guarantees.
```

## 2.1 What Cryptography Is and What It Promises

Cryptography is the science of securing communication and data in the presence of adversaries. It is
the mathematical engine beneath nearly every security control in this book: it is how a website proves
its identity, how a password is stored safely, how a software update is shown to be authentic, and how
a messaging app keeps conversations private. The word comes from the Greek for "hidden writing," but
modern cryptography reaches far beyond secrecy. It provides four distinct services, and keeping them
separate in your mind is essential.

**Confidentiality** ensures that only authorized parties can read a message; this is encryption in the
everyday sense. **Integrity** ensures that a message has not been altered, so the recipient can detect
tampering. **Authentication** ensures that a message genuinely comes from its claimed sender.
**Non-repudiation** ensures that a sender cannot later deny having sent a message, a stronger property
that requires public-key signatures. A single protocol often combines several of these; for example,
when you log in to a bank, TLS provides confidentiality and integrity for the connection and
authenticates the server to you.

A foundational rule governs all serious cryptography: **Kerckhoffs's principle**, which states that a
cryptosystem should remain secure even if everything about the system, except the secret key, is public
knowledge. The modern restatement, attributed to Claude Shannon, is to assume "the enemy knows the
system." This is why reputable cryptographic algorithms are published, standardized, and subjected to
years of public analysis rather than kept secret. Security that depends on hiding the algorithm,
disparagingly called *security through obscurity*, fails the moment the algorithm leaks or is reverse
engineered, and history is littered with such failures. When you design or select cryptography, trust
only algorithms that have survived sustained public scrutiny, and never invent your own cipher for
production use.

It is equally important to know cryptography's limits. Encryption protects data, not the endpoints:
if an attacker controls your device, the strongest cipher will not save you, because the plaintext is
right there. Cryptography also cannot fix a bad protocol around it, cannot compensate for a weak or
leaked key, and is frequently undone not by breaking the mathematics but by implementation mistakes:
predictable randomness, reused keys, timing side channels, and downgrade attacks. Throughout this
chapter, watch how often the *system* fails even when the *algorithm* is sound.
'''))

A(md(r'''## 2.2 Classical Ciphers and Why They Fall

The history of cryptography before the twentieth century is, in effect, a long demonstration of why
intuition is a poor guide to security. Studying classical ciphers is valuable not for their practical
use, which is nil, but because breaking them teaches the analytical habits of the cryptanalyst.

The simplest is the **Caesar cipher**, named for Julius Caesar, which shifts each letter a fixed number
of positions through the alphabet. With a shift of three, A becomes D, B becomes E, and so on. The key
is just the shift amount, of which there are only 25 useful values, so an attacker can simply try all
of them, a *brute-force* attack, and read the one result that makes sense. A cipher whose entire
keyspace can be searched in moments offers no security.

A **monoalphabetic substitution cipher** generalizes this by mapping each letter to an arbitrary other
letter, giving a keyspace of 26 factorial, about 2 to the 88th power, far too large to brute force.
Yet these ciphers fall easily to **frequency analysis**, first described by the ninth-century scholar
al-Kindi. The insight is that a substitution cipher hides *which* letter each symbol represents but
preserves *how often* each appears. Because the letter E is the most common in English, the most
frequent ciphertext symbol very likely represents E, and so on down the distribution, supplemented by
common digrams (TH, ER) and word patterns. The structure of the language leaks straight through the
encryption.

The **Vigenere cipher** attempts to defeat frequency analysis by using a repeating keyword to apply
different Caesar shifts to successive letters, flattening the frequency distribution. It resisted
analysis for centuries and was called *le chiffre indechiffrable*, the indecipherable cipher. But it
too falls: once the key length is found (by the Kasiski examination or by index-of-coincidence
methods), the ciphertext splits into separate Caesar ciphers, each broken by frequency analysis. The
deep lesson, which the one-time pad in the next section makes precise, is that a *short, repeating* key
cannot securely encrypt a *long* message, because the repetition reintroduces exploitable structure.

The code cell below provides tools to experiment with the Caesar cipher and frequency analysis. Try the
challenge ciphertexts and observe how quickly structure betrays the key.
'''))

A(code(r'''# Chapter 2 -- Classical ciphers and frequency analysis (self-contained)
from collections import Counter
import string

def caesar(text, shift):
    out = []
    for ch in text:
        if ch.isupper():
            out.append(chr((ord(ch) - 65 + shift) % 26 + 65))
        elif ch.islower():
            out.append(chr((ord(ch) - 97 + shift) % 26 + 97))
        else:
            out.append(ch)
    return "".join(out)

def caesar_bruteforce(cipher):
    print("All 26 Caesar shifts (look for readable English):")
    for s in range(26):
        print(f"  shift {s:2d}: {caesar(cipher, -s)[:60]}")

def letter_frequency(text):
    letters = [c.lower() for c in text if c.isalpha()]
    n = len(letters)
    freq = Counter(letters)
    print(f"Letter frequencies over {n} letters (English E~12.7%, T~9.1%, A~8.2%):")
    for ch, cnt in freq.most_common(8):
        print(f"  {ch}: {cnt:4d}  ({100*cnt/n:5.1f}%)")

# Demonstration
msg = "The quick brown fox jumps over the lazy dog near the old stone bridge."
ct = caesar(msg, 3)
print("Plaintext :", msg)
print("Caesar(+3):", ct)
print()
caesar_bruteforce("Wkh txlfn eurzq ira")
print()
# Frequency analysis on a longer substitution sample
sample = caesar(msg * 3, 7)   # stand-in for a monoalphabetic ciphertext
letter_frequency(sample)
print("\\nChallenge: cipher = 'Ro)x~)|ynwm)vx{n)xw)lxoonn)}qjw)xw)R])|nl~{r}5'  (try non-26 shifts)")''' ))

print("part A:", len(C), "cells")
pickle.dump(C, open(".build/_ch02_cells.pkl","wb"))
