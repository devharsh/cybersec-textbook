import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# 1. Chain of custody
c = Fig(1100, 460, "Chain of custody: every hand-off recorded, from seizure to court",
        "A responder seizes the laptop, bags it, hashes the image, and signs the custody form. Each transfer, to the courier, the lab "
        "analyst, and the evidence locker, and finally to court, is logged with who, when, and why, and the hash is re-verified. An "
        "unrecorded transfer is a break that lets the defense argue tampering.")
ppl = [("user", "Responder", "seizes, bags, hashes"), ("user2", "Courier", "transports, sealed"), ("user-laptop", "Lab analyst", "works on a verified copy"),
       ("lock", "Evidence locker", "stored, access logged"), ("bank", "Court", "evidence admitted")]
for i, (ic, lab, sub) in enumerate(ppl):
    x = 100 + i * 225
    c.icon(ic, x, 150, 80, lab, sub, step=i + 1); c.badge(i + 1, x - 46, 100, step=i + 1)
    if i < 4:
        c.arrow([(x + 50, 150), (x + 175, 150)], None, BLUE, step=i + 2, width=2.6)
        c.icon("logbook", x + 112, 108, 30, step=i + 2); c.text(x + 112, 182, "signed, timed", 11, BLUE, "bold", step=i + 2)
c.rect(40, 270, 1020, 80, "#1f2933", "#1f2933", 1, rx=8, step=6); c.badge(6, 40, 270, step=6, color=GREEN)
c.text(60, 296, "Custody form, item 1: laptop, serial ...  SHA-256 of image: 9c4e...a71f", 13, "#8fd16a", "bold", "start", step=6)
c.text(60, 320, "2026-03-02 09:14 seized by J. Doe  ->  09:40 courier  ->  11:05 lab  ->  18:30 locker   (hash re-verified each time)", 12, "#e4e7eb", anchor="start", step=6)
c.text(60, 340, "illustrative entries", 11, "#9aa5b1", anchor="start", step=6)
c.icon("warning", 80, 410, 34, step=7); c.badge(7, 50, 392, step=7, color=RED)
c.text(110, 404, "A break, such as an unrecorded transfer or a missing signature, lets the defense argue the evidence was", 13, RED, "bold", "start", step=7)
c.text(110, 422, "tampered with. Corporate cases that may reach court follow the same standard as law enforcement.", 13, RED, "bold", "start", step=7)
c.save(OUT + "ch13_chain_of_custody")

# 2. Acquisition with a write blocker and hash verification
a = Fig(1100, 500, "Forensic acquisition: block writes, image every bit, prove the copy matches",
        "The suspect drive connects through a hardware write blocker to the forensic workstation, which makes a bit-for-bit image "
        "with dd, dcfldd, or FTK Imager, often in E01 format. A SHA-256 hash of the source and of the image must match; any later "
        "re-hash proves the image is unchanged. Analysis happens only on a verified copy. A physical image includes deleted files and "
        "unallocated space that a logical copy misses.")
a.icon("database", 100, 170, 90, "Suspect drive")
a.icon("chip", 320, 170, 80, "Write blocker", "hardware, e.g. Tableau", step=1); a.icon("cross", 340, 120, 24, step=1); a.text(380, 116, "no writes", 12, RED, "bold", "start", step=1)
a.arrow([(148, 170), (276, 170)], "read only", BLUE, step=1, size=12, width=2.6); a.badge(1, 290, 100, step=1)
a.icon("desktop", 560, 170, 90, "Forensic workstation", "dd, dcfldd, FTK Imager", step=2); a.arrow([(364, 170), (510, 170)], None, BLUE, step=2, width=2.6); a.badge(2, 520, 100, step=2)
a.icon("document", 820, 170, 70, "case001.E01", "bit-for-bit image", step=3); a.arrow([(610, 170), (780, 170)], None, BLUE, step=3, width=2.6); a.badge(3, 790, 110, step=3)
a.icon("document", 990, 170, 60, "working copy", step=5); a.arrow([(860, 170), (956, 170)], None, GREEN, step=5, width=2.4); a.badge(5, 1040, 110, step=5, color=GREEN)
a.rect(60, 270, 400, 60, "#ffffff", "#9aa5b1", 1.4, rx=6, step=4); a.text(80, 296, "source SHA-256:  9c4e 1b07 ... a71f", 13, INK, "bold", "start", step=4)
a.text(80, 318, "image  SHA-256:  9c4e 1b07 ... a71f", 13, INK, "bold", "start", step=4)
a.icon("check", 490, 300, 34, step=4); a.text(516, 306, "match: the copy is exact", 14, GREEN, "bold", "start", step=4); a.badge(4, 60, 270, step=4)
a.text(550, 346, "illustrative hash values", 11, MUTED, italic=True, step=4)
for i, (name, what, miss) in enumerate([("Logical acquisition", "visible files and folders", "misses deleted files and unallocated space"),
                                        ("Physical acquisition", "every sector of the device", "slower, but keeps every recoverable artifact")]):
    x = 60 + i * 520
    a.rect(x, 380, 480, 90, "#eef5fc" if i else "#fff8e1", BLUE if i else "#d9a400", 1.6, rx=8, step=6)
    a.text(x + 20, 408, name, 15, BLUE if i else "#8a6d1a", "bold", "start", step=6); a.text(x + 20, 430, "copies: " + what, 13, INK, anchor="start", step=6)
    a.text(x + 20, 452, miss, 13, INK, anchor="start", step=6)
a.badge(6, 60, 380, step=6)
a.save(OUT + "ch13_acquisition")

# 3. Order of volatility
v = Fig(1100, 520, "Order of volatility: collect what disappears first",
        "A staircase from most to least volatile: CPU registers and cache; RAM with processes, network connections, and keys; disk, "
        "swap, and the hibernation file; remote logs and monitoring data; physical configuration and network topology; and archival "
        "media and backups. Collect from the top down, because a reboot erases the first two in an instant.")
lv = [("chip", "1. CPU registers and cache", "gone in nanoseconds"), ("memory", "2. RAM: processes, connections, keys", "gone at power-off"),
      ("database", "3. Disk, swap, hibernation file", "survives reboot, can be overwritten"), ("logbook", "4. Remote logs and monitoring data", "rotates on a schedule"),
      ("nodes", "5. Physical configuration and topology", "changes slowly"), ("document", "6. Archival media and backups", "most durable")]
for i, (ic, lab, sub) in enumerate(lv):
    x = 40 + i * 60; y = 60 + i * 72; w = 1020 - i * 60
    col = ["#c0392b", "#d35400", "#e67e22", "#d4ac0d", "#28b463", "#1e8449"][i]
    v.rect(x, y, w, 62, "#ffffff", col, 2.4, rx=8, step=i + 1); v.rect(x, y, 10, 62, col, col, 1, rx=4, step=i + 1)
    v.icon(ic, x + 50, y + 31, 44, step=i + 1); v.text(x + 86, y + 28, lab, 16, col, "bold", "start", step=i + 1); v.text(x + 86, y + 48, sub, 13, INK, anchor="start", step=i + 1)
    v.badge(i + 1, x + w - 18, y + 16, step=i + 1, color=col)
v.arrow([(1070, 70), (1070, 480)], None, MUTED, step=7, width=2.4); v.text(1060, 500, "less volatile", 12, MUTED, "bold", "end", step=7)
v.text(40, 506, "Collect from the top: a reboot destroys levels 1 and 2 at once.", 14, RED, "bold", "start", step=7)
v.save(OUT + "ch13_volatility")

# 4. Timeline analysis
t = Fig(1100, 520, "Timeline analysis: many artifacts, one normalized sequence",
        "File-system MACB timestamps, event logs, the registry, browser history, and prefetch are parsed by The Sleuth Kit or plaso "
        "into one super-timeline in UTC. Read outward from the initial-access moment, such as an attachment opened, to credential "
        "theft, lateral movement, staging, and exfiltration. Pitfalls: timestomping, clock drift, and mixed time zones.")
src = [("database", "MACB times"), ("logbook", "Event logs"), ("gear", "Registry"), ("browser", "Browser history"), ("document", "Prefetch")]
for i, (ic, lab) in enumerate(src):
    x = 90 + i * 140; t.icon(ic, x, 90, 48, lab, step=1, label_size=12); t.arrow([(x, 140), (430, 206)], None, "#9aa5b1", step=1, width=1.4)
t.badge(1, 30, 70, step=1)
t.card(330, 206, 220, 90, "clock", "plaso super-timeline", None, BLUE, step=2, icon_size=36, title_size=13); t.badge(2, 340, 216, step=2)
t.text(700, 230, "log2timeline.py  then  psort.py", 13, BLUE, "bold", step=2); t.text(700, 252, "or fls -m  then  mactime", 13, BLUE, "bold", step=2)
t.text(700, 274, "all times normalized to UTC", 13, INK, step=2)
Y = 380
t.raw(f'<line x1="60" y1="{Y}" x2="1060" y2="{Y}" stroke="#52606d" stroke-width="3"/>', step=3)
ev = [("envelope", "attachment opened", "initial access"), ("key", "credentials dumped", "credential theft"), ("nodes", "logon to a second host", "lateral movement"),
      ("document", "archive created", "staging"), ("cloud", "large upload", "exfiltration")]
for i, (ic, lab, ph) in enumerate(ev):
    x = 140 + i * 210; col = RED if i == 0 else ORANGE
    t.raw(f'<line x1="{x}" y1="{Y - 8}" x2="{x}" y2="{Y + 8}" stroke="#52606d" stroke-width="3"/>', step=3 + i)
    t.icon(ic, x, Y - 40, 44, step=3 + i); t.text(x, Y + 28, lab, 13, INK, "bold", step=3 + i); t.text(x, Y + 46, ph, 12, col, "bold", step=3 + i)
    t.badge(3 + i, x - 34, Y - 60, step=3 + i, color=col)
t.text(140, Y + 74, "start here, then read outward", 12, RED, italic=True, step=3)
t.icon("warning", 700, Y + 92, 26, step=8); t.badge(8, 672, Y + 80, step=8, color=RED)
t.text(720, Y + 98, "timestomping, clock drift, mixed time zones", 13, RED, "bold", "start", step=8)
t.save(OUT + "ch13_timeline")

# 5. Cloud forensics
f = Fig(1100, 520, "Cloud forensics: snapshots and audit logs instead of a seized disk",
        "In the cloud the investigator cannot seize hardware. Volatile state is captured before an instance is terminated, the virtual "
        "disk is snapshotted and copied to a separate, access-controlled forensic account, and the audit logs, AWS CloudTrail, Azure "
        "Activity Logs with Entra sign-in logs, or Google Cloud Audit Logs, show which API calls were made, by whom, when, and from "
        "where. Challenges: shared responsibility, multi-tenancy, data residency, and short-lived resources.")
f.zone(30, 60, 470, 300, "Production account", RED, "#fdf2f1")
f.icon("server", 140, 180, 80, "Compromised instance"); f.icon("bug", 170, 140, 28)
f.icon("memory", 140, 300, 44, step=1); f.text(190, 306, "capture memory first", 12, RED, "bold", "start", step=1); f.badge(1, 90, 284, step=1, color=RED)
f.icon("database", 360, 180, 70, "disk snapshot", step=2); f.arrow([(186, 180), (320, 180)], None, BLUE, step=2, width=2.4); f.badge(2, 310, 120, step=2)
f.zone(560, 60, 510, 300, "Forensic account (isolated)", GREEN, "#eef8ef", step=3)
f.icon("lock", 600, 106, 30, step=3); f.text(620, 112, "restricted access", 12, GREEN, "bold", "start", step=3); f.icon("database", 780, 180, 70, "snapshot copy", step=3)
f.icon("desktop", 950, 180, 70, "analysis host", step=4)
f.arrow([(400, 180), (740, 180)], None, GREEN, step=3, width=2.6); f.text(650, 168, "copy and hash", 12, GREEN, "bold", step=3); f.badge(3, 860, 110, step=3, color=GREEN)
f.arrow([(820, 180), (910, 180)], None, GREEN, step=4, width=2.4); f.badge(4, 990, 110, step=4, color=GREEN)
f.rect(30, 380, 520, 120, "#1f2933", "#1f2933", 1, rx=8, step=5); f.badge(5, 30, 380, step=5)
f.text(46, 406, "Audit logs: who called which API, when, from where", 13, "#8fd16a", "bold", "start", step=5)
for i, l in enumerate(["AWS: CloudTrail", "Azure: Activity Logs, Entra sign-in logs", "Google Cloud: Cloud Audit Logs"]):
    f.text(46, 432 + i * 22, l, 13, "#e4e7eb", anchor="start", step=5)
f.text(580, 400, "Challenges", 15, ORANGE, "bold", "start", step=6); f.badge(6, 564, 394, step=6, color=ORANGE)
for i, l in enumerate(["shared responsibility: some layers are the provider's", "multi-tenancy and data residency", "short-lived resources: configure logging before an incident"]):
    f.text(590, 426 + i * 22, "- " + l, 13, INK, anchor="start", step=6)
f.save(OUT + "ch13_cloud_forensics")
print("ok")
