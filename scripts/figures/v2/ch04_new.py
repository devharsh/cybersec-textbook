import os
import sys, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# 1. Social-engineering lifecycle
f = Fig(1000, 600, "The social-engineering attack lifecycle: research, hook, play, exit",
        "Four phases around a cycle. Research: the attacker gathers open-source intelligence from websites, social media, job "
        "postings, and trash. Hook: the attacker makes contact with a pretext and builds trust. Play: the attacker uses that trust to "
        "get a password, a wire transfer, physical access, or malware run. Exit: the attacker withdraws without arousing suspicion. "
        "Sophisticated campaigns repeat the cycle for deeper access.")
cx, cy, R = 500, 315, 180
f.circle(cx, cy, R, "none", "#c5ccd3", 3)
f.icon("attacker", cx, cy - 10, 100, "Social engineer")
phases = [("Research", "OSINT: website, social media,\njob posts, dumpster diving", "search", -90, BLUE),
          ("Hook", "make contact, use a pretext,\nbuild rapport and trust", "fishhook", 0, ORANGE),
          ("Play", "exploit the trust: password,\nwire transfer, access, malware", "money", 90, RED),
          ("Exit", "withdraw cleanly so the\nintrusion goes unnoticed", "door", 180, PURPLE)]
for i, (name, sub, ic, ang, col) in enumerate(phases):
    a = math.radians(ang); x, y = cx + R * math.cos(a), cy + R * math.sin(a)
    f.circle(x, y, 50, "#ffffff", col, 3, step=i + 1)
    f.icon(ic, x, y - 4, 64, step=i + 1)
    tx = x + (-75 if ang == 180 else 75); ta = "end" if ang == 180 else "start"
    ty = y - 30 if ang == -90 else y + 22 if ang == 90 else y - 8
    f.text(tx, ty, name, 18, col, "bold", ta, step=i + 1)
    f.text(tx, ty + 20, sub, 13, INK, anchor=ta, step=i + 1)
    f.badge(i + 1, x - 38, y - 38, step=i + 1, color=col)
    a2 = math.radians(ang + 22); a3 = math.radians(ang + 68)
    if i < 3:
        f.arrow([(cx + R * math.cos(a2), cy + R * math.sin(a2)), (cx + (R + 0.1) * math.cos(a3), cy + R * math.sin(a3))], None, col, step=i + 2, width=3)
f.arrow([(cx + R * math.cos(math.radians(202)), cy + R * math.sin(math.radians(202))), (cx + R * math.cos(math.radians(248)), cy + R * math.sin(math.radians(248)))],
        None, MUTED, step=5, width=2.4, dash=True)
f.text(250, 150, "repeat for deeper access", 13, MUTED, "bold", step=5, italic=True); f.badge(5, 250, 172, step=5, color=MUTED)
f.save(OUT + "ch04_se_lifecycle")

# 2. Taxonomy
t = Fig(1100, 600, "The social-engineering toolkit: at a distance and in person",
        "Phishing family: phishing casts a wide net by email; spear phishing targets a researched person; whaling targets "
        "executives, often as CEO fraud; vishing uses the phone; smishing uses text messages; pharming redirects a correct web "
        "address to a fake site by tampering with DNS. Other distance techniques: pretexting, baiting with infected USB drives, quid "
        "pro quo, and reverse social engineering. In person: tailgating, piggybacking, dumpster diving, and shoulder surfing.")
groups = [("Phishing family (at a distance)", BLUE, 1, [("Phishing", "wide net, mostly email", "envelope"), ("Spear phishing", "researched, personal", "fishhook"),
           ("Whaling", "executives, CEO fraud", "user2"), ("Vishing", "voice, phone calls", "headset"), ("Smishing", "SMS with a link", "phone"),
           ("Pharming", "fake site via DNS", "browser")]),
          ("Other distance techniques", ORANGE, 2, [("Pretexting", "an invented story", "idcard"), ("Baiting", "USB drive marked Payroll", "usb"),
           ("Quid pro quo", "help for a password", "gear"), ("Reverse SE", "cause a problem, then fix it", "warning")]),
          ("In person", RED, 3, [("Tailgating", "follow without consent", "door"), ("Piggybacking", "follow with consent", "group"),
           ("Dumpster diving", "documents in the trash", "trash"), ("Shoulder surfing", "watch the PIN typed", "eye")])]
y = 52
for gname, col, st, items in groups:
    t.text(40, y + 16, gname, 16, col, "bold", "start", step=st); t.badge(st, 24, y + 10, step=st, color=col)
    n = len(items); w = 160 if n == 6 else 240
    for j, (name, sub, ic) in enumerate(items):
        x = 40 + j * (w + 8)
        t.card(x, y + 28, w, 140, ic, name, sub, col, step=st, icon_size=60, title_size=15)
    y += 180
t.save(OUT + "ch04_se_taxonomy")

# 3. Anatomy of a phishing email
p = Fig(1100, 600, "Reading a phishing email: six tells, one habit",
        "A mock email claiming to be from IT support. Callouts mark the tells: a look-alike sender domain, urgency and fear, a "
        "request for credentials, a link whose real destination differs when hovered, an unexpected attachment, and sloppy "
        "wording. The habit: verify through an independent channel, the known website or published phone number.")
p.rect(40, 60, 640, 470, "#ffffff", "#9aa5b1", 1.6, rx=8)
p.rect(40, 60, 640, 40, "#e9edf2", "#9aa5b1", 1.6, rx=8)
for i, c in enumerate(["#e74c3c", "#f5b041", "#8fd16a"]): p.circle(62 + i * 18, 80, 6, c, c, 1)
p.text(360, 86, "Inbox", 14, MUTED, "bold")
p.text(60, 130, "From:  IT Support <helpdesk@micros0ft-support.co>", 15, INK, anchor="start")
p.text(60, 156, "Subject:  URGENT: your mailbox will be deleted in 1 hour", 15, INK, "bold", "start")
p.raw('<line x1="60" y1="172" x2="660" y2="172" stroke="#d0d6dd"/>')
p.text(60, 204, "Dear user,", 15, INK, anchor="start")
p.text(60, 232, "We detected unusual activity. Your mailbox will be deleted today", 15, INK, anchor="start")
p.text(60, 256, "unless you verify you're password now.", 15, INK, anchor="start")
p.raw('<line x1="170" y1="263" x2="214" y2="263" stroke="#c0392b" stroke-width="2"/>', step=3)
p.rect(60, 284, 260, 40, "#1f4e9c", "#1f4e9c", 1, rx=6); p.text(190, 310, "Verify my account", 15, "#ffffff", "bold")
p.rect(60, 336, 470, 26, "#fff8e1", "#d9a400", 1, rx=4)
p.text(70, 354, "hover: http://login.micros0ft-support.co/verify?u=", 13, "#8a6d1a", anchor="start")
p.icon("document", 90, 410, 50); p.text(124, 416, "Invoice_2026.pdf.exe", 14, INK, "bold", "start")
p.text(60, 480, "Thank you, IT Support Team", 15, INK, anchor="start")
tells = [(1, 410, 125, "Look-alike sender domain:\nmicros0ft with a zero"), (2, 464, 151, "Urgency and fear:\ndeleted in 1 hour"),
         (3, 218, 266, "Sloppy wording:\nyou're for your"), (4, 326, 304, "Asks for credentials, which\nreal IT never does by email"),
         (5, 540, 349, "Link text and real\ndestination differ"), (6, 264, 411, "Unexpected attachment with\na double extension")]
pos = [(760, 110), (760, 180), (760, 250), (760, 330), (760, 400), (760, 470)]
for (n, ax, ay, lab), (bx, by) in zip(tells, pos):
    p.arrow([(bx - 8, by + 6), (ax + 10, ay)], None, RED, step=n, width=1.8)
    p.badge(n, bx + 6, by + 6, step=n, color=RED)
    p.text(bx + 24, by, lab, 14, INK, "bold", "start", step=n)
p.icon("shield", 724, 556, 40, step=7); p.badge(7, 700, 540, step=7)
p.text(750, 552, "Slow down. Verify through a separate channel:", 13, GREEN, "bold", "start", step=7)
p.text(750, 570, "type the known URL or call the published number.", 13, GREEN, "bold", "start", step=7)
p.save(OUT + "ch04_phishing_anatomy")

# 4. Tailgating and the mantrap
g = Fig(1100, 480, "Tailgating, and the mantrap that stops it",
        "Left: an employee badges in and opens the door; an outsider slips through behind before it closes. Right: a mantrap, or "
        "access-control vestibule, has two interlocking doors; the inner door opens only after the outer door has closed and one "
        "person has been verified, so only one person passes at a time.")
g.zone(20, 50, 520, 390, "Tailgating", RED, "#fdf2f1", step=1); g.badge(1, 522, 66, step=1)
g.icon("door", 380, 220, 150, step=1)
g.icon("user", 220, 200, 90, "Employee", "badges in", step=2); g.icon("idcard", 300, 170, 40, step=2)
g.arrow([(268, 215), (318, 215)], None, BLUE, step=2, width=3); g.badge(2, 170, 150, step=2)
g.icon("attacker", 110, 330, 80, "Outsider", "follows closely", step=3)
g.arrow([(156, 320), (322, 270)], None, RED, step=3, width=3); g.text(300, 330, "slips in before\nthe door closes", 14, RED, "bold", step=3); g.badge(3, 62, 286, step=3)
g.zone(560, 50, 520, 390, "Mantrap (access-control vestibule)", GREEN, "#eef8ef", step=4); g.badge(4, 1062, 66, step=4)
g.icon("door", 660, 220, 130, "Outer door", step=4, label_size=13); g.icon("door", 980, 220, 130, "Inner door", step=4, label_size=13)
g.rect(730, 140, 180, 170, "#ffffff", GREEN, 2, rx=6, step=4); g.icon("user", 820, 230, 80, step=5); g.icon("idcard", 870, 200, 34, step=5)
g.text(820, 300, "one person verified", 13, GREEN, "bold", step=5); g.badge(5, 744, 154, step=5)
g.icon("lock", 660, 130, 30, step=5); g.text(660, 115, "closed and locked", 12, INK, step=5)
g.arrow([(910, 230), (930, 230)], None, GREEN, step=6, width=3); g.icon("check", 980, 120, 30, step=6)
g.text(980, 104, "opens only now", 12, GREEN, "bold", step=6); g.badge(6, 1010, 120, step=6)
g.text(820, 400, "Interlocked doors let only one person through at a time.", 13, INK, "bold", step=6)
g.text(550, 466, "Also: guards, badges worn visibly, CCTV, and a culture where staff challenge unknown visitors.", 13, MUTED, italic=True)
g.save(OUT + "ch04_tailgating")

# 5. MFA and how attackers go after it
m = Fig(1100, 600, "Multi-factor authentication, and three ways attackers go after it",
        "Top: MFA combines something you know (a password), something you have (a phone or token), and something you are (a "
        "fingerprint). Bottom: an attacker who phished the password bombards the victim with push prompts until one is approved "
        "(MFA fatigue), relays one-time codes through a fake login page in real time, or talks the help desk into resetting the "
        "victim's MFA. A FIDO2 security key, bound to the real site, defeats phishing and relay.")
for i, (ic, name, sub) in enumerate([("key", "Something you know", "password, PIN"), ("phone", "Something you have", "phone app, token, smart card"),
                                     ("fingerprint", "Something you are", "fingerprint, face")]):
    m.card(60 + i * 250, 50, 220, 170, ic, name, sub, BLUE, step=1, icon_size=70, title_size=15)
m.text(295, 146, "+", 30, BLUE, "bold", step=1); m.text(545, 146, "+", 30, BLUE, "bold", step=1); m.text(910, 140, "=  MFA", 30, BLUE, "bold", step=1)
m.text(910, 170, "two or more different factors", 14, INK, step=1); m.badge(1, 50, 48, step=1)
m.raw('<line x1="30" y1="244" x2="1070" y2="244" stroke="#d0d6dd" stroke-width="2" stroke-dasharray="6 6"/>')
# fatigue
m.zone(20, 260, 340, 280, "MFA fatigue (push bombing)", RED, "#fdf2f1", step=2); m.badge(2, 342, 276, step=2)
m.icon("attacker", 80, 360, 70, "has the password", step=2, label_size=12)
m.icon("phone", 270, 370, 80, step=2)
for k in range(4): m.rect(300, 310 + k * 24, 54, 18, "#fff", RED, 1.2, rx=3, step=2); m.text(327, 323 + k * 24, "Approve?", 9, RED, "bold", step=2)
m.arrow([(120, 360), (226, 370)], "prompt after prompt", RED, step=2, size=12)
m.text(190, 470, "a tired victim finally taps Approve", 13, RED, "bold", step=2)
m.text(190, 492, "Fix: number matching, alert on bursts", 13, GREEN, "bold", step=2)
# relay
m.zone(380, 260, 340, 280, "Real-time relay of one-time codes", RED, "#fdf2f1", step=3); m.badge(3, 702, 276, step=3)
m.icon("user", 430, 360, 64, "Victim", step=3, label_size=12); m.icon("browser", 550, 340, 70, step=3); m.icon("devil", 580, 315, 28, step=3)
m.icon("server", 670, 360, 64, "Real site", step=3, label_size=12)
m.arrow([(462, 350), (512, 345)], None, RED, step=3); m.arrow([(588, 345), (636, 350)], None, RED, step=3)
m.text(550, 392, "fake login proxy", 12, RED, "bold", step=3)
m.text(550, 470, "password and code typed into the fake", 13, RED, "bold", step=3)
m.text(550, 492, "page are replayed to the real site", 13, RED, "bold", step=3)
# help desk
m.zone(740, 260, 340, 280, "Help-desk reset", RED, "#fdf2f1", step=4); m.badge(4, 1062, 276, step=4)
m.icon("attacker", 800, 360, 70, "caller", step=4, label_size=12); m.icon("headset", 1000, 360, 70, "Help desk", step=4, label_size=12)
m.arrow([(840, 360), (960, 360)], None, RED, step=4); m.text(900, 318, "I lost my phone,\nreset my MFA", 12, RED, "bold", step=4)
m.text(910, 470, "staff re-enroll the attacker's device", 13, RED, "bold", step=4)
m.text(910, 492, "Fix: callback and strong caller checks", 13, GREEN, "bold", step=4)
m.icon("key", 330, 570, 36, step=5); m.badge(5, 300, 560, step=5)
m.text(356, 576, "Phishing-resistant MFA: a FIDO2 key signs only for the real site, so fake pages and relays get nothing.", 14, GREEN, "bold", "start", step=5)
m.save(OUT + "ch04_mfa_attacks")

# 6. Deepfake video-call wire fraud
d = Fig(1100, 520, "Deepfake wire fraud: a video call where every other face is synthetic",
        "Based on the widely reported 2024 Arup case. The attackers gather public video and audio of executives, use AI to clone "
        "their faces and voices, send a message about a confidential transaction, and hold a video call in which the other "
        "participants are deepfakes. The employee makes transfers totaling roughly 25 million US dollars. Callback to a known "
        "number, code words, dual approval, and out-of-band confirmation would have stopped the payment.")
steps = [("search", "Harvest public video\nand audio of executives", BLUE), ("robot", "Clone faces and\nvoices with AI", PURPLE),
         ("envelope", "Message: a confidential\ntransaction is needed", ORANGE), ("videocall", "Video call: the CFO and\ncolleagues are deepfakes", RED),
         ("money", "Employee wires roughly\nUS$25 million", RED)]
for i, (ic, lab, col) in enumerate(steps):
    x = 110 + i * 220
    d.circle(x, 160, 62, "#ffffff", col, 3, step=i + 1); d.icon(ic, x, 156, 80, step=i + 1)
    d.text(x, 250, lab, 14, INK, "bold", step=i + 1); d.badge(i + 1, x - 52, 108, step=i + 1, color=col)
    if i < 4: d.arrow([(x + 66, 160), (x + 152, 160)], None, col, step=i + 2, width=3)
d.raw('<path d="M60 290 v10 h500 v-10" fill="none" stroke="#5b6570" stroke-width="2"/>', step=3); d.text(310, 324, "attackers prepare", 14, MUTED, "bold", step=3)
d.raw('<path d="M720 290 v10 h320 v-10" fill="none" stroke="#c0392b" stroke-width="2"/>', step=5); d.text(880, 324, "the employee acts", 14, RED, "bold", step=5)
d.raw('<rect x="40" y="440" width="1020" height="64" rx="8" fill="#e8f5e9" stroke="#2e7d32" stroke-width="1.6"/>', step=6)
d.icon("shield", 80, 472, 40, step=6); d.badge(6, 40, 440, step=6)
d.text(110, 466, "Verify the request, not the face: call back on a known number, use pre-agreed code words,", 14, GREEN, "bold", "start", step=6)
d.text(110, 488, "require two people to approve large transfers, and confirm out of band on a different channel.", 14, GREEN, "bold", "start", step=6)
d.text(550, 380, "The familiar face and voice are now forgeable,", 14, INK, step=4, italic=True)
d.text(550, 400, "so they no longer prove who is asking.", 14, INK, step=4, italic=True)
d.save(OUT + "ch04_deepfake_fraud")
print("ok")
