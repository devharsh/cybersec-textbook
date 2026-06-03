import sys, pickle; sys.path.insert(0,".build")
from nbbuild import md, code
C = pickle.load(open(".build/_ch01_cells.pkl","rb"))
A = C.append

A(md(r'''## 1.6 Hardware Foundations: Rings, Modes, and the Trusted Computing Base

Security is not only a matter of policy and software; it rests on a foundation built into the
processor itself. Modern CPUs enforce **protection rings**, hierarchical privilege levels that
constrain what code is allowed to do. On the x86 architecture there are four rings numbered 0 through
3, drawn as concentric circles in which the innermost ring is the most privileged.

```{mermaid}
graph TD
    subgraph Privilege Levels
    R0["Ring 0 - Kernel: full hardware access, all instructions"]
    R1["Ring 1 - Device drivers (rarely used)"]
    R2["Ring 2 - Device drivers (rarely used)"]
    R3["Ring 3 - User applications: restricted, no direct hardware"]
    end
    R3 -->|system call / trap| R0
    R0 -->|returns result| R3
```

In practice most operating systems use only two of these levels: **kernel mode** (ring 0), where the
operating-system core runs with unrestricted access to memory and hardware, and **user mode** (ring 3),
where ordinary applications run with sharply limited privileges. A user-mode program cannot directly
touch hardware, access another process's memory, or execute privileged instructions. When it needs the
kernel to do something on its behalf, such as reading a file or sending a network packet, it makes a
**system call**, a controlled transition that traps into kernel mode, performs the privileged operation
under the kernel's supervision, and returns. This boundary is the single most important security
mechanism in a general-purpose computer: it is what stops a buggy or malicious application from simply
taking over the machine.

The ring model has been extended over time. Hardware virtualization introduced a conceptual "ring -1"
for the hypervisor that runs beneath guest operating systems, and platform firmware and management
engines occupy still deeper, more privileged levels sometimes informally called "ring -2" and
"ring -3." Each deeper layer is more powerful and, if compromised, more catastrophic, which is why
firmware and hypervisor security have become major concerns. Attackers, for their part, constantly seek
**privilege escalation**: techniques to cross a ring boundary, moving from user mode into kernel mode,
or from a guest virtual machine into the hypervisor, in order to gain control the system never intended
to grant. Privilege escalation is examined in detail in the chapter on exploitation.

Two further concepts formalize these ideas. The **trusted computing base (TCB)** is the complete set of
hardware, firmware, and software components that are critical to enforcing the system's security policy.
Everything inside the TCB must be trusted, because a flaw anywhere within it can undermine the whole
system; a central design goal is therefore to keep the TCB as small and as carefully verified as
possible. The **reference monitor** is the abstract concept of a component that mediates *every* access
by a subject (a user or process) to an object (a file, device, or memory region), checking each against
the security policy. To be effective a reference monitor must be *tamper-proof*, *always invoked*
(non-bypassable), and *small enough to be thoroughly analyzed and verified*. The concrete implementation
of the reference monitor is called the **security kernel**. These principles, defense built into the
lowest layers, a minimal trusted base, and complete mediation, recur throughout secure system design,
from operating-system kernels to the trusted execution environments discussed in the chapter on
emerging topics.
'''))

A(md(r'''## 1.7 The NIST Cybersecurity Framework

Frameworks give organizations a shared vocabulary and a structured way to organize their security
efforts. The most widely adopted in the United States, and increasingly internationally, is the **NIST
Cybersecurity Framework (CSF)**. Originally published in 2014 for critical-infrastructure operators,
the framework was substantially revised as **CSF 2.0** in 2024 and is now intended for organizations of
every size and sector. Its core organizes all cybersecurity activity into a small number of high-level
*functions*, each broken down into categories and subcategories of outcomes.

The original framework defined five functions. CSF 2.0 added a sixth, **Govern**, which now sits at the
center and informs all the others:

- **Govern (GV)**: establish and monitor the organization's cybersecurity risk-management strategy,
  expectations, policy, roles, and oversight. This function, new in 2.0, recognizes that cybersecurity
  is an enterprise risk to be managed at the leadership level, not merely a technical concern.
- **Identify (ID)**: develop an understanding of the organization's assets, data, systems, suppliers,
  and the risks to them. You cannot protect what you do not know you have.
- **Protect (PR)**: implement safeguards to ensure delivery of critical services, access control, data
  security, awareness training, and maintenance.
- **Detect (DE)**: implement activities to identify the occurrence of a cybersecurity event in a
  timely manner, through continuous monitoring and detection processes.
- **Respond (RS)**: take action once an incident is detected, including response planning, analysis,
  containment, and communication.
- **Recover (RC)**: restore capabilities and services impaired by an incident, and incorporate lessons
  learned into future resilience.

Read in sequence, the functions trace the natural life of risk management: you *govern* the program,
*identify* what matters and what threatens it, *protect* it, *detect* attacks that slip through,
*respond* to contain them, and *recover* to normal operation while improving. This book is organized so
that each function is developed in depth: identification and risk in Chapters 1 and 5, protection in
Chapters 2, 3, and 11, detection in Chapter 12, response in Chapter 14, recovery in Chapters 13 and 14,
and governance in Chapters 5 and 19. Other frameworks, including ISO/IEC 27001, COBIT, and the CIS
Critical Security Controls, serve similar organizing roles and are discussed in the governance chapter.
'''))

A(md(r'''## 1.8 Quantifying Risk in Monetary Terms

Because security competes with every other organizational priority for finite budget, professionals
must be able to express risk in the language executives understand: money. The classic **quantitative
risk model** does exactly this with a small set of formulas.

The starting point is the **asset value (AV)**, the worth of the asset at risk. The **exposure factor
(EF)** is the percentage of that value expected to be lost in a single incident, expressed as a
fraction between 0 and 1. Their product is the **single loss expectancy (SLE)**, the money lost from one
occurrence:

$$ \text{SLE} = \text{AV} \times \text{EF} $$

The **annualized rate of occurrence (ARO)** is the expected number of incidents per year (which may be
a fraction, such as 0.3 for an event expected once every three-plus years). Multiplying SLE by ARO
gives the **annualized loss expectancy (ALE)**, the expected yearly cost of the risk:

$$ \text{ALE} = \text{SLE} \times \text{ARO} = \text{AV} \times \text{EF} \times \text{ARO} $$

The ALE is the single most useful number in risk economics, because it can be compared directly against
the annual cost of a control. If a safeguard reduces the ALE by more than it costs to operate, it is
financially justified. This is captured by the **return on security investment (ROSI)**:

$$ \text{ROSI} = \frac{(\text{ALE}_{\text{before}} - \text{ALE}_{\text{after}}) - \text{Cost}_{\text{control}}}{\text{Cost}_{\text{control}}} $$

A positive ROSI means the control saves more than it costs; a negative ROSI means the organization
would, on average, spend more on the safeguard than it expects to lose without it. These figures are
estimates built on uncertain inputs, and they should inform judgment rather than replace it, but they
impose valuable discipline on security spending. The worked example below computes these values for a
realistic scenario and visualizes the effect of a control.
'''))

A(code(r'''# Chapter 1 -- Worked Example: quantitative risk (SLE, ARO, ALE, ROSI)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# --- Scenario: a customer database faces a breach risk ---
asset_value      = 500_000     # value of the customer database, USD
exposure_factor  = 0.40        # 40% of value lost in a typical breach
aro              = 0.30        # expected 0.30 breaches per year (~once every 3+ years)

sle = asset_value * exposure_factor
ale_before = sle * aro

# A monitoring + encryption + patching programme
control_cost = 20_000          # annual operating cost
residual_factor = 0.15         # control cuts expected loss to 15% of original
ale_after = ale_before * residual_factor
benefit = ale_before - ale_after
rosi = (benefit - control_cost) / control_cost * 100

print("=== Quantitative Risk Assessment ===")
print(f"  Asset value (AV)        : ${asset_value:>12,.0f}")
print(f"  Exposure factor (EF)    : {exposure_factor:>12.0%}")
print(f"  Single loss expect (SLE): ${sle:>12,.0f}")
print(f"  Annual rate (ARO)       : {aro:>12.2f}")
print(f"  ALE before control      : ${ale_before:>12,.0f}")
print(f"  ALE after control       : ${ale_after:>12,.0f}")
print(f"  Annual control cost     : ${control_cost:>12,.0f}")
print(f"  Annual net benefit      : ${benefit - control_cost:>12,.0f}")
print(f"  ROSI                    : {rosi:>11.1f}%")
print(f"  Decision                : {'JUSTIFIED' if rosi > 0 else 'NOT justified'}")

fig, ax = plt.subplots(figsize=(7, 4))
bars = ax.bar(["ALE before", "ALE after", "Control cost"],
              [ale_before, ale_after, control_cost],
              color=["#c0392b", "#27ae60", "#2980b9"])
ax.set_ylabel("Annual cost (USD)")
ax.set_title("Effect of a Security Control on Annualized Loss Expectancy")
for b in bars:
    ax.text(b.get_x() + b.get_width()/2, b.get_height(),
            f"${b.get_height():,.0f}", ha="center", va="bottom", fontsize=9)
plt.tight_layout()
plt.savefig("ch01_risk.png", dpi=110)
print("\\nFigure saved: ch01_risk.png")''' ))
print("part C appended, total cells:", len(C))
import pickle; pickle.dump(C, open(".build/_ch01_cells.pkl","wb"))
