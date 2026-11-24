import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# Redraw: segmentation zones and the ten permitted flows
z = Fig(1100, 720, "A 250-person firm in eight zones, and the ten flows that are permitted",
        "The internet sits above eight zones. Guest, VLAN 170, may reach the internet on TCP 80 and 443. Users, VLAN 110, reach the "
        "internet on TCP 80 and 443 through the proxy, servers on TCP 445, 88, 389, 636, and 3268, print on TCP 9100 and 631, and "
        "out-of-band management on TCP 22 and 443 from named admin hosts. Servers, VLAN 100, reach named internet destinations on "
        "TCP 443 and the camera range in building systems, VLAN 140, on TCP 554 and 80. The DMZ, VLAN 200, reaches 10.0.0.50 on TCP "
        "5432, and the internet reaches the DMZ on TCP 80 and 443 at 203.0.113.10. Voice, VLAN 120, reaches servers on UDP 5060 and "
        "media. Everything else, 62 of 72 directions, is denied.")
z.rect(40, 50, 1020, 70, "#fdecea", RED, 2, rx=10, step=1); z.icon("cloud", 470, 84, 70, step=1)
z.text(560, 82, "Internet", 18, INK, "bold", "start", step=1); z.text(560, 102, "outside every zone, reached only on the paths below", 12, MUTED, anchor="start", step=1)
zones = {"Guest": (40, 220, "VLAN 170", "10.0.70.0/24", "phone", "#fadbd8"), "Users": (300, 220, "VLAN 110", "10.0.10.0/23", "group", "#d6e9f8"),
         "Servers": (600, 220, "VLAN 100", "10.0.0.0/24", "rack", "#aed6f1"), "DMZ": (860, 220, "VLAN 200", "203.0.113.0/24", "server", "#fcf3cf"),
         "Print": (40, 500, "VLAN 130", "10.0.30.0/24", "printer", "#eaecee"), "Out-of-band mgmt": (300, 500, "VLAN 160", "10.0.60.0/24", "switch", "#fae5d3"),
         "Voice": (600, 500, "VLAN 120", "10.0.20.0/24", "headset", "#eaecee"), "Building systems": (860, 500, "VLAN 140", "10.0.40.0/24", "camera", "#eaecee")}
for name, (x, y, vl, net, ic, fill) in zones.items():
    z.rect(x, y, 200, 130, fill, "#2b3138", 1.6, rx=10, step=2)
    z.icon(ic, x + 45, y + 65, 60, step=2); z.text(x + 128, y + 40, name if name != "DMZ" else "DMZ", 15, INK, "bold", step=2)
    z.text(x + 128, y + 70, vl, 13, INK, step=2); z.text(x + 128, y + 92, net, 12, MUTED, step=2)
z.badge(2, 40, 220, step=2)
B = "#1f4e9c"
fl = [([(140, 218), (140, 124)], "TCP 80, 443", (148, 170, "start")),
      ([(400, 218), (400, 124)], "TCP 80, 443 via proxy", (408, 170, "start")),
      ([(700, 218), (700, 124)], "TCP 443 to named\ndestinations", (708, 160, "start")),
      ([(960, 124), (960, 218)], "TCP 80, 443 to\n203.0.113.10", (952, 160, "end")),
      ([(502, 280), (598, 280)], "TCP 445, 88,\n389, 636,\n3268", (550, 236, "middle")),
      ([(858, 300), (802, 300)], "TCP 5432 to\n10.0.0.50 only", (830, 372, "middle")),
      ([(330, 352), (330, 420), (140, 420), (140, 498)], "TCP 9100, 631", (236, 412, "middle")),
      ([(420, 352), (420, 498)], "TCP 22, 443 from\nnamed admin hosts", (428, 440, "start")),
      ([(700, 498), (700, 352)], "UDP 5060, media", (692, 440, "end")),
      ([(760, 352), (760, 400), (960, 400), (960, 498)], "TCP 554, 80 to\nthe camera range", (860, 424, "middle"))]
for i, (pts, lab, (lx, ly, la)) in enumerate(fl):
    z.arrow(pts, None, B, step=3 + i, width=2.6); z.text(lx, ly, lab, 12, B, "bold", la, step=3 + i)
z.badge(3, 120, 190, step=3); z.badge(12, 1030, 470, step=12, color=RED)
z.text(550, 680, "Eight zones give 8 x 7 = 56 directed pairs, plus 8 outbound and 8 inbound internet paths: 72 decisions.", 13, MUTED, step=12)
z.text(550, 702, "Ten are permitted. The other 62 are denied, including users to users and guest to anything internal.", 13, RED, "bold", step=12)
z.save(OUT + "ch11_segmentation_zones_v2")

# New: screened subnet (DMZ) between two bastion hosts
d = Fig(1100, 420, "A DMZ between two bastion hosts",
        "Traffic from the internet passes an outer bastion host into the DMZ, which holds the public web, mail, and DNS servers. An "
        "inner bastion host separates the DMZ from the internal network, so a compromise of the outer host or a DMZ server still "
        "leaves a second barrier in front of internal systems.")
d.icon("cloud", 100, 200, 140, "Internet", step=1)
d.icon("firewall", 290, 200, 90, "Outer bastion", step=2)
d.zone(380, 70, 330, 260, "DMZ", ORANGE, "#fef5e7", step=3)
for k, (ic, lab) in enumerate([("server", "Web"), ("envelope", "Mail"), ("server", "DNS")]): d.icon(ic, 450 + k * 95, 200, 60, lab, step=3, label_size=13)
d.icon("firewall", 790, 200, 90, "Inner bastion", step=4)
d.zone(870, 70, 210, 260, "Internal network", GREEN, "#eef8ef", step=5)
d.icon("desktop", 930, 170, 56, step=5); d.icon("database", 1020, 170, 56, step=5); d.icon("group", 975, 260, 56, step=5)
d.arrow([(170, 200), (244, 200)], None, INK, step=2, width=2.6); d.arrow([(336, 200), (418, 200)], None, INK, step=3, width=2.6)
d.arrow([(682, 200), (744, 200)], None, INK, step=4, width=2.6); d.arrow([(836, 200), (900, 200)], None, INK, step=5, width=2.6)
for n_, x in [(1, 100), (2, 290), (4, 790)]: d.badge(n_, x - 50, 110, step=n_)
d.badge(3, 692, 88, step=3); d.badge(5, 1062, 88, step=5)
d.text(550, 380, "If the outer host or a DMZ server falls, the inner bastion still protects the internal network.", 14, INK, "bold", step=6)
d.save(OUT + "ch11_dmz")

# New: zero trust policy enforcement
t = Fig(1100, 560, "Zero trust: every request is checked, and access is to one application at a time",
        "Left, the old perimeter model: once inside, a compromised host can reach everything. Right, zero trust: a user and device "
        "send each request to a policy enforcement point, which asks the policy decision point to evaluate identity, device health, "
        "location, time, and data sensitivity, and then connects the user only to the one application allowed. Trust is re-evaluated "
        "continuously and can be revoked mid-session.")
t.zone(20, 60, 380, 400, "Perimeter model", RED, "#fdf2f1", step=1); t.badge(1, 382, 76, step=1, color=RED)
t.icon("firewall", 210, 120, 70, "one gate", step=1)
for k, (x, y) in enumerate([(90, 260), (210, 260), (330, 260), (150, 380), (270, 380)]): t.icon(["desktop", "server", "database", "server", "desktop"][k], x, y, 54, step=1)
t.icon("bug", 108, 236, 26, step=1)
for (x, y) in [(210, 260), (330, 260), (150, 380), (270, 380)]: t.arrow([(116, 268), (x - 26, y)], None, RED, step=1, width=1.6, dash=True)
t.text(210, 444, "inside = trusted: one compromised host reaches everything", 12, RED, "bold", step=1)
t.zone(420, 60, 660, 400, "Zero trust", GREEN, "#eef8ef", step=2); t.badge(2, 1062, 76, step=2, color=GREEN)
t.icon("user-laptop", 500, 250, 80, "User + device", step=2)
t.icon("firewall", 680, 250, 80, "Enforcement point", "PEP", step=3)
t.icon("gear", 680, 100, 54, "Decision point", "PDP", step=4)
t.arrow([(548, 250), (634, 250)], "request", BLUE, step=3, size=12); t.badge(3, 560, 206, step=3)
t.arrow([(680, 207), (680, 178)], None, ORANGE, step=4, both=True, width=2.4)
sig = ["identity + MFA", "device health", "location, time", "data sensitivity"]
for k, s2 in enumerate(sig): t.text(760, 96 + k * 20, s2, 12, ORANGE, "bold", "start", step=4)
t.badge(4, 620, 100, step=4, color=ORANGE)
for k, (lab, ok) in enumerate([("Payroll app", True), ("Source code", False), ("Admin console", False)]):
    y = 170 + k * 100
    t.icon("server", 980, y, 56, lab, step=5, label_size=12)
    t.arrow([(726, 250), (944, y)], None, GREEN if ok else "#c5ccd3", step=5, width=2.6 if ok else 1.6, dash=not ok)
    if not ok: t.icon("cross", 900, y + (250 - y) * 0.18, 20, step=5)
t.badge(5, 870, 205, step=5, color=GREEN)
t.icon("clock", 520, 400, 34, step=6); t.badge(6, 490, 390, step=6)
t.text(548, 396, "continuous verification: posture or behavior changes,", 12, INK, "bold", "start", step=6)
t.text(548, 412, "and access steps down or is revoked mid-session", 12, INK, "bold", "start", step=6)
t.text(550, 500, "VPN: authenticate once, broad network reach.   ZTNA: verify each request, reach one app, resources invisible until authorized.", 13, MUTED, italic=True, step=7)
t.save(OUT + "ch11_zero_trust")

# New: remote-access VPN and split tunneling
v = Fig(1100, 560, "A remote-access VPN, and what split tunneling leaves out",
        "Full tunnel: the laptop encrypts all traffic in an IPsec or WireGuard tunnel across the internet to the corporate VPN "
        "gateway, so corporate traffic and web traffic both pass the corporate security stack. Split tunnel: only corporate traffic "
        "uses the tunnel and web traffic goes straight to the internet, so malware talking to its C2 server is never seen by the "
        "corporate stack.")
for p, (title, split, y0) in enumerate([("Full tunnel", False, 70), ("Split tunnel", True, 300)]):
    v.text(40, y0 + 10, title, 16, [GREEN, ORANGE][p], "bold", "start", step=1 + 2 * p); v.badge(1 + 2 * p, 24, y0 + 4, step=1 + 2 * p)
    v.icon("laptop", 110, y0 + 100, 80, "Remote laptop", step=1 + 2 * p)
    v.icon("cloud", 420, y0 + 100, 150, step=1 + 2 * p); v.text(420, y0 + 56, "public internet", 12, MUTED, step=1 + 2 * p)
    v.rect(160, y0 + 84, 520, 34, "#e8f5e9" if not split else "#fff3e0", GREEN, 2.4, rx=17, step=1 + 2 * p)
    v.icon("lock", 300, y0 + 101, 24, step=1 + 2 * p); v.text(430, y0 + 106, "encrypted tunnel (IPsec or WireGuard)", 13, GREEN, "bold", step=1 + 2 * p)
    v.icon("firewall", 730, y0 + 100, 70, "VPN gateway", "security stack", step=1 + 2 * p)
    v.icon("server", 900, y0 + 100, 64, "Corporate apps", step=1 + 2 * p)
    v.arrow([(768, y0 + 100), (864, y0 + 100)], None, GREEN, step=1 + 2 * p, width=2.4)
    if not split:
        v.text(820, y0 + 40, "web traffic also inspected here", 12, GREEN, "bold", step=1)
    else:
        v.icon("bug", 130, y0 + 60, 28, step=4); v.icon("server", 600, y0 + 200, 50, "C2 server", step=4, label_size=12); v.icon("devil", 624, y0 + 180, 24, step=4)
        v.arrow([(150, y0 + 138), (568, y0 + 200)], "web and C2 traffic go direct", RED, step=4, size=12, width=2.6, dash=True, label_dy=24, label_at=.4)
        v.text(820, y0 + 206, "never seen by the corporate stack", 13, RED, "bold", step=4); v.badge(4, 660, y0 + 176, step=4, color=RED)
v.save(OUT + "ch11_vpn")

# New: Tor circuit
r = Fig(1100, 430, "Tor: three relays, three layers, and no relay that knows both ends",
        "The user's Tor client wraps the request in three layers of encryption and sends it through an entry guard, a middle relay, "
        "and an exit relay. The guard sees the user but not the destination, the middle relay sees neither, and the exit sees the "
        "destination but not the user. The exit can read anything not protected by end-to-end encryption, so HTTPS still matters.")
nodes = [("user-laptop", 90, "User", "Tor client"), ("server", 330, "Entry guard", "sees: user"), ("server", 560, "Middle relay", "sees: neither"),
         ("server", 790, "Exit relay", "sees: destination"), ("browser", 1010, "Website", "")]
for i, (ic, x, lab, sub) in enumerate(nodes):
    v2 = i + 1
    r.icon(ic, x, 170, 84, lab, sub, step=v2)
for i, (x1, x2, layers) in enumerate([(140, 280, 3), (380, 510, 2), (610, 740, 1)]):
    for k in range(layers):
        r.rect(x1 + k * 9, 120 + k * 9, x2 - x1 - k * 18, 60 - k * 18, "#ffffff" if k == 0 else "none", ["#8e44ad", "#2471a3", "#16a085"][k + (3 - layers)], 3, rx=14, step=i + 2)
    r.icon("envelope", (x1 + x2) / 2, 150, 26, step=i + 2)
r.arrow([(840, 150), (960, 150)], "HTTPS still needed", ORANGE, step=5, size=12, width=2.4)
for i, (col, lab) in enumerate([("#8e44ad", "layer for the guard"), ("#2471a3", "layer for the middle"), ("#16a085", "layer for the exit")]):
    r.rect(180 + i * 250, 320, 30, 18, "none", col, 3, rx=9, step=6); r.text(220 + i * 250, 334, lab, 13, INK, anchor="start", step=6)
r.badge(6, 150, 320, step=6)
r.text(550, 392, "Proxy: redirects and inspects.   VPN: encrypts and relocates.   Tor: anonymizes.", 15, INK, "bold", step=7)
r.save(OUT + "ch11_tor")
print("ok")
