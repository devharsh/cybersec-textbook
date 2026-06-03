import sys; sys.path.insert(0,".build")
from nbbuild import md, code, write_nb
C = []
A = C.append

A(md(r'''# Chapter 1: Introduction to Cybersecurity

> "The only truly secure system is one that is powered off, cast in a block of concrete, and sealed in a
> lead-lined room with armed guards, and even then I have my doubts." -- Gene Spafford

---

## Learning Objectives

After completing this chapter, you will be able to:

1. Define cybersecurity and distinguish it from information security and computer security.
2. State the CIA triad and explain each property with a real-world example, and extend it with the
   AAA, DAD, and Parkerian models.
3. Identify the four elements of an attack: threat, vulnerability, attack surface, and exploitation,
   and relate them through the risk equation.
4. Explain the adversary model: who attacks, why, and with what capability, from script kiddies to
   advanced persistent threats (APTs).
5. Describe the NIST Cybersecurity Framework 2.0 functions and map them to defensive practice.
6. Apply the single loss expectancy (SLE), annualized rate of occurrence (ARO), annualized loss
   expectancy (ALE), and return on security investment (ROSI) formulas to quantify risk in monetary
   terms.
7. Explain the defense-in-depth principle and the layered security model.
8. Distinguish security controls by function (preventive, detective, corrective, deterrent,
   compensating, directive) and by type (administrative, technical, physical).
9. Describe the hardware foundations of security: CPU protection rings, kernel and user mode, the
   trusted computing base (TCB), and the reference monitor.

## Key Terms

- **Cybersecurity**: the practice of protecting systems, networks, programs, and data in cyberspace
  from digital attack, damage, or unauthorized access.
- **Information security (InfoSec)**: the broader discipline of protecting information in any form,
  digital or physical, across its entire lifecycle.
- **CIA triad**: Confidentiality, Integrity, and Availability; the three core security properties.
- **AAA**: Authentication, Authorization, and Accounting; the operational pillars of access control.
- **Threat**: any circumstance or event with the potential to harm an asset.
- **Threat actor**: the entity (person, group, or automated process) that carries out a threat.
- **Vulnerability**: a weakness in a system that a threat can exploit.
- **Attack surface**: the sum of all points where an unauthorized user can try to enter or extract data.
- **Attack vector**: the specific path or method a threat actor uses to reach a target.
- **Exploit**: code or a technique that takes advantage of a vulnerability.
- **Risk**: the likelihood that a threat will exploit a vulnerability, multiplied by the resulting impact.
- **Asset**: anything of value to an organization that warrants protection.
- **Control (safeguard, countermeasure)**: a measure that reduces risk by mitigating a vulnerability
  or the impact of a threat.
- **Trusted computing base (TCB)**: the totality of hardware, firmware, and software responsible for
  enforcing a system's security policy.
- **Reference monitor**: the abstract machine that mediates every access of a subject to an object.
'''))

A(md(r'''## 1.1 What Is Cybersecurity?

Cybersecurity is the discipline concerned with protecting computer systems, networks, software, and
the data they hold from unauthorized access, disruption, modification, or destruction. The term is
often used interchangeably with *information security*, but the two are not identical. Information
security is the older and broader field: it protects information in **any** form, whether printed on
paper, spoken aloud, stored on a hard drive, or transmitted across a fiber-optic cable. Cybersecurity
is the subset of information security that deals specifically with information and systems that exist
in or are reachable through *cyberspace*, the interconnected domain of digital networks. A third
adjacent term, *computer security*, narrows the focus still further to the protection of individual
machines and their operating systems. In practice these boundaries blur, and most practitioners treat
the three terms as members of the same family, choosing whichever word best fits the audience.

The reason the field exists at all is that modern society has become utterly dependent on digital
systems. Hospitals schedule surgeries and dispense medication through networked software. Power grids,
water treatment plants, and pipelines are operated by industrial control systems. Banks move trillions
of dollars as nothing more than authenticated messages. When these systems fail, whether through
accident or attack, the consequences spill out of the digital world and into the physical one. A
ransomware infection is no longer merely an inconvenience to an IT department; it can close a hospital
emergency room or halt fuel delivery to an entire region. Cybersecurity is therefore best understood
not as a narrow technical specialty but as a form of risk management for a society that runs on code.

It is useful to internalize early that **security is a process, not a product**. There is no single
device, license, or configuration that makes an organization "secure" once and for all. Threats
evolve, software changes, people make mistakes, and yesterday's strong defense becomes today's known
weakness. Security is achieved and maintained through continuous cycles of identifying assets,
assessing risks, applying controls, monitoring for failures, and improving. This mindset, sometimes
summarized as *continuous improvement*, underlies every framework discussed in this book.

A second foundational idea is that **perfect security is impossible**, and pursuing it is usually
wasteful. Gene Spafford's famous quip at the top of this chapter captures the point with deliberate
absurdity: even a computer encased in concrete and guarded around the clock is not perfectly secure,
and it is also perfectly useless. Every real system must balance security against usability, cost,
and performance. The goal of the cybersecurity professional is not to eliminate risk, which cannot be
done, but to reduce it to a level the organization is willing to accept, at a cost the organization is
willing to bear. This is why the language of risk, introduced later in this chapter, pervades the
entire profession.
'''))

A(md(r'''## 1.2 The CIA Triad and Its Extensions

The most enduring model in all of security is the **CIA triad**: Confidentiality, Integrity, and
Availability. These three properties define what it means for information to be secure, and almost
every control, attack, and incident can be understood in terms of which of them is being protected or
violated. Note that "CIA" here has nothing to do with the intelligence agency; it is simply an
acronym for the three properties.

**Confidentiality** means that information is disclosed only to those authorized to see it. It is the
property violated when an attacker steals a database of customer records, when an employee emails a
spreadsheet of salaries to the wrong recipient, or when someone reads sensitive documents left on a
shared printer. Confidentiality is enforced through mechanisms such as encryption, access control
lists, authentication, and the principle of least privilege. The opposite of confidentiality is
*disclosure*.

**Integrity** means that information is accurate and has not been altered in an unauthorized or
undetected way. It is the property violated when an attacker changes the dollar amount on a wire
transfer, when malware modifies system files, or when a transmission error silently corrupts a
record. Integrity is enforced through cryptographic hashes, digital signatures, message authentication
codes, version control, and rigorous change management. The opposite of integrity is *alteration*.

**Availability** means that information and services are accessible to authorized users when they need
them. It is the property violated by a distributed denial-of-service (DDoS) attack that floods a web
server, by ransomware that encrypts files and holds them hostage, or by a simple power failure in a
data center. Availability is enforced through redundancy, backups, failover systems, capacity planning,
and resilient network design. The opposite of availability is *destruction* or *denial*.

These three opposites form a complementary model sometimes called the **DAD triad**: Disclosure,
Alteration, and Destruction (or Denial). Where CIA describes the defender's goals, DAD describes the
attacker's goals, and the two map directly onto each other. A useful mental exercise when analyzing
any incident is to ask which CIA property was the target and which DAD action the adversary performed.

The CIA triad is powerful but incomplete, and several extensions address its gaps. The **AAA** model,
Authentication, Authorization, and Accounting, describes the operational machinery of access control:
*authentication* establishes who a subject is, *authorization* determines what that subject may do,
and *accounting* records what the subject actually did. Closely related are *non-repudiation*, the
assurance that a party cannot credibly deny having performed an action (typically provided by digital
signatures), and *authenticity*, the assurance that data genuinely originates from its claimed source.

The most thorough extension is the **Parkerian hexad**, proposed by Donn Parker, which adds three
further properties to the original three: *possession or control* (having physical or logical custody
of data, which can be lost even when confidentiality is preserved, for example when an encrypted laptop
is stolen), *authenticity* (the data is genuine and correctly attributed), and *utility* (the data is
useful, which is lost, for instance, when the only copy of an encryption key is destroyed, leaving the
ciphertext intact but worthless). While the simple CIA triad suffices for most everyday reasoning, the
hexad is valuable when an incident does not fit neatly into the three classical properties.
'''))
print("part A appended:", len(C), "cells")
import pickle; pickle.dump(C, open(".build/_ch01_cells.pkl","wb"))
