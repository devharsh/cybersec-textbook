import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# 1. OSI layers with the device, data unit, and attacks at each layer
f = Fig(1100, 640, "The OSI model with the device, data unit, and typical attacks at each layer",
        "Seven layers built from the bottom up. Layer 1 Physical carries bits over cables, radio, and fiber, attacked by "
        "wiretapping and jamming. Layer 2 Data Link moves frames by MAC address through switches, attacked by ARP spoofing and MAC "
        "flooding. Layer 3 Network routes packets by IP address through routers, attacked by IP spoofing and BGP hijacking. Layer 4 "
        "Transport carries segments over TCP and UDP ports, filtered by firewalls, attacked by SYN floods and port scans. Layers 5 to "
        "7 carry data for sessions, TLS, and applications such as HTTP, attacked by session hijacking, SSL stripping, injection, and "
        "phishing.")
rows = [("7", "Application", "Data", "HTTP, DNS, SMTP, SSH", "browser", "injection, phishing", "#8e44ad"),
        ("6", "Presentation", "Data", "TLS, encoding, compression", "lock", "SSL stripping, downgrade", "#7d3c98"),
        ("5", "Session", "Data", "sessions, RPC, NetBIOS", "key", "session hijacking", "#6c3483"),
        ("4", "Transport", "Segment", "TCP, UDP, ports", "firewall", "SYN flood, port scanning", "#1f4e9c"),
        ("3", "Network", "Packet", "IP, ICMP, routing", "router", "IP spoofing, BGP hijack", "#2471a3"),
        ("2", "Data Link", "Frame", "Ethernet, MAC, ARP, Wi-Fi", "switch", "ARP spoofing, MAC flooding", "#138d75"),
        ("1", "Physical", "Bits", "cables, radio, fiber", "hub", "wiretapping, jamming", "#1e8449")]
for hx, ht in [(150, "Layer"), (340, "Data unit"), (510, "Example protocols"), (700, "Typical device"), (880, "Typical attacks")]:
    f.text(hx, 66, ht, 14, MUTED, "bold")
for i, (n, name, pdu, protos, ic, atk, col) in enumerate(rows):
    y = 80 + i * 76; st = 7 - i
    f.rect(40, y, 1020, 68, "#ffffff", col, 1.6, rx=8, step=st)
    f.rect(40, y, 220, 68, col, col, 1.6, rx=8, step=st)
    f.text(150, y + 41, f"L{n}  {name}", 18, "#ffffff", "bold", step=st)
    f.text(340, y + 41, pdu, 16, col, "bold", step=st)
    f.text(510, y + 41, protos, 14, INK, step=st)
    f.icon(ic, 700, y + 34, 56, step=st)
    f.icon("warning", 790, y + 34, 22, step=st); f.text(806, y + 39, atk, 14, RED, "bold", "start", step=st)
    f.badge(st, 40, y, step=st)
f.text(550, 625, "Encapsulation runs top to bottom on the sender and bottom to top on the receiver; a defender asks what can go wrong at each layer.", 13, MUTED, italic=True)
f.save(OUT + "ch03_osi_devices")

# 2. TCP three-way handshake
t = Fig(1000, 430, "The TCP three-way handshake",
        "The client sends SYN with its initial sequence number x. The server answers SYN-ACK with its own sequence number y and "
        "acknowledgment x plus 1. The client sends ACK with acknowledgment y plus 1, and the connection is established for data.")
t.icon("laptop", 150, 80, 90, "Client"); t.icon("server", 850, 80, 90, "Server")
t.raw('<line x1="150" y1="140" x2="150" y2="400" stroke="#9aa5b1" stroke-width="3"/><line x1="850" y1="140" x2="850" y2="400" stroke="#9aa5b1" stroke-width="3"/>')
t.arrow([(154, 170), (846, 220)], "SYN, seq = x", BLUE, step=1, size=15, width=2.6); t.badge(1, 154, 170, step=1)
t.arrow([(846, 240), (154, 290)], "SYN-ACK, seq = y, ack = x + 1", BLUE, step=2, size=15, width=2.6); t.badge(2, 846, 240, step=2)
t.arrow([(154, 310), (846, 360)], "ACK, ack = y + 1", BLUE, step=3, size=15, width=2.6); t.badge(3, 154, 310, step=3)
t.rect(380, 378, 240, 34, "#e8f5e9", GREEN, 1.6, rx=6, step=4); t.text(500, 400, "ESTABLISHED: data flows", 14, GREEN, "bold", step=4)
t.badge(4, 380, 378, step=4)
t.text(500, 424, "A SYN flood sends step 1 again and again and never completes step 3 (Section 3.10).", 12, MUTED, italic=True)
t.save(OUT + "ch03_tcp_handshake")

# 3. ARP spoofing
a = Fig(1100, 540, "ARP spoofing: forged replies put the attacker in the middle",
        "A victim PC and the default gateway talk through a switch. The attacker sends a forged ARP reply to the victim saying the "
        "gateway's IP is at the attacker's MAC address, and another to the gateway saying the victim's IP is at the attacker's MAC. "
        "Both caches are poisoned, so traffic between victim and gateway now flows through the attacker. Dynamic ARP inspection on "
        "the switch drops the forged replies.")
a.icon("desktop", 130, 190, 100, "Victim", "192.168.1.10\nMAC AA:AA")
a.icon("switch", 550, 190, 110, "Switch")
a.icon("router", 920, 190, 100, "Gateway", "192.168.1.1\nMAC GG:GG")
a.icon("cloud", 1040, 100, 90); a.raw('<line x1="960" y1="160" x2="1010" y2="120" stroke="#52606d" stroke-width="2"/>')
a.arrow([(190, 190), (490, 190)], None, "#9aa5b1", width=2); a.arrow([(610, 190), (860, 190)], None, "#9aa5b1", width=2)
a.text(380, 180, "normal path", 12, MUTED, italic=True)
a.icon("attacker", 550, 420, 100, "Attacker", "MAC EE:EE")
a.raw('<line x1="550" y1="226" x2="550" y2="360" stroke="#9aa5b1" stroke-width="2"/>')
a.arrow([(498, 410), (180, 270)], None, RED, step=1, dash=True); a.text(360, 280, "ARP reply: 192.168.1.1 is at EE:EE", 13, RED, "bold", step=1)
a.arrow([(602, 410), (880, 270)], None, RED, step=2, dash=True); a.text(720, 268, "ARP reply: 192.168.1.10 is at EE:EE", 13, RED, "bold", step=2)
a.badge(1, 470, 400, step=1); a.badge(2, 630, 400, step=2)
a.rect(20, 56, 220, 60, "#fdecea", RED, 1.6, rx=6, step=3)
a.text(130, 78, "victim ARP cache", 13, RED, "bold", step=3); a.text(130, 100, "192.168.1.1 -> EE:EE", 14, INK, step=3)
a.rect(740, 56, 220, 60, "#fdecea", RED, 1.6, rx=6, step=3)
a.text(850, 78, "gateway ARP cache", 13, RED, "bold", step=3); a.text(850, 100, "192.168.1.10 -> EE:EE", 14, INK, step=3)
a.badge(3, 20, 56, step=3); a.badge(3, 740, 56, step=3)
a.arrow([(240, 380), (480, 470)], None, ORANGE, step=4, width=3); a.arrow([(620, 470), (860, 380)], None, ORANGE, step=4, width=3)
a.text(320, 470, "traffic now flows through the attacker:", 13, ORANGE, "bold", step=4)
a.text(320, 488, "read, record, or alter it", 13, ORANGE, "bold", step=4); a.badge(4, 180, 465, step=4)
a.icon("shield", 640, 150, 40, step=5); a.text(664, 140, "Defense: dynamic ARP inspection,", 13, GREEN, "bold", "start", step=5)
a.text(664, 158, "port security, static ARP for key hosts", 13, GREEN, "bold", "start", step=5); a.badge(5, 618, 128, step=5)
a.save(OUT + "ch03_arp_spoofing")

# 4. DHCP DORA and the rogue server
d = Fig(1100, 560, "DHCP: the four DORA steps, and how starvation and a rogue server abuse them",
        "Left: the client broadcasts Discover, the DHCP server sends an Offer, the client sends Request, and the server sends "
        "Acknowledgment with the lease: IP address, default gateway, and DNS server. Servers use UDP port 67 and clients port 68. "
        "Right: an attacker floods Discover messages from spoofed MAC addresses until the pool is empty, then runs a rogue DHCP "
        "server that names the attacker's machine as the default gateway. DHCP snooping lets only the trusted switch port answer.")
d.icon("laptop", 90, 80, 80, "Client", "UDP 68"); d.icon("server", 470, 80, 80, "DHCP server", "UDP 67")
d.raw('<line x1="90" y1="162" x2="90" y2="430" stroke="#9aa5b1" stroke-width="3"/><line x1="470" y1="162" x2="470" y2="430" stroke="#9aa5b1" stroke-width="3"/>')
for i, (lab, back) in enumerate([("Discover (broadcast)", False), ("Offer: 192.168.1.50", True), ("Request: 192.168.1.50", False),
                                  ("Ack: lease, gateway, DNS", True)]):
    y = 180 + i * 62; pts = [(94, y), (466, y)]
    d.arrow(pts[::-1] if back else pts, lab, BLUE, step=i + 1, size=14, width=2.6); d.badge(i + 1, 466 if back else 94, y, step=i + 1)
d.text(280, 450, "D-O-R-A: Discover, Offer, Request, Acknowledgment", 13, MUTED, "bold")
d.raw('<line x1="560" y1="60" x2="560" y2="520" stroke="#d0d6dd" stroke-width="2" stroke-dasharray="6 6"/>')
d.text(830, 70, "Abuse", 16, RED, "bold")
d.icon("attacker", 640, 170, 86, "Attacker", step=5)
d.icon("server", 980, 170, 80, "Legit server", step=5)
for k in range(4): d.arrow([(690, 150 + k * 12), (930, 150 + k * 12)], None, RED, step=5, width=1.6, dash=True)
d.text(810, 136, "DHCP starvation: Discover floods", 13, RED, "bold", step=5)
d.text(810, 216, "from spoofed MACs; pool exhausted", 13, RED, "bold", step=5); d.badge(5, 600, 120, step=5)
d.icon("server", 680, 330, 70, step=6); d.icon("devil", 708, 300, 32, step=6); d.text(680, 386, "Rogue DHCP", 14, INK, "bold", step=6)
d.icon("laptop", 980, 330, 70, "New client", step=6)
d.arrow([(720, 330), (936, 330)], "Offer: gateway = attacker", RED, step=6, size=14, width=2.6); d.badge(6, 600, 300, step=6)
d.text(830, 410, "the client sends its traffic to the attacker: man in the middle", 13, RED, step=6, italic=True)
d.icon("shield", 620, 470, 40, step=7); d.text(648, 466, "Defense: DHCP snooping trusts only the uplink port to the real", 13, GREEN, "bold", "start", step=7)
d.text(648, 484, "server and drops offers from any other port; add port security.", 13, GREEN, "bold", "start", step=7); d.badge(7, 596, 448, step=7)
d.save(OUT + "ch03_dhcp")

# 5. Hub, switch, and MAC flooding
h = Fig(1100, 470, "Why sniffing a switch takes work: hub, switch, and MAC flooding",
        "With a hub, a frame from A to B is repeated to every port, so the attacker in promiscuous mode sees it. A switch looks up "
        "B in its CAM table and sends the frame only to B's port, so the attacker sees nothing. In MAC flooding the attacker fills "
        "the CAM table with fake source addresses; many switches then fail open and flood every frame to every port like a hub.")
panels = [("hub", "Hub: repeats to every port", 1), ("switch", "Switch: forwards only to B", 2), ("switch", "MAC flooding: switch fails open", 3)]
for p, (dev, title, st) in enumerate(panels):
    x0 = 20 + p * 360; cx = x0 + 170
    h.zone(x0, 50, 340, 380, title, ["#7f8c8d", BLUE, RED][p], ["#f6f7f8", "#eef5fc", "#fdf2f1"][p], step=st)
    h.icon(dev, cx, 230, 96, step=st)
    hosts = [("A", cx - 110, 130, "laptop"), ("B", cx + 110, 130, "desktop"), ("Attacker", cx, 360, "attacker")]
    for lab, hx, hy, ic in hosts: h.icon(ic, hx, hy, 64, lab, step=st, label_size=13)
    h.arrow([(cx - 84, 160), (cx - 40, 208)], None, BLUE, step=st, width=2.6)
    reach_b = True; reach_att = (p != 1)
    h.arrow([(cx + 40, 208), (cx + 84, 160)], None, BLUE, step=st, width=2.6)
    if p == 2:
        h.arrow([(cx - 22, 326), (cx - 22, 268)], "fake MACs", RED, step=3, dash=True, width=2.2, label_anchor="end", label_dy=4, size=12)
        h.arrow([(cx + 22, 262), (cx + 22, 318)], None, RED, step=4, width=2.6); h.icon("eye", cx + 62, 300, 30, step=4); h.badge(4, cx + 92, 300, step=4)
    elif reach_att:
        h.arrow([(cx, 262), (cx, 318)], None, RED, step=st, width=2.6); h.icon("eye", cx + 52, 300, 30, step=st)
    else:
        h.raw(f'<line x1="{cx}" y1="262" x2="{cx}" y2="318" stroke="#c5ccd3" stroke-width="2" stroke-dasharray="4 4"/>', step=st)
        h.icon("cross", cx + 40, 296, 26, step=st)
    h.badge(st, x0 + 322, 66, step=st)
h.rect(752, 330, 112, 74, "#fff8e1", "#d9a400", 1.4, rx=4, step=3)
h.text(808, 348, "CAM table: FULL", 12, RED, "bold", step=3)
h.text(808, 366, "00:1a:.. port 7", 11, INK, step=3); h.text(808, 381, "7e:03:.. port 7", 11, INK, step=3); h.text(808, 396, "... thousands", 11, INK, step=3)
h.text(600, 450, "Hub: passive sniffing works.  Switch: the attacker needs SPAN access, ARP poisoning, or MAC flooding (macof).", 13, MUTED, italic=True)
h.save(OUT + "ch03_hub_switch")

# 6. TCP + TLS 1.3 versus QUIC
q = Fig(1100, 520, "QUIC folds the TLS 1.3 handshake into transport setup: one round trip instead of two",
        "Left, TCP plus TLS 1.3: the TCP handshake takes one round trip, then the TLS handshake takes another, so the first HTTP "
        "request goes out after two round trips. Right, QUIC over UDP: the first packet already carries the TLS ClientHello, the "
        "server answers with its handshake, and the client sends its Finished with the HTTP/3 request after one round trip. Most "
        "QUIC metadata is encrypted, and Encrypted Client Hello also hides the server name.")
for p, (title, msgs, note) in enumerate([
        ("TCP + TLS 1.3 (HTTP/2)", [("SYN", 0), ("SYN-ACK", 1), ("ACK + ClientHello", 0), ("ServerHello ... Finished", 1), ("Finished + HTTP request", 0)], "request after 2 round trips"),
        ("QUIC (HTTP/3 over UDP 443)", [("Initial: ClientHello", 0), ("ServerHello ... Finished", 1), ("Finished + HTTP/3 request", 0)], "request after 1 round trip")]):
    x0 = 30 + p * 550; L, R = x0 + 70, x0 + 450
    q.text(x0 + 260, 64, title, 17, [BLUE, GREEN][p], "bold")
    q.icon("laptop", L, 110, 70); q.icon("server", R, 110, 70)
    q.raw(f'<line x1="{L}" y1="150" x2="{L}" y2="450" stroke="#9aa5b1" stroke-width="3"/><line x1="{R}" y1="150" x2="{R}" y2="450" stroke="#9aa5b1" stroke-width="3"/>')
    for i, (lab, back) in enumerate(msgs):
        y = 175 + i * 56; st = (1 + i) if p == 0 else (7 + i)
        pts = [(L + 4, y), (R - 4, y + 22)]
        col = [BLUE, GREEN][p] if (i >= 2 or p == 1) else "#52606d"
        q.arrow(pts[::-1] if back else pts, lab, col, step=st, size=13, width=2.4)
        q.badge(st, (R - 4) if back else (L + 4), (y + 22) if back else y, step=st)
    last = 175 + (len(msgs) - 1) * 56 + 40
    q.text(x0 + 260, last + 30, note, 15, [ORANGE, GREEN][p], "bold", step=(6 if p == 0 else 10))
q.raw('<line x1="560" y1="56" x2="560" y2="470" stroke="#d0d6dd" stroke-width="2" stroke-dasharray="6 6"/>')
q.text(550, 505, "QUIC encrypts most connection metadata, and Encrypted Client Hello (ECH) hides the server name, so defenders lean on endpoints and DNS logs.", 13, MUTED, italic=True)
q.save(OUT + "ch03_quic")

# 7. The access link
k = Fig(1100, 560, "The access link: how a home or office reaches the internet",
        "Inside the premises, laptops, phones, and desktops connect to a Wi-Fi router. The gateway, a cable modem or optical network "
        "terminal, is the demarcation point with the provider. The link to the ISP is one of four kinds: coaxial cable with DOCSIS, "
        "a shared medium; fiber over a passive optical network such as GPON or XGS-PON; 5G fixed wireless access; or low-earth-orbit "
        "satellite. The ISP then connects to the internet.")
k.zone(20, 50, 330, 470, "Premises (home or office)", BLUE, "#eef5fc", step=1)
k.icon("laptop", 90, 140, 64, "Laptop", step=1, label_size=13); k.icon("phone", 90, 260, 56, "Phone", step=1, label_size=13)
k.icon("desktop", 90, 390, 64, "Desktop", step=1, label_size=13); k.icon("wifi", 230, 270, 84, "Wi-Fi router", step=1, label_size=13)
for yy in (140, 260, 390): k.arrow([(126, yy), (190, 270)], None, "#9aa5b1", step=1, width=1.8)
k.badge(1, 332, 66, step=1)
k.icon("modem", 395, 270, 84, "Gateway", "modem or ONT", step=2, label_size=13)
k.raw('<line x1="350" y1="70" x2="350" y2="510" stroke="#c0392b" stroke-width="3" stroke-dasharray="9 6"/>', step=2)
k.text(350, 536, "demarcation point", 13, RED, "bold", step=2); k.badge(2, 420, 205, step=2)
k.arrow([(272, 270), (360, 270)], None, INK, step=2, width=2.2)
links = [("Coaxial cable (DOCSIS)", "shared with the neighborhood node;\n3.1: up to ~10 Gbps down, 1-2 up", "nodes", "#8e44ad"),
         ("Fiber (PON)", "GPON ~2.5 Gbps down;\nXGS-PON 10 Gbps symmetric", "switch", "#1f8a4c"),
         ("5G fixed wireless", "radio link to a cell tower", "tower", "#2f6fae"),
         ("Low-earth-orbit satellite", "for remote areas", "satellite", "#b9770e")]
for i, (name, sub, ic, col) in enumerate(links):
    y = 100 + i * 110; st = 3 + i
    k.arrow([(440, 270), (560, y)], None, col, step=st, width=2.6)
    k.icon(ic, 600, y, 60, step=st)
    k.text(640, y - 10, name, 15, col, "bold", "start", step=st)
    k.text(640, y + 10, sub, 12, INK, anchor="start", step=st)
    k.arrow([(880, y), (960, 280)], None, col, step=st, width=2.2)
    k.badge(st, 560, y - 38, step=st)
k.icon("rack", 1000, 280, 90, "ISP", step=7); k.icon("cloud", 1040, 450, 100, step=7)
k.text(1040, 510, "Internet", 15, INK, "bold", step=7); k.arrow([(1020, 352), (1034, 404)], None, INK, step=7); k.badge(7, 1060, 220, step=7)
k.save(OUT + "ch03_access_link")

# 8. Range extender versus mesh
m = Fig(1100, 500, "Growing Wi-Fi coverage: a range extender versus a mesh system",
        "Left: a range extender repeats the router's signal on the same radio, which can roughly halve throughput, and older models "
        "create a second network name, so devices do not roam to the stronger signal. Right: a mesh system uses coordinated nodes "
        "with one network name and seamless handoff, ideally over Ethernet backhaul, giving one set of credentials to manage. "
        "Either way, use WPA3, a strong passphrase, current firmware, and a separate guest or IoT network.")
m.zone(20, 50, 520, 360, "Range extender", ORANGE, "#fef5e7", step=1)
m.icon("wifi", 100, 220, 90, "Router", "SSID: Home", step=1)
m.icon("wifi", 290, 220, 90, "Extender", "SSID: Home_EXT", step=2)
m.icon("laptop", 460, 220, 70, "Far laptop", step=3)
m.arrow([(150, 205), (240, 205)], "same radio", ORANGE, step=2, size=12, both=True); m.badge(2, 240, 140, step=2)
m.arrow([(340, 205), (420, 205)], None, ORANGE, step=3); m.badge(3, 420, 150, step=3)
m.icon("warning", 60, 330, 26, step=3); m.text(80, 326, "throughput can roughly halve", 13, ORANGE, "bold", "start", step=3)
m.text(80, 350, "second SSID: devices cling to the weak signal", 13, ORANGE, "bold", "start", step=3)
m.text(80, 374, "an extra, easily forgotten network to secure", 13, ORANGE, "bold", "start", step=3)
m.badge(1, 522, 66, step=1)
m.zone(560, 50, 520, 360, "Mesh system (for example EasyMesh)", GREEN, "#eef8ef", step=4)
m.icon("wifi", 630, 200, 80, "Main node", step=4, label_size=13); m.icon("wifi", 820, 110, 70, "Node", step=4, label_size=13)
m.icon("wifi", 990, 200, 70, "Node", step=4, label_size=13)
m.arrow([(668, 188), (782, 122)], "Ethernet backhaul", GREEN, step=5, size=12, both=True, width=3, label_dy=-14, label_anchor="end", label_at=.45)
m.arrow([(858, 122), (962, 188)], "wireless backhaul", GREEN, step=5, size=12, both=True, dash=True, label_dy=-14, label_at=.35, label_anchor="start")
m.text(820, 250, "one SSID: Home", 15, GREEN, "bold", step=4); m.badge(4, 1062, 66, step=4); m.badge(5, 738, 172, step=5)
m.icon("user2-phone", 760, 320, 60, step=6); m.arrow([(800, 320), (980, 320)], "seamless handoff while roaming", GREEN, step=6, size=12, label_dy=-10)
m.badge(6, 720, 300, step=6)
m.text(820, 396, "one logical network, one set of credentials", 13, GREEN, "bold", step=6)
m.icon("lock", 300, 450, 30, step=7); m.badge(7, 270, 438, step=7)
m.text(322, 456, "Either way: WPA3, a strong unique passphrase, current firmware on every node, and a separate guest or IoT network.", 13, INK, "bold", "start", step=7)
m.save(OUT + "ch03_wifi_mesh")
print("ok")
