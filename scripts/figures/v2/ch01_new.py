import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# Anatomy of an attack
a = Fig(1120, 520, "The anatomy of an attack",
        "A threat actor reaches for an asset. The attack surface is every point an attacker can reach, such as an email inbox, a "
        "web server, or a VPN gateway; an attack vector is the path used, such as a phishing email. A vulnerability is a weakness "
        "in that surface, an exploit is the code or technique that uses it, and a zero-day is a vulnerability with no fix yet. "
        "Risk is the chance the threat reaches the asset; a control reduces it.")
a.icon("attacker", 90, 250, 120, "Threat actor", "the adversary", step=1, label_color=RED); a.badge(1, 40, 180, step=1)
a.zone(250, 64, 300, 400, "Attack surface", ORANGE, "#fff6ec", step=2)
for k, (ic, name, vec) in enumerate([("envelope", "Email inbox", "phishing"), ("server", "Web server", "web request"), ("router", "VPN gateway", "login attempt")]):
    y = 140 + k * 118
    a.icon(ic, 330, y, 64, step=2); a.text(372, y - 4, name, 14, INK, "bold", "start", step=2)
    a.text(372, y + 14, "vector: " + vec, 12, MUTED, anchor="start", step=2)
    a.arrow([(150, 250), (292, y)], None, ORANGE, step=2, width=1.6)
a.badge(2, 262, 96, step=2)
a.icon("warning", 610, 258, 44, step=3); a.text(610, 300, "Vulnerability", 14, ORANGE, "bold", step=3)
a.text(610, 318, "unpatched bug,", 12, MUTED, step=3); a.text(610, 334, "default password", 12, MUTED, step=3); a.badge(3, 580, 230, step=3)
a.arrow([(510, 140), (590, 240)], None, ORANGE, step=3, dash=True)
a.icon("code", 750, 258, 70, "Exploit", "zero-day if no fix exists", step=4, label_color=RED); a.badge(4, 710, 212, step=4)
a.arrow([(634, 258), (712, 258)], None, RED, step=4, width=3)
a.arrow([(788, 258), (960, 258)], None, RED, step=4, width=3)
a.text(874, 214, "risk: the threat", 13, RED, "bold", step=4); a.text(874, 230, "reaches the asset", 13, RED, "bold", step=4)
a.icon("database", 1040, 250, 100, "Asset", "customer data", step=1, label_color=GREEN)
a.icon("shield", 880, 370, 70, "Control", "patch, filter, MFA", step=5, label_color=GREEN); a.badge(5, 840, 340, step=5)
a.arrow([(880, 332), (880, 272)], None, GREEN, step=5, width=3)
a.save(OUT + "ch01_attack_anatomy")

# Threat actors by capability
t = Fig(1120, 470, "Threat actors, from least to most capable",
        "Five kinds of threat actor in order of capability and resources: script kiddies who run published tools for curiosity or "
        "bragging rights; hacktivists who attack for a political or social cause; cybercriminals who attack for money; insiders who "
        "misuse legitimate access, by malice or mistake; and advanced persistent threats, usually state-backed, who pursue long-term "
        "espionage or sabotage. A credible threat needs capability, intent, and opportunity.")
actors = [("user-laptop", "Script kiddie", "runs published tools;\ncuriosity, bragging", "#7f8c8d"),
          ("group", "Hacktivist", "political or\nsocial cause", "#8e44ad"),
          ("attacker", "Cybercriminal", "money: ransomware,\nfraud, data theft", "#c0392b"),
          ("idcard", "Insider", "misuses legitimate\naccess, by malice\nor mistake", "#d35400"),
          ("bank", "APT (often state-backed)", "long-term espionage\nor sabotage", "#1a5276")]
for k, (ic, name, sub, col) in enumerate(actors):
    x = 30 + k * 216
    t.card(x, 70 + (4 - k) * 18, 196, 250, ic, name, sub, col, step=k + 1, icon_size=84, title_size=15)
    t.badge(k + 1, x + 14, 82 + (4 - k) * 18, step=k + 1)
t.arrow([(40, 420), (1080, 420)], "capability, resources, and persistence increase", INK, step=5, width=3, label_dy=-10)
t.text(560, 458, "A credible threat needs all three: capability, intent, and opportunity.", 13, MUTED, italic=True, step=5)
t.save(OUT + "ch01_threat_actors")

# NIST CSF 2.0
import math
n = Fig(900, 620, "NIST Cybersecurity Framework 2.0: six functions",
        "Govern sits at the center and informs the five other functions arranged around it: Identify, Protect, Detect, Respond, "
        "and Recover. CSF 2.0, published in 2024, added Govern to the original five.")
cx, cy = 450, 330
n.circle(cx, cy, 96, "#eaf2fb", "#1f4e9c", 4, step=1); n.icon("bank", cx, cy - 18, 70, step=1)
n.text(cx, cy + 40, "Govern (GV)", 17, "#1f4e9c", "bold", step=1); n.text(cx, cy + 58, "strategy, roles, policy", 12, MUTED, step=1)
n.badge(1, cx - 70, cy - 70, step=1)
fns = [("search", "Identify (ID)", "assets, risks", "#2e86c1"), ("shield", "Protect (PR)", "safeguards", "#8e44ad"),
       ("eye", "Detect (DE)", "find attacks", "#d68910"), ("warning", "Respond (RS)", "contain, act", "#c0392b"),
       ("check", "Recover (RC)", "restore", "#229954")]
for k, (ic, name, sub, col) in enumerate(fns):
    ang = math.radians(-90 + k * 72); x, y = cx + 220 * math.cos(ang), cy + 220 * math.sin(ang)
    n.circle(x, y, 70, "#ffffff", col, 4, step=k + 2); n.icon(ic, x, y - 14, 54, step=k + 2)
    n.text(x, y + 30, name, 14, col, "bold", step=k + 2); n.text(x, y + 47, sub, 12, MUTED, step=k + 2)
    n.badge(k + 2, x - 52, y - 52, step=k + 2)
    n.raw(f'<line x1="{cx + 100 * math.cos(ang):.1f}" y1="{cy + 100 * math.sin(ang):.1f}" x2="{x - 72 * math.cos(ang):.1f}" '
          f'y2="{y - 72 * math.sin(ang):.1f}" stroke="#1f4e9c" stroke-width="2.5" stroke-dasharray="6 5"/>', step=k + 2)
n.save(OUT + "ch01_nist_csf")

# Bell-LaPadula and Biba
b = Fig(1120, 500, "Bell-LaPadula protects confidentiality; Biba protects integrity",
        "Left, Bell-LaPadula with levels Top Secret, Secret, and Unclassified and a subject cleared for Secret: it may read down "
        "but not up (no read up), and write up but not down (no write down). Right, Biba with high, medium, and low integrity and a "
        "medium-integrity subject: it may read up but not down (no read down), and write down but not up (no write up).")
def model(x0, title, levels, cols, rules, step0, col):
    b.text(x0 + 265, 68, title, 18, col, "bold", step=step0)
    for k, (lv, c) in enumerate(zip(levels, cols)):
        y = 86 + k * 128
        b.rect(x0, y, 550, 118, c, "#9aa5b1", 1.5, rx=8, step=step0)
        b.icon("document", x0 + 520, y + 64, 46, step=step0)
        b.text(x0 + 40, y + 24, lv, 15, INK, "bold", "start", step=step0)
    b.icon("user", x0 + 90, 86 + 128 + 64, 80, step=step0)
    b.badge(step0, x0 + 18, 104, step=step0)
    for k, (label, ok, up, dx) in enumerate(rules):
        y1 = 86 + 128 + 59; y2 = 86 + 70 if up else 86 + 256 + 50; st = step0 + 1
        colr = GREEN if ok else RED
        b.arrow([(x0 + dx, y1 + (-20 if up else 20)), (x0 + dx, y2)], None, colr, step=st, width=3, dash=not ok)
        ly = 86 + 64 if up else 86 + 256 + 90
        left = dx < 330
        b.icon("check" if ok else "cross", x0 + dx + (-18 if left else 18), ly - 5, 22, step=st)
        b.text(x0 + dx + (-32 if left else 32), ly, label, 13, colr, "bold", "end" if left else "start", step=st)
    b.text(x0 + 140, 86 + 128 + 70, "subject", 12, MUTED, "bold", "start", step=step0)
model(10, "Bell-LaPadula (confidentiality)", ["Top Secret", "Secret: the subject's clearance", "Unclassified"],
      ["#fdecea", "#fff8e1", "#eef8ef"],
      [("read up: denied", False, True, 300), ("read down: allowed", True, False, 300),
       ("write up: allowed", True, True, 360), ("write down: denied", False, False, 360)], 1, "#1f4e9c")
model(560, "Biba (integrity)", ["High integrity", "Medium integrity: the subject", "Low integrity"],
      ["#eef8ef", "#fff8e1", "#fdecea"],
      [("read up: allowed", True, True, 300), ("read down: denied", False, False, 300),
       ("write up: denied", False, True, 360), ("write down: allowed", True, False, 360)], 3, "#2e7d32")
b.save(OUT + "ch01_blp_biba")

# Security versus resilience
r = Fig(1000, 470, "Security reduces how often incidents happen; resilience reduces what each one costs",
        "Service level over time for two organizations hit by the same attack. The prevention-only organization drops far and "
        "recovers slowly because nothing contains the damage. The resilient organization, with segmentation, tested backups, and "
        "replaceable components, drops less and recovers quickly.")
x0, y0, W, H = 110, 390, 830, 290
r.raw(f'<line x1="{x0}" y1="{y0}" x2="{x0 + W}" y2="{y0}" stroke="#52606d" stroke-width="2"/>'
      f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0 - H}" stroke="#52606d" stroke-width="2"/>')
r.text(x0 + W / 2, y0 + 32, "time", 13, MUTED)
r.raw(f'<text x="{x0 - 30}" y="{y0 - H / 2}" font-family="{FONT}" font-size="13" fill="{MUTED}" text-anchor="middle" '
      f'transform="rotate(-90 {x0 - 30} {y0 - H / 2})">service level</text>')
def curve(depth, recover, col, step, label, lx, ly):
    pts = [(x0, y0 - 250), (x0 + 250, y0 - 250), (x0 + 270, y0 - 250 + depth), (x0 + 270 + recover, y0 - 250 + depth * .3), (x0 + 300 + recover, y0 - 250), (x0 + W, y0 - 250)]
    r.raw(f'<polyline points="{" ".join(f"{a:.0f},{b:.0f}" for a, b in pts)}" fill="none" stroke="{col}" stroke-width="4" stroke-linejoin="round"/>', step)
    r.text(lx, ly, label, 14, col, "bold", "start", step=step)
r.raw(f'<line x1="{x0}" y1="{y0 - 250}" x2="{x0 + 250}" y2="{y0 - 250}" stroke="#52606d" stroke-width="4"/>', step=1)
r.text(x0 + 120, y0 - 262, "normal service", 13, MUTED, "bold", step=1)
r.icon("attacker", x0 + 262, 70, 56, step=2); r.text(x0 + 300, 64, "attack gets through", 13, RED, "bold", "start", step=2)
r.raw(f'<line x1="{x0 + 262}" y1="100" x2="{x0 + 262}" y2="{y0}" stroke="{RED}" stroke-width="1.6" stroke-dasharray="5 5"/>', step=2)
curve(210, 420, RED, 3, "prevention only: deep and slow", x0 + 420, y0 - 60)
curve(80, 110, GREEN, 4, "resilient: shallow and fast", x0 + 420, y0 - 190)
r.badge(3, x0 + 300, y0 - 30, step=3); r.badge(4, x0 + 300, y0 - 160, step=4)
r.save(OUT + "ch01_security_resilience")
print("ok")
