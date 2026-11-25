import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# 802.1X and NAC
x = Fig(1100, 520, "802.1X: the switch admits only authentication traffic until the device is verified",
        "A laptop, the supplicant, plugs into a switch port, the authenticator. The switch blocks everything except EAP frames and "
        "relays the device's credentials to a RADIUS authentication server. If the server accepts and the health check passes, the "
        "switch opens the port onto the user VLAN; a non-compliant device is placed in a remediation VLAN that can reach only update "
        "servers.")
x.icon("laptop", 110, 200, 90, "Supplicant", "the client device")
x.icon("switch", 470, 200, 110, "Authenticator", "switch or access point")
x.icon("server", 860, 200, 90, "Authentication server", "RADIUS")
x.arrow([(160, 190), (410, 190)], "EAP only", BLUE, step=1, size=13, width=2.6); x.badge(1, 170, 170, step=1)
x.icon("lock", 470, 140, 30, step=1); x.text(470, 118, "port blocked for all else", 12, RED, "bold", step=1)
x.arrow([(530, 190), (812, 190)], "credentials relayed (RADIUS)", BLUE, step=2, size=13, width=2.6, both=True); x.badge(2, 540, 170, step=2)
x.icon("check", 860, 120, 30, step=3); x.text(860, 100, "accept + health check passed", 12, GREEN, "bold", step=3); x.badge(3, 900, 120, step=3, color=GREEN)
x.zone(280, 330, 300, 160, "User VLAN", GREEN, "#eef8ef", step=4); x.icon("server", 360, 420, 56, step=4); x.icon("database", 460, 420, 56, step=4)
x.arrow([(440, 300), (420, 338)], None, GREEN, step=4, width=2.4); x.text(424, 322, "compliant", 12, GREEN, "bold", "end", step=4); x.badge(4, 560, 346, step=4, color=GREEN)
x.zone(640, 330, 320, 160, "Remediation VLAN", ORANGE, "#fef5e7", step=5); x.icon("gear", 800, 420, 56, "update servers only", step=5, label_size=12)
x.arrow([(500, 300), (730, 334)], None, ORANGE, step=5, width=2.4); x.text(600, 312, "non-compliant", 12, ORANGE, "bold", "start", step=5); x.badge(5, 942, 346, step=5, color=ORANGE)
x.save(OUT + "ch11_8021x")

# Deception
h = Fig(1100, 500, "Deception: decoys that no legitimate user should ever touch",
        "Inside the production network sit a honeypot, a decoy server, and honeytokens: a fake credential and a canary file. An "
        "attacker who has broken in explores, touches a decoy, and triggers an alert to the security team. Because nobody has a "
        "legitimate reason to use a decoy, the alert is almost never a false positive.")
h.zone(200, 60, 860, 300, "Production network", BLUE, "#eef5fc")
for k, (ic, lab) in enumerate([("server", "file server"), ("database", "database"), ("desktop", "workstation")]): h.icon(ic, 300 + k * 140, 170, 64, lab, label_size=12)
h.icon("honeypot", 760, 160, 80, "Honeypot", "fake RDP server", step=1); h.badge(1, 712, 112, step=1, color=ORANGE)
h.icon("idcard", 900, 140, 50, "fake admin", "credential", step=2, label_size=12); h.icon("document", 990, 140, 50, "canary", "file", step=2, label_size=12)
h.badge(2, 945, 96, step=2, color=ORANGE)
h.text(860, 270, "honeytokens", 13, ORANGE, "bold", step=2)
h.icon("attacker", 90, 220, 80, "Intruder", step=3)
h.arrow([(130, 196), (240, 108), (700, 108), (730, 128)], "explores, then touches a decoy", RED, step=3, size=12, width=2.6, label_at=.5, label_dy=-6, dash=True)
h.badge(3, 140, 180, step=3, color=RED)
h.icon("eye", 760, 430, 50, "Security team", step=4); h.icon("warning", 700, 300, 34, step=4)
h.arrow([(760, 222), (760, 400)], None, RED, step=4, width=2.6); h.text(772, 330, "alert", 13, RED, "bold", "start", step=4); h.badge(4, 800, 360, step=4, color=RED)
h.rect(40, 390, 520, 80, "#e8f5e9", GREEN, 1.6, rx=8, step=5); h.badge(5, 40, 390, step=5, color=GREEN)
h.text(60, 420, "near-zero false positives:", 14, GREEN, "bold", "start", step=5)
h.text(60, 444, "any interaction with a decoy is evidence of an intruder", 13, INK, anchor="start", step=5)
h.save(OUT + "ch11_honeypot")

# CVE-2024-3400
g = Fig(1100, 420, "When the firewall is the door: CVE-2024-3400 in PAN-OS GlobalProtect",
        "An unauthenticated request to the GlobalProtect feature leads to arbitrary file creation, then OS command injection, then "
        "code execution as root on the firewall, and from there a pivot into the protected internal network. Rated CVSS 10.0 and "
        "exploited as a zero-day from late March 2024 in Operation MidnightEclipse.")
steps = [("attacker", "Unauthenticated\nrequest to GlobalProtect"), ("document", "Arbitrary file\ncreation"), ("code", "OS command\ninjection"),
         ("firewall", "Root code execution\non the firewall"), ("nodes", "Pivot into the\ninternal network")]
for i, (ic, lab) in enumerate(steps):
    x = 110 + i * 220; col = RED if i >= 3 else ORANGE
    g.circle(x, 170, 62, "#ffffff", col, 3, step=i + 1); g.icon(ic, x, 166, 76, step=i + 1)
    g.text(x, 262, lab, 14, INK, "bold", step=i + 1); g.badge(i + 1, x - 52, 118, step=i + 1, color=col)
    if i < 4: g.arrow([(x + 66, 170), (x + 154, 170)], None, col, step=i + 2, width=3)
g.icon("bug", 770, 120, 30, step=4)
g.rect(40, 320, 1020, 76, "#e8f5e9", GREEN, 1.6, rx=8, step=6); g.icon("shield", 76, 358, 40, step=6); g.badge(6, 40, 320, step=6, color=GREEN)
g.text(108, 352, "Lessons: treat edge appliances as targets, patch within days, limit what root on the edge can reach,", 14, GREEN, "bold", "start", step=6)
g.text(108, 374, "and monitor for the post-exploitation pivot.", 14, GREEN, "bold", "start", step=6)
g.save(OUT + "ch11_globalprotect")

# NAT
n = Fig(1100, 540, "NAT rewrites addresses; the protection people credit to it comes from filtering",
        "Internal hosts 192.168.1.10 and 192.168.1.20 send traffic out. The NAT router rewrites each to the one public address "
        "203.0.113.5 with a distinct port and records the mapping. Replies match a mapping and are translated back. An unsolicited "
        "inbound packet has no mapping and is dropped, which is filtering state, not translation. A static mapping of all ports to "
        "one host leaves that host as exposed as with no NAT at all.")
n.zone(20, 60, 330, 330, "Inside: 192.168.1.0/24", BLUE, "#eef5fc")
n.icon("desktop", 110, 160, 70, "192.168.1.10", step=1, label_size=13); n.icon("laptop", 110, 290, 70, "192.168.1.20", step=1, label_size=13)
n.icon("router", 420, 225, 90, "NAT router", "203.0.113.5", step=1)
n.icon("cloud", 800, 225, 170, step=1); n.icon("server", 980, 225, 70, "Web server", step=1)
n.arrow([(150, 160), (380, 210)], None, BLUE, step=2, width=2.2); n.arrow([(150, 290), (380, 240)], None, BLUE, step=2, width=2.2)
n.arrow([(470, 215), (940, 215)], "from 203.0.113.5:40001 and :40002", BLUE, step=2, size=12, width=2.6, label_at=.3, label_dy=-36)
n.rect(380, 56, 330, 90, "#1f2933", "#1f2933", 1, rx=8, step=3)
n.text(396, 80, "inside          ->  outside", 13, "#8fd16a", "bold", "start", step=3)
n.text(396, 102, "192.168.1.10:52100 -> 203.0.113.5:40001", 13, "#e4e7eb", anchor="start", step=3)
n.text(396, 124, "192.168.1.20:52200 -> 203.0.113.5:40002", 13, "#e4e7eb", anchor="start", step=3); n.badge(3, 380, 56, step=3)
n.arrow([(940, 240), (470, 240)], "reply matches a mapping: forwarded", GREEN, step=4, size=12, width=2.6, label_at=.72, label_dy=20); n.badge(4, 900, 260, step=4, color=GREEN)
n.badge(2, 460, 180, step=2)
n.icon("attacker", 980, 380, 64, "unsolicited", step=5, label_size=12)
n.arrow([(944, 372), (490, 296)], None, RED, step=5, width=2.2, dash=True); n.icon("cross", 516, 300, 26, step=5)
n.text(700, 372, "no mapping: dropped (filtering state)", 13, RED, "bold", step=5); n.badge(5, 940, 330, step=5, color=RED)
n.rect(40, 430, 1020, 86, "#fff8e1", "#d9a400", 1.6, rx=8, step=6); n.icon("warning", 76, 472, 36, step=6); n.badge(6, 40, 430, step=6, color=ORANGE)
n.text(108, 464, "RFC 4864: translation alone is not security. A static NAT of all ports to one host leaves it fully exposed;", 13, INK, "bold", "start", step=6)
n.text(108, 486, "the real protection is a stateful filter, which a firewall provides deliberately and logs.", 13, INK, "bold", "start", step=6)
n.save(OUT + "ch11_nat")

# VLAN hopping
v = Fig(1100, 560, "Two ways out of a VLAN: switch spoofing and double tagging",
        "Left: with Dynamic Trunking Protocol, an attacker's port set to dynamic desirable or auto agrees to become a trunk, and every "
        "permitted VLAN arrives at the attacker tagged and readable. Right: an attacker in the native VLAN 1 sends a frame with an "
        "outer tag for VLAN 1 and an inner tag for VLAN 140; switch 1 strips the outer tag as native and forwards it on the trunk; "
        "switch 2 reads VLAN 140 and delivers it. Double tagging is one-way. Fixes: switchport nonegotiate, an unused native VLAN, "
        "an allowed list, and tagging the native VLAN.")
v.zone(20, 60, 500, 340, "", RED, "#fdf2f1", step=1); v.badge(1, 42, 78, step=1, color=RED)
v.text(62, 83, "Switch spoofing (DTP)", 14, RED, "bold", "start", step=1)
v.icon("attacker", 100, 260, 76, "Attacker", step=1); v.icon("switch", 330, 260, 100, "Switch", "port: dynamic desirable", step=1)
v.arrow([(140, 245), (280, 245)], "DTP: let's trunk", RED, step=2, size=12, width=2.4); v.badge(2, 150, 222, step=2, color=RED)
for k, (vl, col) in enumerate([("VLAN 100", "#2471a3"), ("VLAN 110", "#16a085"), ("VLAN 140", "#8e44ad")]):
    v.arrow([(280, 285 + k * 18), (140, 285 + k * 18)], None, col, step=3, width=2.4); v.text(210, 282 + k * 18, vl, 11, col, "bold", step=3)
v.text(210, 370, "every allowed VLAN arrives, tagged", 13, RED, "bold", step=3); v.badge(3, 380, 360, step=3, color=RED)
v.zone(540, 60, 540, 340, "", RED, "#fdf2f1", step=4)
v.text(582, 83, "Double tagging (one-way)", 14, RED, "bold", "start", step=4)
v.icon("attacker", 600, 170, 64, "VLAN 1 = native", step=4, label_size=12)
v.icon("switch", 760, 170, 84, "Switch 1", step=4); v.icon("switch", 1000, 170, 84, "Switch 2", step=4)
v.rect(626, 100, 90, 24, "#fff3e0", ORANGE, 1.4, rx=4, step=4); v.text(671, 116, "1 | 140 | data", 11, INK, "bold", step=4)
v.arrow([(636, 150), (712, 150)], None, RED, step=4, width=2.2); v.badge(4, 562, 78, step=4, color=RED)
v.arrow([(806, 170), (954, 170)], "trunk, outer tag stripped", RED, step=5, size=12, width=2.4, label_dy=-26)
v.rect(835, 178, 90, 24, "#fff3e0", ORANGE, 1.4, rx=4, step=5); v.text(880, 194, "140 | data", 11, INK, "bold", step=5); v.badge(5, 880, 230, step=5, color=RED)
v.icon("server", 1000, 320, 60, "VLAN 140 host", step=6, label_size=12); v.arrow([(1000, 238), (1000, 286)], None, RED, step=6, width=2.4)
v.badge(6, 960, 300, step=6, color=RED); v.text(760, 330, "delivered into VLAN 140;", 13, RED, "bold", step=6); v.text(760, 348, "no reply comes back", 13, RED, "bold", step=6)
v.rect(20, 420, 1060, 120, "#1f2933", "#1f2933", 1, rx=8, step=7); v.badge(7, 20, 420, step=7, color=GREEN)
for k, (cmd, why) in enumerate([("switchport mode access + switchport nonegotiate", "closes switch spoofing"),
                                ("switchport trunk native vlan 999", "no attacker sits in the native VLAN"),
                                ("switchport trunk allowed vlan 100,110,120,130,140", "prunes what a hop could reach"),
                                ("vlan dot1q tag native", "nothing on a trunk is untagged")]):
    v.text(40, 450 + k * 24, cmd, 13, "#8fd16a", "bold", "start", step=7); v.text(560, 450 + k * 24, "! " + why, 13, "#e4e7eb", anchor="start", step=7)
v.save(OUT + "ch11_vlan_hopping")
print("ok")
