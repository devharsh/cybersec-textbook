import sys, json; sys.path.insert(0,".build")
from nbbuild import md
path="chapters/01_intro/chapter01.ipynb"
nb=json.load(open(path))

taxonomy = md(r'''## 1.11 A Taxonomy of Threats and a Roadmap to This Book

The threats a modern organization faces are numerous, but they fall into a manageable number of
families. Surveying them now provides both a mental filing system and a map of the chapters ahead.

**Malware** is malicious software in all its forms: viruses that attach to files, worms that
self-propagate across networks, trojans that masquerade as legitimate programs, ransomware that
encrypts data for extortion, spyware and keyloggers that steal information, rootkits that hide deep in
the system, and botnets that conscript machines into attacker-controlled networks. Malware is examined
in depth in Chapter 15.

**Social-engineering attacks** target people rather than machines, exploiting trust, authority, fear,
and urgency. Phishing emails, voice-based vishing, SMS-based smishing, pretexting, baiting, and
business email compromise all manipulate human psychology to extract credentials, money, or access.
Because humans are involved in nearly every system, social engineering bypasses technical controls and
is consistently among the most effective attack categories; it is the subject of Chapter 4.

**Network attacks** abuse the protocols and infrastructure that connect systems: sniffing and
eavesdropping, man-in-the-middle interception, spoofing of addresses and identities, denial-of-service
and distributed denial-of-service floods, and session hijacking. The networking foundations are laid
in Chapter 3 and the offensive techniques developed in Chapters 7 through 9, with defenses in
Chapters 11 and 12.

**Application and web attacks** exploit flaws in software, especially the web applications and APIs
that expose organizations to the internet. Injection (including SQL injection), cross-site scripting,
broken authentication, insecure deserialization, and server-side request forgery are perennial
problems catalogued by the OWASP Top Ten. These are the focus of Chapter 10, with the underlying
exploitation mechanics, including memory-corruption bugs and return-oriented programming, in Chapter 9.

**Cryptographic attacks** target the algorithms and protocols meant to protect data, exploiting weak
ciphers, poor key management, flawed randomness, or implementation mistakes and side channels.
Cryptography and its failure modes occupy Chapter 2, with forward-looking concerns such as the
quantum threat and homomorphic and functional encryption in Chapters 2 and 17.

**Physical and supply-chain attacks** sidestep digital defenses entirely. Physical access to hardware,
theft of devices, tampering with equipment, and the insertion of malicious components or compromised
software updates upstream in the supply chain can defeat otherwise strong systems. The high-profile
software-supply-chain compromises of recent years show how a single trusted vendor can become a vector
to thousands of victims; these concerns thread through the governance and emerging-topics chapters.

**Threats to specialized environments** round out the landscape. Cloud platforms introduce shared
responsibility and misconfiguration risks; mobile devices, the Internet of Things, and operational
technology each expand the attack surface in distinctive ways. Industrial control systems that run
critical infrastructure, examined in Chapter 20, raise the stakes from data loss to physical safety.

No single book chapter, and no single control, addresses all of these. That is exactly why the
risk-based, defense-in-depth, framework-driven approach introduced in this chapter matters: it gives
the practitioner a way to reason about an open-ended and shifting set of threats without being
overwhelmed by their variety. With this foundation in place, the next chapter turns to cryptography,
the mathematical machinery on which so much of modern security ultimately rests.
''')

idx=None
for i,c in enumerate(nb["cells"]):
    if c["cell_type"]=="markdown" and "".join(c["source"]).startswith("## Chapter Summary"):
        idx=i; break
assert idx is not None
nb["cells"][idx:idx]=[taxonomy]
json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in nb["cells"] if c["cell_type"]=="markdown")
print(f"chapter01 now {len(nb['cells'])} cells, {mdw} md words (~{mdw/500:.1f} pages)")
