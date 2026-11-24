import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""
PUB, PRIV = "#2e7d32", "#c0392b"

def bits(f, x, y, s, col, step, w=22):
    for i, ch in enumerate(s):
        f.rect(x + i * w, y, w - 2, 28, "#ffffff", col, 1.4, rx=3, step=step)
        f.text(x + i * w + (w - 2) / 2, y + 19, ch, 14, col, "bold", step=step)

# One-time pad
o = Fig(1000, 400, "The one-time pad: XOR with a truly random key used once",
        "Message bits are combined with an equally long random key by XOR to give ciphertext. XOR with the same key again gives "
        "the message back. Because every key is equally likely, every message of that length is equally likely, which is perfect "
        "secrecy; the key must be as long as the message and never reused.")
m, k = "01001000", "11010110"; c = "".join(str(int(a) ^ int(b)) for a, b in zip(m, k))
o.icon("user2-phone", 70, 200, 90, "Alice", step=1)
o.text(160, 116, "message m", 14, BLUE, "bold", "start", step=1); bits(o, 300, 96, m, BLUE, 1)
o.text(160, 166, "random key k", 14, PRIV, "bold", "start", step=2); bits(o, 300, 146, k, PRIV, 2); o.icon("key", 510, 160, 40, step=2)
o.raw('<line x1="300" y1="186" x2="474" y2="186" stroke="#1f2933" stroke-width="2"/>', step=3)
o.text(268, 214, "⊕", 24, INK, "bold", step=3)
o.text(160, 216, "ciphertext c", 14, INK, "bold", "start", step=3); bits(o, 300, 196, c, INK, 3)
o.badge(1, 136, 110, step=1); o.badge(2, 136, 160, step=2); o.badge(3, 136, 210, step=3); o.badge(4, 600, 170, step=4)
o.arrow([(560, 210), (700, 210)], "c", INK, step=4, size=15); o.icon("cloud", 630, 210, 120, step=4)
o.icon("user-laptop", 920, 200, 90, "Bob", step=5)
o.text(770, 280, "c ⊕ k = m", 18, GREEN, "bold", step=5); o.badge(5, 712, 274, step=5)
o.icon("cross", 140, 330, 30, step=6)
o.text(162, 336, "Reuse k and c1 ⊕ c2 = m1 ⊕ m2 leaks both messages; the key must be as long as the message.", 14, RED, "bold", "start", step=6)
o.save(OUT + "ch02_otp")

# MAC, after the Stevens slide
mc = Fig(1000, 400, "Message authentication code: tag with a shared key, verify on arrival",
         "Alice and Bob share a secret key k. Alice computes tag t over message m and sends m with t. Mallory in the network can "
         "change m and t but cannot forge a valid pair without k. Bob recomputes the tag with k: a match is accepted, a mismatch "
         "is rejected.")
mc.icon("key", 300, 120, 40, step=1); mc.text(300, 160, "k", 18, PRIV, "bold", step=1)
mc.icon("key", 700, 120, 40, step=1); mc.text(700, 160, "k", 18, PRIV, "bold", step=1)
mc.arrow([(300, 170), (262, 226)], None, PRIV, step=1); mc.arrow([(700, 170), (738, 226)], None, PRIV, step=1)
mc.text(500, 128, "shared secret key", 13, PRIV, "bold", step=1); mc.badge(1, 410, 122, step=1)
mc.icon("user2-phone", 78, 255, 96, "Alice", step=2)
mc.arrow([(130, 258), (196, 258)], "m", BLUE, step=2, size=16)
mc.box(200, 232, 110, 52, "Tag", step=2); mc.badge(2, 200, 232, step=2)
mc.icon("cloud", 500, 262, 210, step=3); mc.icon("devil", 466, 214, 52, step=3)
mc.text(434, 220, "Mallory", 15, INK, "bold", "end", step=3)
mc.text(470, 336, "can change m and t, cannot forge without k", 13, RED, "bold", step=3, italic=True)
mc.arrow([(312, 258), (688, 258)], "m, t", BLUE, step=3, label_at=.1, size=16, width=2.6); mc.badge(3, 412, 258, step=3)
mc.box(690, 232, 110, 52, "Verify", step=4); mc.badge(4, 690, 232, step=4)
mc.arrow([(802, 258), (866, 258)], None, BLUE, step=4); mc.icon("user-laptop", 922, 255, 96, "Bob", step=4)
mc.icon("check", 704, 316, 28, step=4); mc.text(724, 321, "ACCEPT: tags match", 13, GREEN, "bold", "start", step=4)
mc.icon("cross", 704, 348, 28, step=4); mc.text(724, 353, "REJECT: tags differ", 13, RED, "bold", "start", step=4)
mc.text(500, 390, "Unlike a signature, either key holder could have made t, so a MAC gives integrity and authenticity but not non-repudiation.", 13, MUTED, italic=True)
mc.save(OUT + "ch02_mac")

# Salted password storage
p = Fig(1100, 470, "Storing passwords: a unique salt and a slow, memory-hard hash",
        "At sign-up the server makes a random salt for the user, runs the password and salt through a slow key-derivation function "
        "such as Argon2id, bcrypt, scrypt, or PBKDF2, and stores the user name, salt, and hash, never the password. At login it "
        "repeats the computation with the stored salt and compares. Unique salts defeat precomputed tables, and the slow function "
        "makes each guess expensive for an attacker who steals the database.")
p.icon("user-laptop", 80, 170, 96, "User", step=1)
p.arrow([(132, 170), (262, 170)], "password", BLUE, step=1, size=13); p.badge(1, 170, 196, step=1)
p.icon("server", 330, 170, 96, "Server", step=1)
p.box(420, 90, 150, 50, "random salt", step=2, kind="note"); p.badge(2, 420, 90, step=2)
p.box(620, 140, 200, 60, "Argon2id\n(slow, memory-hard)", step=3); p.badge(3, 620, 140, step=3)
p.arrow([(378, 170), (614, 170)], None, INK, step=3); p.arrow([(570, 115), (680, 115), (680, 136)], None, INK, step=3)
p.arrow([(822, 170), (900, 170)], None, INK, step=4)
p.icon("database", 960, 170, 90, step=4)
p.raw('<rect x="760" y="250" width="320" height="86" rx="6" fill="#f5f7f9" stroke="#9aa5b1"/>', step=4)
p.text(776, 274, "user   | salt        | hash", 13, INK, "bold", "start", step=4)
p.text(776, 298, "alice  | 9f2c...e1  | $argon2id$...Qx", 13, INK, anchor="start", step=4)
p.text(776, 320, "bob    | 41ab...07  | $argon2id$...7k", 13, INK, anchor="start", step=4)
p.badge(4, 760, 250, step=4)
p.icon("attacker", 140, 390, 86, step=5)
p.text(200, 372, "If the database is stolen:", 14, RED, "bold", "start", step=5)
p.text(200, 394, "unique salts defeat precomputed tables, and each guess costs", 13, INK, anchor="start", step=5)
p.text(200, 412, "real time and memory, so cracking strong passwords is slow.", 13, INK, anchor="start", step=5)
p.badge(5, 110, 348, step=5)
p.icon("cross", 500, 448, 24, step=5); p.text(518, 453, "Never store plaintext, and never a fast unsalted hash such as MD5.", 13, RED, "bold", "start", step=5)
p.save(OUT + "ch02_password_storage")

# Diffie-Hellman
d = Fig(1100, 500, "Diffie-Hellman: agreeing on a key over a public channel",
        "Alice and Bob agree in public on a large prime p and a generator g. Alice picks a secret a and sends A = g to the a mod p; "
        "Bob picks a secret b and sends B = g to the b mod p. Eve sees p, g, A, and B. Each side combines the other's public value "
        "with its own secret and gets the same key, g to the ab mod p, which Eve cannot compute without solving the discrete "
        "logarithm problem.")
d.icon("user2-phone", 90, 150, 96, "Alice", step=1); d.icon("user-laptop", 1010, 150, 96, "Bob", step=1)
d.box(400, 66, 300, 44, "public: prime p, generator g", step=1, kind="plain"); d.badge(1, 400, 66, step=1)
d.icon("key", 90, 260, 40, step=2); d.text(90, 300, "secret a", 14, PRIV, "bold", step=2)
d.icon("key", 1010, 260, 40, step=2); d.text(1010, 300, "secret b", 14, PRIV, "bold", step=2)
d.badge(2, 50, 250, step=2)
d.icon("cloud", 550, 250, 200, step=3); d.icon("devil", 520, 200, 50, step=3); d.text(490, 206, "Eve", 15, INK, "bold", "end", step=3)
d.arrow([(150, 210), (950, 210)], "A = g^a mod p", BLUE, step=3, label_at=.2, size=15); d.badge(3, 170, 210, step=3)
d.arrow([(950, 290), (150, 290)], "B = g^b mod p", BLUE, step=4, label_at=.2, size=15, label_dy=24); d.badge(4, 930, 290, step=4)
d.text(550, 360, "Eve sees p, g, A, and B, but not a or b", 13, RED, "bold", step=4, italic=True)
d.box(30, 390, 260, 58, "K = B^a mod p", step=5, kind="ok", size=16); d.box(810, 390, 260, 58, "K = A^b mod p", step=5, kind="ok", size=16)
d.text(550, 418, "same key: K = g^(ab) mod p", 17, GREEN, "bold", step=5); d.badge(5, 30, 390, step=5)
d.text(550, 476, "Unauthenticated DH is open to a man in the middle; TLS signs the exchange with the server's certificate.", 13, MUTED, italic=True)
d.save(OUT + "ch02_diffie_hellman")

# PKI chain of trust
k = Fig(1100, 460, "Public key infrastructure: a chain of trust from a root the browser already trusts",
        "A root certificate authority, kept offline, signs an intermediate CA certificate. The intermediate signs the web server's "
        "leaf certificate. The server sends its leaf and the intermediate; the browser checks each signature up to a root in its "
        "trust store, checks names, dates, and revocation, and only then trusts the server's public key.")
chain = [("Root CA", "self-signed, kept offline,\nin every trust store", "#8e44ad"), ("Intermediate CA", "signed by the root;\nissues day to day", "#2f6fae"),
         ("Leaf certificate", "www.example.com\nsigned by the intermediate", "#2e7d32")]
for kk, (name, sub, col) in enumerate(chain):
    x = 40 + kk * 270
    k.card(x, 80, 220, 230, "certificate", name, sub, col, step=kk + 1, icon_size=96, title_size=16)
    k.badge(kk + 1, x + 14, 92, step=kk + 1)
    if kk: k.arrow([(x - 50, 196), (x - 4, 196)], "signs", INK, step=kk + 1, label_dy=-8, size=12)
k.icon("server", 880, 150, 90, "Web server", step=4)
k.arrow([(800, 196), (840, 170)], None, INK, step=4)
k.icon("desktop", 880, 360, 100, "Browser", step=5)
k.arrow([(880, 210), (880, 300)], "leaf + intermediate", BLUE, step=5, label_dy=0, label_anchor="start", size=12)
k.arrow([(820, 360), (130, 360), (130, 316)], "verifies each signature up to a trusted root", GREEN, step=6, label_at=.45, label_dy=-10)
k.badge(4, 920, 100, step=4); k.badge(5, 930, 300, step=5); k.badge(6, 470, 360, step=6)
k.text(550, 440, "The browser also checks the name, the validity dates, and revocation before it trusts the server's key.", 13, MUTED, italic=True)
k.save(OUT + "ch02_pki_chain")

# TLS 1.3 handshake
t = Fig(1100, 560, "The TLS 1.3 handshake: one round trip to an encrypted channel",
        "The client sends ClientHello with supported cipher suites and a key share. The server answers with ServerHello and its "
        "key share; both now derive handshake keys. Still in the same flight, the server sends, encrypted, its certificate, a "
        "CertificateVerify signature over the handshake, and Finished. The client checks the certificate chain and signature, "
        "sends Finished, and application data flows under keys from the ephemeral exchange.")
t.icon("laptop", 120, 100, 90, "Client"); t.icon("server", 980, 100, 90, "Server")
t.raw('<line x1="120" y1="150" x2="120" y2="520" stroke="#9aa5b1" stroke-width="3"/><line x1="980" y1="150" x2="980" y2="520" stroke="#9aa5b1" stroke-width="3"/>')
msgs = [(1, False, "ClientHello: cipher suites, key share (X25519 + ML-KEM)", BLUE, False),
        (2, True, "ServerHello: chosen suite, key share", BLUE, False),
        (3, True, "encrypted: Certificate, CertificateVerify, Finished", GREEN, True),
        (4, False, "encrypted: Finished", GREEN, True),
        (5, False, "application data, both directions", GREEN, True)]
for i, (n_, back, lab, col, enc) in enumerate(msgs):
    y = 190 + i * 66 + (14 if i >= 2 else 0)
    pts = [(124, y), (976, y)]
    t.arrow(pts[::-1] if back else pts, lab, col, step=n_, label_dy=-8, size=13, width=2.6, both=(n_ == 5))
    t.badge(n_, 976 if back else 124, y, step=n_)
    if enc: t.icon("lock", 548 + (250 if n_ == 3 else 0), y + 22, 26, step=n_)
t.text(550, 282, "both sides now derive handshake keys from the key shares", 12, MUTED, step=2, italic=True)
t.text(550, 545, "The client checks the certificate chain and the CertificateVerify signature; keys from the ephemeral exchange give forward secrecy.",
       13, MUTED, italic=True)
t.save(OUT + "ch02_tls13")

# Hybrid post-quantum key exchange and the timeline
h = Fig(1100, 460, "Post-quantum migration: hybrid key exchange now, classical algorithms retired by 2035",
        "In a hybrid key exchange the client and server run a classical elliptic-curve exchange, X25519, and the post-quantum "
        "ML-KEM together, and feed both shared secrets into the key derivation function, so the session stays safe if either "
        "one breaks. NIST IR 8547 deprecates RSA and elliptic-curve cryptography after 2030 and disallows them after 2035.")
h.icon("laptop", 90, 150, 86, "Client", step=1); h.icon("server", 1010, 150, 86, "Server", step=1)
h.box(380, 70, 340, 50, "X25519 (classical ECDH)", step=1, kind="process"); h.badge(1, 380, 70, step=1)
h.box(380, 150, 340, 50, "ML-KEM (post-quantum, FIPS 203)", step=2, kind="ok"); h.badge(2, 380, 150, step=2)
for y, st in [(95, 1), (175, 2)]:
    h.arrow([(140, 150), (374, y)], None, INK, step=st, width=1.8); h.arrow([(726, y), (960, 150)], None, INK, step=st, width=1.8)
h.arrow([(550, 122), (550, 146)], None, MUTED, step=3)
h.arrow([(550, 202), (550, 236)], None, INK, step=3)
h.box(420, 240, 260, 50, "KDF(secret1 || secret2)", step=3, kind="note"); h.badge(3, 420, 240, step=3)
h.icon("key", 720, 265, 40, step=3); h.text(748, 270, "session key: safe if either holds", 13, GREEN, "bold", "start", step=3)
# timeline
y0 = 380
h.raw(f'<line x1="80" y1="{y0}" x2="1040" y2="{y0}" stroke="#52606d" stroke-width="3"/>', step=4)
for yr, x in [(2024, 120), (2026, 330), (2030, 640), (2035, 960)]:
    h.raw(f'<line x1="{x}" y1="{y0 - 8}" x2="{x}" y2="{y0 + 8}" stroke="#52606d" stroke-width="3"/>', step=4)
    h.text(x, y0 + 28, str(yr), 14, INK, "bold", step=4)
h.text(120, y0 - 16, "FIPS 203/204/205", 12, GREEN, "bold", step=4)
h.text(330, y0 - 16, "NIST IR 8547 final (Oct)", 12, BLUE, "bold", step=4)
h.icon("warning", 640, y0 - 34, 30, step=5); h.text(640, y0 + 48, "RSA and ECC deprecated", 12, ORANGE, "bold", step=5)
h.icon("cross", 960, y0 - 34, 30, step=5); h.text(960, y0 + 48, "RSA and ECC disallowed", 12, RED, "bold", step=5)
h.badge(4, 80, y0, step=4); h.badge(5, 1040, y0, step=5)
h.save(OUT + "ch02_pq_hybrid")
print("ok")
