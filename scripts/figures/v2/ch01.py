import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
import math
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# AAA
f = Fig(1060, 290, "AAA: Authentication, Authorization, Accounting",
        "A user reaches a protected server through three checks in order: authentication asks who are you and verifies "
        "identity, authorization asks what may you do and applies permissions, and accounting asks what did you do and "
        "records it in logs for audit.")
f.icon("user-laptop", 70, 155, 96, "User", step=1)
cards = [("idcard", "Authentication", "Who are you?\n(verify identity)", "#2f6fae"),
         ("checklist", "Authorization", "What may you do?\n(permissions)", "#2e7d32"),
         ("logbook", "Accounting", "What did you do?\n(logging, audit)", "#b7791f")]
for k, (ic, t, sub, col) in enumerate(cards):
    x = 160 + k * 255
    f.card(x, 64, 210, 190, ic, t, sub, col, step=k + 1, icon_size=88)
    f.badge(k + 1, x + 14, 76, step=k + 1)
    if k: f.arrow([(x - 44, 160), (x - 4, 160)], None, INK, step=k + 1)
f.arrow([(122, 160), (156, 160)], None, INK, step=1)
f.arrow([(926, 160), (958, 160)], None, INK, step=3)
f.icon("server", 1005, 152, 92, "Resource", step=3)
f.save(OUT + "ch01_aaa")

# CIA and DAD
g = Fig(1060, 520, "CIA triad (defender goals) and DAD triad (attacker goals)",
        "Two triangles side by side. The CIA triad has confidentiality, integrity, and availability at its corners, with a "
        "shield for the defender. The DAD triad has disclosure, alteration, and destruction, each the opposite of one CIA goal, "
        "with an attacker.")
def tri(cx, color, fill, corners, center_icon, center_label, step):
    top, bl, br = (cx, 136), (cx - 200, 426), (cx + 200, 426)
    g.poly([top, bl, br], fill, color, 3, step=step, opacity=.16)
    g.icon(center_icon, cx, 330, 92, center_label, step=step, label_color=color)
    g.badge(step, cx - text_width(center_label, 15, True) / 2 - 18, 386, step=step, color=color)
    for (px, py), (ic, name) in zip([top, bl, br], corners):
        g.circle(px, py, 40, "#ffffff", color, 3, step=step)
        g.icon(ic, px, py, 52, step=step)
        ly = py - 50 if py < 200 else py + 64
        g.text(px, ly, name, 16, color, "bold", step=step)
tri(270, "#2f6fae", "#2f6fae", [("lock", "Confidentiality"), ("checklist", "Integrity"), ("clock", "Availability")],
    "shield", "Defender", 1)
tri(790, RED, RED, [("eye", "Disclosure"), ("bug", "Alteration"), ("cross", "Destruction")], "attacker", "Attacker", 2)
g.arrow([(484, 280), (576, 280)], "each attack goal\nbreaks one defense goal", MUTED, step=2, both=True, label_dy=-26, size=12)
g.save(OUT + "ch01_cia_dad")

# DIE
h = Fig(1000, 350, "DIE triad for infrastructure: Distributed, Immutable, Ephemeral",
        "Three cards. Distributed: spread out, so losing one node does not stop service, which supports availability. Immutable: "
        "never changed in place but replaced, which supports integrity. Ephemeral: short-lived, so there is less to steal, which "
        "supports confidentiality. The DIE triad complements the CIA triad, which protects data: cattle, not pets.")
cards = [("nodes", "Distributed", "spread out, so one loss\ndoes not stop service\n(supports Availability)", "#16a085"),
         ("lock", "Immutable", "never changed in place;\nreplace, do not patch\n(supports Integrity)", "#8e44ad"),
         ("hourglass", "Ephemeral", "short-lived, so there is\nless to steal\n(supports Confidentiality)", "#d35400")]
for k, (ic, t, sub, col) in enumerate(cards):
    x = 70 + k * 300
    h.card(x, 60, 260, 240, ic, t, sub, col, step=k + 1, icon_size=96)
    h.badge(k + 1, x + 14, 72, step=k + 1)
h.text(500, 332, "Complements CIA, which protects data: treat servers as cattle, not pets.", 14, MUTED, italic=True, step=3)
h.save(OUT + "ch01_die")

# Parkerian hexad
p = Fig(860, 720, "Parkerian hexad: six attributes of information security",
        "Six attributes arranged around a hexagon: confidentiality, possession or control, integrity, authenticity, availability, "
        "and utility. Donn Parker added possession, authenticity, and utility to the CIA triad.")
cx, cy, R = 430, 360, 215
p.poly([(cx + 170 * math.cos(math.radians(a)), cy + 170 * math.sin(math.radians(a))) for a in range(0, 360, 60)], "#dfe4ea", "#aab4bf", 2)
p.text(cx, cy - 4, "Parkerian", 22, INK, "bold"); p.text(cx, cy + 22, "hexad", 22, INK, "bold")
items = [("eye", "Confidentiality", "#2f6fae"), ("key", "Possession / control", "#8e44ad"), ("shield", "Integrity", "#27ae60"),
         ("certificate", "Authenticity", "#d9822b"), ("clock", "Availability", "#16a085"), ("gear", "Utility", "#c0392b")]
angles = [-90, -150, 150, 90, 30, -30]
for k, ((ic, name, col), a) in enumerate(zip(items, angles)):
    x, y = cx + R * math.cos(math.radians(a)), cy + R * math.sin(math.radians(a))
    p.circle(x, y, 58, "#ffffff", col, 4, step=k + 1)
    p.icon(ic, x, y, 66, step=k + 1)
    p.text(x, y - 70 if a == -90 else y + 80, name, 15, col, "bold", step=k + 1)
p.text(cx, 700, "Possession, authenticity, and utility are Parker's additions to confidentiality, integrity, and availability.",
       13, MUTED, italic=True, step=6)
p.save(OUT + "ch01_parkerian")

# Defense in depth
d = Fig(1120, 760, "Defense in depth: overlapping layers of control",
        "Concentric layers around a central asset, numbered from the outside in: one, policies and people with training; two, "
        "physical controls such as locks and guards; three, the perimeter with firewalls and IDS or IPS; four, the internal "
        "network with segmentation; five, the host with EDR and patching; six, the application with hardening and SAST; seven, "
        "data with encryption and DLP. An attacker must get through every layer to reach the asset.")
cx, cy = 470, 400
layers = [("group", "Policies and people", "training"), ("lock", "Physical", "locks, guards"),
          ("firewall", "Perimeter", "firewall, IDS/IPS"), ("switch", "Internal network", "segmentation"),
          ("server", "Host", "EDR, patching"), ("code", "Application", "hardening, SAST"), ("database", "Data", "encryption, DLP")]
blues = ["#dbe9f6", "#c3dbf1", "#a6c8e8", "#85b2dd", "#5f97cf", "#3f7cbd", "#2b62a3"]
for k, (ic, name, sub) in enumerate(layers):
    r = 320 - k * 40
    d.circle(cx, cy, r, blues[k], "#ffffff", 3, step=k + 1)
    d.badge(k + 1, cx, cy - r + 20, step=k + 1)
    y = 110 + k * 82
    d.icon(ic, 850, y, 56, step=k + 1)
    d.badge(k + 1, 810, y - 18, step=k + 1)
    d.text(886, y - 2, name, 15, INK, "bold", "start", step=k + 1)
    d.text(886, y + 16, sub, 13, MUTED, anchor="start", step=k + 1)
d.circle(cx, cy, 40, "#173f6e", "#ffffff", 3, step=8); d.icon("key", cx, cy - 6, 44, step=8)
d.text(cx, cy + 28, "ASSET", 12, "#ffffff", "bold", step=8)
d.icon("attacker", 70, 660, 100, "Attacker", step=9, label_color=RED)
d.arrow([(118, 620), (220, 560)], None, RED, step=9, width=3)
d.text(28, 586, "must pass\nevery layer", 12, RED, "bold", "start", step=9)
d.save(OUT + "ch01_defense_in_depth")

# Threat, vulnerability, mitigation
t = Fig(1060, 470, "Threat, vulnerability, and mitigation",
        "An attacker, the threat, pushes against a wall of controls that protects servers and data. A crack in the wall is the "
        "vulnerability that lets the threat through to the assets, which is risk. A mitigation, such as a patch or a control, "
        "closes the crack, so the threat no longer reaches the assets.")
t.zone(600, 96, 430, 300, "Assets", GREEN, "#eef8ef")
t.icon("server", 730, 240, 100, "Servers", step=1); t.icon("database", 910, 240, 100, "Data", step=1)
t.raw('<rect x="470" y="96" width="64" height="300" rx="4" fill="url(#g-brick)" stroke="#7a2e18" stroke-width="2"/>'
      + "".join(f'<line x1="470" y1="{120+i*25}" x2="534" y2="{120+i*25}" stroke="#f6d3c4" stroke-width="2"/>' for i in range(11)), step=1)
t.text(502, 418, "Wall of controls", 13, INK, "bold", step=1)
t.icon("attacker", 130, 246, 130, "Threat", "a person or event\nthat can cause harm", step=2, label_color=RED)
t.arrow([(204, 232), (462, 232)], "threat pressure", RED, step=2, width=4)
t.raw('<path d="M502 180 l-10 22 14 14 -12 24 10 18 -8 22" fill="none" stroke="#1f1f1f" stroke-width="4" stroke-linejoin="round"/>', step=3)
t.icon("warning", 440, 60, 40, step=3)
t.text(466, 56, "Vulnerability", 15, ORANGE, "bold", "start", step=3); t.text(466, 74, "a weakness: the crack", 12, MUTED, anchor="start", step=3)
t.arrow([(512, 272), (672, 300)], None, RED, step=3, dash=True)
t.text(780, 330, "the threat reaches the assets: risk", 12, RED, "bold", step=3)
t.icon("shield", 502, 236, 76, step=4)
t.icon("check", 440, 444, 30, step=4)
t.text(462, 450, "Mitigation: a patch or control closes the crack", 14, GREEN, "bold", "start", step=4)
t.save(OUT + "ch01_threat_vuln_mitigation")

# Risk: annualized loss expectancy
r = Fig(900, 500, "Effect of a security control on annualized loss expectancy",
        "Bar chart in US dollars a year: ALE before the control is 60,000, ALE after the control is 9,000, and the control costs "
        "20,000 a year. The control is worth buying because it cuts expected losses by 51,000 a year for 20,000.")
x0, y0, H = 130, 420, 270
r.raw(f'<line x1="{x0}" y1="{y0}" x2="840" y2="{y0}" stroke="#52606d" stroke-width="2"/>')
for v in range(0, 70001, 10000):
    y = y0 - H * v / 70000
    r.raw(f'<line x1="{x0}" y1="{y:.1f}" x2="840" y2="{y:.1f}" stroke="#e4e7eb"/>')
    r.text(x0 - 10, y + 4, f"{v:,}", 12, MUTED, anchor="end")
r.raw('<text x="36" y="285" font-family="Helvetica, Arial, sans-serif" font-size="13" fill="#52606d" text-anchor="middle" '
      'transform="rotate(-90 36 285)">US dollars per year</text>')
bars = [("ALE before", 60000, "#c0392b", "warning"), ("ALE after", 9000, "#27ae60", "shield"), ("Control cost", 20000, "#2f6fae", "gear")]
for k, (name, v, col, ic) in enumerate(bars):
    x = 190 + k * 220; hh = H * v / 70000
    r.rect(x, y0 - hh, 120, hh, col, col, 1, rx=3, step=k + 1)
    r.icon(ic, x + 60, y0 - hh - 30, 46, step=k + 1)
    r.text(x + 60, y0 - hh - 60, f"{v:,}", 15, INK, "bold", step=k + 1)
    r.text(x + 60, y0 + 22, name, 14, INK, "bold", step=k + 1)
r.text(470, 484, "Savings of 51,000 a year for a 20,000 control: worth buying.", 13, MUTED, italic=True, step=3)
r.save(OUT + "ch01_risk")
print("ok")
