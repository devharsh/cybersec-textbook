import sys, json, uuid; sys.path.insert(0,".build")
from nbbuild import md
path="chapters/02_cryptography/chapter02.ipynb"
nb=json.load(open(path))
cells=nb["cells"]

def find(prefix):
    for i,c in enumerate(cells):
        if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith(prefix):
            return i
    return None

# 1) Prepend transition bridges to existing section openers (idempotent: skip if already added)
bridges = {
 "## 2.1": "We begin where all of security ultimately bottoms out. Before any firewall or password matters, we need the mathematics that makes secrecy and trust possible at all, so this section defines what cryptography promises and, just as importantly, what it does not.",
 "## 2.2": "With the goals and the ground rule (Kerckhoffs's principle) in hand, the natural way to build intuition is to watch weak systems fail. The classical ciphers below show, concretely, why amateur schemes collapse, and they teach the cryptanalyst's habits we will rely on for the rest of the chapter.",
 "## 2.3": "Breaking classical ciphers raises an obvious question: is unbreakable encryption even possible? Shannon answered yes, and the answer reshapes how we think about every cipher that follows.",
 "## 2.4": "Perfect secrecy depended entirely on one assumption we glossed over, a truly random key. That assumption is so load-bearing, and so often violated in practice, that it deserves a section of its own before we build real ciphers on top of it.",
 "## 2.5": "Armed with secure randomness, we can finally build the practical, scalable ciphers that protect real data. We trade Shannon's perfect secrecy for computational security and gain something invaluable: short keys that encrypt long messages.",
 "## 2.6": "A block cipher by itself only transforms a single block, which is almost never what we need. How we stitch many blocks together, the mode of operation, turns out to matter as much as the cipher, and is where security is most often quietly lost.",
 "## 2.7": "So far we have pursued confidentiality. But security also demands knowing that data has not changed, and that requires a different primitive entirely. Hash functions give us a compact fingerprint of data, the foundation for integrity, signatures, and much more.",
 "## 2.8": "A hash alone proves a message is unchanged only if the digest itself cannot be forged, which fails the moment an attacker can recompute it. Adding a secret key closes that gap and lets us combine integrity with confidentiality.",
 "## 2.9": "Keys and the passwords behind them are only as strong as how we derive and store them. Having built encryption and authentication, we now confront the very human problem of turning weak passwords into strong keys without handing attackers an easy target.",
 "## 2.10": "Everything so far assumed the two parties already shared a secret key, which simply relocates the problem. Public-key cryptography dissolves it, and we start with the system that made the idea concrete.",
 "## 2.11": "RSA lets us encrypt to a public key, but asymmetric operations are slow, so in practice we use them mainly to agree on a fast symmetric key. The most elegant way to do that, over a fully public channel, is the next topic.",
 "## 2.12": "Classical RSA and Diffie-Hellman are secure only with large, costly keys. Elliptic curves deliver the same security far more cheaply, which is why they now dominate new systems and why they deserve their own treatment.",
 "## 2.13": "Public-key encryption and key exchange both assume you know whose public key you hold. Signatures and the trust machinery of PKI are how that assumption is justified at internet scale.",
 "## 2.14": "We have now assembled every primitive separately: key exchange, certificates, signatures, hashing, and authenticated encryption. TLS is where they all come together in the single most important protocol on the internet, so it makes an ideal capstone.",
 "## 2.15": "The cryptography above secures today's systems. The frontier, computing on encrypted data and surviving quantum computers, is moving quickly from theory into deployment, and a practitioner should understand where it is heading.",
}
for pref,text in bridges.items():
    i=find(pref)
    if i is None: continue
    body="".join(cells[i]["source"])
    if text[:40] in body:  # already added
        continue
    # insert bridge as a new paragraph right after the heading line
    lines=body.split("\n")
    # heading is line 0 (## x.y Title); keep any blank line then insert bridge
    head=lines[0]
    rest="\n".join(lines[1:]).lstrip("\n")
    newbody=head+"\n\n"+text+"\n\n"+rest
    cells[i]["source"]=newbody.splitlines(keepends=True)

# 2) Deepen 2.2 (classical) by appending transposition + Enigma paragraph
i=find("## 2.2")
add22=r'''

Beyond substitution lies a second classical family, the **transposition ciphers**, which do not replace
letters but *rearrange* them according to a secret pattern, such as writing the message into a grid by
rows and reading it out by columns (the columnar transposition). Transposition preserves the letter
frequencies of the plaintext, so a frequency count alone looks like normal language; the cryptanalyst
must instead detect anagram structure and probable column orderings. Real historical systems often
combined substitution and transposition to frustrate both attacks at once. The most sophisticated
pre-computer machine, the German **Enigma** of the Second World War, used rotating wired rotors to
create a polyalphabetic substitution that changed with every keypress, yielding an astronomically large
key space. It was nonetheless broken by Allied cryptanalysts at Bletchley Park, led by Marian Rejewski's
earlier Polish work and by Alan Turing, who exploited operational mistakes, predictable message
formats, and the machine's one structural flaw (a letter never encrypted to itself) using
electromechanical "bombes." Enigma's defeat is the historical bridge to the computer age and a permanent
reminder that procedural and implementation errors, not just weak algorithms, decide real outcomes.'''
cells[i]["source"]=(("".join(cells[i]["source"])).rstrip()+add22+"\n").splitlines(keepends=True)

# 3) Deepen 2.5 (symmetric) with Feistel/DES/3DES paragraph
i=find("## 2.5")
add25=r'''

It is worth understanding the structure AES replaced, because it still appears in legacy systems and in
exam questions. The **Data Encryption Standard (DES)**, standardized in 1977, is built on a **Feistel
network**, a design that splits each block in half and, over sixteen rounds, repeatedly mixes one half
into the other using a round function and round keys. The Feistel structure has an elegant property: the
same circuitry performs encryption and decryption simply by reversing the order of round keys, which
made hardware cheap. DES's fatal weakness was not its design but its **56-bit key**, far too small;
by the late 1990s purpose-built machines and distributed efforts brute-forced DES keys in days, then
hours. The stop-gap **Triple DES (3DES)** applied DES three times with multiple keys to enlarge the
effective key length, but it is slow, has a small 64-bit block that invites birthday-bound attacks on
large data volumes (the Sweet32 attack), and is now deprecated. AES, a substitution-permutation network
rather than a Feistel cipher, with 128-bit blocks and 128- to 256-bit keys, resolved all of these
issues and is the symmetric standard today. The lesson for selecting cryptography is concrete: key
length and block size are not academic parameters but the difference between secure and broken.'''
cells[i]["source"]=(("".join(cells[i]["source"])).rstrip()+add25+"\n").splitlines(keepends=True)

# 4) Insert two new sections (2.16 Key Management, 2.17 Attack taxonomy) before "## Why This Matters"
wi=find("## Why This Matters")
keymgmt=md(r'''## 2.16 Key Management

If the previous sections taught how algorithms work, this one addresses the problem that breaks more
real systems than any algorithmic weakness: managing the keys those algorithms depend on. A cipher is
only as strong as the secrecy and integrity of its keys, and the unglamorous discipline of *key
management* spans the entire lifecycle of a key, generation, distribution, storage, use, rotation,
revocation, and destruction.

**Generation** must use a CSPRNG with adequate entropy, as Section 2.4 stressed; a key guessable
because of weak randomness is no key at all. **Distribution** is the classic problem that public-key
cryptography and key-exchange protocols solve, but symmetric keys shared out of band must travel over an
already-secure channel. **Storage** is where keys most often leak: hard-coding keys in source code,
committing them to version control, or leaving them in configuration files and environment variables has
exposed countless organizations. The defenses are dedicated **key vaults** and, for the highest
assurance, **hardware security modules (HSMs)**, tamper-resistant devices that generate and use keys
internally so the private key never leaves the hardware in plaintext. On endpoints, a **Trusted Platform
Module (TPM)** plays an analogous role, anchoring disk-encryption and platform-integrity keys in
hardware.

**Use** should honor *key separation* (a key serves one purpose, for example never reusing an
encryption key as a signing key) and *cryptoperiods* (limits on how much data or time a key covers).
**Rotation** periodically replaces keys to limit the damage of an undetected compromise and to bound the
data encrypted under any single key. **Revocation** invalidates keys and certificates known or suspected
to be compromised, the PKI machinery of Section 2.13. Finally, **destruction** ensures retired keys
cannot be recovered, which is also the basis of *crypto-shredding*: deliberately destroying the key to
render encrypted data permanently unreadable, a powerful tool for data disposal and the right to
erasure. A related governance question is **key escrow**, storing a copy of keys with a trusted third
party so data can be recovered (or lawfully accessed); escrow improves recoverability but creates a
high-value target and civil-liberties concerns, a tension explored further in the privacy and law
chapter. Mature organizations formalize all of this in a key-management policy and increasingly automate
it through key-management services, because manual key handling does not scale and does not survive
employee turnover.''')

attacks=md(r'''## 2.17 A Taxonomy of Cryptographic Attacks

Having seen how cryptography is built, we close the technical material by cataloguing how it is broken,
because choosing and configuring cryptography well means anticipating the adversary. CISSP's Domain 3
tests exactly this vocabulary, and the categories below recur throughout the book.

Attacks divide first by what the adversary can access. In a **ciphertext-only** attack the adversary
sees only ciphertext; in a **known-plaintext** attack they have some plaintext-ciphertext pairs; in a
**chosen-plaintext** attack (CPA) they can encrypt messages of their choosing; and in a
**chosen-ciphertext** attack (CCA) they can submit ciphertexts for decryption and observe the result.
Modern schemes are designed to resist the strongest of these, which is why IND-CPA and IND-CCA are the
benchmark security goals introduced earlier.

A second family targets the mathematics or the key. **Brute-force** attacks try every key and are
defeated only by sufficient key length. **Birthday attacks** exploit the square-root collision bound to
forge hashes or MACs with shorter digests. **Mathematical** attacks attempt to solve the underlying hard
problem more cleverly (improved factoring or discrete-log algorithms), and quantum algorithms, discussed
in Section 2.15, are the extreme case. **Frequency analysis**, from Section 2.2, is the classical
ancestor of all statistical attacks.

The most important family in practice attacks the *implementation* rather than the algorithm.
**Side-channel** attacks extract secrets from physical leakage, timing, power consumption, electromagnetic
emissions, or even sound, and timing attacks in particular have repeatedly recovered keys from naive
code, which is why constant-time implementations and constant-time comparisons matter. **Fault-injection**
attacks deliberately induce hardware errors to expose keys. **Padding-oracle** attacks (Section 2.8) turn
a decryptor's error behavior into a plaintext leak. **Replay** attacks resend captured valid messages,
defeated by nonces and timestamps. **Downgrade** attacks trick parties into negotiating weaker, breakable
parameters, the reason protocols must refuse obsolete ciphers. And the **man-in-the-middle** attack,
which plain Diffie-Hellman invites, is defeated only by authentication. The unifying insight, repeated
deliberately throughout this chapter, is that strong algorithms are necessary but never sufficient:
security is a property of the whole system, including its randomness, its key management, its protocol
design, and the code that implements it.''')

for c in (keymgmt, attacks):
    c.setdefault("id", uuid.uuid4().hex[:12])
cells[wi:wi]=[keymgmt, attacks]

# 5) add a closing forward link to the last reference/summary-ish: append forward sentence to 2.17? Better: add to Why This Matters end.
wi=find("## Why This Matters")
fwd="\n\nWith the mathematical foundations of security in place, the next chapter turns to the networks "\
    "over which all of this cryptography travels: how data moves, how the protocols work, and how both "\
    "are attacked and defended."
cells[wi]["source"]=(("".join(cells[wi]["source"])).rstrip()+fwd+"\n").splitlines(keepends=True)

for c in cells: c.setdefault("id", uuid.uuid4().hex[:12])
json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="markdown")
print(f"chapter02: {len(cells)} cells, {mdw} md words (~{mdw/500:.1f} pages)")
