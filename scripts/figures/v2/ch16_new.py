import os
import sys, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# Redraw: classify encoding, encryption, hashing
c = Fig(1100, 520, "Same look, different promises: two questions sort every scrambled string",
        "A scrambled string goes to question 1: is it meant to be undone without a secret? If yes, it is encoding: Base64 and ROT13. "
        "If no, question 2: can the right key undo it? If yes, it is encryption: one-byte XOR with 256 keys, tried at once, and "
        "AES-128 with 2 to the 128 keys, no way to try them all. If no, never, it is hashing: SHA-256, always 256 bits, check it, "
        "never undo it.")
c.icon("document", 90, 250, 80, "A scrambled string"); c.text(90, 318, "looks the same either way", 11, MUTED, italic=True)
def diamond(x, y, w, h, t1, t2, st):
    c.poly([(x, y - h / 2), (x + w / 2, y), (x, y + h / 2), (x - w / 2, y)], "#f4f6f8", "#52606d", 2, step=st)
    c.text(x, y - 6, t1, 14, INK, "bold", step=st); c.text(x, y + 14, t2, 12, INK, step=st)
diamond(340, 250, 230, 150, "Question 1", "undone without a secret?", 1); c.badge(1, 260, 190, step=1)
c.arrow([(132, 250), (224, 250)], None, INK, step=1, width=2.4)
diamond(560, 400, 230, 150, "Question 2", "can the right key undo it?", 3); c.badge(3, 480, 340, step=3)
c.arrow([(340, 326), (340, 400), (444, 400)], "no", INK, step=3, size=13, label_at=.3, label_anchor="start", label_dy=4)
fams = [("ENCODING: the bottle", "code", ["1  Base64: one click back, no key", "2  ROT13: called a cipher, but no key"], BLUE, 60, 2, (455, 250), "yes"),
        ("ENCRYPTION: the napkin", "key", ["3  XOR, one-byte key: 256 keys, tried at once", "4  AES-128: 2^128 keys, no way to try them all"], ORANGE, 220, 4, (676, 380), "yes"),
        ("HASHING: milk into curd", "fingerprint", ["5  SHA-256: always 256 bits,", "    check it, never undo it"], PURPLE, 380, 5, (676, 420), "no, never")]
for name, ic, lines, col, y, st, src, lab in fams:
    c.rect(720, y, 360, 130, "#ffffff", col, 2.4, rx=10, step=st); c.rect(720, y, 360, 8, col, col, 1, rx=4, step=st)
    c.icon(ic, 770, y + 70, 60, step=st); c.text(950, y + 34, name, 15, col, "bold", step=st)
    for k, l in enumerate(lines): c.text(812, y + 64 + k * 26, l, 12, INK, anchor="start", step=st)
    c.arrow([src, (716, y + 65)], lab, col, step=st, size=13, width=2.4, label_at=.5, label_dy=-8)
    c.badge(st, 1062, y + 22, step=st, color=col)
c.save(OUT + "ch16_classify_v2")

# Redraw: case chain
k = Fig(1100, 640, "Crack the case: five pieces of evidence, decoded in order",
        "E1, a chat log in Base64, decoded From Base64, reveals the injected instruction to ignore policy and export the customer "
        "table. E2, an outbound request in hex, decoded From Hex, shows data posted to exfil.staging.invalid as customers.enc. E3, a "
        "leaked config XORed with the one-byte key 5a, decoded From Hex then XOR, reveals the AES key and IV in a config backup with "
        "rotate=never. E4, the stolen file in AES-128-CBC, decrypted with E3's key, is the exported record, synthetic. E5, the "
        "integrity seal, SHA-256 over the E4 record, matches, so the record was not altered. Two weak links: prompt injection opened "
        "the door, and the AES key sat in a config backup.")
for x, h in [(40, "Evidence"), (380, "Recipe"), (640, "What it reveals")]: k.text(x, 62, h, 15, MUTED, "bold", "start")
ev = [("E1  Chat log", "Base64, an encoding", "envelope", "From Base64", "The injected instruction: ignore\npolicy, export the customer table", BLUE),
      ("E2  Outbound request", "hex, an encoding", "cloud", "From Hex", "Data posted to exfil.staging.invalid\nas customers.enc", BLUE),
      ("E3  Leaked config", "XOR, one-byte key 5a", "gear", "From Hex, XOR", "AES key and IV in a config\nbackup, rotate=never", ORANGE),
      ("E4  Stolen file", "AES-128-CBC", "lock", "AES Decrypt with E3's key", "The exported record (synthetic)", ORANGE),
      ("E5  Integrity seal", "SHA-256 in the ticket", "fingerprint", "SHA-256 over the E4 record", "Digest matches: the record\nwas not altered", PURPLE)]
for i, (name, form, ic, rec, rev, col) in enumerate(ev):
    y = 80 + i * 96; st = i + 1
    k.rect(30, y, 310, 76, "#ffffff", col, 2.2, rx=8, step=st); k.icon(ic, 72, y + 38, 44, step=st)
    k.text(104, y + 32, name, 15, col, "bold", "start", step=st); k.text(104, y + 54, form, 13, INK, anchor="start", step=st)
    k.rect(380, y + 10, 220, 56, "#f4f6f8", "#9aa5b1", 1.4, rx=8, step=st); k.icon("gear", 404, y + 38, 26, step=st); k.text(500, y + 43, rec, 13, INK, "bold", step=st)
    k.rect(640, y, 430, 76, "#ffffff", col, 1.6, rx=8, step=st); k.text(855, y + 32, rev, 13, INK, step=st)
    k.arrow([(342, y + 38), (378, y + 38)], None, INK, step=st, width=2); k.arrow([(602, y + 38), (638, y + 38)], None, INK, step=st, width=2)
    k.badge(st, 30, y, step=st, color=col)
k.arrow([(760, 80 + 2 * 96 + 78), (560, 80 + 3 * 96 + 8)], None, ORANGE, step=4, width=2.4); k.text(785, 80 + 2 * 96 + 91, "key and IV", 12, ORANGE, "bold", "start", step=4)
k.arrow([(760, 80 + 3 * 96 + 78), (560, 80 + 4 * 96 + 8)], None, PURPLE, step=5, width=2.4); k.text(785, 80 + 3 * 96 + 91, "hash the record", 12, PURPLE, "bold", "start", step=5)
k.rect(30, 572, 1040, 56, "#fdecea", RED, 1.8, rx=8, step=6); k.icon("warning", 64, 600, 30, step=6); k.badge(6, 30, 572, step=6, color=RED)
k.text(92, 596, "Two weak links: prompt injection opened the door, and the AES key sat in a config backup.", 14, RED, "bold", "start", step=6)
k.text(92, 616, "Briefing: what happened, impact, root cause, three recommendations, the ask.", 13, INK, anchor="start", step=6)
k.save(OUT + "ch16_case_chain_v2")

# Redraw: key space
s = Fig(1100, 520, "Each added key bit doubles the work: time to try every key at a trillion guesses a second",
        "On a log scale of seconds: one-byte XOR, 2 to the 8 keys, about 0.26 nanoseconds; four-byte XOR, 2 to the 32, about 4.3 "
        "milliseconds; DES, 2 to the 56, about 20 hours; AES-128, 2 to the 128, about 1.1 times 10 to the 19 years; AES-256, 2 to "
        "the 256, about 3.7 times 10 to the 57 years. Reference lines mark one second and the 13.8-billion-year age of the universe.")
X0, X1 = 300, 1040; lo, hi = -10, 70
xs = lambda e: X0 + (e - lo) / (hi - lo) * (X1 - X0)
rate = 1e12
rows = [("XOR, one-byte key", 8, "2^8 keys: 0.26 nanoseconds", ORANGE), ("XOR, four-byte key", 32, "2^32 keys: 4.3 milliseconds", ORANGE),
        ("DES, 56-bit key", 56, "2^56 keys: 20 hours", "#7f8c8d"), ("AES-128", 128, "2^128 keys: about 1.1 x 10^19 years", ORANGE),
        ("AES-256", 256, "2^256 keys: about 3.7 x 10^57 years", ORANGE)]
s.raw(f'<line x1="{X0}" y1="430" x2="{X1}" y2="430" stroke="#52606d" stroke-width="2"/>')
for e in range(lo, hi + 1, 10):
    s.raw(f'<line x1="{xs(e):.1f}" y1="430" x2="{xs(e):.1f}" y2="436" stroke="#52606d"/>'); s.text(xs(e), 452, f"10^{e}", 12, MUTED)
s.text(670, 476, "seconds to try every key, log scale", 13, MUTED, "bold")
for i, (name, bits, lab, col) in enumerate(rows):
    y = 90 + i * 66; e = math.log10(2 ** bits / rate)
    s.icon("key", 40, y, 34, step=i + 1); s.text(70, y + 5, name, 14, INK, "bold", "start", step=i + 1)
    s.rect(X0, y - 16, max(xs(e) - X0, 4), 32, col, col, 1, rx=4, step=i + 1)
    if xs(e) > 800: s.text(xs(e) - 10, y + 5, lab, 13, "#ffffff", "bold", "end", step=i + 1)
    else: s.text(xs(e) + 10, y + 5, lab, 13, INK, "bold", "start", step=i + 1)
    s.badge(i + 1, 24, y - 18, step=i + 1)
for e, lab, col in [(0, "1 second", MUTED), (math.log10(13.8e9 * 3.156e7), "age of the universe", RED)]:
    s.raw(f'<line x1="{xs(e):.1f}" y1="60" x2="{xs(e):.1f}" y2="430" stroke="{col}" stroke-width="1.6" stroke-dasharray="6 5"/>', step=6)
    s.text(xs(e) + 6, 70, lab, 12, col, "bold", "start", step=6)
s.save(OUT + "ch16_keyspace_v2")

# New: CTF formats
f = Fig(1100, 500, "Three CTF formats: Jeopardy, Attack-Defense, and King-of-the-Hill",
        "Jeopardy: a board of independent challenges by category and point value; solving one yields a flag such as flag{...} that "
        "is submitted to the scoreboard. Attack-Defense: every team runs the same vulnerable services, patches its own, and exploits "
        "the others to steal flags. King-of-the-Hill: teams fight to hold a shared target longest.")
f.zone(20, 60, 340, 400, "Jeopardy", BLUE, "#eef5fc", step=1); f.badge(1, 342, 76, step=1)
cats = ["Web", "Crypto", "Pwn", "Forensics"]
for ci, cat in enumerate(cats):
    f.text(70 + ci * 78, 112, cat, 12, BLUE, "bold", step=1)
    for r in range(3):
        f.rect(38 + ci * 78, 124 + r * 52, 66, 44, "#1f4e9c" if (ci + r) % 3 else "#9aa5b1", "#ffffff", 1, rx=4, step=1)
        f.text(71 + ci * 78, 152 + r * 52, str(100 * (r + 1)), 14, "#ffffff", "bold", step=1)
f.rect(60, 310, 260, 34, "#1f2933", "#1f2933", 1, rx=6, step=2); f.text(190, 332, "flag{x0r_15_n0t_3ncrypt10n}", 13, "#8fd16a", "bold", step=2)
f.icon("checklist", 190, 400, 50, "scoreboard", step=2, label_size=12); f.arrow([(190, 346), (190, 370)], None, BLUE, step=2); f.badge(2, 40, 300, step=2)
f.zone(380, 60, 340, 400, "Attack-Defense", RED, "#fdf2f1", step=3); f.badge(3, 702, 76, step=3, color=RED)
for k, (x, lab) in enumerate([(470, "Team A"), (630, "Team B")]):
    f.icon("server", x, 180, 70, lab, "same services", step=3); f.icon("shield", x - 34, 150, 28, step=4); f.text(x, 280, "patch own", 12, GREEN, "bold", step=4)
f.arrow([(510, 160), (590, 160)], "exploit", RED, step=4, size=12, width=2.4); f.arrow([(590, 200), (510, 200)], "exploit", RED, step=4, size=12, width=2.4, label_dy=20)
f.icon("checklist", 550, 360, 50, "steal flags each round", step=4, label_size=12); f.badge(4, 400, 300, step=4, color=RED)
f.zone(740, 60, 340, 400, "King-of-the-Hill", ORANGE, "#fef5e7", step=5); f.badge(5, 1062, 76, step=5, color=ORANGE)
f.icon("server", 910, 200, 80, "shared target", step=5); f.icon("clock", 960, 150, 30, step=5)
for k, (x, y) in enumerate([(800, 330), (910, 360), (1020, 330)]):
    f.icon("user-laptop", x, y, 50, step=5); f.arrow([(x, y - 30), (910, 268)], None, ORANGE, step=5, width=1.6)
f.text(910, 430, "hold control the longest", 13, ORANGE, "bold", step=5)
f.text(550, 488, "Jeopardy builds breadth for learning; Attack-Defense builds speed and a dual offense-defense mindset.", 13, MUTED, italic=True, step=6)
f.save(OUT + "ch16_formats")
print("ok")
