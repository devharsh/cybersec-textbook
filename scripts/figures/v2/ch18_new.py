import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# GDPR roles and the breach clock
g = Fig(1100, 540, "GDPR roles, and the 72-hour breach clock",
        "The data subject is the person the data is about. The controller decides why and how personal data is processed and needs a "
        "lawful basis; the processor handles the data on the controller's behalf, such as a cloud or payroll provider. The data "
        "subject holds rights such as access and rectification. If a breach occurs, the controller must notify the supervisory "
        "authority within 72 hours of becoming aware, unless the breach is unlikely to put people at risk, and must tell the "
        "individuals without undue delay when the risk to them is high.")
g.icon("user", 110, 170, 90, "Data subject", "the person the data is about", step=1)
g.icon("bank", 480, 170, 90, "Controller", "decides why and how; needs a lawful basis", step=2)
g.icon("cloud", 860, 170, 110, "Processor", "processes on the controller's behalf", step=3)
g.arrow([(160, 150), (430, 150)], "personal data", BLUE, step=2, size=12, width=2.4)
g.arrow([(430, 190), (160, 190)], "rights: access, rectification, erasure", GREEN, step=2, size=12, width=2.2, label_dy=20)
g.arrow([(530, 170), (800, 170)], "written contract", PURPLE, step=3, size=12, width=2.4, both=True)
for n_, x in [(1, 60), (2, 430), (3, 800)]: g.badge(n_, x, 110, step=n_)
Y = 400
g.raw(f'<line x1="80" y1="{Y}" x2="1020" y2="{Y}" stroke="#52606d" stroke-width="3"/>', step=4)
g.icon("warning", 120, Y - 44, 40, step=4); g.text(120, Y + 28, "controller becomes", 13, INK, "bold", step=4); g.text(120, Y + 46, "aware of a breach", 13, INK, "bold", step=4)
g.icon("clock", 560, Y - 44, 46, step=5); g.text(560, Y + 28, "72 hours", 18, RED, "bold", step=5); g.raw(f'<rect x="120" y="{Y - 6}" width="860" height="12" fill="#c0392b" opacity=".25"/>', step=5)
g.icon("bank", 980, Y - 44, 46, step=6); g.text(980, Y + 28, "notify the supervisory", 13, INK, "bold", step=6); g.text(980, Y + 46, "authority", 13, INK, "bold", step=6)
g.badge(4, 80, Y - 70, step=4, color=RED); g.badge(5, 520, Y - 70, step=5, color=RED); g.badge(6, 940, Y - 70, step=6, color=RED)
g.text(550, Y + 100, "High risk to people: tell them too, without undue delay. Unlikely risk, such as encrypted data with no key exposed: no report.", 13, MUTED, italic=True, step=7)
g.save(OUT + "ch18_gdpr_roles")

# PCI DSS scope reduction
p = Fig(1100, 500, "PCI DSS scope: every system that touches card data is in the CDE, so touch less",
        "Left: the merchant's web store, application servers, database, and backups all store, process, or transmit card numbers, so "
        "all of them sit in the cardholder data environment and must meet every applicable requirement. Right: a tokenization "
        "provider takes the card number in a hosted field and returns a token; the merchant's systems store only tokens, and the CDE "
        "shrinks to near zero. PCI DSS v4.0.1 has six objectives and twelve requirements.")
p.zone(20, 60, 500, 360, "Without tokenization", RED, "#fdf2f1", step=1); p.badge(1, 502, 76, step=1, color=RED)
for k, (ic, lab) in enumerate([("browser", "Web store"), ("server", "App servers"), ("database", "Database"), ("document", "Backups")]):
    x = 90 + k * 115; p.icon(ic, x, 200, 56, lab, step=1, label_size=12); p.icon("idcard", x + 22, 170, 22, step=1)
    if k: p.arrow([(x - 85, 200), (x - 30, 200)], None, RED, step=1, width=1.8)
p.rect(50, 290, 440, 100, "#ffffff", RED, 2.2, rx=10, step=2, dash=True); p.text(270, 320, "CDE: all four systems in scope", 15, RED, "bold", step=2)
p.text(270, 346, "every applicable requirement applies to each", 13, INK, step=2); p.text(270, 368, "(and to anything connected to them)", 12, MUTED, step=2); p.badge(2, 50, 290, step=2, color=RED)
p.zone(560, 60, 520, 360, "With a tokenization provider", GREEN, "#eef8ef", step=3); p.badge(3, 1062, 76, step=3, color=GREEN)
p.icon("cloud", 940, 180, 110, "Tokenization provider", "in scope: their problem", step=3)
p.icon("browser", 640, 180, 56, "hosted card field", step=3, label_size=12); p.arrow([(670, 170), (886, 170)], "card number", ORANGE, step=3, size=12, width=2.2)
p.arrow([(886, 196), (670, 196)], "token", GREEN, step=4, size=12, width=2.2, label_dy=20)
for k, (ic, lab) in enumerate([("server", "App"), ("database", "DB"), ("document", "Backups")]):
    x = 640 + k * 110; p.icon(ic, x, 330, 46, lab + ": tokens only", step=4, label_size=11)
p.badge(4, 580, 290, step=4, color=GREEN)
p.text(550, 462, "PCI DSS v4.0.1 (June 2024): six control objectives, twelve requirements, over 300 sub-requirements.", 13, MUTED, italic=True, step=5)
p.save(OUT + "ch18_pci_scope")

# Katz REP test (mermaid companion)
k = Fig(1100, 460, "The Katz test: two questions decide whether there was a Fourth Amendment search",
        "First: did the person have an actual, subjective expectation of privacy? If not, there was no search. Second: is that "
        "expectation one society recognizes as reasonable? If not, there was no search. If both are yes, the government action is a "
        "search, and a warrant supported by probable cause is generally required.")
k.icon("user", 90, 200, 80, "A person", "and their data")
def dia(x, y, t1, t2, st):
    k.poly([(x, y - 80), (x + 140, y), (x, y + 80), (x - 140, y)], "#f4f6f8", "#52606d", 2, step=st)
    k.text(x, y - 10, t1, 14, INK, "bold", step=st); k.text(x, y + 10, t2, 12, INK, step=st)
dia(330, 200, "1. Actual expectation", "of privacy?", 1); dia(660, 200, "2. Reasonable to", "society?", 2)
k.arrow([(132, 200), (188, 200)], None, INK, step=1, width=2.4); k.arrow([(472, 200), (518, 200)], "yes", GREEN, step=2, size=13, width=2.4)
k.card(860, 130, 220, 140, "bank", "A search", "warrant generally required", GREEN, step=3, icon_size=50, title_size=16)
k.arrow([(802, 200), (856, 200)], "yes", GREEN, step=3, size=13, width=2.4)
k.card(420, 340, 260, 100, None, "No REP: no search", "no warrant requirement", RED, step=4, title_size=16)
k.arrow([(330, 282), (330, 390), (416, 390)], "no", RED, step=4, size=13, width=2.2, label_at=.2, label_anchor="start", label_dy=4)
k.arrow([(660, 282), (660, 336)], "no", RED, step=4, size=13, width=2.2, label_anchor="start", label_dy=4)
for n_, x in [(1, 240), (2, 570), (3, 870), (4, 430)]: k.badge(n_, x, 130 if n_ < 4 else 350, step=n_, color=RED if n_ == 4 else BLUE)
k.save(OUT + "ch18_katz")

# Lawful access versus end-to-end encryption
e = Fig(1100, 500, "End-to-end encryption and the lawful-access debate",
        "Top: with end-to-end encryption, Alice's message is encrypted on her phone and decrypted only on Bob's; the service relays "
        "ciphertext it cannot read. Bottom: exceptional access adds an escrowed key that lets an authorized party decrypt, but the "
        "escrowed key is a single point of failure that attackers will target. Strong encryption protects everyone and can impede "
        "investigations; there is no purely technical resolution.")
e.text(40, 80, "End-to-end encryption", 16, GREEN, "bold", "start", step=1); e.badge(1, 24, 74, step=1, color=GREEN)
e.icon("user2-phone", 120, 160, 70, "Alice", step=1); e.icon("user-laptop", 980, 160, 70, "Bob", step=1)
e.icon("server", 550, 160, 70, "Messaging service", "sees only ciphertext", step=1)
e.arrow([(166, 150), (506, 150)], None, GREEN, step=1, width=2.4); e.arrow([(594, 150), (934, 150)], None, GREEN, step=1, width=2.4)
e.icon("lock", 330, 130, 28, step=1); e.icon("lock", 770, 130, 28, step=1)
e.raw('<line x1="30" y1="260" x2="1070" y2="260" stroke="#d0d6dd" stroke-width="2" stroke-dasharray="6 6"/>')
e.text(40, 300, "Exceptional access (key escrow)", 16, ORANGE, "bold", "start", step=2); e.badge(2, 24, 294, step=2, color=ORANGE)
e.icon("user2-phone", 120, 380, 70, "Alice", step=2); e.icon("user-laptop", 980, 380, 70, "Bob", step=2)
e.icon("server", 550, 380, 70, step=2); e.arrow([(166, 370), (506, 370)], None, ORANGE, step=2, width=2.4); e.arrow([(594, 370), (934, 370)], None, ORANGE, step=2, width=2.4)
e.icon("key", 550, 300, 40, "escrowed key", step=3, label_size=12); e.icon("bank", 360, 460, 50, step=3); e.text(420, 466, "authorized access", 12, INK, "bold", "start", step=3)
e.arrow([(530, 312), (380, 430)], None, ORANGE, step=3, dash=True, width=2); e.badge(3, 500, 290, step=3, color=ORANGE)
e.icon("attacker", 760, 460, 50, step=4); e.text(790, 466, "also a target for attackers", 12, RED, "bold", "start", step=4)
e.arrow([(740, 440), (575, 316)], None, RED, step=4, dash=True, width=2); e.badge(4, 720, 420, step=4, color=RED)
e.save(OUT + "ch18_lawful_access")
print("ok")
