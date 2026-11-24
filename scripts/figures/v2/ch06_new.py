import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

def hat(f, x, y, col, step, s=1.0):
    f.raw(f'<ellipse cx="{x}" cy="{y}" rx="{30 * s}" ry="{7 * s}" fill="{col}" stroke="#2b3138" stroke-width="1.4"/>'
          f'<path d="M{x - 17 * s} {y - 1} q2 {-24 * s} {17 * s} {-24 * s} q15 0 {17 * s} {24 * s} Z" fill="{col}" stroke="#2b3138" stroke-width="1.4"/>'
          f'<rect x="{x - 17 * s}" y="{y - 9 * s}" width="{34 * s}" height="{5 * s}" fill="#8a6d1a"/>', step=step)

# 1. Hats and team colors
h = Fig(1100, 560, "Hats describe authorization and intent; team colors describe roles in an exercise",
        "Left: white hats are authorized and aim to improve security; gray hats often mean no harm but act without full "
        "authorization, which is still illegal; black hats act without authorization and with malicious intent. Right: the red team "
        "emulates attackers, the blue team defends with monitoring, detection, and response, and purple teaming is a way of working "
        "in which red and blue share techniques so detection improves at once.")
h.text(280, 66, "Hats: individuals", 17, INK, "bold")
for i, (name, col, sub, verdict, vcol) in enumerate([("White hat", "#f4f6f8", "authorized; improves security", "legal", GREEN),
                                                     ("Gray hat", "#9aa3ae", "partly or not authorized;\noften not malicious", "still illegal", ORANGE),
                                                     ("Black hat", "#2b3138", "no authorization;\nmalicious intent", "criminal", RED)]):
    y = 150 + i * 135
    h.icon("user", 90, y, 90, step=i + 1); hat(h, 90, y - 30, col, i + 1)
    h.text(160, y - 14, name, 18, INK, "bold", "start", step=i + 1); h.text(160, y + 8, sub, 13, INK, anchor="start", step=i + 1)
    h.rect(400, y - 20, 110, 32, "#ffffff", vcol, 2, rx=16, step=i + 1); h.text(455, y + 1, verdict, 14, vcol, "bold", step=i + 1)
    h.badge(i + 1, 40, y - 50, step=i + 1)
h.raw('<line x1="560" y1="60" x2="560" y2="520" stroke="#d0d6dd" stroke-width="2" stroke-dasharray="6 6"/>')
h.text(820, 66, "Teams: roles in an exercise", 17, INK, "bold")
h.card(590, 90, 220, 200, "attacker", "Red team", "emulates adversaries\nto test defenses", RED, step=4, icon_size=80, title_size=17)
h.card(840, 90, 220, 200, "eye", "Blue team", "monitors, detects,\nand responds", BLUE, step=5, icon_size=80, title_size=17)
h.badge(4, 600, 100, step=4); h.badge(5, 850, 100, step=5)
h.arrow([(700, 296), (720, 350)], None, RED, step=6, width=3); h.arrow([(950, 296), (930, 350)], None, BLUE, step=6, width=3)
h.card(700, 352, 250, 150, "group", "Purple teaming", "red shares techniques, blue\nimproves detection at once", "#7d3c98", step=6, icon_size=60, title_size=17)
h.badge(6, 710, 362, step=6)
h.save(OUT + "ch06_hats_teams")

# 2. Box knowledge levels
b = Fig(1100, 560, "Black, gray, and white box: how much the tester knows before starting",
        "Black box: the tester knows nothing and must discover everything, the most realistic outside view but the most time spent "
        "on reconnaissance. Gray box: partial knowledge such as user credentials or network diagrams, a common balance that also "
        "simulates an insider or a foothold. White box, also called crystal box: full knowledge of source code, architecture, and "
        "earlier scans, giving the widest coverage at the lowest cost per finding but less realism.")
boxes = [("Black box", "#2b3138", "#ffffff", "no prior knowledge", [], "most realistic outside view;\nmost time on discovery"),
         ("Gray box", "#7f8c8d", "#ffffff", "partial knowledge", ["idcard", "nodes"], "user credentials, network diagram;\nsimulates a foothold or insider"),
         ("White (crystal) box", "#d5dbe1", INK, "full knowledge", ["code", "nodes", "checklist"], "source code, architecture, scans;\nwidest coverage, least realistic")]
for i, (name, fill, tc, lab, gifts, sub) in enumerate(boxes):
    x = 40 + i * 350
    b.raw(f'<path d="M{x + 60} 140 l40 -30 h180 l-40 30 Z" fill="{fill}" opacity=".75" stroke="#2b3138" stroke-width="1.4"/>'
          f'<path d="M{x + 240} 140 l40 -30 v150 l-40 30 Z" fill="{fill}" opacity=".9" stroke="#2b3138" stroke-width="1.4"/>'
          f'<rect x="{x + 60}" y="140" width="180" height="150" fill="{fill}" stroke="#2b3138" stroke-width="1.4"/>', step=i + 1)
    if not gifts:
        b.text(x + 150, 235, "?", 64, "#ffffff", "bold", step=i + 1)
    else:
        for k, g in enumerate(gifts): b.icon(g, x + 100 + k * 55 if len(gifts) == 3 else x + 115 + k * 70, 215, 50, step=i + 1)
    b.text(x + 150, 76, name, 19, INK, "bold", step=i + 1)
    b.text(x + 150, 320, lab, 15, INK, "bold", step=i + 1); b.text(x + 150, 342, sub, 13, MUTED, step=i + 1)
    b.badge(i + 1, x + 40, 70, step=i + 1)
    b.icon("user-laptop", x + 30, 250, 56, step=i + 1)
rows = [("Realism (outside attacker)", [3, 2, 1]), ("Time spent on discovery", [3, 2, 1]), ("Coverage", [1, 2, 3]), ("Cost per finding", [3, 2, 1])]
for j, (lab, vals) in enumerate(rows):
    y = 412 + j * 34
    b.text(30, y + 4, lab, 13, INK, "bold", "start", step=4)
    for i, v in enumerate(vals):
        for k in range(3):
            b.rect(250 + i * 350 + k * 34, y - 10, 28, 16, BLUE if k < v else "#e4e7eb", "#ffffff", 1, rx=3, step=4)
b.badge(4, 30, 384, step=4); b.text(60, 390, "Trade-offs (more bars = more)", 14, MUTED, "bold", "start", step=4)
b.save(OUT + "ch06_box_levels")

# 3. Phases of a penetration test
p = Fig(1100, 470, "The phases of a penetration test, from permission to report and retest",
        "Eight phases in order: permission and scoping; reconnaissance; scanning and enumeration; gaining access; privilege "
        "escalation; maintaining access; post-exploitation validation and cleanup; and reporting, which leads to remediation and a "
        "retest under a new authorization.")
ph = [("Permission\nand scoping", "certificate"), ("Reconnaissance", "search"), ("Scanning and\nenumeration", "nodes"), ("Gaining\naccess", "key"),
      ("Privilege\nescalation", "user2"), ("Maintaining\naccess", "clock"), ("Validation\nand cleanup", "trash"), ("Reporting", "logbook")]
for i, (lab, ic) in enumerate(ph):
    x = 70 + i * 137; col = GREEN if i == 0 else PURPLE if i == 7 else BLUE
    p.circle(x, 170, 54, "#ffffff", col, 3, step=i + 1); p.icon(ic, x, 166, 66, step=i + 1)
    p.text(x, 252, lab, 14, INK, "bold", step=i + 1); p.badge(i + 1, x - 44, 124, step=i + 1, color=col)
    if i < 7: p.arrow([(x + 56, 170), (x + 80, 170)], None, col, step=i + 2, width=2.6)
p.arrow([(1029, 296), (1029, 360), (70, 360), (70, 300)], "remediation and retest", PURPLE, step=9, dash=True, width=2.6, label_at=.5)
p.badge(9, 560, 384, step=9, color=PURPLE)
p.text(550, 430, "PTES groups the work as pre-engagement, intelligence gathering, threat modeling, vulnerability analysis,", 13, MUTED, italic=True)
p.text(550, 450, "exploitation, post-exploitation, and reporting; NIST SP 800-115 gives the U.S. government's technical guide.", 13, MUTED, italic=True)
p.save(OUT + "ch06_phases")

# 4. Rules of engagement
r = Fig(1100, 580, "Rules of engagement: the signed document that authorizes and bounds the test",
        "At the center is the RoE. Around it: scope with in-scope and out-of-scope IP lists, permitted dates and times, the testing "
        "team's source IP addresses, a single client monitor who can halt the test, permitted and forbidden techniques such as "
        "denial of service or social engineering, immediate reporting of critical findings, data handling, restoration after the "
        "test, and the approval signatures that make it lawful.")
r.card(420, 170, 260, 260, "certificate", "Rules of engagement", "signed before any\npacket is sent", BLUE, step=1, icon_size=110, title_size=18)
r.badge(1, 430, 180, step=1)
items = [("checklist", "Scope", "in-scope and out-of-scope\nIP lists, targets, vectors", 130, 110),
         ("clock", "Dates and times", "exact windows and locations", 130, 250),
         ("laptop", "Tester source IPs", "so defenders can tell test\ntraffic from real attacks", 130, 390),
         ("headset", "One client monitor", "single contact who can\nhalt the test", 130, 520),
         ("warning", "Allowed techniques?", "DoS, MITM, reboots, physical\nentry, social engineering", 900, 110),
         ("bug", "Critical findings", "reported immediately,\nnot at the end", 900, 250),
         ("lock", "Data handling", "how client data is kept\nand destroyed", 900, 390),
         ("gear", "Restoration", "remove artifacts, help\nrestore systems", 900, 520)]
for k, (ic, t1, t2, x, y) in enumerate(items):
    st = 2 + k // 2
    r.icon(ic, x - 70, y, 50, step=st)
    left = x < 550
    r.text(x - 36, y - 8, t1, 15, INK, "bold", "start", step=st); r.text(x - 36, y + 12, t2, 12, INK, anchor="start", step=st)
    r.arrow([(x + 150 if left else x - 120, y), (420 if left else 680, 300 + (y - 315) * 0.35)], None, "#9aa5b1", step=st, width=1.6)
r.badge(2, 20, 80, step=2); r.badge(3, 20, 360, step=3); r.badge(4, 800, 80, step=4); r.badge(5, 800, 360, step=5); r.badge(6, 520, 490, step=6)
r.icon("cross", 550, 490, 30, step=6); r.text(550, 530, "Scope creep, testing beyond what was signed, is unauthorized access.", 14, RED, "bold", step=6)
r.save(OUT + "ch06_roe")

# 5. Critical path and pivoting
v = Fig(1100, 600, "Pivoting along a documented critical path",
        "From the tester's Kali machine at 192.168.1.10, an nmap scan of file server FS1 at 10.10.10.100 finds Apache 2.0.48, RDP, "
        "and SMB. An authorized Metasploit exploit of the vulnerable Apache gives a Meterpreter session. A post-exploitation survey of "
        "FS1 finds cached credentials. With them the tester moves laterally to domain controller DC1 at 10.10.10.101, and notifies "
        "the client monitor. Every step is time-stamped in the operational notes.")
v.zone(20, 60, 230, 300, "Tester", "#7f8c8d", "#f6f7f8")
v.icon("laptop", 135, 190, 96, "Kali", "192.168.1.10")
v.icon("firewall", 330, 190, 80); v.text(330, 248, "Firewall", 14, INK, "bold")
v.zone(400, 60, 680, 300, "Client network 10.10.10.0/24", BLUE, "#eef5fc")
v.icon("server", 560, 190, 96, "FS1", "10.10.10.100")
v.icon("server", 930, 190, 96, "DC1", "10.10.10.101"); v.icon("idcard", 965, 150, 34)
v.arrow([(185, 165), (510, 165)], "nmap scan", BLUE, step=1, size=13, label_at=.8, label_dy=-30); v.badge(1, 190, 165, step=1)
v.arrow([(185, 215), (510, 215)], "exploit Apache", RED, step=2, size=13, label_at=.88, label_dy=24, width=2.6); v.badge(2, 190, 215, step=2, color=RED)
v.icon("key", 650, 285, 40, step=3); v.text(650, 324, "cached credentials", 13, ORANGE, "bold", step=3); v.badge(3, 612, 285, step=3, color=ORANGE)
v.arrow([(610, 190), (880, 190)], "lateral movement with credentials", RED, step=4, size=13, width=3); v.badge(4, 745, 212, step=4, color=RED)
v.icon("headset", 960, 470, 64, "Client monitor", step=5); v.arrow([(930, 285), (950, 430)], None, ORANGE, step=5, dash=True); v.text(932, 400, "notified", 13, ORANGE, "bold", "end", step=5)
v.badge(5, 920, 450, step=5, color=ORANGE)
v.rect(30, 390, 820, 190, "#1f2933", "#1f2933", 1, rx=8, step=6)
v.text(50, 418, "Operational notes (critical path: Kali -> FS1 -> DC1)", 13, "#8fd16a", "bold", "start", step=6)
for k, line in enumerate(["13:42  nmap -T4 -Pn -sT -p 443,445,389,3389 10.10.10.100  ->  443 Apache 2.0.48; 3389 RDP; 445 SMB",
                          "13:59  vulnerable Apache; authorized Metasploit exploit  ->  Meterpreter session",
                          "14:12  post-exploitation survey of FS1  ->  located cached credentials",
                          "14:40  lateral movement to DC1 using recovered credentials (success)  ->  NOTIFIED MONITOR"]):
    v.text(50, 450 + k * 30, line, 13, "#e4e7eb", anchor="start", step=6)
v.badge(6, 30, 390, step=6)
v.save(OUT + "ch06_pivoting")
print("ok")
