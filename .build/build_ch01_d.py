import sys, pickle; sys.path.insert(0,".build")
from nbbuild import md, code, write_nb
C = pickle.load(open(".build/_ch01_cells.pkl","rb"))
A = C.append

A(code(r'''# Chapter 1 -- Visualizing defense in depth as concentric layers
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

layers = [
    ("Data (encryption, DLP)",        1.0, "#1a5276"),
    ("Application (hardening, SAST)",  2.0, "#1f6f8b"),
    ("Host (EDR, patching)",          3.0, "#2980b9"),
    ("Internal network (segmentation)",4.0, "#5499c7"),
    ("Perimeter (firewall, IDS/IPS)", 5.0, "#7fb3d5"),
    ("Physical (locks, guards)",      6.0, "#aed6f1"),
    ("Policies & people (training)",  7.0, "#d6eaf8"),
]
fig, ax = plt.subplots(figsize=(7, 7))
for label, r, color in reversed(layers):
    ax.add_patch(Circle((0, 0), r, color=color, ec="white", lw=1.5))
    ax.text(0, r - 0.45, label, ha="center", va="center", fontsize=8.5,
            color="white" if r <= 4 else "#1a1a1a")
ax.text(0, 0, "ASSET", ha="center", va="center", fontsize=11, fontweight="bold", color="white")
ax.set_xlim(-7.5, 7.5); ax.set_ylim(-7.5, 7.5)
ax.set_aspect("equal"); ax.axis("off")
ax.set_title("Defense in Depth: Overlapping Layers of Control", fontsize=12)
plt.tight_layout()
plt.savefig("ch01_defense_in_depth.png", dpi=110)
print("Figure saved: ch01_defense_in_depth.png")''' ))

A(md(r'''## Why This Matters

The concepts in this chapter are not academic abstractions; they are the lens through which every later
topic is viewed. When you study cryptography, you are learning mechanisms that enforce confidentiality
and integrity. When you study penetration testing, you are learning to think like the threat actors
described here and to map an organization's attack surface. When you study incident response, you are
operating the Detect, Respond, and Recover functions of the NIST framework. A security professional who
internalizes the CIA triad, the risk equation, the control taxonomy, and the defense-in-depth principle
can reason about an unfamiliar system, technology, or threat that did not even exist when they were
trained. That transferable judgment, not memorized facts, is what distinguishes a practitioner from a
technician, and it is what every major certification ultimately tests.
'''))

A(md(r'''## News in Focus: The Colonial Pipeline Ransomware Incident (2021)

In May 2021, Colonial Pipeline, which supplies a large share of the fuel consumed on the United States
East Coast, halted operations for several days after a ransomware attack. The intrusion has been widely
attributed to the DarkSide ransomware-as-a-service operation, and public reporting indicated that the
initial access was gained through a single compromised virtual private network (VPN) account that was
no longer in active use but remained enabled and was not protected by multi-factor authentication.

Viewed through this chapter's vocabulary, the incident is instructive. The **asset** was the company's
ability to operate the pipeline and bill customers. The **vulnerability** was a dormant remote-access
account with a reused password and no multi-factor authentication, part of an avoidable **attack
surface**. The **threat actor** was a financially motivated cybercriminal group. The attack primarily
struck **availability**, the pipeline stopped, with secondary confidentiality impact from data theft
used for extortion. Several inexpensive **preventive** controls, disabling unused accounts and
enforcing multi-factor authentication, would likely have blocked the initial access, illustrating both
attack-surface reduction and the outsized return that basic controls can deliver. The episode also
showed how a digital event cascades into the physical world, triggering fuel shortages and emergency
government action. The technical and reporting details here are drawn from public accounts and may be
revised as investigations conclude.
'''))

A(md(r'''## Review Questions

**Q1.** Which CIA property is primarily violated when ransomware encrypts a hospital's patient files?
A. Confidentiality only  B. Integrity only  C. Availability (and potentially integrity)  D. None

**Q2.** An employee accidentally emails a customer list to the wrong recipient. Which property fails?
A. Availability  B. Confidentiality  C. Integrity  D. Non-repudiation

**Q3.** The formula ALE = SLE x ARO produces a value measured in:
A. Risk units  B. Dollars per year  C. Probability  D. Number of patches

**Q4.** The function added to the NIST Cybersecurity Framework in the 2.0 (2024) revision is:
A. Identify  B. Detect  C. Govern  D. Protect

**Q5.** Defense in depth is best described as:
A. Buying the most expensive control available
B. Multiple overlapping controls so a single failure does not cause a breach
C. Patching all systems within 24 hours
D. Encrypting all data at rest

**Q6.** A visible surveillance camera in a data center is best classified as which control functions?
A. Preventive only  B. Corrective only  C. Detective and deterrent  D. Compensating only

**Q7.** A script kiddie differs from an APT actor primarily in:
A. Motivation only  B. Technical sophistication and resources  C. Use of phishing  D. Choice of operating system

**Q8.** The attack surface of an application is reduced by:
A. Buying a faster server
B. Disabling unused services and applying least privilege
C. Adding more verbose logging
D. Increasing the encryption key size

**Q9.** If SLE = $80,000 and ARO = 0.25, the ALE is:
A. $80,000  B. $320,000  C. $20,000  D. $100,000

**Q10.** On the x86 ring model, ordinary user applications normally execute in:
A. Ring 0 (kernel mode)  B. Ring 1  C. Ring 2  D. Ring 3 (user mode)

**Q11.** The three required properties of a reference monitor are that it be:
A. Fast, cheap, and encrypted
B. Tamper-proof, always invoked, and small enough to be verified
C. Cloud-based, redundant, and logged
D. Open-source, audited, and signed

**Q12.** A control that provides an alternative when a primary control cannot be implemented (for
example isolating an unpatchable legacy system) is called:
A. Deterrent  B. Corrective  C. Compensating  D. Directive

---

### Answer Key

1: C 2: B 3: B 4: C 5: B 6: C 7: B 8: B 9: C 10: D 11: B 12: C

**Q9 worked:** ALE = SLE x ARO = $80,000 x 0.25 = $20,000 per year.
'''))

A(md(r'''## Hands-on Labs

**Lab 1.1 - Asset and risk register.** Choose a small organization you know (a club, a family
business, or a hypothetical startup). List at least eight assets, and for each one identify a threat, a
vulnerability, and one control. Estimate AV, EF, and ARO for two assets and compute their ALE. Present
your results in a table and write a short paragraph recommending which risk to address first and why.

**Lab 1.2 - Control classification.** Walk through your own home or workplace and identify ten security
controls. Classify each on both axes (type: administrative/technical/physical; function:
preventive/detective/corrective/deterrent/compensating/directive). Note any control that fills more
than one role, and identify any function that is missing entirely from your environment.

**Lab 1.3 - Mapping an incident.** Find a publicly reported breach from the past year using reputable
sources. Write a one-page analysis identifying the asset, threat actor, vulnerability, attack vector,
which CIA properties were violated, and at least two controls that could have prevented or limited the
incident. Map the defenders' likely response to the six NIST CSF functions.

**Lab 1.4 - Privilege boundaries (optional, technical).** On a Linux system, run a non-privileged
command and then the same operation requiring root, observing the permission error and the role of the
kernel boundary. Use `strace` on a simple program (for example `cat`) to observe the system calls it
makes, and identify three calls that transition from user mode to kernel mode. Write a short note
explaining what the ring boundary is protecting against.
'''))

A(md(r'''## References

1. Spafford, E. H. Widely quoted remark on the impossibility of perfect security.
2. National Institute of Standards and Technology. *The NIST Cybersecurity Framework (CSF) 2.0*,
   NIST CSWP 29, 2024.
3. National Institute of Standards and Technology. *Guide for Conducting Risk Assessments*,
   NIST Special Publication 800-30 Revision 1, 2012.
4. Parker, D. B. *Fighting Computer Crime: A New Framework for Protecting Information.* Wiley, 1998.
5. Lockheed Martin. *Cyber Kill Chain.* Intrusion Kill Chain framework white paper, 2011.
6. MITRE. *MITRE ATT&CK Knowledge Base.* https://attack.mitre.org
7. Saltzer, J. H., and Schroeder, M. D. "The Protection of Information in Computer Systems."
   *Proceedings of the IEEE*, 63(9), 1975.
8. Cybersecurity and Infrastructure Security Agency (CISA). Public advisories on the 2021 Colonial
   Pipeline incident.
'''))

write_nb("chapters/01_intro/chapter01.ipynb", C)
