import sys, pickle; sys.path.insert(0,".build")
from nbbuild import md, code
C=[]; A=C.append

A(md(r'''# Chapter 5: Risk Management

> "Risk management is the identification, assessment, and prioritization of risks followed by the
> coordinated and economical application of resources to minimize, monitor, and control the probability
> or impact of unfortunate events." -- a working definition widely used in the profession

---

The previous four chapters surveyed threats, from broken ciphers to deceived employees. No organization
can defend against all of them at once, with unlimited budget and perfect coverage. Risk management is
the discipline that decides what to defend, how much to spend, and what to accept, turning the open-ended
catalog of threats into a prioritized, economically rational program. It is, in a real sense, the
management layer that sits above every technical control in this book, and it is tested heavily across
the CISSP, CISA, and CGRC certifications.

## Learning Objectives

After completing this chapter, you will be able to:

1. Define risk and its components, asset, threat, vulnerability, likelihood, and impact, and relate them.
2. Describe the risk-management lifecycle: identify, assess, treat, and monitor.
3. Perform qualitative risk assessment using likelihood and impact and a risk matrix.
4. Perform quantitative risk assessment using asset value (AV), exposure factor (EF), single loss
   expectancy (SLE), annualized rate of occurrence (ARO), annualized loss expectancy (ALE), and return
   on security investment (ROSI).
5. Select among the risk-treatment options: avoid, mitigate, transfer, and accept, and explain residual
   risk, risk appetite, and risk tolerance.
6. Apply threat-modeling methods such as STRIDE and attack trees.
7. Compare the major risk frameworks: the NIST Risk Management Framework (RMF), NIST Cybersecurity
   Framework (CSF) 2.0, ISO/IEC 27005 and 31000, and the FAIR model.
8. Explain business continuity and disaster recovery concepts, including business impact analysis (BIA),
   recovery time objective (RTO), and recovery point objective (RPO).

## Key Terms

- **Risk**: the likelihood that a threat exploits a vulnerability, combined with the resulting impact.
- **Asset**: anything of value to the organization that warrants protection.
- **Threat**: any agent or circumstance that could cause harm to an asset.
- **Vulnerability**: a weakness that a threat can exploit.
- **Likelihood**: the probability that a given threat exploits a given vulnerability.
- **Impact**: the magnitude of harm if the risk is realized.
- **Inherent risk**: risk before controls; **residual risk**: risk remaining after controls.
- **Risk appetite**: the amount of risk an organization is willing to pursue; **risk tolerance**: the
  acceptable variation around it.
- **ALE (Annualized Loss Expectancy)**: expected yearly loss from a risk, SLE multiplied by ARO.
- **RMF (Risk Management Framework)**: NIST's structured process for managing information-system risk.
- **BIA (Business Impact Analysis)**: analysis identifying critical functions and the impact of their
  disruption.
- **RTO / RPO (Recovery Time / Point Objective)**: maximum tolerable downtime / data loss.
'''))

A(md(r'''## 5.1 Risk as the Organizing Principle of Security

Chapter 1 introduced risk informally as probability times impact; this chapter develops it into the
central management discipline of the field. The reason risk management matters is the same reason
security is hard: resources are finite, threats are unlimited, and perfect security is impossible.
Spending must therefore be allocated where it does the most good, which requires a defensible way to
compare unlike dangers, a ransomware outbreak against a stolen laptop against a regulatory fine, on a
common scale. Risk management provides that scale and the process for acting on it.

A useful framing, drawn directly from professional practice, is that security is always a balance among
*security, functionality, and usability*: pushing hard toward one diminishes the others. A system locked
down to the point of being unusable provides no value, while one optimized purely for convenience invites
compromise. Finding the right balance requires knowing the organization's goals, understanding what
security means in that context, and being able to measure the threats. Risk management is the structured
way to strike and continually re-strike that balance as the organization, the technology, and the threat
landscape change.

Two further ideas frame the chapter. First, risk management is *continuous*, not a one-time project,
because assets, threats, and controls all change. Second, it operates at multiple levels: the technical
risk of a single system, the operational risk of a business process, and the strategic, enterprise risk
that boards and executives must own. Mature programs connect these levels, so that a vulnerability in a
server can be traced up to its business consequence and a board's risk appetite can be traced down to
concrete control decisions. We begin with the vocabulary that makes such reasoning precise.
'''))

A(md(r'''## 5.2 The Vocabulary of Risk

Precise terms are the prerequisite for measuring anything, so we sharpen the definitions Chapter 1
introduced. **Risk** is the probability that a threat will successfully exploit a vulnerability, together
with the resulting impact. It is built from three basic elements. An **asset** is any item of value, a
database, a server, a reputation, a business process, owned by the organization. A **threat** is any
agent, condition, or circumstance that could cause harm, loss, or compromise to an asset; from a security
perspective, threats are categorized by which property of the CIA triad they endanger. A **vulnerability**
is a weakness in design, implementation, code, or process, or the absence of a needed control, that a
threat can exploit. The **exploit**, though not strictly a component of risk, is the tool or technique by
which a threat acts on a vulnerability.

From these, two further quantities give risk its shape. **Likelihood** is the probability that a
particular threat exploits a particular vulnerability, influenced by the threat's capability and
motivation and by the presence or absence of countermeasures. **Impact** is the magnitude of harm if the
risk is realized, which may be measured in lost lives, dollars, reputation, market share, or disrupted
operations, and is commonly graded as high (serious loss or business interruption), medium (a short pause
or moderate loss), or low (mild damage with no interruption of critical processes). The core relationship,
which every risk method elaborates, is that **risk is a function of likelihood and impact**: a severe
consequence that is highly likely is a top priority, while a trivial consequence that is unlikely can
often be accepted.

Two refinements complete the vocabulary. *Inherent risk* is the risk present before any controls are
applied; *residual risk* is what remains after controls, and it is the residual risk that an organization
must consciously accept or further treat. *Risk appetite* expresses how much risk an organization is
willing to take in pursuit of its objectives, and *risk tolerance* the acceptable variation around that
level. These concepts turn risk from a vague worry into something an organization can state, measure, and
govern, which is the subject of the lifecycle that follows.
'''))

A(md(r'''## 5.3 The Risk-Management Lifecycle

Having defined risk, we need a repeatable process for managing it, because a one-time assessment ages the
moment it is finished. Although frameworks differ in their labels, virtually all describe the same cycle,
which the EC-Council, for example, renders as risk identification, assessment, treatment, tracking, and
review. We will use four core stages: identify, assess, treat, and monitor.

**Identify** establishes what could go wrong: cataloguing assets and their value, the threats that face
them, and the vulnerabilities through which those threats could act. **Assess** analyzes the identified
risks to determine their likelihood and impact, qualitatively, quantitatively, or both, and ranks them so
that attention flows to what matters most. **Treat** chooses and implements a response for each
significant risk, avoiding, mitigating, transferring, or accepting it, and records the residual risk that
remains. **Monitor** (and review) tracks the treated risks and the environment over time, verifying that
controls remain effective and re-running the cycle as assets, threats, and the business change.

```{mermaid}
graph LR
    A[Identify - assets, threats, vulnerabilities] --> B[Assess - likelihood x impact, prioritize]
    B --> C[Treat - avoid / mitigate / transfer / accept]
    C --> D[Monitor & Review - track residual risk, re-evaluate]
    D --> A
```

The loop is deliberate: risk management never ends, because the conditions it manages never stop
changing. The remaining sections follow this lifecycle in order, beginning with identification, then the
two assessment methods, then treatment, and then the frameworks and specialized areas, business
continuity and supply-chain risk, that apply the same cycle to particular problems.
'''))
print("part A:", len(C))
pickle.dump(C, open(".build/_ch05.pkl","wb"))
