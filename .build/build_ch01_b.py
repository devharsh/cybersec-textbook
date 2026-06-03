import sys, pickle; sys.path.insert(0,".build")
from nbbuild import md, code
C = pickle.load(open(".build/_ch01_cells.pkl","rb"))
A = C.append

A(md(r'''## 1.3 The Anatomy of an Attack

To defend systems systematically, we need a precise vocabulary for the elements of an attack. Five
terms recur throughout this book, and confusing them is a common source of muddled thinking.

An **asset** is anything of value worth protecting: a customer database, a domain controller, an
employee's credentials, a company's reputation, or the availability of a production website. A
**threat** is any potential event or circumstance that could harm an asset. Threats may be deliberate
(a criminal seeking to steal data), accidental (an administrator who mistypes a command), or
environmental (a flood, fire, or power surge). The entity that carries out a deliberate threat is the
**threat actor** or *adversary*.

A **vulnerability** is a weakness that a threat can exploit. Vulnerabilities take many forms: an
unpatched software bug, a default password, a misconfigured cloud storage bucket, an employee
susceptible to a phishing email, or a building with an unlocked server-room door. A vulnerability is
harmless in isolation; it becomes dangerous only when a threat exists that can take advantage of it.

The **attack surface** is the sum of all the points, the vulnerabilities and entry paths, where an
unauthorized actor could attempt to interact with a system. Every running network service, every input
field on a web form, every USB port, every employee with email, and every third-party integration
adds to the attack surface. A central goal of defensive engineering is **attack surface reduction**:
disabling unused services, closing unnecessary ports, removing default accounts, and applying the
principle of least functionality so that there is simply less for an attacker to target. The specific
route an attacker takes across the attack surface is the **attack vector**.

An **exploit** is the actual code, command, or technique that takes advantage of a vulnerability to
produce an unintended effect, such as executing arbitrary code, escalating privileges, or crashing a
service. When an exploit is used successfully, *exploitation* has occurred. The window between the
public disclosure of a vulnerability and the availability of a fix is especially dangerous; a
vulnerability that is exploited before any patch exists is called a **zero-day**.

Finally, **risk** ties these concepts together. Informally, risk is the probability that a threat will
successfully exploit a vulnerability, multiplied by the magnitude of the resulting harm. The
relationships among these elements are shown below.

```{mermaid}
graph LR
    A[Threat Actor] -->|launches| B[Threat]
    B -->|exploits| C[Vulnerability]
    C -->|resides in| D[Attack Surface]
    B -->|via| E[Attack Vector]
    E --> C
    C -->|leads to| F[Exploitation]
    F -->|causes| G[Impact / Loss]
    G -->|combined with probability| H[Risk]
    I[Control] -->|reduces| C
    I -->|reduces| G
```

The diagram makes an important point visible: a **control** can reduce risk either by removing or
hardening the vulnerability (lowering the probability of exploitation) or by limiting the impact when
exploitation does occur. Effective security programs apply both kinds of control rather than relying
on prevention alone.
'''))

A(md(r'''## 1.4 Threat Actors and the Adversary Model

Not all attackers are equal, and a defense calibrated for a bored teenager will not stop a
nation-state intelligence service. Understanding the **adversary model**, who might attack, what they
want, and what resources they command, lets defenders allocate effort proportionately. Security
professionals describe an adversary's strength in terms of *capability* (skill, tooling, and funding),
*intent* (motivation and goals), and *opportunity* (access to the target). A credible threat requires
all three.

The weakest deliberate actors are **script kiddies**, individuals with little original skill who run
pre-built tools and published exploits they do not fully understand. Their motivation is often
curiosity, vandalism, or bragging rights. They are numerous and noisy, and basic hygiene, patching,
strong passwords, and default-deny firewalls, defeats most of them.

**Hacktivists** attack to advance a political or social cause, defacing websites, leaking documents,
or launching denial-of-service campaigns against organizations they oppose. Their capability varies
widely, but their public, ideological motivation makes their targeting somewhat predictable.

**Cybercriminals** and organized crime groups attack for financial gain. This is the largest category
by volume and includes ransomware operators, banking-trojan crews, business-email-compromise
fraudsters, and the sprawling underground economy that sells stolen data and access. Modern
cybercrime is professionalized, with specialized roles, customer support, and *ransomware-as-a-service*
affiliate programs. Their capability ranges from moderate to very high.

**Insiders** are employees, contractors, or partners who abuse legitimate access. A *malicious insider*
acts deliberately, perhaps a disgruntled administrator or an employee bribed by a competitor, while a
*negligent insider* causes harm through carelessness. Insiders are dangerous precisely because they
begin inside the trust boundary, bypassing perimeter defenses entirely.

The most capable adversaries are **advanced persistent threats (APTs)**, typically nation-state
intelligence and military services or their contractors. The label captures three characteristics:
*advanced* (sophisticated, sometimes custom tooling and zero-day exploits), *persistent* (long-term
campaigns that may maintain covert access for months or years), and *threat* (well-resourced, patient,
and goal-directed). APTs pursue espionage, sabotage, or strategic advantage rather than quick profit.
Defending against them requires assuming breach, detecting subtle anomalies, and limiting lateral
movement, because preventing initial access against an adversary with effectively unlimited time and
budget is unrealistic.

| Actor | Typical capability | Primary motivation | Defining trait |
|---|---|---|---|
| Script kiddie | Low | Curiosity, status | Uses others' tools |
| Hacktivist | Low to high | Ideology | Public, cause-driven |
| Cybercriminal | Moderate to high | Financial gain | Professionalized, scalable |
| Insider | Variable | Grievance, greed, error | Starts inside the perimeter |
| APT / nation-state | Very high | Espionage, sabotage | Patient, resourced, stealthy |

A complementary tool for reasoning about adversaries is the **cyber kill chain**, which breaks an
intrusion into ordered stages, reconnaissance, weaponization, delivery, exploitation, installation,
command and control, and actions on objectives. Disrupting any single stage can defeat the whole
attack, which is the strategic basis for layered defense. The kill chain and the related MITRE ATT&CK
knowledge base are developed further in the chapters on penetration testing and detection.
'''))

A(md(r'''## 1.5 Defense in Depth and Security Controls

Because no single safeguard is perfect, sound security architecture relies on **defense in depth**:
multiple, overlapping, independent layers of control, so that the failure of any one layer does not
result in a breach. The metaphor is a medieval castle, with a moat, outer walls, inner walls,
a keep, and armed guards, so that an attacker who scales the wall still faces further obstacles. In a
modern enterprise the layers might include perimeter firewalls, network segmentation, host-based
protection, application hardening, encryption of data at rest and in transit, strong authentication,
continuous monitoring, and a trained, alert workforce. A closely related idea is **layered security**;
the two terms are often used synonymously, though purists distinguish defense in depth (diverse
controls across people, process, and technology) from layered security (multiple technical controls of
the same kind).

A **security control** (also called a *safeguard* or *countermeasure*) is any mechanism that reduces
risk. Controls are classified along two independent axes, and being fluent in this taxonomy is
essential both for examinations and for designing real defenses.

The first axis is the control's **type**, describing how it is implemented:

- **Administrative (managerial)** controls are policies, procedures, standards, training, and
  governance, the human and organizational rules that direct behavior.
- **Technical (logical)** controls are implemented in hardware and software: firewalls, encryption,
  access control lists, intrusion detection systems, and authentication mechanisms.
- **Physical** controls protect the tangible environment: locks, fences, badge readers, security
  guards, cameras, and mantraps.

The second axis is the control's **function**, describing what it does relative to an incident:

- **Preventive** controls stop an incident before it occurs (a firewall blocking traffic, a lock on
  a door, mandatory access control).
- **Detective** controls identify and signal an incident in progress or after the fact (intrusion
  detection systems, audit logs, security cameras, file-integrity monitoring).
- **Corrective** controls restore systems after an incident (restoring from backup, applying a patch,
  removing malware).
- **Deterrent** controls discourage an attacker from attempting an attack (warning banners, visible
  cameras, the credible threat of prosecution).
- **Compensating** controls provide an alternative when a primary control is not feasible (network
  isolation of a legacy system that cannot be patched).
- **Directive** controls instruct or mandate behavior (signage, acceptable-use policies).

A single safeguard can play several roles at once. A surveillance camera, for example, is
simultaneously *physical* in type, *detective* in that it records intrusions, and *deterrent* in that
its visible presence discourages them. When you encounter a control, practice classifying it on both
axes; this habit sharpens the analytical reasoning that examinations such as CISSP and Security+
reward, and it ensures that a real-world control set is balanced rather than, say, heavy on prevention
but lacking detection and recovery.
'''))
print("part B appended, total cells:", len(C))
import pickle; pickle.dump(C, open(".build/_ch01_cells.pkl","wb"))
