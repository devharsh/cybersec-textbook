import os
"""Is this AI score prohibited social scoring? The EU AI Act Article 5(1)(c) test.
One drawing, two label sets: the cybersecurity book (ch17) and the Bedrock book (bk)."""
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

LABELS = {
    "ch17_social_scoring": {
        "title": "Is this AI score prohibited social scoring?",
        "banned": ("Banned", "Library fines and social media posts", "lower a resident's housing priority"),
        "allowed": ("Not banned, still regulated", "A bank's credit score from repayment", "history: high-risk, not prohibited")},
    "bk_social_scoring": {
        "title": "Is this AI score prohibited social scoring? A Bedrock view",
        "banned": ("Banned", "The tone of a customer's support chats", "is used to deny them a loan"),
        "allowed": ("Not banned, still regulated", "A loan assistant scores creditworthiness", "from financial data: high-risk")},
}

def card(p, x, w, color, fill, icon, lines, n, step):
    p.rect(x, 52, w, 214, fill, color, 2, rx=14, step=step)
    p.icon(icon, x + w / 2, 100, 52, step=step)
    y = 152
    for i, t in enumerate(lines):
        p.text(x + w / 2, y + i * 20, t, 14 if i == 0 else 12.5, INK if i == 0 else MUTED,
               "bold" if i == 0 else "normal", step=step)
    p.badge(n, x + w - 20, 72, step=step, color=color)

def draw(name):
    L = LABELS[name]
    p = Fig(1180, 520, L["title"],
            "A decision flow for Article 5(1)(c) of the EU AI Act. First, the system scores or classifies people over "
            "time from their social behavior or personal traits. Second, the score leads to worse treatment. Third, "
            "either the treatment happens in a context unrelated to where the data came from, or it is unjustified or "
            "disproportionate to the behavior. If both earlier steps hold and either third test is met, the practice "
            "has been prohibited since February 2, 2025, for public and private actors alike. If neither third test "
            "is met, the score is not banned but may still be high-risk, as credit scoring is, and GDPR Article 22 "
            "limits decisions based solely on it.")
    W, G, X0 = 262, 30, 18
    xs = [X0 + i * (W + G) for i in range(4)]
    card(p, xs[0], W, BLUE, "#eef5fc", "group", ["Scores people over time", "from social behavior or", "personal or personality traits"], 1, 1)
    card(p, xs[1], W, BLUE, "#eef5fc", "warning", ["Leads to worse treatment", "detrimental or unfavorable", "for the person or group"], 2, 2)
    # 3: the two alternative tests
    x = xs[2]
    p.rect(x, 52, W, 214, "#fff4e8", ORANGE, 2, rx=14, step=3)
    p.text(x + W / 2, 82, "Either test is enough", 14, ORANGE, "bold", step=3)
    p.rect(x + 14, 96, W - 28, 74, "#ffffff", ORANGE, 1.5, rx=8, step=3)
    p.text(x + W / 2, 122, "A. Unrelated context", 13.5, INK, "bold", step=3)
    p.text(x + W / 2, 142, "data from one setting used", 12.5, MUTED, step=3)
    p.text(x + W / 2, 158, "against the person in another", 12.5, MUTED, step=3)
    p.rect(x + 14, 180, W - 28, 74, "#ffffff", ORANGE, 1.5, rx=8, step=3)
    p.text(x + W / 2, 206, "B. Out of proportion", 13.5, INK, "bold", step=3)
    p.text(x + W / 2, 226, "unjustified or too harsh", 12.5, MUTED, step=3)
    p.text(x + W / 2, 242, "for the behavior or its gravity", 12.5, MUTED, step=3)
    p.badge(3, x + W - 20, 72, step=3, color=ORANGE)
    card(p, xs[3], W, RED, "#fdeeee", "cross", ["Prohibited: Art. 5(1)(c)", "since February 2, 2025,", "for public and private actors"], 4, 4)
    for i in range(3):
        p.arrow([(xs[i] + W + 3, 159), (xs[i + 1] - 3, 159)], color=INK, step=i + 2, width=2.2)
    p.text(xs[3] - 15, 150, "yes", 12, RED, "bold", step=4)
    # 5: neither test met, down to the regulated panel
    p.arrow([(xs[2] + W / 2, 266), (xs[2] + W / 2, 300), (430, 300), (430, 318)], color=GREEN, step=5, width=2.2)
    p.text(xs[2] + W / 2 + 8, 290, "neither", 12, GREEN, "bold", anchor="start", step=5)
    p.zone(18, 318, 560, 184, "Not banned, still regulated", color=GREEN, fill="#edf7ee", step=5)
    p.icon("bank", 64, 384, 44, step=5)
    p.text(98, 378, "Credit scoring is high-risk (Annex III),", 13.5, INK, "bold", anchor="start", step=5)
    p.text(98, 396, "with duties from December 2, 2027", 12.5, MUTED, anchor="start", step=5)
    p.icon("document", 64, 452, 44, step=5)
    p.text(98, 446, "GDPR Article 22 limits decisions", 13.5, INK, "bold", anchor="start", step=5)
    p.text(98, 464, "based solely on an automated score", 12.5, MUTED, anchor="start", step=5)
    p.badge(5, 558, 338, step=5, color=GREEN)
    # 6: two examples side by side
    p.zone(602, 318, 560, 184, "Two scores, two outcomes", color=INK, fill="#f6f7f9", step=6)
    b, a = L["banned"], L["allowed"]
    p.icon("cross", 640, 384, 34, step=6)
    p.text(668, 368, b[0], 13.5, RED, "bold", anchor="start", step=6)
    p.text(668, 386, b[1], 12.5, INK, anchor="start", step=6)
    p.text(668, 402, b[2], 12.5, INK, anchor="start", step=6)
    p.icon("check", 640, 452, 34, step=6)
    p.text(668, 436, a[0], 13.5, GREEN, "bold", anchor="start", step=6)
    p.text(668, 454, a[1], 12.5, INK, anchor="start", step=6)
    p.text(668, 470, a[2], 12.5, INK, anchor="start", step=6)
    p.badge(6, 1142, 338, step=6, color=INK)
    p.save(OUT + name)

if __name__ == "__main__":
    for nm in LABELS: draw(nm)
    print("ok")
