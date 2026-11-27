import os
"""Identity security posture management (ISPM): the continuous posture loop and where ISPM fits.
One drawing, two label sets: the cybersecurity book (ch17) and the Bedrock book (bk)."""
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

LABELS = {
    "ch17_ispm_loop": {
        "title": "Identity security posture management: a continuous loop",
        "cards": [
            ("search", "Discover identities", ["people, service accounts,", "AI agents, OAuth grants"]),
            ("nodes", "Correlate a graph", ["one owner, many accounts;", "effective permissions"]),
            ("warning", "Find weak posture", ["dormant, orphaned, unused,", "toxic combos, no MFA"]),
            ("attacker", "Rank by exposure", ["attack paths to crown", "jewels, not alert count"]),
            ("gear", "Fix with guardrails", ["automate only low-risk,", "reversible hygiene"]),
            ("check", "Verify and repeat", ["confirm nothing broke,", "then scan again"]),
        ]},
    "bk_ispm_loop": {
        "title": "Identity security posture management for a Bedrock account",
        "cards": [
            ("search", "Discover identities", ["IAM users and roles,", "agent and tool identities"]),
            ("nodes", "Correlate a graph", ["trust policies, role", "chains, effective access"]),
            ("warning", "Find weak posture", ["unused roles and keys,", "unused actions, no MFA"]),
            ("attacker", "Rank by exposure", ["paths to models, data,", "and stored OAuth tokens"]),
            ("gear", "Fix with guardrails", ["automate only low-risk,", "reversible hygiene"]),
            ("check", "Verify and repeat", ["confirm nothing broke,", "then scan again"]),
        ]},
}
FIT = [
    ("checklist", "IGA", ["Who should have access?", "requests, approvals, reviews"], BLUE, "#eef5fc"),
    ("shield", "ISPM", ["Is identity posture risky now?", "continuous and preventive"], GREEN, "#edf7ee"),
    ("eye", "ITDR", ["Is an identity attack underway?", "detect and respond live"], RED, "#fdeeee"),
    ("chip", "AI-SPM", ["Are AI models and data exposed?", "models, pipelines, shadow AI"], PURPLE, "#f3eef9"),
]

def draw(name):
    L = LABELS[name]
    p = Fig(1180, 532, L["title"],
            "Identity security posture management runs as a continuous loop. Step 1 discovers every identity, "
            "including people, service accounts, AI agents, and OAuth grants. Step 2 correlates them into a graph of "
            "owners, accounts, and effective permissions. Step 3 finds weak posture such as dormant, orphaned, or "
            "unused access, toxic combinations, and missing MFA. Step 4 ranks findings by exposure, meaning attack "
            "paths to crown jewels, not by alert count. Step 5 fixes findings with guardrails, automating only "
            "low-risk, reversible hygiene. Step 6 verifies that nothing broke and scans again. Step 7 places ISPM "
            "among related tools: identity governance and administration asks who should have access, ISPM asks "
            "whether posture is risky now, identity threat detection and response asks whether an attack is "
            "underway, and AI security posture management asks whether AI models and data are exposed.")
    W, G, X0, Y0, H = 172, 22, 18, 52, 184
    xs = [X0 + i * (W + G) for i in range(6)]
    for i, (ic, head, sub) in enumerate(L["cards"]):
        x, col = xs[i], (ORANGE if i in (2, 3) else BLUE)
        fill = "#fff4e8" if i in (2, 3) else "#eef5fc"
        p.rect(x, Y0, W, H, fill, col, 2, rx=14, step=i + 1)
        p.icon(ic, x + W / 2, Y0 + 52, 50, step=i + 1)
        p.text(x + W / 2, Y0 + 112, head, 14, INK, "bold", step=i + 1)
        p.text(x + W / 2, Y0 + 138, sub[0], 12, MUTED, step=i + 1)
        p.text(x + W / 2, Y0 + 156, sub[1], 12, MUTED, step=i + 1)
        p.badge(i + 1, x + W - 20, Y0 + 20, step=i + 1, color=col)
        if i < 5:
            p.arrow([(x + W + 2, Y0 + H / 2), (xs[i + 1] - 2, Y0 + H / 2)], color=INK, step=i + 2, width=2.2)
    # loop back: continuous
    yb = Y0 + H + 22
    p.arrow([(xs[5] + W / 2, Y0 + H + 2), (xs[5] + W / 2, yb), (xs[0] + W / 2, yb), (xs[0] + W / 2, Y0 + H + 4)],
            color=GREEN, step=6, width=2.2, dash=True)
    p.text((xs[0] + xs[5] + W) / 2, yb - 6, "repeat continuously, not once a quarter", 12.5, GREEN, "bold", step=6)
    # 7: where ISPM fits
    zy = 284
    p.zone(18, zy, 1144, 230, "Where ISPM fits among related tools", color=INK, fill="#f6f7f9", step=7)
    BW, BG = 262, 22
    for j, (ic, head, sub, col, fill) in enumerate(FIT):
        bx = 38 + j * (BW + BG)
        p.rect(bx, zy + 40, BW, 172, fill, col, 2.5 if head == "ISPM" else 1.5, rx=12, step=7)
        p.icon(ic, bx + BW / 2, zy + 84, 46, step=7)
        p.text(bx + BW / 2, zy + 136, head, 15, col, "bold", step=7)
        p.text(bx + BW / 2, zy + 160, sub[0], 12.5, INK, step=7)
        p.text(bx + BW / 2, zy + 180, sub[1], 12, MUTED, step=7)
    p.badge(7, 1142, zy + 20, step=7, color=INK)
    p.save(OUT + name)

if __name__ == "__main__":
    for nm in LABELS: draw(nm)
    print("ok")
