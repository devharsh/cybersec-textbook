import sys, pickle; sys.path.insert(0,".build")
from nbbuild import md, code
C=pickle.load(open(".build/_ch05.pkl","rb")); A=C.append

A(md(r'''## 5.4 Risk Identification

The lifecycle begins with identification, because a risk that is never identified can never be managed,
and the most dangerous risks are often the unknown ones. Identification has three intertwined activities:
inventorying and valuing assets, enumerating threats, and discovering vulnerabilities.

**Asset identification and valuation** comes first, because you cannot protect what you do not know you
have, and you cannot prioritize without knowing what each asset is worth. An asset inventory spans
hardware, software, data, people, facilities, and intangibles such as reputation and intellectual
property. Valuation may be quantitative (a replacement cost or revenue contribution in dollars) or
qualitative (a criticality rating), and it should reflect not just the asset's direct value but the
consequences of its loss, the stolen laptop whose real value is the unreleased product plans it holds.

**Threat identification** asks what could harm each asset. Threat sources are commonly grouped as
adversarial (the threat actors of Chapter 1, from script kiddies to nation-states), accidental (human
error), structural (equipment and software failure), and environmental (fire, flood, power loss).
Cataloguing threats is aided by threat intelligence, historical incident data, and structured threat
modeling, discussed in Section 5.8. **Vulnerability identification** asks where each asset is weak,
drawing on vulnerability scanning and penetration testing (Chapters 6 through 10), configuration reviews,
audits, and the absence of needed controls. The product of this stage is a *risk register*: a living
catalog that pairs assets with the threats and vulnerabilities that endanger them, ready for the
assessment stage to score and rank. The quality of everything that follows depends on the completeness of
this identification, which is why mature programs invest heavily in asset management and continuous
discovery.
'''))

A(md(r'''## 5.5 Qualitative Risk Assessment

Once risks are identified, they must be assessed so that limited resources flow to the most important
ones, and the faster, more flexible of the two assessment methods is the qualitative approach.
**Qualitative assessment** rates risk in relative terms, typically high, medium, and low, rather than in
precise figures. It is essentially structured, educated judgment, and its strengths are speed,
flexibility, and the ability to incorporate intangible factors such as reputation that resist a dollar
figure. Its weakness is subjectivity: two analysts may rate the same risk differently.

The mechanics are simple and rest on the core relationship that *risk equals likelihood times impact*.
Each risk is assigned a likelihood level (for example high, medium, or low, perhaps mapped to rough
probabilities) and an impact level (high meaning serious loss or business interruption, medium a moderate
or short-lived disruption, low mild damage). Combining the two on a **risk matrix** (also called a heat
map) yields a priority: a risk that is both highly likely and high impact lands in the red zone and
demands immediate attention, while a low-likelihood, low-impact risk lands in the green zone and may be
accepted. The matrix is valuable precisely because it communicates priorities visually to non-technical
decision-makers, turning a long list of risks into an at-a-glance picture. The code cell renders a
representative five-by-five risk matrix.
'''))

A(code(r'''# Chapter 5 -- A 5x5 qualitative risk matrix (likelihood x impact)
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

likelihood = ["Rare","Unlikely","Possible","Likely","Almost certain"]
impact     = ["Negligible","Minor","Moderate","Major","Severe"]
# score = (row index +1) * (col index +1); higher = worse
grid = np.array([[(r+1)*(c+1) for c in range(5)] for r in range(5)])

fig, ax = plt.subplots(figsize=(7.5, 5))
# color by score band
colors = np.empty(grid.shape, dtype=object)
for r in range(5):
    for c in range(5):
        s = grid[r, c]
        colors[r, c] = "#2ecc71" if s <= 4 else "#f1c40f" if s <= 9 else "#e67e22" if s <= 14 else "#e74c3c"
for r in range(5):
    for c in range(5):
        ax.add_patch(plt.Rectangle((c, r), 1, 1, facecolor=colors[r, c], edgecolor="white"))
        ax.text(c+0.5, r+0.5, str(grid[r, c]), ha="center", va="center", fontweight="bold")
ax.set_xticks(np.arange(5)+0.5); ax.set_xticklabels(impact, rotation=20)
ax.set_yticks(np.arange(5)+0.5); ax.set_yticklabels(likelihood)
ax.set_xlim(0,5); ax.set_ylim(0,5)
ax.set_xlabel("Impact"); ax.set_ylabel("Likelihood")
ax.set_title("Qualitative Risk Matrix (green=accept, red=urgent)")
plt.tight_layout(); plt.savefig("ch05_risk_matrix.png", dpi=110)
print("Saved ch05_risk_matrix.png  (score = likelihood rank x impact rank)")''' ))

A(md(r'''```{admonition} Knowledge Check
:class: hint
1. On a risk matrix, where does a risk that is "almost certain" but "negligible" in impact fall, and how
   should it generally be treated?
2. Why might an organization prefer qualitative assessment for a brand-new type of risk with no
   historical data?

*Answers:* (1) High likelihood but low impact lands in a low-to-moderate (often yellow/green) zone;
such risks are typically accepted or addressed with low-cost controls, not treated as emergencies. (2)
Qualitative assessment relies on expert judgment and does not require the historical frequency and loss
data that quantitative methods need, so it works when reliable numbers do not yet exist.
```

## 5.6 Quantitative Risk Assessment

Where qualitative assessment ranks risks in relative terms, **quantitative assessment** expresses them in
money, which is the language executives use to allocate budget, so the two methods are complementary and
often combined. The classic model, introduced in Chapter 1 and developed here, builds from a small chain
of defined quantities.

The **asset value (AV)** is the worth of the asset. The **exposure factor (EF)** is the percentage of
that value lost in a single incident; for a stolen laptop holding unencrypted personal data, the exposure
factor is 100 percent, because the device and all its data are gone. Their product is the **single loss
expectancy (SLE)**, the money lost from one occurrence: SLE equals AV times EF. The **annualized rate of
occurrence (ARO)** estimates how many times per year the event is expected, and multiplying gives the
**annualized loss expectancy (ALE)**: ALE equals SLE times ARO. The ALE is the pivotal figure, because it
states an expected yearly cost that can be compared directly against the annual cost of a control. When a
safeguard reduces the ALE by more than it costs to run, it is justified, a comparison captured by the
**return on security investment (ROSI)**. The code cell works a complete example, and the In-Class
Exercise that follows lets students compute their own.
'''))

A(code(r'''# Chapter 5 -- Quantitative risk: SLE, ARO, ALE, and a control's ROSI
def assess(asset_value, exposure_factor, aro):
    sle = asset_value * exposure_factor
    ale = sle * aro
    return sle, ale

# Example from a typical exam-style question
AV, EF, ARO = 100_000, 0.25, 3
SLE, ALE = assess(AV, EF, ARO)
print(f"Asset value (AV)         : ${AV:,.0f}")
print(f"Exposure factor (EF)     : {EF:.0%}")
print(f"Single loss expectancy   : ${SLE:,.0f}   (AV x EF)")
print(f"Annual rate (ARO)        : {ARO}")
print(f"Annualized loss expect.  : ${ALE:,.0f}   (SLE x ARO)\n")

# Evaluate a proposed control that cuts ARO from 3 to 0.5 and costs $30,000/yr
new_ARO = 0.5
control_cost = 30_000
_, ALE_after = assess(AV, EF, new_ARO)
benefit = ALE - ALE_after
rosi = (benefit - control_cost) / control_cost * 100
print(f"ALE after control        : ${ALE_after:,.0f}")
print(f"Annual benefit           : ${benefit:,.0f}")
print(f"Control cost             : ${control_cost:,.0f}")
print(f"ROSI                     : {rosi:.0f}%  -> {'JUSTIFIED' if rosi>0 else 'NOT justified'}")''' ))

A(md(r'''```{admonition} In-Class Exercise: run a quantitative assessment
:class: note
Individually or in pairs, pick one asset from your own life or a fictional company (for example a laptop,
a customer database, or an e-commerce server). Estimate its asset value, assign an exposure factor for a
specific threat (theft, ransomware, hardware failure), and estimate the annualized rate of occurrence.
Compute the SLE and ALE. Then propose one control, estimate its annual cost and its effect on the
exposure factor or rate of occurrence, and compute the ROSI to decide whether the control is justified.
Compare results across the class and discuss why estimates of ARO and EF vary so widely, and what that
implies about relying on quantitative figures alone.
```
'''))
print("part B:", len(C))
pickle.dump(C, open(".build/_ch05.pkl","wb"))
