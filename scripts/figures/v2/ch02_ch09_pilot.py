import os
from fig import *

# A. Symmetric encryption, in the style of the Stevens deck
f = Fig(1000, 380, "Symmetric encryption: one shared secret key",
        "Alice encrypts message m with key k into ciphertext c, c crosses an untrusted network where Eve sees only c, "
        "and Bob decrypts c with the same key k to recover m. A key generator gives both parties the same k.")
f.box(440, 58, 120, 44, "Gen", step=1)
f.arrow([(440, 90), (268, 228)], None, RED, step=1)
f.arrow([(560, 90), (732, 228)], None, RED, step=1)
f.icon("key", 300, 134, 40, step=1); f.text(298, 178, "k", 18, RED, "bold", step=1)
f.icon("key", 700, 134, 40, step=1); f.text(702, 178, "k", 18, RED, "bold", step=1)
f.badge(1, 418, 80)
f.icon("user2-phone", 78, 255, 96, "Alice", step=2)
f.arrow([(130, 258), (196, 258)], "m", BLUE, step=2, size=16)
f.box(200, 232, 110, 52, "Enc", step=2)
f.badge(2, 200, 232, step=2)
f.icon("cloud", 500, 262, 210, step=3)
f.icon("devil", 466, 214, 52, step=3)
f.text(434, 220, "Eve", 15, INK, "bold", "end", step=3)
f.text(500, 336, "Eve sees only c", 13, RED, "bold", step=3, italic=True)
f.arrow([(312, 258), (688, 258)], "c", BLUE, step=3, label_at=.08, size=16, width=2.6)
f.badge(3, 402, 258, step=3)
f.box(690, 232, 110, 52, "Dec", step=4)
f.arrow([(802, 258), (866, 258)], "m", BLUE, step=4, size=16)
f.icon("user-laptop", 922, 255, 96, "Bob", step=4)
f.badge(4, 690, 232, step=4)
f.text(500, 366, "The same key encrypts and decrypts (AES, ChaCha20). It is fast; sharing k safely is the hard part.",
       13, MUTED, italic=True)
f.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "symmetric"))

# B. Kerberos exchanges as a sequence with device icons
g = Fig(1120, 560, "Kerberos in three exchanges: the password never crosses the network",
        "A client computer exchanges two messages with each of three servers in turn. One and two: AS-REQ, a timestamp "
        "encrypted with the password-derived key, and AS-REP, a Ticket-Granting Ticket encrypted with the krbtgt key, with the "
        "Authentication Server. Three and four: TGS-REQ, the TGT and the service name, and TGS-REP, a service ticket encrypted "
        "with the service account key, with the Ticket-Granting Server. Both servers run on the domain controller, the Key "
        "Distribution Center. Five and six: AP-REQ with the service ticket and AP-REP with the service, which never contacts the KDC.")
g.icon("desktop", 120, 290, 120, "Client", "user signs in")
g.raw('<line x1="236" y1="96" x2="236" y2="500" stroke="#9aa5b1" stroke-width="3" stroke-linecap="round"/>')
g.zone(760, 54, 340, 312, "Key Distribution Center", "#2f6fae", "#eef5fc")
g.text(1084, 76, "on the domain controller", 12, "#2f6fae", anchor="end")
rows = [(150, "AS", "Authentication Server",
         "AS-REQ: timestamp encrypted with the password-derived key", "AS-REP: Ticket-Granting Ticket (TGT), encrypted with the krbtgt key", RED),
        (300, "TGS", "Ticket-Granting Server",
         "TGS-REQ: TGT + the service it wants (SPN)", "TGS-REP: service ticket, encrypted with the service account key", RED),
        (452, "Service", "file server",
         "AP-REQ: service ticket", "AP-REP: session established; the KDC is not contacted", GREEN)]
n = 1
for y, name, sub, req, rep, rc in rows:
    g.icon("server", 900, y - 4, 84, None)
    g.text(968, y - 6, name, 16, INK, "bold", "start"); g.text(968, y + 12, sub, 12, MUTED, anchor="start")
    g.arrow([(240, y - 16), (852, y - 16)], req, BLUE, step=n, label_at=.5, label_dy=-8, size=13)
    g.badge(n, 262, y - 16, step=n); n += 1
    g.arrow([(852, y + 16), (240, y + 16)], rep, rc, step=n, label_at=.5, label_dy=22, size=13)
    g.badge(n, 830, y + 16, step=n); n += 1
g.text(560, 540, "Every ticket is encrypted with a key the client does not have, so the client can carry a ticket it cannot read or alter.",
       13, MUTED, italic=True)
g.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "kerberos"))
print("ok")
