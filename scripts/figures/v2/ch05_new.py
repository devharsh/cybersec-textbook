import os
import sys, json; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# Redraw: 5x5 risk matrix
r = Fig(1000, 600, "A 5 by 5 qualitative risk matrix: score = likelihood rank times impact rank",
        "Likelihood from Rare to Almost certain on the vertical axis and impact from Negligible to Severe on the horizontal axis. "
        "Each cell holds the product of the two ranks, from 1 to 25. Scores up to 4 are green and can be accepted, 5 to 9 are "
        "yellow, 10 to 14 are orange, and 15 and above are red and urgent.")
lik = ["Rare", "Unlikely", "Possible", "Likely", "Almost certain"]; imp = ["Negligible", "Minor", "Moderate", "Major", "Severe"]
x0, y0, cw, ch = 200, 70, 120, 84
band = lambda s: (2, "#2ecc71") if s <= 4 else (3, "#f1c40f") if s <= 9 else (4, "#e67e22") if s <= 14 else (5, "#e74c3c")
for ri in range(5):
    r.text(x0 - 14, y0 + (4 - ri) * ch + ch / 2 + 5, lik[ri], 15, INK, "bold", "end", step=1)
for ci in range(5):
    r.text(x0 + ci * cw + cw / 2, y0 + 5 * ch + 24, imp[ci], 15, INK, "bold", step=1)
r.text(x0 + 2.5 * cw, y0 + 5 * ch + 52, "Impact", 16, MUTED, "bold", step=1)
r.raw(f'<text x="44" y="{y0 + 2.5 * ch}" font-family="{FONT}" font-size="16" font-weight="bold" fill="{MUTED}" text-anchor="middle" transform="rotate(-90 44 {y0 + 2.5 * ch})">Likelihood</text>', step=1)
for ri in range(5):
    for ci in range(5):
        s = (ri + 1) * (ci + 1); st, col = band(s)
        r.rect(x0 + ci * cw + 2, y0 + (4 - ri) * ch + 2, cw - 4, ch - 4, col, "#ffffff", 2, rx=6, step=st)
        r.text(x0 + ci * cw + cw / 2, y0 + (4 - ri) * ch + ch / 2 + 8, str(s), 22, "#1f2933", "bold", step=st)
legend = [(2, "#2ecc71", "check", "1 to 4: low, accept"), (3, "#f1c40f", "eye", "5 to 9: medium, monitor"),
          (4, "#e67e22", "warning", "10 to 14: high, treat soon"), (5, "#e74c3c", "warning", "15 to 25: urgent")]
for i, (st, col, ic, lab) in enumerate(legend):
    y = 110 + i * 90
    r.rect(815, y - 26, 172, 70, "#ffffff", col, 2.4, rx=8, step=st)
    r.icon(ic, 845, y + 8, 34, step=st); r.text(867, y + 2, lab.split(": ")[0], 13, INK, "bold", "start", step=st)
    r.text(867, y + 20, lab.split(": ")[1], 13, INK, anchor="start", step=st); r.badge(st, 815, y - 26, step=st)
r.badge(1, 200, 70, step=1)
r.save(OUT + "ch05_risk_matrix_v2")

# Redraw: Monte Carlo annual loss
mc = json.load(open("/tmp/mc.json")) if False else None
import random
random.seed(7); trials = 20000; losses = []
for _ in range(trials):
    events = sum(1 for _ in range(5) if random.random() < 0.10)
    annual = 0.0
    for _ in range(events): annual += random.triangular(50_000, 1_200_000, 300_000)
    losses.append(annual)
mean = sum(losses) / trials; p95 = sorted(losses)[int(0.95 * trials)]; zero = sum(1 for l in losses if l == 0)
bins = [0] * 27
for l in losses:
    if l > 0: bins[min(int(l // 100_000), 26)] += 1
m = Fig(1100, 560, "One ALE number hides the bad years: 20,000 simulated years of loss",
        f"A Monte Carlo simulation of 20,000 years. In {zero:,} years, about {zero / trials:.0%}, no loss event happens at all. The "
        f"other years form a long right tail of losses from about 50,000 to 2.6 million dollars. The mean annual loss, the ALE, "
        f"is about {mean / 1000:,.0f} thousand dollars, but one year in twenty loses more than {p95 / 1000:,.0f} thousand.")
m.card(30, 70, 220, 300, "check", f"{zero:,} years", f"about {zero / trials:.0%} of all years:\nno loss event at all", GREEN, step=1, icon_size=80, title_size=20)
m.badge(1, 30, 70, step=1)
X0, Y0, W, H = 320, 80, 740, 330; ymax = 1200
m.raw(f'<line x1="{X0}" y1="{Y0 + H}" x2="{X0 + W}" y2="{Y0 + H}" stroke="#52606d" stroke-width="2"/><line x1="{X0}" y1="{Y0}" x2="{X0}" y2="{Y0 + H}" stroke="#52606d" stroke-width="2"/>', step=2)
for v in (0, 400, 800, 1200):
    yy = Y0 + H - v / ymax * H
    m.raw(f'<line x1="{X0}" y1="{yy:.1f}" x2="{X0 + W}" y2="{yy:.1f}" stroke="#e4e7eb" stroke-width="1"/>', step=2)
    m.text(X0 - 8, yy + 4, f"{v:,}", 12, MUTED, anchor="end", step=2)
bw = W / 27
for i, b in enumerate(bins):
    h = b / ymax * H
    m.rect(X0 + i * bw + 1, Y0 + H - h, bw - 2, h, "#8e44ad", "#8e44ad", 0.5, rx=2, step=2)
for v in (0, 500, 1000, 1500, 2000, 2500):
    xx = X0 + v / 100 * bw; m.text(xx, Y0 + H + 20, f"{v:,}", 12, MUTED, step=2)
m.text(X0 + W / 2, Y0 + H + 44, "annual loss in thousands of US dollars (years with at least one loss event)", 13, MUTED, "bold", step=2)
m.text(X0 - 30, Y0 - 16, "years", 12, MUTED, "bold", step=2); m.badge(2, X0 + W - 20, Y0, step=2)
for v, col, lab, st in [(mean, INK, f"ALE (mean) ~${mean / 1000:,.0f}k", 3), (p95, RED, f"95th percentile ~${p95 / 1000:,.0f}k", 4)]:
    xx = X0 + v / 100_000 * bw
    m.raw(f'<line x1="{xx:.1f}" y1="{Y0}" x2="{xx:.1f}" y2="{Y0 + H}" stroke="{col}" stroke-width="2.6" stroke-dasharray="8 5"/>', step=st)
    m.text(xx + 8, Y0 + 20 + (st - 3) * 26, lab, 14, col, "bold", "start", step=st); m.badge(st, xx, Y0 - 2, step=st, color=col)
m.icon("warning", 360, 515, 30, step=5); m.badge(5, 330, 500, step=5)
m.text(384, 520, f"Planning to the ALE alone budgets for a typical year; one year in twenty loses more than ${p95 / 1000:,.0f}k.", 14, RED, "bold", "start", step=5)
m.save(OUT + "ch05_montecarlo_v2")

# New: risk-management lifecycle
l = Fig(1100, 400, "The risk-management lifecycle is a loop that never ends",
        "Identify assets, threats, and vulnerabilities; assess likelihood times impact and prioritize; treat by avoiding, "
        "mitigating, transferring, or accepting; then monitor and review residual risk, which feeds the next round of "
        "identification.")
stg = [("Identify", "assets, threats,\nvulnerabilities", "search", BLUE), ("Assess", "likelihood x impact,\nprioritize", "checklist", ORANGE),
       ("Treat", "avoid, mitigate,\ntransfer, accept", "shield", GREEN), ("Monitor and review", "track residual risk,\nre-evaluate", "eye", PURPLE)]
for i, (name, sub, ic, col) in enumerate(stg):
    x = 30 + i * 270
    l.card(x, 60, 230, 220, ic, name, sub, col, step=i + 1, icon_size=80, title_size=17); l.badge(i + 1, x + 14, 72, step=i + 1, color=col)
    if i < 3: l.arrow([(x + 232, 170), (x + 268, 170)], None, col, step=i + 2, width=3)
l.arrow([(955, 282), (955, 340), (145, 340), (145, 284)], "conditions keep changing, so the loop repeats", MUTED, step=5, width=2.6, label_at=.5, label_dy=-8)
l.badge(5, 955, 312, step=5, color=MUTED)
l.save(OUT + "ch05_rm_lifecycle")

# New: four treatment options with the bicycle
t = Fig(1100, 520, "Four ways to treat a risk, shown with a bicycle and with a data breach",
        "Mitigate: a good lock lowers the chance of theft, like a security control. Transfer: insurance moves the financial loss to "
        "someone else but prevents nothing, like cyber insurance. Accept: decide in writing to live with scratches, like a "
        "documented risk acceptance within appetite. Avoid: do not ride in heavy traffic, like not collecting data you do not need. "
        "Real plans combine all four.")
opts = [("Mitigate", "lock", "Bicycle: a good lock", "Data: encryption, MFA, patching", "lowers likelihood or impact", BLUE),
        ("Transfer", "certificate", "Bicycle: theft insurance", "Data: cyber insurance, outsourcing", "moves the money, not the risk", ORANGE),
        ("Accept", "logbook", "Bicycle: live with scratches", "Data: signed acceptance in the register", "only if documented and within appetite", PURPLE),
        ("Avoid", "cross", "Bicycle: skip the busy street", "Data: do not collect what you do not need", "also gives up the benefit", RED)]
for i, (name, ic, bike, data, note, col) in enumerate(opts):
    x = 30 + (i % 2) * 530; y = 50 + (i // 2) * 200
    t.rect(x, y, 510, 180, "#ffffff", col, 2.4, rx=10, step=i + 1)
    t.rect(x, y, 510, 8, col, col, 1, rx=4, step=i + 1)
    t.icon(ic, x + 70, y + 92, 90, step=i + 1)
    t.text(x + 140, y + 46, name, 20, col, "bold", "start", step=i + 1)
    t.text(x + 140, y + 76, bike, 14, INK, anchor="start", step=i + 1)
    t.text(x + 140, y + 100, data, 14, INK, "bold", "start", step=i + 1)
    t.text(x + 140, y + 128, note, 13, MUTED, anchor="start", step=i + 1, italic=True)
    t.badge(i + 1, x + 492, y + 20, step=i + 1, color=col)
t.text(550, 480, "A real plan mixes them: lock the bike, insure it, accept the scratches, and avoid one street after dark.", 15, INK, "bold", step=5)
t.text(550, 504, "Insurance never transfers the loss of trust, and legal accountability usually stays with the organization.", 13, MUTED, step=5, italic=True)
t.badge(5, 90, 470, step=5)
t.save(OUT + "ch05_treatment")

# New: attack tree with icons
a = Fig(1100, 520, "An attack tree: one goal, several paths to it",
        "The root goal is to steal customer data. It branches into compromising the web app, by SQL injection or by exploiting an "
        "unpatched component; compromising the database directly through an exposed port or weak credentials; or phishing an "
        "administrator, by a spear-phishing email or by vishing the help desk.")
a.card(430, 46, 240, 120, "database", "Goal: steal customer data", None, RED, step=1, icon_size=60, title_size=15); a.badge(1, 430, 46, step=1, color=RED)
mids = [(180, "browser", "Compromise web app", BLUE), (550, "server", "Compromise database directly", ORANGE), (920, "user", "Phish an administrator", PURPLE)]
leaves = {0: [(90, "code", "SQL injection"), (270, "bug", "Exploit unpatched\ncomponent")], 1: [(550, "lock", "Exposed port or\nweak credentials")],
          2: [(830, "envelope", "Spear-phishing\nemail"), (1010, "headset", "Vishing the\nhelp desk")]}
for j, (x, ic, lab, col) in enumerate(mids):
    a.arrow([(550, 168), (x, 216)], None, col, step=2, width=2.4)
    a.card(x - 110, 220, 220, 110, ic, lab, None, col, step=2, icon_size=54, title_size=14)
    for lx, lic, llab in leaves[j]:
        a.arrow([(x, 332), (lx, 372)], None, col, step=3, width=2)
        a.icon(lic, lx, 410, 56, step=3); a.text(lx, 460, llab, 14, INK, "bold", step=3)
a.badge(2, 70, 220, step=2); a.badge(3, 40, 384, step=3)
a.text(550, 508, "Threat modeling then rates and mitigates each leaf, so the risk register reflects real attack paths.", 13, MUTED, italic=True, step=4)
a.save(OUT + "ch05_attack_tree")

# New: data-flow diagram with trust boundaries and STRIDE
s = Fig(1100, 560, "Threat modeling a web app: a data-flow diagram, trust boundaries, and STRIDE",
        "A customer's browser sends login and order data across the internet trust boundary to a web application, which reads and "
        "writes a database inside the internal boundary and calls an external payment API. Each flow that crosses a boundary is "
        "checked against STRIDE: spoofing, tampering, repudiation, information disclosure, denial of service, and elevation of "
        "privilege, each with its matching control.")
s.icon("user-laptop", 90, 200, 90, "Customer", "external entity", step=1)
s.zone(250, 60, 520, 330, "Company network (trust boundary)", RED, "#fdf7f6", step=2, dash=True)
s.icon("server", 380, 200, 90, "Web app", "process", step=1)
s.zone(540, 150, 210, 200, "Internal data zone", ORANGE, "#fef9f0", step=2, dash=True)
s.icon("database", 645, 255, 90, "Customer DB", "data store", step=1)
s.icon("cloud", 930, 200, 110, step=1); s.icon("bank", 930, 196, 40, step=1); s.text(930, 270, "Payment API", 15, INK, "bold", step=1)
s.text(930, 288, "external service", 12, MUTED, step=1)
s.arrow([(140, 190), (330, 190)], "login, orders", BLUE, step=1, both=True, width=2.6, label_at=.25)
s.arrow([(430, 215), (596, 250)], "SQL queries", BLUE, step=1, both=True, width=2.6, label_dy=-10, label_at=.28)
s.arrow([(420, 150), (880, 120)], "charge card", BLUE, step=1, both=True, width=2.6, label_at=.6)
s.badge(1, 50, 120, step=1); s.badge(2, 752, 76, step=2)
for (bx, by), n in [((250, 190), "A"), ((540, 237), "B"), ((770, 127), "C")]:
    s.circle(bx, by, 13, "#ffffff", RED, 2.4, step=3); s.text(bx, by + 5, n, 13, RED, "bold", step=3)
s.badge(3, 250, 222, step=3)
rows = [("S", "Spoofing", "authentication, MFA"), ("T", "Tampering", "integrity checks, TLS"), ("R", "Repudiation", "logging, signatures"),
        ("I", "Information disclosure", "encryption, access control"), ("D", "Denial of service", "rate limits, redundancy"), ("E", "Elevation of privilege", "authorization, least privilege")]
s.text(40, 420, "At each crossing (A, B, C) ask all six STRIDE questions:", 14, INK, "bold", "start", step=4); s.badge(4, 24, 414, step=4)
for i, (k, name, ctl) in enumerate(rows):
    x = 40 + (i % 3) * 350; y = 446 + (i // 3) * 50
    s.rect(x, y, 330, 40, "#ffffff", "#9aa5b1", 1.4, rx=6, step=4)
    s.circle(x + 20, y + 20, 14, RED, RED, 1, step=4); s.text(x + 20, y + 25, k, 14, "#ffffff", "bold", step=4)
    s.text(x + 42, y + 17, name, 13, INK, "bold", "start", step=4); s.text(x + 42, y + 33, "control: " + ctl, 12, GREEN, anchor="start", step=4)
s.save(OUT + "ch05_dfd_stride")

# New: RPO, RTO, MTD on a timeline, and recovery sites
d = Fig(1100, 560, "RPO, RTO, and MTD on a timeline, and the sites that meet them",
        "On the timeline, the last good backup is followed by the disaster. The recovery point objective is the most data, measured "
        "in time, that may be lost between the last backup and the disaster. The recovery time objective is the longest a function "
        "may stay down before service is restored, and the maximum tolerable downtime bounds the total outage. Below, a cold site has "
        "space and power only and is cheap but slow, a warm site is partly equipped, and a hot site is fully equipped and nearly "
        "instant but expensive.")
y0 = 190
d.raw(f'<line x1="60" y1="{y0}" x2="1050" y2="{y0}" stroke="#52606d" stroke-width="4"/>')
d.text(1050, y0 + 26, "time", 13, MUTED, "bold", "end")
d.icon("database", 250, y0 - 50, 60, step=1); d.text(250, y0 + 28, "last good backup", 14, BLUE, "bold", step=1); d.badge(1, 210, y0 - 86, step=1)
d.icon("warning", 500, y0 - 52, 56, step=2); d.text(500, y0 + 28, "disaster strikes", 14, RED, "bold", step=2); d.badge(2, 460, y0 - 86, step=2)
d.icon("server", 820, y0 - 50, 60, step=4); d.text(820, y0 + 28, "service restored", 14, GREEN, "bold", step=4)
d.rect(250, y0 + 44, 250, 34, "#fdecea", RED, 1.6, rx=6, step=3)
d.text(375, y0 + 66, "RPO: data lost (backup gap)", 14, RED, "bold", step=3); d.badge(3, 236, y0 + 61, step=3)
d.rect(500, y0 + 44, 320, 34, "#fff3e0", ORANGE, 1.6, rx=6, step=4)
d.text(660, y0 + 66, "RTO: downtime until restored", 14, ORANGE, "bold", step=4); d.badge(4, 836, y0 + 61, step=4)
d.rect(500, y0 + 86, 480, 30, "#ffffff", "#8e44ad", 1.6, rx=6, step=5, dash=True)
d.text(740, y0 + 106, "MTD: the most total outage the function can survive", 13, "#8e44ad", "bold", step=5); d.badge(5, 980, y0 + 86, step=5)
d.text(375, y0 + 134, "shorter RPO = more frequent backups", 13, MUTED, step=3, italic=True)
d.text(660, y0 + 134, "shorter RTO = faster, costlier recovery", 13, MUTED, step=4, italic=True)
sites = [("Cold site", "space and power only", "cheapest, slowest to bring up", "#2f6fae", ["factory"]),
         ("Warm site", "some hardware ready", "moderate cost and speed", ORANGE, ["factory", "server"]),
         ("Hot site", "fully equipped, data mirrored", "fast, nearly instant; costly", RED, ["factory", "server", "database"])]
for i, (name, sub, trade, col, ics) in enumerate(sites):
    x = 60 + i * 340
    d.rect(x, 360, 310, 170, "#ffffff", col, 2.2, rx=10, step=6 + i)
    for k, ic in enumerate(ics): d.icon(ic, x + 50 + k * 60, 420, 56, step=6 + i)
    d.text(x + 155, 476, name, 17, col, "bold", step=6 + i); d.text(x + 155, 496, sub, 13, INK, step=6 + i)
    d.text(x + 155, 516, trade, 13, MUTED, step=6 + i, italic=True); d.badge(6 + i, x + 292, 360, step=6 + i, color=col)
d.save(OUT + "ch05_rto_rpo")

# New: software supply chain
c = Fig(1100, 520, "Supply-chain risk: one trusted update can reach thousands of customers",
        "A vendor's developers and open-source dependencies feed a build pipeline that produces a signed update. If an attacker "
        "compromises the build system, as in SolarWinds, the malicious code is signed and shipped to thousands of customers who "
        "trust the vendor. Controls: assess vendors with SOC 2 or ISO/IEC 27001 evidence, put security and audit rights in "
        "contracts, keep a software bill of materials, verify the integrity and provenance of updates, secure the build "
        "pipeline, and monitor vendors over time.")
c.icon("user-laptop", 80, 140, 80, "Developers", step=1); c.icon("nodes", 80, 290, 80, "Open-source", "dependencies", step=1)
c.zone(170, 70, 400, 290, "Vendor", BLUE, "#eef5fc", step=1)
c.icon("code", 250, 210, 70, "Source", step=1)
c.icon("gear", 390, 210, 80, step=2); c.text(390, 160, "Build server", 15, INK, "bold", step=2); c.icon("certificate", 510, 210, 70, "Signed update", step=2)
c.arrow([(120, 150), (214, 200)], None, INK, step=1); c.arrow([(120, 280), (214, 222)], None, INK, step=1)
c.arrow([(288, 210), (346, 210)], None, INK, step=2); c.arrow([(432, 210), (472, 210)], None, INK, step=2)
c.icon("attacker", 390, 320, 70, step=3); c.arrow([(390, 284), (390, 254)], None, RED, step=3, width=3); c.text(428, 306, "implants code", 13, RED, "bold", "start", step=3)
c.icon("bug", 420, 180, 32, step=3)
for k in range(9):
    xx = 700 + (k % 3) * 120; yy = 110 + (k // 3) * 90
    c.icon("desktop", xx, yy, 56, step=4); c.icon("bug", xx + 20, yy - 20, 22, step=4)
c.arrow([(548, 210), (640, 120)], None, RED, step=4, width=2.4); c.arrow([(548, 210), (640, 200)], None, RED, step=4, width=2.4)
c.arrow([(548, 210), (640, 290)], None, RED, step=4, width=2.4)
c.text(820, 370, "thousands of trusting customers", 15, RED, "bold", step=4)
c.badge(1, 552, 80, step=1); c.badge(2, 456, 236, step=2); c.badge(3, 340, 340, step=3, color=RED); c.badge(4, 640, 80, step=4, color=RED)
ctl = ["vendor assessment: SOC 2, ISO/IEC 27001", "contract: security terms, right to audit", "SBOM: know every component",
       "verify update integrity and provenance", "harden and monitor the build pipeline", "monitor vendors over time"]
c.rect(30, 400, 1040, 100, "#e8f5e9", GREEN, 1.6, rx=8, step=5); c.icon("shield", 66, 450, 44, step=5); c.badge(5, 30, 400, step=5)
for i, tx in enumerate(ctl):
    c.text(100 + (i % 3) * 330, 436 + (i // 3) * 34, tx, 13, GREEN, "bold", "start", step=5)
c.save(OUT + "ch05_supply_chain")
print("ok")
