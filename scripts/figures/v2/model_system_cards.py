import os
"""Model card versus system card: what the model is, and how the deployed system behaves.
One drawing, two label sets: the cybersecurity book (ch17) and the Bedrock book (bk)."""
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

LABELS = {
    "ch17_model_system_cards": {
        "title": "Model card versus system card",
        "pipe": [("user", "User", "input"), ("shield", "Input", "filter"), ("search", "Retrieval", "and tools"),
                 ("nodes", "Model", ""), ("shield", "Output", "filter"), ("browser", "Response", "")],
        "measured": ("Measured in use", "jailbreak rate, refusals, red-team findings, incidents"),
        "writer": "Written by whoever runs the system"},
    "bk_model_system_cards": {
        "title": "Model card versus system card for a Bedrock application",
        "pipe": [("user", "User", "input"), ("shield", "Guardrail", "input check"), ("search", "Knowledge", "base, tools"),
                 ("nodes", "Bedrock", "model"), ("shield", "Guardrail", "output check"), ("browser", "Response", "")],
        "measured": ("You own this card", "your prompts, guardrails, data, tools, and logs"),
        "writer": "Written by you, for your application"},
}

def draw(name):
    L = LABELS[name]
    p = Fig(1180, 540, L["title"],
            "Two panels. Left, a model card documents the model itself: its training data, its evaluations broken down "
            "by group, its intended and out-of-scope uses, and its known limitations. Right, a system card documents the "
            "deployed system, in which the model is one component in a pipeline from user input through filters, "
            "retrieval, and tools to the response, surrounded by monitoring, human oversight, policies, and deployment risks.")
    # 1: the model card
    p.zone(16, 50, 436, 474, "Model card: what the model is", color=BLUE, fill="#eef5fc", step=1)
    p.icon("nodes", 234, 118, 62, label="The model", sub="weights and architecture", step=1, label_color=BLUE)
    rows = [("database", "Training data", "sources, cutoff date, known gaps"),
            ("checklist", "Evaluations", "benchmarks, results broken down by group"),
            ("group", "Intended use", "who it is for, and out-of-scope uses"),
            ("warning", "Limitations and risks", "failure modes, biases, safety tests")]
    for i, (ic, t, sub) in enumerate(rows):
        y = 224 + i * 64
        p.rect(36, y - 26, 396, 54, "#ffffff", BLUE, 1.5, rx=8, step=1)
        p.icon(ic, 66, y + 1, 34, step=1)
        p.text(94, y - 3, t, 14, INK, "bold", anchor="start", step=1)
        p.text(94, y + 15, sub, 12, MUTED, anchor="start", step=1)
    p.text(234, 500, "Written by the model's developer", 13, BLUE, "bold", step=1)
    p.badge(1, 434, 70, step=1, color=BLUE)

    # 2: the system, with the model as one component
    p.zone(468, 50, 696, 474, "System card: how the deployed system behaves", color=GREEN, fill="#edf7ee", step=2)
    xs = [526 + i * 110 for i in range(6)]
    for i, (ic, a, b) in enumerate(L["pipe"]):
        big = ic == "nodes"
        p.icon(ic, xs[i], 128, 56 if big else 46, label=a, sub=b or None, step=2,
               label_color=GREEN if big else INK, label_size=13)
        if i < 5:
            p.arrow([(xs[i] + 30, 128), (xs[i + 1] - 30, 128)], color=GREEN, step=2, width=2)
    p.rect(xs[3] - 44, 86, 88, 120, "none", GREEN, 2, rx=10, step=2, dash=True)
    p.badge(2, 1144, 70, step=2, color=GREEN)
    # 3: what surrounds the model in use
    ctrls = [("eye", "Monitoring", "and logs"), ("user", "Human", "oversight"),
             ("document", "Policies and", "guardrails"), ("warning", "Deployment", "risks")]
    cx = [560 + i * 162 for i in range(4)]
    p.raw(f'<line x1="{cx[0]}" y1="252" x2="{cx[-1]}" y2="252" stroke="{GREEN}" stroke-width="2" stroke-dasharray="6 5"/>', step=3)
    p.raw(f'<line x1="{xs[3]}" y1="206" x2="{xs[3]}" y2="252" stroke="{GREEN}" stroke-width="2" stroke-dasharray="6 5"/>', step=3)
    for x, (ic, a, b) in zip(cx, ctrls):
        p.raw(f'<line x1="{x}" y1="252" x2="{x}" y2="276" stroke="{GREEN}" stroke-width="2" stroke-dasharray="6 5"/>', step=3)
        p.icon(ic, x, 306, 44, label=a, sub=b, step=3, label_size=13)
    p.badge(3, 1144, 262, step=3, color=GREEN)
    # 4: measured in use, and who writes it
    p.rect(490, 418, 652, 62, "#ffffff", GREEN, 1.5, rx=8, step=4)
    p.icon("checklist", 522, 449, 34, step=4)
    p.text(552, 444, L["measured"][0], 14, GREEN, "bold", anchor="start", step=4)
    p.text(552, 463, L["measured"][1], 12.5, MUTED, anchor="start", step=4)
    p.text(816, 506, L["writer"], 13, GREEN, "bold", step=4)
    p.badge(4, 1144, 410, step=4, color=GREEN)
    p.save(OUT + name)

if __name__ == "__main__":
    for nm in LABELS: draw(nm)
    print("ok")
