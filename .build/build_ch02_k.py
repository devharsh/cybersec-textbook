import sys, json; sys.path.insert(0,".build")
path="chapters/02_cryptography/chapter02.ipynb"
nb=json.load(open(path)); cells=nb["cells"]
def find(p):
    for i,c in enumerate(cells):
        if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith(p): return i
def app(p,t):
    i=find(p); cells[i]["source"]=(("".join(cells[i]["source"])).rstrip()+t+"\n").splitlines(keepends=True)

app("## 2.11", r'''

To see why authentication is non-negotiable, trace the man-in-the-middle attack on unauthenticated
Diffie-Hellman concretely. Alice sends A = g^a to Bob, but the attacker Mallory intercepts it and sends
her own M = g^m to Bob; Bob replies with B = g^b, which Mallory again intercepts, sending her own value
back to Alice. Now Alice has unknowingly established a shared secret g^(am) with Mallory, and Bob has
established g^(bm) with Mallory, while each believes they are talking to the other. Mallory sits in the
middle, decrypting, reading, and re-encrypting every message, completely transparent to both parties.
Nothing in the mathematics of Diffie-Hellman detects this, because the protocol guarantees only that two
parties share a secret, not *which* two parties. The fix, used by TLS, SSH, and Signal alike, is to
authenticate the exchange: each side signs its key share, or the keys are bound to certificates or to
pre-verified identities, so Mallory cannot substitute her own values without detection. This is the
single most important practical lesson about key exchange and a frequent source of real vulnerabilities
in custom protocols that "use Diffie-Hellman" but forget to authenticate it.''')

app("## 2.15", r'''

Zero-knowledge proofs deserve a closer look, because they have moved from theoretical curiosity to
deployed technology. A **zero-knowledge proof** lets a *prover* convince a *verifier* that a statement is
true while revealing nothing beyond the fact of its truth, not the underlying secret. The textbook
intuition is the "Ali Baba cave": a prover repeatedly demonstrates they can open a secret door without
ever showing the verifier the password, by emerging from whichever side the verifier randomly demands.
Formally, a zero-knowledge proof must satisfy *completeness* (a true statement is accepted), *soundness*
(a false statement is rejected except with negligible probability), and the *zero-knowledge* property
(the verifier learns nothing they could not have produced alone). Modern *non-interactive* variants,
notably zk-SNARKs and zk-STARKs, compress such proofs to small sizes that anyone can verify, and they
now power privacy-preserving cryptocurrencies (proving a transaction is valid without revealing its
amounts or parties) and scalability systems that prove the correctness of large computations cheaply.
Zero-knowledge proofs combine naturally with the secure-computation primitives above, and together they
point toward a future in which one can prove properties of data, and compute on it, without ever exposing
it, which is why this area is among the most active in both research and industry.''')

app("## 2.5", r'''

Before detailing block ciphers, it is worth fixing the broader trade-off that explains why symmetric
cryptography remains indispensable despite the elegance of public-key methods covered later. Symmetric
ciphers are typically several orders of magnitude faster than asymmetric ones and produce no ciphertext
expansion to speak of, which is why essentially all bulk data, disk volumes, network streams, database
fields, is protected symmetrically. The price is the key-distribution problem, and the standard
architecture resolves it through *hybrid encryption*: use a slow public-key operation once, only to
establish or transport a fresh symmetric session key, then encrypt all the actual data with that fast
symmetric key. TLS, encrypted email, and messaging apps all follow this pattern, and recognizing it now
will make the later sections on RSA, Diffie-Hellman, and TLS fall into place as solutions to the single
problem this section sets up.''')

json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="markdown")
codew=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="code")
print(f"chapter02 FINAL: {len(cells)} cells, {mdw} md words (~{mdw/500:.1f} pg) + {codew} code = {mdw+codew} total")
