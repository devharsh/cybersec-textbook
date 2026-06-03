import sys, pickle, uuid; sys.path.insert(0,".build")
from nbbuild import md, code, write_nb
C=pickle.load(open(".build/_ch04.pkl","rb")); A=C.append

A(md(r'''```{admonition} Current News: help-desk social engineering and deepfakes (2024-2025)
:class: important
The most consequential intrusions of 2024 and 2025 began not with malware but with conversations. The
threat group commonly called **Scattered Spider** (also tracked as UNC3944) compromised major
organizations by socially engineering IT help desks: callers impersonated employees, talked support staff
into resetting passwords and re-enrolling multi-factor authentication, and then moved laterally to deploy
ransomware. After targeting Las Vegas casino operators in 2023, the group was linked in public reporting
to attacks on UK retailers including Marks & Spencer, the Co-op, and Harrods in May 2025, and the United
States Cybersecurity and Infrastructure Security Agency (CISA) updated its joint advisory on the group in
2025. Separately, in a widely reported 2024 case, an employee at the engineering firm Arup was deceived
into transferring roughly 25 million US dollars after joining a video call in which **deepfake** audio and
video impersonated senior executives. Together these incidents, drawn from public reporting, show the two
frontiers of modern social engineering: hardened, multi-call help-desk manipulation that defeats MFA
through process, and artificial-intelligence-generated deepfakes that defeat the human instinct to trust a
familiar face and voice.
```
'''))

A(md(r'''## Why This Matters

Social engineering is the through-line that connects every other chapter, because almost every major
breach begins with a human being who is deceived, not a cipher that is broken. The attacker who cannot
crack your encryption will phish your password; the one who cannot breach your firewall will talk their
way past your receptionist or your help desk. This is why the human element is treated as a first-class
attack surface and why awareness, verification procedures, and a healthy, blame-free reporting culture are
as much a part of security as any technical control. The psychological principles in this chapter,
authority, urgency, social proof, liking, reciprocity, and the exploitation of fear and curiosity, do not
change with technology, even as the delivery evolves from a forged email to a deepfaked video call.
A professional who can recognize those levers, in themselves and in others, and who builds organizations
where verifying is the default rather than an act of rudeness, addresses the root cause that so much
technical security leaves untouched.
'''))

A(md(r'''## Chapter Summary

This chapter examined the layer no patch protects: people. **Social engineering** manipulates human
psychology, authority, urgency and scarcity, social proof, liking, reciprocity, and commitment, along
with the emotions of fear, greed, and curiosity, to bypass technical defenses. Attacks follow a
**lifecycle** of research, hook, play, and exit, fueled by **open-source intelligence** that people
scatter publicly, including geotagged photos. The **phishing family** (phishing, spear phishing,
whaling, vishing, smishing, and pharming) dominates, alongside **pretexting, baiting, quid pro quo,
reverse social engineering, tailgating, piggybacking, dumpster diving, and shoulder surfing**.
Recognizing phishing, by checking sender addresses, hovering over links, and distrusting urgency and
requests for credentials, is the most valuable everyday skill, and verification through an independent
channel is the reliable response. Physical security, locks and their bypasses, facility controls,
mantraps, and badges, is social engineering's partner, since the goal of a pretext is often a door, and
**authentication factors** (something you know, have, and are) combined as **multi-factor authentication**
raise the bar, though modern attackers now target MFA itself. The defenses are predominantly human:
**awareness training, clear policies, hardened help-desk verification, sound hiring and termination
procedures, and a blame-free reporting culture**. With the human element understood, the next chapter
turns to risk management, the discipline that decides which of all these threats an organization should
spend its limited resources to address first.
'''))

A(md(r'''## Review Questions

**Q1.** Social engineering primarily exploits:
A. Software bugs  B. Human psychology and trust  C. Weak encryption  D. Network misconfiguration

**Q2.** A phishing attack targeted at a company's CEO is called:
A. Vishing  B. Smishing  C. Whaling  D. Pharming

**Q3.** Which Cialdini principle is exploited by a message saying "your account closes in 1 hour"?
A. Liking  B. Urgency/scarcity  C. Social proof  D. Reciprocity

**Q4.** Voice phishing conducted over the telephone is called:
A. Smishing  B. Vishing  C. Pharming  D. Baiting

**Q5.** Following an authorized person through a secure door without their knowledge is:
A. Piggybacking  B. Tailgating  C. Pretexting  D. Shimming

**Q6.** Pharming differs from phishing in that it:
A. Uses SMS  B. Redirects victims to a fake site, often via DNS, rather than luring with a link
C. Targets executives  D. Requires physical access

**Q7.** Leaving a malware-laden USB drive labeled "Payroll" for a victim to find is:
A. Baiting  B. Whaling  C. Tailgating  D. Vishing

**Q8.** In reverse social engineering, the attacker:
A. Works backward through a network  B. Creates a problem then poses as the helper so the victim makes
contact  C. Decrypts traffic  D. Uses a bump key

**Q9.** Which is the best response to an urgent email demanding your password?
A. Reply with the password  B. Click the link to check  C. Verify via the organization's known channel
independently  D. Forward it to colleagues

**Q10.** The three classic authentication factors are something you:
A. Know, have, and are  B. Type, click, and see  C. Buy, own, and rent  D. Read, write, and execute

**Q11.** A mantrap (access-control vestibule) primarily counters:
A. Phishing  B. Tailgating  C. DNS spoofing  D. Dumpster diving

**Q12.** Cross-cut shredding is preferred over strip-cut because it:
A. Is faster  B. Makes reconstructing documents much harder  C. Uses less power  D. Handles more paper

**Q13.** Why have attackers shifted to attacking MFA via help desks?
A. MFA is illegal  B. MFA blocks simple credential phishing, so attackers trick staff into resetting it
C. Help desks have no phones  D. MFA only protects email

**Q14.** Geotagging is a social-engineering concern because it:
A. Encrypts photos  B. Reveals a person's exact location from posted photos  C. Blocks phishing
D. Speeds up DNS

**Q15.** The most effective long-term defense against social engineering is:
A. A bigger firewall  B. Ongoing security awareness training plus verification policies  C. Longer
passwords  D. Disabling email

---

### Answer Key

1: B 2: C 3: B 4: B 5: B 6: B 7: A 8: B 9: C 10: A 11: B 12: B 13: B 14: B 15: B
'''))

A(md(r'''## Hands-on Labs

**Lab 4.1 (beginner) - Phishing red-flag hunt.** Collect five phishing emails (from a spam folder or a
public awareness archive) and, without clicking anything, complete a table identifying for each: the true
sender, the impersonated brand, the emotional trigger used, at least one disguised link or attachment,
and the verification step a recipient should take. Rank them from most to least convincing and explain
why.

**Lab 4.2 (beginner/intermediate) - OSINT self-assessment.** Search for your own publicly available
information as an attacker would: social-media profiles, photos (check for geotags), and any work or
contact details. Write a short report on what a spear-phisher could learn about you and craft (but do not
send) a hypothetical pretext, then list the privacy settings and habits that would reduce your exposure.

**Lab 4.3 (intermediate) - Build a verification policy.** Draft a one-page help-desk verification policy
for a fictional company that would have stopped a Scattered-Spider-style password-reset attack. Specify
the identity checks required before any password or MFA reset, and explain how each step defeats a
specific social-engineering technique from this chapter.

**Lab 4.4 (advanced/research) - Extend the phishing checker.** Starting from the Section 4.6 code, add at
least three new indicators (for example, look-alike/homoglyph domains, mismatched reply-to addresses, or
suspicious attachment types) and test it against a labeled set of phishing and legitimate emails.
Report its accuracy and discuss why purely rule-based detection is insufficient against
artificial-intelligence-generated phishing, referencing the deepfake trend in this chapter's Current News.
'''))

A(md(r'''## References

1. Hadnagy, C. *Social Engineering: The Science of Human Hacking*, 2nd ed. Wiley, 2018.
2. Cialdini, R. *Influence: The Psychology of Persuasion.* Harper Business.
3. Mitnick, K., and Simon, W. *The Art of Deception: Controlling the Human Element of Security.* Wiley,
   2002.
4. Cybersecurity and Infrastructure Security Agency (CISA). *Scattered Spider*, Joint Cybersecurity
   Advisory AA23-320A (updated 2025).
5. Anti-Phishing Working Group (APWG). *Phishing Activity Trends Reports.* https://apwg.org
6. National Institute of Standards and Technology. *Digital Identity Guidelines*, NIST SP 800-63.
7. Verizon. *Data Breach Investigations Report (DBIR)* (annual), human-element findings.
'''))

for c in C: c.setdefault("id", uuid.uuid4().hex[:12])
write_nb("chapters/04_social_engineering/chapter04.ipynb", C)
