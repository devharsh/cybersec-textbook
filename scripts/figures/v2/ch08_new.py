import os
import sys, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# 1. Scanning pipeline
s = Fig(1100, 470, "The scanning pipeline: each stage refines what the last one found",
        "Seven stages left to right: host discovery finds live IP addresses; network mapping finds the routers and firewalls in "
        "between; port scanning finds open, closed, and filtered ports; fingerprinting infers the operating system; version scanning "
        "pins down the exact software; vulnerability scanning finds weaknesses; exploitation follows in Chapter 9. Time dominates: "
        "65,536 ports at one second each on 500 hosts takes about 1.1 years.")
stg = [("Host discovery", "live IPs", "laptop"), ("Network mapping", "topology", "router"), ("Port scanning", "open, closed,\nfiltered", "firewall"),
       ("Fingerprinting", "OS, behavior", "fingerprint"), ("Version scanning", "exact software", "code"), ("Vulnerabilities", "misconfigurations,\nmissing patches", "bug"),
       ("Exploitation", "Chapter 9", "key")]
for i, (name, sub, ic) in enumerate(stg):
    x = 75 + i * 157; col = RED if i == 6 else BLUE
    s.card(x - 68, 60, 136, 230, ic, name, None, col, step=i + 1, icon_size=70, title_size=13)
    s.text(x, 200, sub, 12, MUTED, step=i + 1); s.badge(i + 1, x - 56, 72, step=i + 1, color=col)
    if i < 6: s.arrow([(x + 70, 175), (x + 87, 175)], None, col, step=i + 2, width=2.6)
s.rect(140, 330, 820, 110, "#fff8e1", "#d9a400", 1.6, rx=10, step=8); s.icon("hourglass", 200, 385, 70, step=8); s.badge(8, 140, 330, step=8)
s.text(250, 372, "Why time dominates planning:", 15, INK, "bold", "start", step=8)
s.text(250, 400, "65,536 ports x 1 second x 500 hosts = 32,768,000 seconds = about 1.1 years (TCP alone)", 15, INK, anchor="start", step=8)
s.text(250, 424, "so testers prioritize ports, tune timing, and scan in stages.", 13, MUTED, anchor="start", step=8, italic=True)
s.save(OUT + "ch08_scan_pipeline")

# 2. Ping sweep and Nmap discovery probes
p = Fig(1100, 560, "Host discovery: a ping sweep, and why silence does not mean absence",
        "The scanner sends ICMP Echo Requests, type 8, across a range. Live hosts answer with Echo Replies, type 0. Addresses with no "
        "host stay silent, but so does a live host that blocks ICMP, which is why Nmap adds other probes. As root on the same subnet "
        "Nmap sends an ARP request; on a different subnet it sends an ICMP echo, a TCP SYN to 443, a TCP ACK to 80, and an ICMP "
        "timestamp request. The -Pn option skips discovery.")
p.icon("laptop", 90, 250, 90, "Scanner", "fping, nmap -sn")
hosts = [(".10", "desktop", "reply"), (".11", None, "none"), (".12", "server", "reply"), (".13", None, "none"), (".14", "desktop", "blocked")]
for k, (ip, ic, res) in enumerate(hosts):
    y = 90 + k * 82; x = 560
    p.arrow([(140, 250), (x - 44, y)], None, BLUE, step=1, width=1.8)
    if ic: p.icon(ic, x, y, 60, step=1)
    else: p.rect(x - 26, y - 22, 52, 44, "#ffffff", "#c5ccd3", 1.6, rx=6, step=1, dash=True)
    p.text(x + 48, y + 5, "192.168.1" + ip, 14, INK, "bold", "start", step=1)
    if res == "reply":
        p.arrow([(x + 180, y), (x + 260, y)], None, GREEN, step=2, width=2); p.icon("check", x + 290, y, 30, step=2)
        p.text(x + 314, y + 5, "Echo Reply (type 0): alive", 13, GREEN, "bold", "start", step=2)
    elif res == "none":
        p.icon("cross", x + 290, y, 26, step=2); p.text(x + 314, y + 5, "no reply: nothing there", 13, MUTED, "bold", "start", step=2)
    else:
        p.icon("firewall", x - 50, y - 26, 34, step=3); p.icon("warning", x + 290, y, 28, step=3)
        p.text(x + 314, y - 4, "no reply, yet alive:", 13, ORANGE, "bold", "start", step=3); p.text(x + 314, y + 14, "ICMP blocked", 13, ORANGE, "bold", "start", step=3)
p.text(330, 70, "ICMP Echo Request (type 8)", 13, BLUE, "bold", step=1)
p.badge(1, 230, 160, step=1); p.badge(2, 820, 60, step=2, color=GREEN); p.badge(3, 820, 400, step=3, color=ORANGE)
p.rect(40, 480, 1020, 66, "#eef5fc", BLUE, 1.6, rx=8, step=4); p.badge(4, 40, 480, step=4)
p.text(60, 506, "Nmap as root, same subnet: ARP request.   Different subnet: ICMP echo + TCP SYN to 443 + TCP ACK to 80 + ICMP timestamp.", 13, INK, "bold", "start", step=4)
p.text(60, 530, "Unprivileged: full TCP connect to 80 and 443.   -Pn skips discovery when a host blocks pings but is known to be up.", 13, INK, anchor="start", step=4)
p.save(OUT + "ch08_ping_sweep")

# 3. Traceroute and firewalking
t = Fig(1100, 540, "Traceroute uses TTL to make each router reveal itself; firewalking reuses the trick",
        "The scanner sends a probe with TTL 1; the first router decrements it to zero and returns ICMP time exceeded. TTL 2 is answered "
        "by the second router, and TTL 3 reaches the target, which returns an echo reply. Firewalking sets the TTL one hop beyond the "
        "firewall: if a time-exceeded message comes back from the next hop, the firewall allowed that port.")
nodes = [("laptop", 90, "Scanner"), ("router", 330, "Router 1"), ("router", 560, "Router 2"), ("server", 800, "Target")]
for ic, x, lab in nodes: t.icon(ic, x, 120, 80, lab)
for k, (ttl, dst, back) in enumerate([(1, 330, "ICMP time exceeded"), (2, 560, "ICMP time exceeded"), (3, 800, "ICMP echo reply")]):
    y = 210 + k * 70
    t.arrow([(90, y), (dst - 4, y)], f"TTL = {ttl}", BLUE, step=2 * k + 1, size=13, width=2.4)
    t.badge(2 * k + 1, 90, y, step=2 * k + 1)
    t.arrow([(dst - 4, y + 26), (94, y + 26)], back, GREEN if k == 2 else ORANGE, step=2 * k + 2, size=12, dash=True, label_dy=16, label_at=.75)
    t.badge(2 * k + 2, dst - 4, y + 26, step=2 * k + 2, color=GREEN if k == 2 else ORANGE)
    t.icon("cross", dst - 30, y - 14, 18, step=2 * k + 1) if k < 2 else None
t.text(960, 220, "Unix: UDP from port 33434,", 12, MUTED, anchor="start" if False else "middle")
t.text(960, 236, "3 probes per hop", 12, MUTED); t.text(960, 260, "Windows tracert: ICMP", 12, MUTED)
t.raw('<line x1="30" y1="420" x2="1070" y2="420" stroke="#d0d6dd" stroke-width="2" stroke-dasharray="6 6"/>')
t.text(40, 448, "Firewalking", 16, INK, "bold", "start", step=7); t.badge(7, 24, 442, step=7)
t.icon("laptop", 200, 490, 50, step=7); t.icon("firewall", 400, 490, 50, step=7); t.icon("router", 580, 490, 50, step=7)
t.arrow([(228, 480), (552, 480)], "TCP 443, TTL = firewall hop + 1", BLUE, step=7, size=12)
t.arrow([(552, 504), (228, 504)], None, GREEN, step=7, dash=True)
t.text(640, 486, "time exceeded from the next hop", 13, GREEN, "bold", "start", step=7)
t.text(640, 506, "= the firewall forwarded port 443", 13, GREEN, "bold", "start", step=7)
t.save(OUT + "ch08_traceroute")

# 4. SYN scan states and the connect scan
y0 = 120
q = Fig(1100, 520, "Reading a SYN scan: open, closed, or filtered",
        "Open: the scanner sends SYN, the target answers SYN-ACK, and the scanner sends RST instead of completing the handshake. "
        "Closed: the target answers RST. Filtered: a firewall drops the probe, so there is no response, or an ICMP unreachable comes "
        "back. A connect scan completes the full handshake, needs no privileges, and is far more likely to be logged.")
cases = [("Open", GREEN, [("SYN", 0, BLUE), ("SYN-ACK", 1, GREEN), ("RST (never completes)", 0, MUTED)]),
         ("Closed", ORANGE, [("SYN", 0, BLUE), ("RST", 1, ORANGE)]),
         ("Filtered", RED, [("SYN", 0, BLUE), ("no response, or ICMP unreachable", 1, RED)]),
         ("Connect scan (-sT)", PURPLE, [("SYN", 0, BLUE), ("SYN-ACK", 1, GREEN), ("ACK: connection made", 0, PURPLE), ("RST", 0, MUTED)])]
for i, (name, col, msgs) in enumerate(cases):
    x0 = 20 + i * 270; L, R = x0 + 40, x0 + 220
    q.zone(x0, 50, 255, 400, name, col, "#ffffff", step=i + 1); q.badge(i + 1, x0 + 237, 66, step=i + 1, color=col)
    q.icon("laptop", L, y0, 50, step=i + 1); q.icon("firewall" if name == "Filtered" else "server", R, y0, 50, step=i + 1)
    q.raw(f'<line x1="{L}" y1="{y0 + 32}" x2="{L}" y2="420" stroke="#c5ccd3" stroke-width="2"/><line x1="{R}" y1="{y0 + 32}" x2="{R}" y2="420" stroke="#c5ccd3" stroke-width="2"/>', step=i + 1)
    for k, (lab, back, mc) in enumerate(msgs):
        y = 190 + k * 56
        if name == "Filtered" and back:
            q.text((L + R) / 2, y + 18, lab, 12, mc, "bold", step=i + 1); q.icon("cross", R - 18, y - 30, 20, step=i + 1); continue
        pts = [(L + 2, y), (R - 2, y + 18)]
        q.arrow(pts[::-1] if back else pts, lab, mc, step=i + 1, size=12, width=2.2, dash=(mc == MUTED))
q.text(147, 420 + 24, "nmap -sS (root): stealthier", 12, INK, "bold", step=1)
q.text(957, 420 + 24, "any user, often logged", 12, INK, "bold", step=4)
q.text(550, 490, "Nmap scans the top 1,000 ports by default, not all 65,535.", 13, MUTED, italic=True, step=4)
q.save(OUT + "ch08_syn_scan")

# 5. Decoys and other evasion
d = Fig(1100, 520, "Decoy scanning: hiding the real scanner among spoofed sources",
        "With nmap -D the real scanner's probes are mixed with probes that appear to come from several spoofed decoy addresses, so the "
        "intrusion detection system logs many sources and cannot easily tell which is real. Other evasion tricks are fragmentation, "
        "source-port and timing changes, bad checksums to spot firewalls, and IPv6. Defenses: rate-limit and correlate, alert on "
        "illegal flags, reassemble fragments, validate checksums, and police IPv6 like IPv4.")
srcs = [("203.0.113.5", False), ("198.51.100.7", False), ("192.0.2.44 (real)", True), ("203.0.113.90", False), ("198.51.100.23", False)]
for k, (ip, real) in enumerate(srcs):
    y = 80 + k * 72
    if real: d.icon("attacker", 90, y, 60, step=1)
    else: d.icon("laptop", 90, y, 52, step=2); d.raw(f'<rect x="58" y="{y - 26}" width="64" height="52" rx="6" fill="none" stroke="#9aa5b1" stroke-dasharray="4 3"/>', step=2)
    d.text(140, y + 5, ip, 13, RED if real else MUTED, "bold", "start", step=1 if real else 2)
    d.arrow([(270, y), (520, 250)], None, RED if real else "#9aa5b1", step=1 if real else 2, width=2.4 if real else 1.6, dash=not real)
d.text(90, 445, "decoys: spoofed sources", 13, MUTED, "bold", step=2)
d.icon("firewall", 560, 250, 70, step=1); d.icon("server", 680, 250, 70, "Target", step=1)
d.badge(1, 40, 210, step=1, color=RED); d.badge(2, 40, 70, step=2)
d.icon("eye", 620, 360, 46, "IDS", step=3)
d.rect(540, 410, 200, 80, "#fff8e1", "#d9a400", 1.4, rx=6, step=3)
d.text(640, 432, "scan from 5 sources:", 12, INK, "bold", step=3); d.text(640, 452, "which one is real?", 13, RED, "bold", step=3); d.badge(3, 540, 410, step=3)
ev = [("Fragmentation -f", "modern sensors reassemble"), ("Timing -T0, --source-port", "correlate over longer windows"),
      ("--badsum firewall spotting", "only a non-validating device replies"), ("IPv6 -6", "apply the same rules to IPv6")]
d.text(790, 80, "Other tricks, and the defense", 15, INK, "bold", "start", step=4); d.badge(4, 774, 74, step=4)
for k, (a, b) in enumerate(ev):
    y = 120 + k * 80
    d.rect(780, y - 18, 290, 62, "#ffffff", "#9aa5b1", 1.4, rx=6, step=4)
    d.text(794, y + 4, a, 13, RED, "bold", "start", step=4); d.icon("shield", 800, y + 28, 18, step=4); d.text(814, y + 32, b, 12, GREEN, "bold", "start", step=4)
d.save(OUT + "ch08_decoys")

# 6. CTEM loop fed by EASM and CAASM
c = Fig(1100, 560, "Continuous threat exposure management: scanning becomes a loop",
        "External attack surface management discovers internet-facing assets from the outside, and cyber asset attack surface "
        "management consolidates inventory from existing tools through their APIs. Both feed a repeating five-stage cycle: scoping "
        "what matters, discovery of assets and exposures, prioritization by real-world exploitability and business impact, "
        "validation that an exposure is reachable and dangerous, and mobilization of remediation.")
cx, cy, R = 720, 300, 180
c.circle(cx, cy, R, "none", "#c5ccd3", 3)
c.icon("shield", cx, cy - 6, 80, "CTEM")
st = [("Scoping", "what matters most", "checklist", BLUE), ("Discovery", "assets and exposures", "search", "#16a085"),
      ("Prioritization", "exploitability, impact", "warning", ORANGE), ("Validation", "really reachable?", "check", RED), ("Mobilization", "fix and verify", "gear", PURPLE)]
for i, (name, sub, ic, col) in enumerate(st):
    ang = -90 + i * 72; a = math.radians(ang); x, y = cx + R * math.cos(a), cy + R * math.sin(a)
    c.circle(x, y, 44, "#ffffff", col, 3, step=i + 2); c.icon(ic, x, y - 2, 50, step=i + 2); c.badge(i + 2, x - 34, y - 34, step=i + 2, color=col)
    if ang == -90: tx, ty, ta = x + 58, y - 40, "start"
    elif math.cos(a) > 0.1: tx, ty, ta = x + 56, y - 4, "start"
    else: tx, ty, ta = x - 56, y - 4, "end"
    c.text(tx, ty, name, 16, col, "bold", ta, step=i + 2); c.text(tx, ty + 18, sub, 13, INK, anchor=ta, step=i + 2)
    a2, a3 = math.radians(ang + 17), math.radians(ang + 55)
    c.arrow([(cx + R * math.cos(a2), cy + R * math.sin(a2)), (cx + R * math.cos(a3), cy + R * math.sin(a3))], None, col, step=i + 3, width=3)
c.card(30, 90, 220, 160, "attacker", "EASM", "outside-in: domains, IPs,\ncerts, exposed services", BLUE, step=1, icon_size=56, title_size=16)
c.card(30, 300, 220, 160, "database", "CAASM", "inside-out: inventory from\nyour tools' APIs", BLUE, step=1, icon_size=56, title_size=16)
c.arrow([(252, 170), (330, 240)], None, BLUE, step=1, width=2.4); c.arrow([(252, 380), (330, 330)], None, BLUE, step=1, width=2.4)
c.badge(1, 30, 90, step=1)
c.text(640, 540, "From point-in-time scans to a continuous loop that keeps pace with a changing environment.", 14, MUTED, italic=True, step=7)
c.save(OUT + "ch08_ctem")
print("ok")
