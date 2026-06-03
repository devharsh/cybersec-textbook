import sys, json, uuid; sys.path.insert(0,".build")
from nbbuild import md
path="chapters/04_social_engineering/chapter04.ipynb"
nb=json.load(open(path)); cells=nb["cells"]
def find(p):
    for i,c in enumerate(cells):
        if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith(p): return i
def app(p,t):
    i=find(p); cells[i]["source"]=(("".join(cells[i]["source"])).rstrip()+t+"\n").splitlines(keepends=True)

app("## 4.2", r'''

```{admonition} Going Deeper (graduate/research): cognitive biases behind compliance
:class: tip
Cialdini's principles sit atop a deeper layer of cognitive science. Dual-process theory distinguishes
fast, automatic "System 1" thinking from slow, deliberate "System 2" reasoning, and social engineers
deliberately keep victims in System 1, where heuristics and emotion dominate, by inducing time pressure
and stress. Several documented biases are routinely exploited: *authority bias* (overweighting the
instructions of perceived authorities), *the halo effect* (assuming a confident, well-presented person is
trustworthy), *optimism bias* ("it won't happen to me," which suppresses caution), *loss aversion* (fear
of losing access or money drives hasty action), and *the foot-in-the-door effect* underlying commitment
and consistency. Stress and cognitive load measurably degrade judgment, which is why attacks engineer
urgency, and why the most effective single countermeasure is procedural: a rule that forces a pause and an
independent verification converts a System 1 snap decision back into a System 2 deliberation. Designing
defenses around human cognition, rather than merely exhorting users to "be careful," is an active area of
usable-security research.
```''')

app("## 4.4", r'''

Several further techniques round out the modern repertoire and appear frequently in real incidents. A
**watering-hole attack** compromises a website that a target group is known to visit, so that victims
infect themselves simply by browsing a site they trust, a method favored against specific industries or
communities. **Business email compromise (BEC)** is a high-value form of whaling and pretexting combined:
the attacker impersonates an executive or a trusted vendor (often after compromising or spoofing a real
mailbox) and instructs finance staff to make an urgent wire transfer or change payment details, a fraud
that has cost organizations enormous sums precisely because it uses no malware and slips past technical
filters. **Scareware** and **fake antivirus** frighten victims with bogus infection warnings and trick
them into installing malware or paying for useless software. **Tech-support scams** combine vishing and
pretexting: the attacker claims to be from a well-known technology company, manufactures evidence of a
"problem," and talks the victim into granting remote access or paying. A **honey trap** exploits romantic
or social interest to extract information or money. What unifies these with the earlier list is that each
is simply a different costume over the same psychological machinery, which is why learning the principles
matters more than memorizing an ever-growing catalog of names.

```{admonition} Knowledge Check
:class: hint
1. How does a watering-hole attack differ from spear phishing in how it reaches its victims?
2. Why is business email compromise (BEC) so hard for technical email filters to stop?

*Answers:* (1) Spear phishing sends a crafted message directly to the target, whereas a watering-hole
attack compromises a third-party website the target already trusts and waits for them to visit. (2) BEC
often uses legitimate or convincingly spoofed accounts and contains no malware or malicious link, only a
plausible business request, so there is little for content filters to detect.
```''')

app("## 4.5", r'''

In practice, OSINT collection follows a rough methodology that defenders should understand in order to
counter it. The attacker typically begins with the organization's own footprint, its website, leadership
page, job postings, and press releases, then pivots to individual employees through professional and
personal social networks, building an organizational chart and a list of relationships, roles, and
routines. Specialized search techniques (sometimes called Google dorking, covered in Chapter 7) surface
exposed documents and login portals, and breach-data repositories reveal which employee credentials have
appeared in past leaks, feeding credential-stuffing and convincing pretexts. Metadata in published
documents and photos can leak usernames, software versions, and, through geotags, locations. The
defensive counter is *digital footprint management*: periodically performing this same reconnaissance
against one's own organization, minimizing unnecessary public exposure, scrubbing metadata from published
files, and training employees on what is safe to share. Reconnaissance is treated as a full discipline in
Chapter 7; the point here is that targeted social engineering is only as good as the intelligence behind
it, so denying that intelligence is a direct defense.''')

app("## 4.9", r'''

### Technical Controls That Reinforce the Human Defenses

While social engineering targets people, several technical controls meaningfully reduce its success and
should accompany the human measures above. For email specifically, three authentication standards work
together to make sender spoofing harder: the **Sender Policy Framework (SPF)** lets a domain publish which
mail servers may send on its behalf; **DomainKeys Identified Mail (DKIM)** cryptographically signs
outbound messages so recipients can verify integrity and origin; and **Domain-based Message
Authentication, Reporting and Conformance (DMARC)** ties the two together, telling receivers how to
handle messages that fail and providing reporting. Properly deployed, these reduce, though they do not
eliminate, the impersonation of trusted domains. Secure email gateways and modern filters add malicious
URL detection, attachment sandboxing, and impersonation analysis. At the network layer, **DNS filtering**
blocks access to known phishing and malware domains even if a user clicks, and browser safe-browsing
warnings do the same. **Phishing-resistant MFA** based on hardware security keys (the FIDO2 and WebAuthn
standards) defeats credential phishing and real-time relay because the cryptographic credential is bound
to the legitimate site and never leaves the device. None of these replaces awareness, layered defense
means that when an employee is deceived, these technical controls still have a chance to catch the attack,
and when the controls miss, an aware, empowered employee is the last and often decisive line.''')

# New section: AI-enabled SE, inserted before "## Why This Matters"
ai=md(r'''## 4.10 Social Engineering in the Age of Artificial Intelligence

The techniques in this chapter are old, but artificial intelligence (AI) has sharply lowered their cost
and raised their quality, so a modern treatment must address it directly. Three shifts are underway.
First, **AI-generated phishing** removes the spelling and grammar errors that once betrayed many lures,
and large language models can personalize messages at scale by drawing on scraped public data, making
mass phishing as convincing as hand-crafted spear phishing once was. Second, **voice cloning** lets an
attacker reproduce a specific person's voice from a short sample, supercharging vishing: a panicked call
from a "relative" or an instruction from a familiar-sounding "executive" is now within reach of ordinary
criminals. Third, **deepfake video** can impersonate executives in real time on video calls, as in the
widely reported case in which an employee was deceived into transferring roughly 25 million US dollars
after a video conference populated by synthetic participants.

These developments do not introduce new psychology, they exploit the same authority, urgency, and trust
this chapter has described, but they erode the sensory cues people have always relied on to judge
authenticity, the familiar face and voice. The defensive implications are significant. Verification must
shift from "does this look and sound right?" to procedural checks that an attacker cannot fake: callback
to known numbers, pre-agreed code words for sensitive requests, multi-person approval for large financial
transactions, and out-of-band confirmation that does not depend on the channel the request arrived on.
Organizations are beginning to train staff specifically on synthetic-media threats and to build
"verify, do not trust the medium" into financial and access-granting procedures. The arms race will
continue, with AI also aiding the defense through better anomaly detection, but the durable lesson is
that as the fakes become perfect, trust must move from the appearance of a request to its verifiable
provenance.''')
ai.setdefault("id", uuid.uuid4().hex[:12])
wi=find("## Why This Matters")
cells[wi:wi]=[ai]

for c in cells: c.setdefault("id", uuid.uuid4().hex[:12])
json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="markdown")
codew=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="code")
print(f"chapter04: {len(cells)} cells, {mdw} md words (~{mdw/500:.1f} pg) + {codew} code = {mdw+codew}")
