import os
import sys, math, datetime as dt; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# Redraw: Japan, October 2026
D = dt.date
ev = [(D(2026, 10, 1), "Active Cyber Defense powers\nand reporting take effect", 1, "shield", BLUE),
      (D(2026, 10, 7), "IDC Frontier ransomware reported;\n495 companies and local governments", -1, "bug", RED),
      (D(2026, 10, 9), "National Cybersecurity Office advisory;\nLDP official: an emergency in cyberspace", 2, "warning", ORANGE),
      (D(2026, 10, 20), "LDP emergency proposals:\na headquarters under the PM's office", -2, "bank", BLUE),
      (D(2026, 10, 23), "PM: the National Cybersecurity\nOffice is the command center", 1, "bank", BLUE),
      (D(2026, 10, 24), "GMO asks for active cyber defense;\nup to 26,739 servers may be affected", -1, "server", RED),
      (D(2026, 10, 26), "PM orders emergency measures\nby the end of the next week", 2, "checklist", BLUE)]
j = Fig(1100, 640, "Japan, October 2026: from a breach wave to a national response",
        "October 1: Active Cyber Defense powers and reporting take effect. October 7: IDC Frontier ransomware reported, affecting 495 "
        "companies and local governments. October 9: National Cybersecurity Office advisory, and an LDP official calls it an "
        "emergency in cyberspace. October 20: LDP emergency proposals for a headquarters under the Prime Minister's office. October "
        "23: the Prime Minister names the National Cybersecurity Office the command center. October 24: GMO asks for active cyber "
        "defense; up to 26,739 servers may be affected. October 26: the Prime Minister orders emergency measures by the end of the "
        "next week.")
x = lambda d: 80 + (d - D(2026, 9, 28)).days * 31
Y = 330
j.raw(f'<line x1="40" y1="{Y}" x2="1060" y2="{Y}" stroke="#2b3138" stroke-width="3"/>')
for d in [D(2026, 10, k) for k in (1, 7, 9, 20, 23, 26)]: j.text(x(d), Y + 28 if d.day not in (20, 23, 26) or True else 0, d.strftime("Oct %d"), 12, MUTED, "bold")
offs = {1: 0, 7: 0, 9: 0, 20: -30, 23: -62, 24: 30, 26: 0}
for i, (d, lab, lev, ic, col) in enumerate(ev):
    xx = x(d) + offs[d.day]; yy = Y - lev * 110 + (0 if lev > 0 else 30)
    j.raw(f'<line x1="{x(d)}" y1="{Y}" x2="{xx}" y2="{yy + (40 if lev > 0 else -40)}" stroke="#9aa5b1" stroke-width="1.6"/>', step=i + 1)
    j.circle(x(d), Y, 8, col, "#ffffff", 2, step=i + 1)
    j.rect(xx - 150, yy - 36, 300, 76, "#ffffff", col, 1.8, rx=8, step=i + 1)
    j.icon(ic, xx - 125, yy + 2, 36, step=i + 1)
    j.text(xx + 22, yy - 6, lab, 12, INK, "bold", step=i + 1); j.badge(i + 1, xx + 142, yy - 36, step=i + 1, color=col)
j.save(OUT + "ch14_japan_timeline_v2")

# The six-phase lifecycle
c = Fig(1000, 600, "The incident response lifecycle: six phases and a feedback loop",
        "Preparation, identification, containment, eradication, recovery, and lessons learned, in a cycle. Lessons learned feeds back "
        "into preparation, so each incident makes the next response faster.")
cx, cy, R = 500, 320, 200
c.circle(cx, cy, R, "none", "#c5ccd3", 3); c.icon("shield", cx, cy - 8, 90, "Incident response")
ph = [("Preparation", "team, playbooks, tools", "checklist", BLUE), ("Identification", "is it real? how big?", "search", "#16a085"),
      ("Containment", "stop the spread", "firewall", ORANGE), ("Eradication", "remove the cause", "trash", RED),
      ("Recovery", "restore, monitor", "gear", GREEN), ("Lessons learned", "fix the gaps", "logbook", PURPLE)]
for i, (name, sub, ic, col) in enumerate(ph):
    ang = -90 + i * 60; a = math.radians(ang); px, py = cx + R * math.cos(a), cy + R * math.sin(a)
    c.circle(px, py, 46, "#ffffff", col, 3, step=i + 1); c.icon(ic, px, py - 2, 54, step=i + 1); c.badge(i + 1, px - 36, py - 36, step=i + 1, color=col)
    if abs(math.cos(a)) < 0.2: tx, ty, ta = px + 58, py - 34 if py < cy else py + 26, "start"
    elif math.cos(a) > 0: tx, ty, ta = px + 56, py - 4, "start"
    else: tx, ty, ta = px - 56, py - 4, "end"
    c.text(tx, ty, name, 16, col, "bold", ta, step=i + 1); c.text(tx, ty + 18, sub, 13, INK, anchor=ta, step=i + 1)
    a2, a3 = math.radians(ang + 14), math.radians(ang + 46)
    c.arrow([(cx + R * math.cos(a2), cy + R * math.sin(a2)), (cx + R * math.cos(a3), cy + R * math.sin(a3))], None, col, step=i + 2, width=3)
c.save(OUT + "ch14_ir_lifecycle")

# Locky case
l = Fig(1100, 520, "The Locky case: one opened attachment, four steps during, four after",
        "On a Monday morning one user with permissions opened a malicious attachment and Locky began encrypting files. During the "
        "attack the team examined logs, switched the affected server's file system to read-only to stop further encryption, found the "
        "infected system and cut it off the network, and prepared to recover. Afterward they documented, restored from backups, "
        "educated users, and communicated.")
l.icon("envelope", 90, 150, 60, "attachment", step=1); l.icon("user-laptop", 220, 150, 80, "one user", "with permissions", step=1)
l.arrow([(122, 150), (172, 150)], None, RED, step=1, width=2.4); l.badge(1, 50, 100, step=1, color=RED)
l.icon("server", 400, 150, 80, "File server", step=2); l.icon("lock", 440, 110, 30, step=2); l.icon("bug", 360, 110, 28, step=2)
l.arrow([(268, 150), (356, 150)], "Locky encrypts", RED, step=2, size=12, width=2.6); l.badge(2, 360, 70, step=2, color=RED)
dur = [("search", "Examine logs", "network, server, access"), ("document", "Read-only", "stop more encryption"), ("firewall", "Isolate", "cut the host off the network"), ("gear", "Prepare", "to recover")]
aft = [("logbook", "Document", ""), ("database", "Restore", "from backups"), ("group", "Educate", "spot the next lure"), ("envelope", "Communicate", "")]
l.text(560, 80, "During the attack", 16, ORANGE, "bold", "start", step=3)
for i, (ic, a, b) in enumerate(dur):
    xx = 560 + i * 130; l.icon(ic, xx + 30, 140, 46, step=3 + i); l.text(xx + 30, 186, a, 13, ORANGE, "bold", step=3 + i); l.text(xx + 30, 202, b, 11, INK, step=3 + i)
    l.badge(3 + i, xx + 4, 112, step=3 + i, color=ORANGE)
l.raw('<line x1="30" y1="240" x2="1070" y2="240" stroke="#d0d6dd" stroke-width="2" stroke-dasharray="6 6"/>')
l.text(40, 280, "After the attack", 16, GREEN, "bold", "start", step=7)
for i, (ic, a, b) in enumerate(aft):
    xx = 80 + i * 250; l.icon(ic, xx, 340, 56, step=7 + i); l.text(xx + 44, 336, a, 15, GREEN, "bold", "start", step=7 + i); l.text(xx + 44, 356, b, 12, INK, anchor="start", step=7 + i)
    l.badge(7 + i, xx - 40, 310, step=7 + i, color=GREEN)
    if i < 3: l.arrow([(xx + 160, 340), (xx + 210, 340)], None, GREEN, step=8 + i, width=2.2)
l.rect(40, 420, 1020, 70, "#fff8e1", "#d9a400", 1.6, rx=8, step=11); l.icon("warning", 76, 455, 32, step=11)
l.text(106, 450, "The responders say they were partly lucky and skipped steps they later formalized:", 13, INK, "bold", "start", step=11)
l.text(106, 470, "breaches start with people, process beats panic, and recovery depends on backups made long before.", 13, INK, "bold", "start", step=11)
l.save(OUT + "ch14_locky")

# Ransomware response, hour by hour
r = Fig(1100, 540, "A ransomware response: detect, triage, contain two ways, eradicate, recover",
        "The EDR platform flags a host renaming files with a new extension and deleting volume shadow copies. The team triages and "
        "scopes, then contains on two tracks at once: isolate hosts and disable accounts, and capture memory and disk images. Then it "
        "eradicates persistence and resets credentials, recovers from clean, offline backups, and records lessons learned.")
r.card(30, 90, 200, 150, "desktop", "Detection", "EDR: mass renames,\nvssadmin delete shadows", RED, step=1, icon_size=54, title_size=15); r.badge(1, 40, 100, step=1, color=RED)
r.card(270, 90, 180, 150, "search", "Triage, scope", "which hosts, which\naccounts?", ORANGE, step=2, icon_size=54, title_size=15); r.badge(2, 280, 100, step=2, color=ORANGE)
r.arrow([(232, 165), (268, 165)], None, INK, step=2, width=2.4)
r.card(500, 60, 220, 130, "firewall", "Isolate hosts", "disable accounts", ORANGE, step=3, icon_size=50, title_size=15)
r.card(500, 220, 220, 130, "memory", "Preserve evidence", "memory and disk images", BLUE, step=3, icon_size=50, title_size=15)
r.arrow([(452, 150), (498, 125)], None, INK, step=3, width=2.2); r.arrow([(452, 180), (498, 285)], None, INK, step=3, width=2.2); r.badge(3, 480, 200, step=3)
r.card(770, 130, 140, 150, "trash", "Eradicate", "persistence out,\ncredentials reset", PURPLE, step=4, icon_size=46, title_size=14)
r.arrow([(722, 125), (768, 180)], None, INK, step=4, width=2.2); r.arrow([(722, 285), (768, 230)], None, INK, step=4, width=2.2); r.badge(4, 780, 140, step=4, color=PURPLE)
r.card(950, 130, 130, 150, "database", "Recover", "clean, offline\nbackups", GREEN, step=5, icon_size=46, title_size=14); r.badge(5, 960, 140, step=5, color=GREEN)
r.arrow([(912, 205), (948, 205)], None, INK, step=5, width=2.4)
r.arrow([(1015, 282), (1015, 410), (130, 410), (130, 242)], "lessons learned and hardening feed the next preparation", MUTED, step=6, dash=True, width=2.4, label_at=.42)
r.badge(6, 570, 410, step=6, color=MUTED)
r.text(550, 480, "Contain and preserve run in parallel: isolate to stop the spread, but capture volatile evidence first where you can.", 14, INK, "bold", step=6)
r.save(OUT + "ch14_ransomware_response")

# CSIRT and communication
k = Fig(1100, 540, "The CSIRT: an incident commander, a cross-functional team, and planned communication",
        "The incident commander runs the response with technical responders, legal, communications and PR, human resources, and "
        "executive leadership, organized with a RACI chart. Communication goes out of band, because the attacker may be reading "
        "corporate email, to customers, regulators, law enforcement, and the public. Notification clocks such as GDPR's 72 hours start "
        "during the incident, so counsel joins early.")
k.icon("user2", 550, 250, 100, "Incident commander", "RACI: who is Responsible,\nAccountable, Consulted, Informed", step=1); k.badge(1, 490, 180, step=1)
team = [("user-laptop", "Technical responders"), ("certificate", "Legal counsel"), ("envelope", "Communications, PR"), ("idcard", "Human resources"), ("group", "Executives")]
for i, (ic, lab) in enumerate(team):
    ang = math.radians(200 + i * 35); px, py = 550 + 330 * math.cos(ang) * 0.9, 250 + 200 * math.sin(ang)
    px = 120 + i * 0 if False else px
for i, (ic, lab) in enumerate(team):
    px, py = 150, 80 + i * 90
    k.icon(ic, px, py, 50, step=2); k.text(px + 40, py + 5, lab, 14, INK, "bold", "start", step=2); k.arrow([(345, py), (490, 250)], None, BLUE, step=2, width=1.6, both=True)
k.badge(2, 100, 50, step=2)
ext = [("group", "Customers"), ("bank", "Regulators", "GDPR: 72 hours"), ("shield", "Law enforcement"), ("browser", "The public")]
for i, e in enumerate(ext):
    px, py = 930, 90 + i * 100
    k.icon(e[0], px, py, 50, step=3); k.text(px + 40, py + 2, e[1], 14, INK, "bold", "start", step=3)
    if len(e) > 2: k.text(px + 40, py + 20, e[2], 12, RED, "bold", "start", step=3)
    k.arrow([(610, 250), (888, py)], None, ORANGE, step=3, width=1.6, dash=True)
k.badge(3, 880, 50, step=3, color=ORANGE)
k.icon("phone", 760, 150, 40, step=4); k.text(760, 120, "out-of-band channel", 12, ORANGE, "bold", step=4)
k.icon("cross", 720, 370, 26, step=4); k.icon("envelope", 760, 370, 34, step=4); k.text(760, 410, "not corporate email:", 12, RED, "bold", step=4); k.text(760, 426, "the attacker may read it", 12, RED, "bold", step=4)
k.badge(4, 700, 180, step=4, color=ORANGE)
k.save(OUT + "ch14_csirt_comms")

# BEC
b = Fig(1100, 560, "Business email compromise: no malware, just a mailbox and a changed bank account",
        "An accounts-payable clerk enters credentials on a lookalike Microsoft 365 login page; with no MFA the attacker logs in, reads "
        "the mailbox for days, and adds an inbox rule that forwards and deletes messages containing invoice or payment. Posing as a "
        "known vendor from a lookalike domain, the attacker sends an invoice with new bank details, and the clerk wires a large sum. "
        "Response: revoke sessions, reset the password with MFA, remove the rule, and call the bank and law enforcement at once, "
        "which recovered part of the funds. Fixes: MFA, block external auto-forwarding, and verify payment changes by phone.")
b.icon("browser", 90, 140, 70, "lookalike login", step=1); b.icon("user-laptop", 260, 140, 80, "AP clerk", step=1)
b.arrow([(212, 140), (128, 140)], "credentials", RED, step=1, size=12, width=2.4); b.badge(1, 50, 90, step=1, color=RED)
b.icon("attacker", 450, 140, 76, "Attacker", "no MFA: logs in", step=2); b.arrow([(130, 160), (400, 160)], None, RED, step=2, width=2, dash=True); b.badge(2, 410, 90, step=2, color=RED)
b.icon("envelope", 640, 140, 64, "Mailbox", "read for days", step=3); b.arrow([(492, 140), (604, 140)], None, RED, step=3, width=2.4)
b.rect(720, 100, 340, 80, "#1f2933", "#1f2933", 1, rx=8, step=3)
b.text(736, 124, "Inbox rule: if subject or body has", 12, "#8fd16a", "bold", "start", step=3)
b.text(736, 146, "'invoice' or 'payment': forward, then delete", 12, "#e4e7eb", anchor="start", step=3); b.text(736, 166, "the tell to check first", 11, "#f5b041", anchor="start", step=3)
b.badge(3, 720, 100, step=3, color=RED)
b.icon("document", 300, 290, 60, "invoice, new bank details", step=4, label_size=12); b.icon("devil", 330, 260, 26, step=4)
b.text(300, 352, "from a lookalike vendor domain", 12, RED, step=4); b.badge(4, 250, 250, step=4, color=RED)
b.icon("money", 600, 290, 70, "large wire sent", step=5); b.arrow([(340, 290), (560, 290)], None, RED, step=5, width=2.6); b.badge(5, 560, 240, step=5, color=RED)
b.icon("bank", 860, 290, 70, "bank + FBI IC3", "partial recovery", step=6); b.arrow([(640, 290), (816, 290)], "recall the wire, fast", GREEN, step=6, size=12, width=2.4)
b.badge(6, 820, 240, step=6, color=GREEN)
b.rect(30, 400, 1040, 140, "#e8f5e9", GREEN, 1.6, rx=8, step=7); b.badge(7, 30, 400, step=7, color=GREEN); b.icon("shield", 70, 440, 40, step=7)
b.text(100, 432, "Contain: revoke sessions and tokens, reset the password with MFA enrollment, remove the inbox rule.", 13, GREEN, "bold", "start", step=7)
b.text(100, 458, "Fix the process: enforce MFA, block external auto-forwarding, and confirm any change to payment", 13, GREEN, "bold", "start", step=7)
b.text(100, 478, "details by calling a known number.", 13, GREEN, "bold", "start", step=7)
b.text(100, 510, "Nothing malicious ran on any endpoint, which is why malware-focused defenses miss BEC.", 13, INK, anchor="start", step=7, italic=True)
b.save(OUT + "ch14_bec")
print("ok")
