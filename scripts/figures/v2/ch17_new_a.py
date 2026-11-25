import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# Redraw: agent access
g = Fig(1100, 520, "Two ways an AI agent can reach a bank account",
        "The customer asks an AI agent to act. Upper path: the customer shares the password, the agent logs in as the customer, and the "
        "bank sees the customer with full read and write and cannot reliably tell the agent from the user. Lower path: the customer "
        "grants consent, the agent gets a delegated token that is named, scoped, and revocable, and the bank sees this agent with "
        "read-only access or payments with approval, cut off by revoking. A hidden instruction in a web page or email can steer either "
        "agent; only the lower path limits what the agent can then do.")
g.icon("user", 100, 250, 90, "Customer", "asks an AI agent to act")
g.icon("robot", 420, 120, 84, "Agent with the password", "logs in as the customer", step=1); g.icon("key", 470, 80, 30, step=1)
g.arrow([(146, 228), (370, 130)], None, RED, step=1, width=2.6); g.text(220, 160, "shares password", 13, RED, "bold", step=1)
g.icon("bank", 820, 120, 84, "Bank sees: the customer", "full read and write; cannot\nreliably tell agent from user", step=2)
g.arrow([(470, 120), (770, 120)], None, RED, step=2, width=2.6); g.icon("warning", 620, 90, 28, step=2)
g.badge(1, 168, 196, step=1, color=RED); g.badge(2, 700, 70, step=2, color=RED)
g.icon("robot", 420, 380, 84, "Agent with a delegated token", "named, scoped, revocable", step=3); g.icon("idcard", 470, 340, 32, step=3)
g.arrow([(146, 272), (370, 370)], None, GREEN, step=3, width=2.6); g.text(220, 345, "grants consent", 13, GREEN, "bold", step=3)
g.icon("bank", 820, 380, 84, "Bank sees: this agent", "read-only, or payments with\napproval; cut off by revoking", step=4)
g.arrow([(470, 380), (770, 380)], None, GREEN, step=4, width=2.6); g.icon("check", 620, 350, 28, step=4)
g.badge(3, 168, 304, step=3, color=GREEN); g.badge(4, 700, 330, step=4, color=GREEN)
g.icon("browser", 600, 250, 50, step=5); g.icon("devil", 624, 230, 22, step=5); g.badge(5, 560, 230, step=5, color=ORANGE)
g.text(650, 256, "a hidden instruction can steer either agent;", 13, ORANGE, "bold", "start", step=5)
g.text(650, 274, "only the lower path limits the damage", 13, ORANGE, "bold", "start", step=5)
g.save(OUT + "ch17_agent_access_v2")

# Redraw: LiteLLM timeline
t = Fig(1100, 620, "LiteLLM 2026: months of exposure, minutes of compromise, hours of exposure again",
        "May 27: a master key is committed to a public repository, force-pushed over, never revoked. October 10 at 21:27 UTC the key "
        "returns an organization owner's GitHub token, not scoped down; at 22:11 workflow runs send more maintainer tokens to an "
        "outside endpoint. Eleven days later, October 21 from 10:08 to 11:40, branch protection is overridden and a release is built "
        "from the fork Berri-AI/litellm; from 11:39 to 11:47 signed wheels reach PyPI and images reach Docker Hub and GHCR, including "
        "latest; about 11:47 Socket flags the wheels, about seven minutes after publication; from 13:23 to 14:20 PyPI is frozen and "
        "tags are pulled, live about two hours; from 16:20 to 17:01 stolen AWS credentials are tested, consistent with LLMjacking.")
left = [("May 27", "master key committed to a public", "repository; force-pushed over, never revoked", "key", ORANGE),
        ("Oct 10, 21:27 UTC", "the key returns an organization", "owner's GitHub token, not scoped down", "idcard", ORANGE),
        ("Oct 10, 22:11 UTC", "workflow runs send more", "maintainer tokens to an outside endpoint", "gear", ORANGE)]
right = [("Oct 21, 10:08 to 11:40", "branch protection overridden; release", "built from the fork Berri-AI/litellm", "code", BLUE),
         ("11:39 to 11:47", "signed wheels on PyPI; images on", "Docker Hub and GHCR, including latest", "bug", RED),
         ("about 11:47", "Socket flags the wheels,", "about seven minutes after publication", "eye", BLUE),
         ("13:23 to 14:20", "PyPI frozen, tags pulled:", "live about two hours", "lock", BLUE),
         ("16:20 to 17:01", "stolen AWS credentials tested,", "consistent with LLMjacking (Wiz)", "cloud", RED)]
for i, (when, a, b, ic, col) in enumerate(left):
    y = 70 + i * 150; st = i + 1
    t.rect(30, y, 420, 110, "#ffffff", col, 2.2, rx=10, step=st); t.icon(ic, 78, y + 55, 50, step=st)
    t.text(270, y + 34, when, 15, col, "bold", step=st); t.text(270, y + 60, a, 13, INK, step=st); t.text(270, y + 80, b, 13, INK, step=st)
    t.badge(st, 30, y, step=st, color=col)
    if i: t.arrow([(240, y - 38), (240, y - 2)], None, col, step=st, width=2.4)
for i, (when, a, b, ic, col) in enumerate(right):
    y = 60 + i * 108; st = 4 + i
    t.rect(560, y, 510, 88, "#ffffff", col, 2.2, rx=10, step=st); t.icon(ic, 604, y + 44, 44, step=st)
    t.text(840, y + 28, when, 14, col, "bold", step=st); t.text(840, y + 50, a, 12, INK, step=st); t.text(840, y + 68, b, 12, INK, step=st)
    t.badge(st, 560, y, step=st, color=col)
    if i: t.arrow([(815, y - 18), (815, y - 2)], None, col, step=st, width=2.2)
t.arrow([(452, 400), (556, 104)], None, MUTED, step=4, width=2.4); t.raw('<text x="492" y="250" font-family="Helvetica, Arial, sans-serif" font-size="14" font-weight="bold" fill="#52606d" text-anchor="middle" transform="rotate(-70 492 250)">11 days</text>', step=4)
t.save(OUT + "ch17_litellm_timeline_v2")

# Redraw: ML detection comparison
m = Fig(1100, 540, "Why learning-based detection complements signatures (illustrative numbers)",
        "Illustrative detection rates. Pattern matching: 97 percent on known threats, 10 percent on novel ones. Machine learning: 93 "
        "and 62 percent. Deep learning: 95 and 74 percent. Signatures excel on known threats but miss novel ones; learned models "
        "generalize better.")
meth = [("Pattern matching", "search", 0.97, 0.10), ("Machine learning", "nodes", 0.93, 0.62), ("Deep learning", "chip", 0.95, 0.74)]
X0, Y0, H = 140, 450, 340
m.raw(f'<line x1="{X0}" y1="{Y0}" x2="1040" y2="{Y0}" stroke="#52606d" stroke-width="2"/>')
for v in (0, .25, .5, .75, 1.0):
    yy = Y0 - v * H; m.raw(f'<line x1="{X0}" y1="{yy:.0f}" x2="1040" y2="{yy:.0f}" stroke="#eef0f2"/>'); m.text(X0 - 10, yy + 4, f"{v:.0%}", 12, MUTED, anchor="end")
for i, (name, ic, k_, n_) in enumerate(meth):
    cx = 290 + i * 290
    m.icon(ic, cx, Y0 + 40, 44, step=i + 1); m.text(cx, Y0 + 80, name, 15, INK, "bold", step=i + 1)
    for j, (v, col, lab) in enumerate([(k_, "#2e86c1", "known"), (n_, "#e67e22", "novel")]):
        x = cx - 92 + j * 96
        m.rect(x, Y0 - v * H, 88, v * H, col, col, 1, rx=4, step=i + 1); m.text(x + 44, Y0 - v * H - 8, f"{v:.0%}", 14, INK, "bold", step=i + 1)
    m.badge(i + 1, cx - 120, Y0 - 0.97 * H - 30, step=i + 1)
for j, (col, lab) in enumerate([("#2e86c1", "Known threats"), ("#e67e22", "Novel (zero-day) threats")]):
    m.rect(400 + j * 200, 58, 22, 16, col, col, 1, rx=3); m.text(430 + j * 200, 71, lab, 13, INK, "bold", "start")
m.save(OUT + "ch17_ml_detection_v2")

# New: detection pipeline (mermaid companion)
p = Fig(1100, 460, "Three ways to turn raw data into an alert, and the analyst loop that improves them",
        "Raw data such as emails, files, logs, and flows feeds pattern matching with signatures, regular expressions, and YARA; "
        "machine learning, which turns features into a model and a prediction; and deep learning, where a neural network learns its own "
        "features. All three raise an alert or a classification for analyst triage, and the analyst's feedback updates rules and "
        "retrains models.")
p.icon("database", 90, 220, 80, "Raw data", "emails, files,\nlogs, flows", step=1)
ap = [("search", "Pattern matching", "signatures, regex, YARA", 110), ("nodes", "Machine learning", "features -> model -> prediction", 220), ("chip", "Deep learning", "network learns its own features", 330)]
for i, (ic, name, sub, y) in enumerate(ap):
    p.rect(260, y - 40, 340, 80, "#ffffff", BLUE, 2, rx=8, step=2 + i); p.icon(ic, 300, y, 44, step=2 + i)
    p.text(336, y - 4, name, 15, BLUE, "bold", "start", step=2 + i); p.text(336, y + 16, sub, 12, INK, anchor="start", step=2 + i)
    p.arrow([(130, 220), (256, y)], None, BLUE, step=2 + i, width=1.8); p.arrow([(602, y), (706, 220)], None, BLUE, step=2 + i, width=1.8)
    p.badge(2 + i, 260, y - 40, step=2 + i)
p.icon("warning", 750, 220, 60, "Alert or", "classification", step=5); p.icon("user", 950, 220, 70, "Analyst triage", step=6)
p.arrow([(784, 220), (908, 220)], None, ORANGE, step=6, width=2.6); p.badge(5, 720, 160, step=5, color=ORANGE); p.badge(6, 990, 160, step=6, color=ORANGE)
p.arrow([(950, 270), (950, 420), (430, 420), (430, 372)], "feedback: retrain models, update rules", GREEN, step=7, dash=True, width=2.4, label_at=.36)
p.badge(7, 690, 420, step=7, color=GREEN)
p.save(OUT + "ch17_detection_pipeline")

# New: harvest now, decrypt later
h = Fig(1100, 460, "Harvest now, decrypt later: today's traffic, tomorrow's quantum computer",
        "Today an adversary records encrypted traffic protected by RSA or ECC key exchange and stores it. Years later, a large "
        "fault-tolerant quantum computer running Shor's algorithm breaks the key exchange, and the stored traffic is read. Secrets "
        "that stay sensitive for 10 to 15 years, such as state secrets, health data, and legal records, are at risk now, which is why "
        "migration to ML-KEM, ML-DSA, and SLH-DSA starts before quantum computers arrive.")
h.text(280, 70, "Today", 18, BLUE, "bold"); h.text(830, 70, "In 10 to 15 years?", 18, PURPLE, "bold")
h.raw('<line x1="550" y1="60" x2="550" y2="330" stroke="#d0d6dd" stroke-width="2" stroke-dasharray="6 6"/>')
h.icon("laptop", 90, 180, 70, "Hospital"); h.icon("server", 450, 180, 70, "Records service")
h.arrow([(130, 170), (410, 170)], "TLS with RSA or ECC key exchange", BLUE, step=1, size=12, width=2.6, both=True); h.icon("lock", 270, 196, 26, step=1)
h.badge(1, 140, 140, step=1)
h.icon("attacker", 270, 290, 60, "Adversary records", step=2); h.arrow([(270, 210), (270, 256)], None, RED, step=2, dash=True, width=2)
h.icon("database", 420, 300, 54, "stored ciphertext", step=2, label_size=12); h.arrow([(304, 290), (390, 296)], None, RED, step=2, width=2)
h.badge(2, 220, 260, step=2, color=RED)
h.icon("chip", 700, 180, 80, "Fault-tolerant", "quantum computer", step=3); h.text(700, 270, "Shor's algorithm", 13, PURPLE, "bold", step=3); h.badge(3, 650, 130, step=3, color=PURPLE)
h.arrow([(450, 300), (640, 200)], None, PURPLE, step=3, width=2.2, dash=True)
h.icon("document", 920, 180, 70, "Readable records", step=4); h.arrow([(744, 180), (880, 180)], "key broken", RED, step=4, size=12, width=2.6)
h.badge(4, 870, 130, step=4, color=RED)
h.rect(30, 360, 1040, 80, "#e8f5e9", GREEN, 1.6, rx=8, step=5); h.icon("shield", 66, 400, 40, step=5); h.badge(5, 30, 360, step=5, color=GREEN)
h.text(100, 394, "Long-lived secrets are exposed today. Migrate key exchange to ML-KEM (often hybrid with X25519) and", 13, GREEN, "bold", "start", step=5)
h.text(100, 416, "signatures to ML-DSA or SLH-DSA, starting with data that must stay secret the longest.", 13, GREEN, "bold", "start", step=5)
h.save(OUT + "ch17_hndl")

# New: federated and split learning
f = Fig(1100, 520, "Training without pooling the data: federated learning and split learning",
        "Federated learning: clients A and B train on their own data and send only model updates to a secure aggregation step, which "
        "produces a global model; updates can still leak through membership inference and model inversion, so secure aggregation, "
        "differential privacy, or homomorphic encryption are added. Split learning: the client runs the first layers on its raw data "
        "and sends only the smashed activations to the server, which runs the remaining layers.")
f.zone(20, 60, 520, 400, "Federated learning", BLUE, "#eef5fc", step=1)
for k, (lab, y) in enumerate([("Client A", 150), ("Client B", 330)]):
    f.icon("database", 90, y, 56, lab + " data", step=1, label_size=12); f.icon("chip", 210, y, 50, "local update", step=2, label_size=12)
    f.arrow([(120, y), (184, y)], None, BLUE, step=2, width=2); f.arrow([(238, y), (368, 222 + (y - 240) * 0.1)], None, BLUE, step=3, width=2.2)
f.text(150, 248, "updates only,", 12, BLUE, "bold", step=3); f.text(150, 264, "no raw data", 12, BLUE, "bold", step=3)
f.icon("lock", 400, 220, 56, "Secure aggregation", step=3); f.icon("nodes", 400, 350, 56, "Global model", step=4)
f.arrow([(400, 268), (400, 318)], None, BLUE, step=4, width=2.4)
f.badge(1, 522, 76, step=1); f.badge(2, 180, 100, step=2); f.badge(3, 350, 180, step=3); f.badge(4, 450, 330, step=4)
f.text(270, 444, "updates can still leak: add DP or HE", 12, RED, "bold", step=4)
f.zone(560, 60, 520, 400, "Split learning", PURPLE, "#f5eef8", step=5)
f.icon("database", 620, 160, 56, "Raw data", step=5, label_size=12); f.icon("chip", 750, 160, 50, "client layers", step=5, label_size=12)
f.icon("document", 900, 160, 46, "smashed", "activations", step=6, label_size=12); f.icon("server", 1010, 160, 50, "server layers", step=7, label_size=12)
f.arrow([(650, 160), (724, 160)], None, PURPLE, step=5, width=2); f.arrow([(776, 160), (874, 160)], None, PURPLE, step=6, width=2); f.arrow([(924, 160), (982, 160)], None, PURPLE, step=7, width=2)
f.icon("check", 1010, 300, 40, "prediction", step=8, label_size=12); f.arrow([(1010, 214), (1010, 276)], None, PURPLE, step=8, width=2)
f.badge(5, 1062, 76, step=5, color=PURPLE); f.badge(6, 880, 116, step=6, color=PURPLE); f.badge(7, 972, 120, step=7, color=PURPLE); f.badge(8, 970, 290, step=8, color=PURPLE)
f.text(820, 380, "raw data never leaves the client;", 12, PURPLE, "bold", step=8); f.text(820, 398, "only activations cross the boundary", 12, PURPLE, "bold", step=8)
f.raw('<line x1="830" y1="100" x2="830" y2="250" stroke="#c0392b" stroke-width="2" stroke-dasharray="5 4"/>', step=6)
f.text(830, 92, "client | server", 11, RED, "bold", step=6)
f.save(OUT + "ch17_fl_split")
print("ok")
