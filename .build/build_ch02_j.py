import sys, json; sys.path.insert(0,".build")
path="chapters/02_cryptography/chapter02.ipynb"
nb=json.load(open(path)); cells=nb["cells"]
def find(prefix):
    for i,c in enumerate(cells):
        if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith(prefix):
            return i
    return None
def append_to(prefix, text):
    i=find(prefix); cells[i]["source"]=(("".join(cells[i]["source"])).rstrip()+text+"\n").splitlines(keepends=True)

append_to("## 2.3", r'''

```{admonition} Going Deeper (graduate/research): the semantic-security game
:class: tip
Computational security is defined through *games* between a challenger and an adversary. In the
indistinguishability under chosen-plaintext attack (IND-CPA) game, the adversary may encrypt arbitrary
messages, then submits two equal-length messages m0 and m1; the challenger secretly flips a bit b and
returns the encryption of m_b; the adversary, still able to request more encryptions, must guess b. The
scheme is IND-CPA secure if no efficient adversary guesses correctly with probability more than
negligibly above one-half. This formalism explains several earlier points at once. It is why encryption
must be *randomized* or nonce-based: a deterministic scheme loses the game instantly, because the
adversary just encrypts m0 and m1 and compares. It is why ECB fails: identical blocks are
distinguishable. And it scales up to IND-CCA, where the adversary also gets a decryption oracle, the
model that authenticated encryption is built to satisfy. Reasoning in terms of what an adversary can
*distinguish*, rather than merely what they can *read*, is the conceptual leap that separates modern
provable-security cryptography from its classical predecessors, and it is the foundation on which Boneh
and Shoup, and Katz and Lindell, build their treatments.
```''')

append_to("## 2.8", r'''

A subtle but important question is *composition order* when building authenticated encryption from
separate encryption and MAC primitives, a topic that has caused real vulnerabilities. There are three
options: Encrypt-and-MAC (MAC the plaintext, used by SSH), MAC-then-Encrypt (MAC the plaintext, then
encrypt both, used by older TLS), and Encrypt-then-MAC (encrypt, then MAC the ciphertext, used by IPsec).
Cryptographers showed that only **Encrypt-then-MAC** is generically secure, because it lets the receiver
verify integrity *before* doing any decryption, so malformed ciphertexts are rejected without ever
exposing decryption behavior to the attacker, which is exactly what defeats padding-oracle attacks. This
is one more reason to prefer a vetted AEAD construction that gets the composition right internally rather
than assembling encryption and MAC by hand. It also illustrates a meta-lesson of the chapter: the
*details of how primitives are combined* are themselves security-critical, not mere engineering trivia.''')

append_to("## 2.16", r'''

For the highest-value keys, organizations apply two further controls worth knowing by name. **Split
knowledge** divides a key (or the secret that protects it) so that no single person holds the whole
thing; reconstructing it requires several authorized people to combine their parts, which prevents any
lone insider from misusing it. The formal mechanism is **secret sharing**, most famously Shamir's
scheme, which splits a secret into n shares such that any threshold t of them reconstructs it but any
fewer reveal nothing, often described as M-of-N control. **Dual control** similarly requires two
authorized operators to act together for sensitive key operations, the cryptographic analog of the
two-person rule for launching weapons. These controls trade some convenience for strong protection
against insider compromise and accidental loss, and they appear directly in standards governing payment
systems and certificate authorities, connecting this section to the governance and compliance material
later in the book.''')

append_to("## 2.9", r'''

Two refinements deserve mention because they appear in practice and on examinations. A **pepper** is a
secret value added to the password before hashing, like a salt but kept *separate* from the database
(for example in application configuration or an HSM), so that a database breach alone does not give the
attacker everything needed to start cracking. Unlike salts, a pepper is shared across users and must
remain secret. The second is breach response: when a password database is exposed, the correct reaction
depends on how it was stored. If passwords were stored with a strong salted, memory-hard KDF, attackers
still face enormous cost per guess, buying defenders time to force resets; if they were stored with a
fast hash or, worse, in plaintext, the credentials must be considered immediately compromised, including
everywhere users reused them, which is why *credential stuffing* (replaying leaked passwords against
other sites) is among the most common real-world attacks. These practices link cryptographic storage to
the incident-response and identity-management chapters, where the organizational response to credential
exposure is developed in full.''')

json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="markdown")
codew=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="code")
print(f"chapter02: {len(cells)} cells, {mdw} md words (~{mdw/500:.1f} pg), +{codew} code, total~{mdw+codew}")
