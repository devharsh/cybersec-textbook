import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# DDoS attack and defense
d = Fig(1100, 560, "Distributed denial of service: attack and defense",
        "An attacker sends commands to a botnet of compromised laptops, phones, cameras, and servers. The bots flood the victim "
        "with traffic, so a legitimate user can be denied service. A scrubbing service with rate limiting absorbs and filters the "
        "flood, so only clean traffic reaches the victim server.")
d.icon("attacker", 90, 260, 120, "Attacker", "command and control", step=1, label_color=RED)
d.zone(250, 54, 230, 470, "Botnet", RED, "#fdf2f1")
bots = [("laptop", 120), ("phone", 205), ("desktop", 290), ("router", 375), ("bot", 460)]
for k, (ic, y) in enumerate(bots):
    d.icon(ic, 365, y - 6, 64, step=1)
    d.arrow([(150, 250), (325, y - 6)], None, "#8d6e63", step=1, width=1.6)
    d.arrow([(400, y - 6), (630, 290)], None, RED, step=2, width=2.6)
d.badge(1, 160, 200, step=1); d.badge(2, 520, 200, step=2)
d.text(520, 176, "flood", 14, RED, "bold", step=2)
d.icon("firewall", 690, 290, 100, "Scrubbing and", "rate limiting", step=4)
d.badge(4, 690, 222, step=4)
d.arrow([(744, 290), (880, 290)], "clean traffic", GREEN, step=4, label_dy=-10)
d.icon("rack", 960, 290, 110, "Victim server", step=2)
d.icon("user-laptop", 960, 110, 90, "Legitimate user", step=3)
d.arrow([(960, 166), (960, 222)], "may be denied service", MUTED, step=3, dash=True, label_dy=4, label_anchor="start", size=12)
d.badge(3, 900, 70, step=3)
d.text(550, 548, "Many sources flood the target at the volumetric, protocol, or application layer; defenses absorb, filter, and rate-limit.",
       13, MUTED, italic=True)
d.save(OUT + "ddos")

# SYN flood
s = Fig(1100, 560, "TCP three-way handshake versus a SYN flood",
        "Left: a normal handshake. The client sends SYN, the server replies SYN-ACK, the client sends ACK, and the connection "
        "is established. Right: an attacker sends many SYN packets from spoofed source addresses and never sends the final ACK, "
        "so half-open connections fill the server's backlog and a legitimate client is refused.")
s.zone(20, 50, 470, 470, "Normal handshake", "#2f6fae", "#f4f8fd")
s.icon("laptop", 90, 150, 80, "Client")
s.icon("server", 420, 150, 80, "Server")
for k, (lab, y, rev, col) in enumerate([("SYN", 250, False, BLUE), ("SYN-ACK", 320, True, GREEN), ("ACK", 390, False, BLUE)]):
    pts = [(130, y), (378, y)]
    s.arrow(pts[::-1] if rev else pts, lab, col, step=k + 1, label_dy=-8); s.badge(k + 1, 110 if not rev else 398, y, step=k + 1)
s.icon("check", 160, 460, 34, step=3); s.text(184, 466, "connection established", 15, GREEN, "bold", "start", step=3)
s.zone(520, 50, 560, 470, "SYN flood (half-open exhaustion)", RED, "#fdf4f3")
s.icon("attacker", 600, 128, 90, "Attacker", "spoofed sources", label_color=RED, step=4)
s.icon("server", 1000, 150, 80, "Server")
for k in range(5):
    y = 236 + k * 34
    s.arrow([(665, y), (958, y)], f"SYN (spoofed source {k + 1})", RED, step=4 + (k > 1), label_dy=-5, size=12, width=1.8)
s.badge(4, 665, 236, step=4)
# backlog slots
s.text(1000, 228, "backlog", 12, MUTED, "bold", step=5)
for k in range(6):
    s.rect(972, 236 + k * 20, 56, 16, "#e57373" if k < 5 else "#ffffff", RED, 1.2, rx=2, step=5)
s.badge(5, 1046, 236, step=5)
s.text(1000, 372, "half-open, no final ACK", 12, RED, "bold", step=5)
s.icon("user-laptop", 640, 440, 70, None, step=6)
s.arrow([(680, 440), (958, 440)], "SYN from a real client", BLUE, step=6, label_dy=-8, size=12)
s.icon("cross", 990, 440, 40, step=6); s.badge(6, 680, 470, step=6)
s.text(800, 500, "backlog full: refused", 14, RED, "bold", step=6)
s.text(550, 548, "Defenses: SYN cookies, larger backlogs with shorter timeouts, and upstream filtering.", 13, MUTED, italic=True)
s.save(OUT + "syn_flood")

# Encapsulation
e = Fig(1100, 560, "Encapsulation down the TCP/IP stack",
        "A laptop sends application data. The transport layer adds a TCP header to make a segment, the internet layer adds an IP "
        "header to make a packet, and the link layer adds an Ethernet header and trailer to make a frame. The frame crosses the "
        "network through a switch and router, and the server strips the headers in reverse order.")
e.icon("laptop", 70, 300, 90, "Sender")
e.icon("server", 1040, 300, 90, "Receiver")
L = [("Application", "data", [("data", "#d6eaf8", 300)]),
     ("Transport", "segment", [("TCP hdr", "#f9e79f", 90), ("data", "#d6eaf8", 300)]),
     ("Internet", "packet", [("IP hdr", "#f5cba7", 80), ("TCP hdr", "#f9e79f", 90), ("data", "#d6eaf8", 300)]),
     ("Link", "frame", [("Eth hdr", "#d2b4de", 80), ("IP hdr", "#f5cba7", 80), ("TCP hdr", "#f9e79f", 90), ("data", "#d6eaf8", 300), ("FCS", "#d2b4de", 50)])]
for k, (layer, unit, blocks) in enumerate(L):
    y = 80 + k * 86; st = k + 1
    e.text(150, y + 26, layer, 15, INK, "bold", "start", step=st)
    total = sum(b[2] for b in blocks); x = 560 - total / 2 + 70
    for name, col, wdt in blocks:
        e.rect(x, y, wdt, 40, col, "#52606d", 1.4, rx=3, step=st)
        e.text(x + wdt / 2, y + 25, name, 13, INK, "bold", step=st); x += wdt
    e.text(x + 12, y + 25, unit.upper(), 13, BLUE, "bold", "start", step=st)
    e.badge(st, 132, y + 20, step=st)
e.icon("switch", 470, 470, 70, step=5); e.icon("router", 640, 470, 70, step=5)
e.arrow([(110, 360), (110, 470), (430, 470)], None, INK, step=5)
e.arrow([(510, 470), (600, 470)], None, INK, step=5)
e.arrow([(680, 470), (1040, 470), (1040, 360)], "server strips headers in reverse", GREEN, step=6, label_at=.3, label_dy=-10)
e.badge(5, 300, 470, step=5); e.badge(6, 960, 470, step=6)
e.text(550, 548, "Each layer adds its own header on the way down; the receiver removes them on the way up.", 13, MUTED, italic=True)
e.save(OUT + "ch03_encapsulation")

# Record DDoS sizes in 2025
b = Fig(900, 470, "Record DDoS attacks mitigated by Cloudflare during 2025 (as reported)",
        "Bar chart of peak attack size in terabits per second: May 7.3, September 11.5, late September 22.2, fourth quarter 29.7, "
        "and the fourth-quarter peak 31.4. Each record stood for only weeks.")
b.bars(110, 400, 740, 280, ["May", "Sep", "Late Sep", "Q4", "Q4 peak"], [7.3, 11.5, 22.2, 29.7, 31.4], 35, 5,
       "Peak attack size (Tbps)", "#2c7fb8", ["bot", "bot", "bot", "bot", "warning"])
b.text(450, 458, "Each record stood for only weeks: the DDoS arms race of 2025.", 13, MUTED, italic=True, step=5)
b.save(OUT + "ch03_ddos_2025")
print("ok")
