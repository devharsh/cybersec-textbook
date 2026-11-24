import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""
PUB, PRIV = "#2e7d32", "#c0392b"

# Asymmetric encryption
f = Fig(1000, 400, "Asymmetric encryption: encrypt with the recipient's public key",
        "Bob makes a key pair and publishes the public key. Alice encrypts message m with Bob's public key into ciphertext c. "
        "c crosses the network, where Eve sees only c. Bob decrypts c with his private key, which never leaves him.")
f.box(700, 58, 140, 44, "Gen (key pair)", step=1)
f.arrow([(700, 82), (300, 82), (262, 228)], None, PUB, step=1)
f.icon("key", 470, 82, 44, step=1); f.text(470, 62, "Bob's public key, published to anyone", 13, PUB, "bold", step=1)
f.arrow([(800, 104), (760, 228)], None, PRIV, step=1)
f.icon("key", 862, 150, 40, step=1); f.text(862, 186, "Bob's private key", 13, PRIV, "bold", step=1)
f.text(862, 202, "never leaves Bob", 12, MUTED, step=1)
f.badge(1, 690, 60)
f.icon("user2-phone", 78, 255, 96, "Alice", step=2)
f.arrow([(130, 258), (196, 258)], "m", BLUE, step=2, size=16)
f.box(200, 232, 110, 52, "Enc", step=2); f.badge(2, 200, 232, step=2)
f.icon("cloud", 500, 262, 210, step=3); f.icon("devil", 466, 214, 52, step=3)
f.text(434, 220, "Eve", 15, INK, "bold", "end", step=3)
f.text(500, 336, "Eve sees only c and the public key", 13, RED, "bold", step=3, italic=True)
f.arrow([(312, 258), (688, 258)], "c", BLUE, step=3, label_at=.08, size=16, width=2.6); f.badge(3, 402, 258, step=3)
f.box(690, 232, 110, 52, "Dec", step=4); f.badge(4, 690, 232, step=4)
f.arrow([(802, 258), (866, 258)], "m", BLUE, step=4, size=16)
f.icon("user-laptop", 922, 255, 96, "Bob", step=4)
f.text(500, 386, "Anyone can encrypt with the public key; only the private key holder can decrypt.", 13, MUTED, italic=True)
f.save(OUT + "asymmetric")

# Digital signature, in the style of the Stevens MAC slide
g = Fig(1000, 420, "Digital signature: sign with the private key, verify with the public key",
        "Alice signs message m with her private key to make signature s and sends m and s. Mallory in the network can change "
        "them but cannot forge a valid pair. Bob verifies with Alice's public key: an unchanged pair is accepted, a changed "
        "pair is rejected. The roles of the keys are the reverse of encryption.")
g.icon("key", 300, 128, 40, step=1); g.text(300, 168, "Alice's private key", 13, PRIV, "bold", step=1)
g.icon("key", 700, 128, 40, step=1); g.text(700, 168, "Alice's public key", 13, PUB, "bold", step=1)
g.arrow([(300, 180), (262, 226)], None, PRIV, step=1); g.arrow([(700, 180), (738, 226)], None, PUB, step=1)
g.badge(1, 250, 128)
g.icon("user2-phone", 78, 255, 96, "Alice", step=2)
g.arrow([(130, 258), (196, 258)], "m", BLUE, step=2, size=16)
g.box(200, 232, 110, 52, "Sign", step=2); g.badge(2, 200, 232, step=2)
g.icon("cloud", 500, 262, 210, step=3); g.icon("devil", 466, 214, 52, step=3)
g.text(434, 220, "Mallory", 15, INK, "bold", "end", step=3)
g.text(470, 336, "can alter m or s, cannot forge a valid pair", 13, RED, "bold", step=3, italic=True)
g.arrow([(312, 258), (688, 258)], "m, s", BLUE, step=3, label_at=.1, size=16, width=2.6); g.badge(3, 412, 258, step=3)
g.text(650, 246, "m', s'", 15, BLUE, "bold", step=3)
g.box(690, 232, 110, 52, "Verify", step=4); g.badge(4, 690, 232, step=4)
g.arrow([(802, 258), (866, 258)], None, BLUE, step=4)
g.icon("user-laptop", 922, 255, 96, "Bob", step=4)
g.icon("check", 704, 316, 28, step=4); g.text(724, 321, "ACCEPT if unchanged", 13, GREEN, "bold", "start", step=4)
g.icon("cross", 704, 348, 28, step=4); g.text(724, 353, "REJECT if changed", 13, RED, "bold", "start", step=4)
g.text(500, 404, "Gives authenticity, integrity, and non-repudiation: only Alice's private key could have made s.", 13, MUTED, italic=True)
g.save(OUT + "digital_signature")

# Encoding, encryption, hashing
h = Fig(1100, 520, "Encoding, encryption, and hashing",
        "Three rows. Encoding: data goes through a public scheme such as ASCII or Base64 and anyone can reverse it, no key. "
        "Encryption: data goes through a cipher with a secret key, such as AES or RSA, and only a key holder can reverse it. "
        "Hashing: data goes through a hash function into a fixed-size digest, with no key and no way back.")
rows = [("Encoding", "no key, reversible by anyone", "code", "Encode\n(public scheme)", "Encoded text", "ASCII, Base64", GREEN, "anyone can decode"),
        ("Encryption", "secret key, reversible only with the key", "lock", "Encrypt\n(+ key)", "Ciphertext", "AES, RSA", BLUE, "only a key holder can decrypt"),
        ("Hashing", "no key, not reversible, fixed size", "search", "Hash\nfunction", "Digest (fixed size)", "SHA-256", RED, "no way back")]
for k, (name, sub, ic, proc, out, ex, col, back) in enumerate(rows):
    y = 80 + k * 148; st = k + 1
    h.text(38, y, name, 17, col, "bold", "start", step=st); h.text(38 + len(name) * 10 + 14, y, sub, 13, MUTED, anchor="start", step=st)
    h.icon("document", 90, y + 62, 72, "Data", step=st)
    h.arrow([(134, y + 58), (284, y + 58)], None, INK, step=st)
    h.box(290, y + 30, 170, 58, proc, step=st)
    h.icon(ic, 520, y + 58, 50, step=st)
    h.arrow([(552, y + 58), (690, y + 58)], None, INK, step=st)
    h.icon("document", 740, y + 62, 72, out, ex, step=st)
    h.arrow([(790, y + 58), (850, y + 58)], None, MUTED, step=st, dash=True)
    h.icon(["check", "key", "cross"][k], 878, y + 58, 34, step=st)
    h.text(900, y + 63, back, 13, col, "bold", "start", step=st)
    h.badge(st, 18, y - 5, step=st)
h.save(OUT + "encoding_encryption_hashing")

# Wrong-key decryption
w = Fig(1000, 440, "Wrong-key decryption: garbage output versus a clean rejection",
        "Ciphertext decrypted with the wrong key behaves three ways. Stream and counter modes such as CTR, CFB, and OFB give "
        "garbage with no error. CBC or ECB with padding gives a padding error about 255 times in 256 and garbage about once in "
        "256. AEAD modes such as AES-GCM and ChaCha20-Poly1305 reject the input because authentication fails.")
w.icon("document", 80, 214, 78, "Ciphertext", step=1); w.icon("key", 150, 160, 44, step=1)
w.icon("cross", 170, 146, 22, step=1); w.text(150, 128, "wrong key", 13, RED, "bold", step=1)
modes = [("Stream / CTR / CFB / OFB", "warning", "Garbage output", "no error at all", "#fff4d6", ORANGE),
         ("CBC / ECB + padding", "warning", "Padding error ~255/256", "garbage ~1/256", "#ffe8cc", ORANGE),
         ("AEAD: AES-GCM,\nChaCha20-Poly1305", "shield", "Clean rejection", "authentication fails", "#e6f4ea", GREEN)]
for k, (m, ic, res, sub, fill, col) in enumerate(modes):
    y = 90 + k * 118; st = k + 1  # the ciphertext and wrong key build with mode 1, matching the (1)-(3) labels in the code cell
    w.arrow([(126, 214), (300, y + 30)], None, INK, step=st)
    w.box(306, y, 250, 60, m, step=st, size=14)
    w.arrow([(560, y + 30), (640, y + 30)], None, INK, step=st)
    w.raw(f'<rect x="646" y="{y}" width="300" height="60" rx="8" fill="{fill}" stroke="{col}" stroke-width="1.8"/>', step=st)
    w.icon(ic, 680, y + 30, 40, step=st)
    w.text(710, y + 26, res, 15, INK, "bold", "start", step=st); w.text(710, y + 46, sub, 13, MUTED, anchor="start", step=st)
    w.badge(st, 306, y, step=st)
w.text(500, 428, "Only authenticated encryption tells you the key or ciphertext is wrong; the other modes fail silently or leak.", 13, MUTED, italic=True)
w.save(OUT + "ch02_wrongkey")
print("ok")

# ECB versus CBC, using the three panels of the original image
import base64, io
from PIL import Image
src = Image.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "assets", "figures", "") + "ch02_ecb_vs_cbc.png").convert("RGB")
def uri(box):
    b = io.BytesIO(); src.crop(box).save(b, "PNG"); return "data:image/png;base64," + base64.b64encode(b.getvalue()).decode()
orig, ecb, cbc = uri((18, 30, 398, 410)), uri((415, 30, 795, 410)), uri((813, 30, 1193, 410))
e = Fig(1100, 560, "ECB versus CBC: why the mode of operation matters",
        "The same image is encrypted with AES twice. In ECB mode every identical block encrypts to the same ciphertext, so the "
        "shapes of the original image remain visible. In CBC mode each block is chained to the previous ciphertext and a random "
        "IV, so the result looks like random noise.")
img = lambda x, y, s, u, step: e.raw(f'<image x="{x}" y="{y}" width="{s}" height="{s}" href="{u}"/>'
                                    f'<rect x="{x}" y="{y}" width="{s}" height="{s}" fill="none" stroke="#52606d" stroke-width="2"/>', step)
img(50, 150, 250, orig, 1); e.text(175, 136, "Original image", 16, INK, "bold", step=1); e.badge(1, 50, 150, step=1)
e.arrow([(304, 250), (420, 170), (560, 170)], None, INK, step=2); e.icon("lock", 470, 140, 46, step=2)
e.text(470, 202, "AES-ECB", 14, INK, "bold", step=2)
img(570, 60, 210, ecb, 2); e.badge(2, 570, 60, step=2)
e.icon("warning", 820, 110, 46, step=2)
e.text(850, 104, "Structure leaks", 16, RED, "bold", "start", step=2)
e.text(850, 124, "equal blocks give equal", 13, MUTED, anchor="start", step=2)
e.text(850, 140, "ciphertext blocks", 13, MUTED, anchor="start", step=2)
e.arrow([(304, 300), (420, 390), (560, 390)], None, INK, step=3); e.icon("lock", 470, 360, 46, step=3)
e.text(470, 422, "AES-CBC + random IV", 14, INK, "bold", step=3)
img(570, 290, 210, cbc, 3); e.badge(3, 570, 290, step=3)
e.icon("check", 820, 340, 46, step=3)
e.text(850, 334, "Looks random", 16, GREEN, "bold", "start", step=3)
e.text(850, 354, "each block is chained to", 13, MUTED, anchor="start", step=3)
e.text(850, 370, "the one before it", 13, MUTED, anchor="start", step=3)
e.text(550, 540, "Never use ECB for data longer than one block; prefer an AEAD mode such as AES-GCM.", 13, MUTED, italic=True)
e.save(OUT + "ch02_ecb_vs_cbc")

# eMudhra trust chain and response
m = Fig(1120, 640, "Distrusting a certificate authority: the eMudhra emSign G3 response, October 2026",
        "A root certificate, emSign ECC Root CA - G3, cross-signs TLS and code-signing sub-roots. Under it, eight weak P-384 "
        "intermediates, six TLS and two code signing, issued no customer certificates, while sibling intermediates under the same "
        "root carry about 30,800 unexpired precertificates that had to move. The response runs from narrowest to widest: one, "
        "revocation by the CA on October 18; two, browser blocklists on October 17 and 20; three, root removal announced "
        "October 20; four, collateral as customers migrate and eMudhra exits the TLS business on October 22.")
m.icon("certificate", 380, 92, 70, step=1)
m.raw('', step=1)
m.box(430, 58, 400, 70, "emSign ECC Root CA - G3\ncross-signs the G3 TLS and code-signing sub-roots;\ndistrust announced Oct 20, Chrome removal set for Oct 27", step=1, kind="danger", size=13)
m.arrow([(560, 130), (330, 176)], None, INK, step=1); m.arrow([(700, 130), (860, 176)], None, INK, step=1)
m.icon("certificate", 120, 222, 60, step=1); m.icon("warning", 150, 196, 28, step=1)
m.box(160, 180, 360, 78, "8 weak intermediates (P-384)\n6 TLS, 2 code signing; private keys were\nintegers below 256; no customer certificates", step=1, kind="note", size=13)
m.icon("certificate", 1050, 222, 60, step=1)
m.box(640, 180, 380, 78, "Sibling intermediates, same root\nabout 30,800 unexpired precertificates\n(Chrome) had to move to another hierarchy", step=1, kind="process", size=13)
m.text(60, 302, "Response, from narrowest to widest (2026, UTC)", 16, MUTED, "bold", "start", step=1)
resp = [("cross", "Revocation by the CA", "October 18: all eight revoked as a CA compromise"),
        ("desktop", "Browser blocklists", "Oct 17: Chrome CRLSet 19:45, Firefox OneCRL 22:59; Windows list, Oct 20"),
        ("certificate", "Root removal", "Oct 20: Mozilla announces it; Chrome follows; Windows drops G3 roots, Oct 26"),
        ("group", "Collateral", "customers under the root migrate; eMudhra exits the TLS business, Oct 22")]
for k, (ic, name, detail) in enumerate(resp):
    y = 322 + k * 72; st = k + 2
    m.raw(f'<rect x="60" y="{y}" width="1000" height="58" rx="8" fill="#f5f7f9" stroke="#9aa5b1" stroke-width="1.5"/>', step=st)
    m.badge(st, 84, y + 29, step=st)
    m.icon(ic, 130, y + 29, 44, step=st)
    m.text(164, y + 34, name, 15, INK, "bold", "start", step=st)
    m.text(370, y + 34, detail, 14, INK, anchor="start", step=st)
m.save(OUT + "ch02_emudhra_response")
print("ok2")
