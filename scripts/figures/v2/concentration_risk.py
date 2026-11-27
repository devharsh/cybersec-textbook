import os
"""Concentration risk: many business processes depend on one foundation model.
One drawing, two label sets: the cybersecurity book (ch17) and the Bedrock book (bk)."""
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

LABELS = {
    "ch17_concentration_risk": {
        "title": "Concentration risk: many processes, one model",
        "procs": [("shield", "Alert triage"), ("envelope", "Phishing review"),
                  ("code", "Code review"), ("headset", "Customer chat")],
        "model": ("One model", "one provider"),
        "gate": ("Gateway", "routes and logs every call"),
        "primary": ("Primary model", "provider A"),
        "fallback": ("Tested fallback", "provider B"),
        "contract": ("Contract", "change notice, version pinning,", "exit plan")},
    "bk_concentration_risk": {
        "title": "Concentration risk in a Bedrock application",
        "procs": [("headset", "Support chatbot"), ("document", "Document summaries"),
                  ("money", "Claims triage"), ("code", "Code assistant")],
        "model": ("One model", "one provider, one Region"),
        "gate": ("Converse API", "the model ID is a setting"),
        "primary": ("Primary model", "cross-Region profile"),
        "fallback": ("Tested fallback", "another provider's model"),
        "contract": ("Lifecycle and contract", "watch Legacy notices,", "keep an exit plan")},
}

def proc_cards(p, x, w, procs, color, step):
    ys = [104, 190, 276, 362]
    for (ic, name), y in zip(procs, ys):
        p.rect(x, y, w, 62, "#ffffff", color, 2, rx=10, step=step)
        p.icon(ic, x + 32, y + 31, 38, step=step)
        p.text(x + 58, y + 36, name, 13.5, INK, "bold", anchor="start", step=step)
    return [y + 31 for y in ys]

def draw(name):
    L = LABELS[name]
    p = Fig(1180, 524, L["title"],
            "Two panels. Left: four business processes all call one model from one provider; an outage, a change, "
            "or a flaw in that model hits all four at once. Right: the same processes call a gateway that routes to a "
            "primary model and fails over to a tested fallback from another provider, with contract terms that give "
            "notice of changes and an exit plan.")
    # Left: concentrated
    p.zone(16, 50, 566, 458, "Concentrated: every process calls one model", color=RED, fill="#fdeeee", step=1)
    cys = proc_cards(p, 62, 210, L["procs"], RED, 1)
    mx, my = 470, 300
    for cy in cys:
        p.arrow([(276, cy), (mx - 52, my)], color=RED, step=1, width=2)
    p.icon("robot", mx, my, 84, label=L["model"][0], sub=L["model"][1], step=1, label_color=RED)
    p.badge(1, 276, 92, step=1, color=RED)
    # 2: one outage, change, or flaw at the shared model
    p.icon("warning", mx, 128, 50, step=2)
    p.text(mx, 178, "outage, change, or flaw", 13, RED, "bold", step=2)
    p.arrow([(mx, 188), (mx, my - 50)], color=RED, step=2, dash=True, width=2)
    p.badge(2, mx + 40, 112, step=2, color=RED)
    # 3: every process fails at once
    for cy in cys:
        p.icon("cross", 40, cy, 26, step=3)
    p.text(160, 456, "All four fail at the same time", 14, RED, "bold", step=3)
    p.text(160, 476, "because they share one dependency", 12.5, MUTED, step=3)
    p.badge(3, 40, 446, step=3, color=RED)

    # Right: reduced
    p.zone(598, 50, 566, 458, "Reduced: gateway, tested fallback, contract", color=GREEN, fill="#edf7ee", step=4)
    cys = proc_cards(p, 618, 206, L["procs"], GREEN, 4)
    gx, gy, bus = 930, 236, 846
    for cy in cys:   # each process joins one collector line, which feeds the gateway
        p.raw(f'<line x1="824" y1="{cy}" x2="{bus}" y2="{cy}" stroke="{GREEN}" stroke-width="2"/>', step=4)
    p.raw(f'<line x1="{bus}" y1="{cys[0]}" x2="{bus}" y2="{cys[-1]}" stroke="{GREEN}" stroke-width="2"/>', step=4)
    p.arrow([(bus, gy), (gx - 36, gy)], color=GREEN, step=4, width=2)
    p.icon("router", gx, gy, 64, label=L["gate"][0], sub=L["gate"][1], step=4, label_color=GREEN)
    p.badge(4, gx - 44, gy - 40, step=4, color=GREEN)
    # 5: primary and a tested fallback
    px, py1, py2 = 1080, 130, 318
    p.arrow([(gx + 34, gy - 14), (px - 34, py1 + 6)], color=GREEN, step=5, width=2.2)
    p.arrow([(gx + 34, gy + 14), (px - 34, py2 - 6)], color=GREEN, step=5, width=2.2, dash=True)
    p.text(gx + 88, gy + 26, "on failure", 12, GREEN, "bold", anchor="start", step=5)
    p.icon("robot", px, py1, 60, label=L["primary"][0], sub=L["primary"][1], step=5, label_color=GREEN, label_size=14)
    p.icon("robot", px, py2, 60, label=L["fallback"][0], sub=L["fallback"][1], step=5, label_color=GREEN, label_size=14)
    p.badge(5, px + 44, py2 - 36, step=5, color=GREEN)
    # 6: contract and lifecycle terms
    cx, cy0 = 1010, 440
    p.icon("document", cx - 92, cy0, 46, step=6)
    p.text(cx - 60, cy0 - 12, L["contract"][0], 14, GREEN, "bold", anchor="start", step=6)
    p.text(cx - 60, cy0 + 7, L["contract"][1], 12.5, MUTED, anchor="start", step=6)
    p.text(cx - 60, cy0 + 24, L["contract"][2], 12.5, MUTED, anchor="start", step=6)
    p.badge(6, cx - 120, cy0 - 26, step=6, color=GREEN)
    p.save(OUT + name)

if __name__ == "__main__":
    for nm in LABELS: draw(nm)
    print("ok")
