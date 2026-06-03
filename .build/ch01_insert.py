import sys, json; sys.path.insert(0,".build")
from nbbuild import md
path="chapters/01_intro/chapter01.ipynb"
nb=json.load(open(path))

principles = md(r'''## 1.9 The Saltzer and Schroeder Design Principles

In 1975, Jerome Saltzer and Michael Schroeder articulated a set of design principles for secure
systems that remain remarkably current half a century later. They are tested directly on professional
examinations and, more importantly, they provide a checklist against which any design decision can be
evaluated.

**Economy of mechanism.** Keep the design as simple and small as possible. Complexity is the enemy of
security because every additional feature, option, and line of code is another place for a flaw to
hide and another thing a defender must understand. Simple systems can be reviewed and reasoned about;
sprawling ones cannot. This principle motivates keeping the trusted computing base minimal.

**Fail-safe defaults.** Base access decisions on permission rather than exclusion: the default should
be to deny, and access should be granted only by explicit allowance. A system that fails closed denies
service when something goes wrong, which is annoying but safe; a system that fails open grants access
on error, which is convenient but catastrophic. Default-deny firewall rules embody this principle.

**Complete mediation.** Every access to every object must be checked against the access-control policy,
every time. Systems that check permission once and then cache the result, or that allow some paths to
bypass the check, invite abuse. This is precisely the property required of the reference monitor.

**Open design.** The security of a system should not depend on the secrecy of its design or
implementation, only on the secrecy of keys. This is the security analog of **Kerckhoffs's principle**
in cryptography, which holds that a cryptosystem should remain secure even if everything about it
except the key is public knowledge. Security through obscurity, hiding how a system works and hoping
attackers never find out, is brittle: secrets leak, and a defense that collapses once understood was
never strong. Open designs can be scrutinized by many eyes and earn justified confidence.

**Separation of privilege.** Where practical, require more than one condition or party to authorize an
important action. Requiring two officers to launch a missile, or two signatures to release a large
payment, means that no single compromised credential or corrupt individual is sufficient. This is the
basis of **separation of duties**, which splits a sensitive task so that no one person controls it end
to end, and of multi-factor authentication, which requires more than one kind of evidence of identity.

**Least privilege.** Every user, process, and program should operate with the minimum set of
privileges necessary to perform its function, and no more. If a web server only needs to read certain
files, it should not run as an administrator. Least privilege limits the damage that a compromised
component or a careless user can do, because the attacker inherits only the narrow rights the victim
held. It is one of the most powerful and most frequently violated principles in practice.

**Least common mechanism.** Minimize the mechanisms that are shared by, and depended on by, more than
one user or process. Shared mechanisms are potential channels for unintended information flow and
single points of failure; isolating users from one another reduces the blast radius of a compromise.

**Psychological acceptability.** Security mechanisms must be easy enough to use that people actually
use them correctly. A control that is cumbersome will be bypassed, written on a sticky note, or worked
around, defeating its purpose. Usable security is not a luxury; it is a precondition for real-world
effectiveness, and it explains why poorly designed password policies often make security worse.

Together these principles encode hard-won wisdom: prefer simplicity, deny by default, check everything,
do not rely on secrecy, divide power, grant the least authority needed, share as little as possible,
and make the secure path the easy path.
''')

mindset = md(r'''## 1.10 The Security Mindset, Ethics, and the Law

Beyond specific techniques, cybersecurity demands a particular way of thinking that the cryptographer
Bruce Schneier calls the **security mindset**: the habit of looking at any system and asking not "how
does this work?" but "how can this be made to fail?" Where a typical engineer asks how to make a
feature function, the security professional asks how an adversary could abuse it, what assumptions it
silently depends on, and what happens when those assumptions are violated. This adversarial perspective
can be learned, and cultivating it is one of the central aims of this book.

The same knowledge that lets a defender anticipate attacks would let an attacker carry them out, and
this dual-use character makes **ethics and law** inseparable from technical skill. The defining
distinction is **authorization**. Probing, scanning, or exploiting a system you do not own and have not
been given explicit, documented permission to test is, in most jurisdictions, a crime, regardless of
your intentions or whether you cause harm. In the United States the principal statute is the Computer
Fraud and Abuse Act; many other countries have analogous laws such as the United Kingdom's Computer
Misuse Act. Penetration testers operate under written contracts and carefully scoped **rules of
engagement**, a topic developed in the chapter on penetration-testing methodology, precisely because
authorization is what separates a professional service from a felony.

Ethical practice also includes **responsible disclosure**: when a researcher discovers a vulnerability,
the accepted norm is to report it privately to the vendor and allow reasonable time for a fix before
any public discussion, balancing the public's right to know against the risk of arming attackers.
Professional bodies reinforce these expectations through codes of conduct; the (ISC)2 Code of Ethics,
for instance, obliges members to protect society and the common good and to act honorably and legally.
Throughout this book, every offensive technique is presented for the purpose of building better
defenses, and the reader is expected to apply it only within the bounds of explicit authorization and
applicable law.
''')

summary = md(r'''## Chapter Summary

This chapter established the conceptual foundation for everything that follows. Cybersecurity is the
practice of managing risk to digital systems and data; it is a continuous process rather than a
product, and perfect security is neither achievable nor the goal. The **CIA triad**, confidentiality,
integrity, and availability, defines the properties we protect, with the **DAD** triad, **AAA** model,
and **Parkerian hexad** extending the picture. An attack is best analyzed through five linked elements,
**asset, threat, vulnerability, attack surface, and exploitation**, tied together by **risk**.
Adversaries range from low-skill script kiddies to patient, well-funded advanced persistent threats,
and calibrating defenses to the relevant adversary is essential. **Defense in depth** layers diverse,
overlapping controls, which we classify by type (administrative, technical, physical) and by function
(preventive, detective, corrective, deterrent, compensating, directive). Security rests on hardware
foundations, **CPU protection rings**, the user/kernel boundary, the **trusted computing base**, and
the **reference monitor**, and on enduring design principles from Saltzer and Schroeder such as least
privilege, fail-safe defaults, complete mediation, and open design. The **NIST Cybersecurity Framework
2.0** organizes all of this into six functions, and **quantitative risk analysis** (SLE, ARO, ALE,
ROSI) lets us justify security spending in monetary terms. Finally, the **security mindset** and a firm
grounding in **ethics and law**, above all the requirement of authorization, are what make this
knowledge a profession rather than a hazard. The chapters ahead apply these ideas to cryptography,
networking, offensive and defensive techniques, and governance.
''')

# insert before the "Why This Matters" cell
idx=None
for i,c in enumerate(nb["cells"]):
    if c["cell_type"]=="markdown" and "".join(c["source"]).startswith("## Why This Matters"):
        idx=i; break
assert idx is not None, "anchor not found"
nb["cells"][idx:idx]=[principles, mindset, summary]
json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in nb["cells"] if c["cell_type"]=="markdown")
print(f"inserted; chapter01 now {len(nb['cells'])} cells, {mdw} md words (~{mdw/500:.1f} pages)")
