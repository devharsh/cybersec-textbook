import sys, pickle; sys.path.insert(0,".build")
from nbbuild import md, code
C=pickle.load(open(".build/_ch05.pkl","rb")); A=C.append

A(md(r'''## 5.7 Risk Treatment

Assessment tells us which risks matter; treatment decides what to do about them, which is where risk
management becomes action. For every significant risk, an organization chooses among four classic
responses, and the art lies in matching the response to the risk's likelihood, impact, and cost to
address.

**Risk avoidance** eliminates the risk by not engaging in the activity that creates it, declining to
collect sensitive data the organization does not need, or discontinuing a risky product line. Avoidance
removes the risk entirely but also forgoes whatever benefit the activity offered, so it suits risks whose
potential harm outweighs their value. **Risk mitigation (reduction)** applies controls to lower the
likelihood or impact to an acceptable level; this is the most common response and encompasses nearly
every technical and administrative control in this book. **Risk transfer (sharing)** shifts the financial
consequence to a third party, most commonly through cyber-insurance, or by outsourcing a function to a
provider contractually responsible for it; transfer addresses the impact but not the underlying
likelihood, and it never transfers reputational harm or, usually, legal accountability. **Risk
acceptance** consciously decides to bear a risk, appropriate when the cost of treatment exceeds the
expected loss or when the residual risk falls within the organization's risk appetite; crucially,
acceptance must be a documented, authorized decision, not mere inaction.

Two ideas govern these choices. First, no treatment reduces risk to zero, so what remains after controls
is **residual risk**, which must be explicitly accepted by an appropriate authority, the formal sign-off
that the authorization step of the NIST RMF (Section 5.9) makes concrete. Second, treatment decisions are
bounded by the organization's **risk appetite and tolerance**: a risk within appetite may simply be
accepted, while one beyond tolerance must be avoided, mitigated, or transferred until it fits. Good risk
treatment is therefore not about eliminating risk but about deliberately, and accountably, choosing which
risks to keep.
'''))

A(md(r'''## 5.8 Threat Modeling

Risk identification and assessment become far more rigorous when they are driven by a structured way of
imagining how a system could be attacked, which is the purpose of threat modeling. **Threat modeling** is
an engineering technique for systematically identifying threats, attacks, vulnerabilities, and
countermeasures that could affect a system, ideally performed early and repeatedly during design rather
than bolted on afterward. A common five-step formulation is to define security requirements, create a
diagram of the application and its data flows, identify threats, mitigate them, and validate that the
mitigations work; the EC-Council renders the phases as identifying security objectives, building an
application overview, decomposing the application, identifying threats, and identifying vulnerabilities.

Several methodologies structure the threat-identification step. **STRIDE**, developed at Microsoft, is a
mnemonic for six threat categories: Spoofing (impersonation, countered by authentication), Tampering
(unauthorized modification, countered by integrity controls), Repudiation (denying an action, countered
by non-repudiation and logging), Information disclosure (countered by confidentiality), Denial of service
(countered by availability controls), and Elevation of privilege (countered by authorization). Walking a
data-flow diagram and asking which STRIDE threats apply to each element is a powerful, repeatable habit.
Other approaches include **DREAD** (a rating scheme: Damage, Reproducibility, Exploitability, Affected
users, Discoverability), **PASTA** (the Process for Attack Simulation and Threat Analysis, a risk-centric
seven-stage method), and **attack trees**, which decompose an attacker's goal into the sub-goals and
steps needed to achieve it.

```{mermaid}
graph TD
    G[Attacker goal: steal customer data] --> A[Compromise web app]
    G --> B[Compromise database directly]
    G --> C[Phish an administrator]
    A --> A1[SQL injection]
    A --> A2[Exploit unpatched component]
    B --> B1[Exposed port / weak credentials]
    C --> C1[Spear-phishing email]
    C --> C2[Vishing the help desk]
```

The attack tree above shows how a single objective branches into multiple paths, each of which threat
modeling then assesses and mitigates. Threat modeling is itself an element of risk management: it feeds
the identification and assessment stages with a disciplined, attacker's-eye inventory of what could go
wrong, ensuring the risk register reflects realistic attack paths rather than a generic checklist.
'''))

A(md(r'''## 5.9 Risk Frameworks and Standards

Organizations rarely invent risk processes from scratch; they adopt established frameworks that encode
good practice, provide a common language, and satisfy auditors and regulators. Because the certifications
this book targets test these frameworks directly, we survey the most important, noting that deeper
governance treatment appears in Chapter 19.

The **NIST Risk Management Framework (RMF)**, defined in NIST Special Publication 800-37, gives U.S.
federal systems (and many others) a seven-step lifecycle: Prepare, Categorize the system and its data,
Select controls, Implement them, Assess their effectiveness, Authorize the system to operate (the formal
acceptance of residual risk by a senior official), and Monitor continuously. It is supported by NIST
SP 800-30 (conducting risk assessments) and SP 800-39 (organization-wide risk management), and it is the
backbone of the CGRC certification, whose practice areas map almost one-to-one onto the RMF steps. The
**NIST Cybersecurity Framework (CSF) 2.0**, updated in 2024, organizes activity into six functions,
Govern, Identify, Protect, Detect, Respond, and Recover, and is widely used across sectors as a
flexible, outcome-based way to assess and communicate cybersecurity posture.

International standards play the same role globally. **ISO/IEC 27005** provides guidance specifically on
information-security risk management within the broader **ISO/IEC 27001** Information Security Management
System (ISMS), against which organizations seek accredited certification, while **ISO 31000** offers
generic, enterprise-wide risk-management principles applicable beyond information technology. For
organizations that want rigorous *quantitative* risk analysis, the **FAIR (Factor Analysis of Information
Risk)** model decomposes risk into measurable factors, loss event frequency and loss magnitude and their
sub-components, to produce defensible, probabilistic loss estimates rather than simple high-medium-low
ratings. Related governance and control frameworks, COBIT for IT governance, and control catalogs such as
NIST SP 800-53 and the CIS Critical Security Controls, connect risk decisions to specific safeguards.
The practical point is not to memorize every framework but to recognize that they all implement the same
identify-assess-treat-monitor lifecycle, differing mainly in scope, sector, and rigor, so an organization
chooses the one that fits its regulatory context and maturity.
'''))
print("part C:", len(C))
pickle.dump(C, open(".build/_ch05.pkl","wb"))
