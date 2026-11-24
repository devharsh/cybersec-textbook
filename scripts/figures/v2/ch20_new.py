import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# Redraw: Modbus frame with the devices that send it
m = Fig(1100, 500, "A complete Modbus TCP request: write coil 10 to ON, sent to TCP port 502",
        "Top: an HMI and an attacker on the same segment can both send the same request to the PLC on TCP port 502, and the PLC cannot "
        "tell them apart. Below, the twelve bytes: MBAP header of 7 bytes, transaction ID 00 01, protocol ID 00 00, length 00 06, unit "
        "ID 01; then the protocol data unit of 5 bytes, function code 05 Write Single Coil, output address 00 0A for coil 10, output "
        "value FF 00 for ON. No field carries identity, integrity, or freshness.")
m.icon("hmi", 120, 120, 70, "Operator HMI", step=1); m.icon("attacker", 120, 230, 60, "Anyone on the segment", step=4, label_size=12)
m.icon("plc", 900, 160, 80, "PLC", "TCP port 502", step=1); m.icon("gear", 1010, 160, 50, "coil 10: ON", step=3, label_size=12)
m.arrow([(160, 120), (850, 150)], "write coil 10 = ON", BLUE, step=1, size=13, width=2.6); m.arrow([(160, 230), (850, 175)], "the same 12 bytes", RED, step=4, size=13, width=2.6, dash=True, label_dy=24)
m.badge(1, 60, 70, step=1); m.badge(4, 60, 190, step=4, color=RED); m.arrow([(944, 160), (980, 160)], None, GREEN, step=3, width=2.2); m.badge(3, 1050, 110, step=3, color=GREEN)
fields = [("00 01", "Transaction ID", 2), ("00 00", "Protocol ID", 2), ("00 06", "Length", 2), ("01", "Unit ID", 1),
          ("05", "Function code:\nWrite Single Coil", 1), ("00 0A", "Output address:\ncoil 10", 2), ("FF 00", "Output value:\nON", 2)]
x = 40; W = 1020 / 12
for i, (b, lab, n) in enumerate(fields):
    w = n * W; col = "#dbe7f5" if i < 4 else "#fcf3cf"
    m.rect(x, 300, w - 4, 54, col, "#2b3138", 1.6, rx=4, step=2); m.text(x + (w - 4) / 2, 335, b, 20, INK, "bold", step=2)
    m.text(x + (w - 4) / 2, 374, lab, 12, INK, step=2); x += w
m.text(40 + 7 * W / 2, 290, "MBAP header, 7 bytes", 13, BLUE, "bold", step=2); m.text(40 + 7 * W + 5 * W / 2, 290, "Protocol data unit, 5 bytes", 13, "#8a6d1a", "bold", step=2)
m.badge(2, 40, 300, step=2)
m.rect(40, 430, 1020, 44, "#fdecea", RED, 1.6, rx=8, step=5); m.badge(5, 40, 430, step=5, color=RED)
m.text(550, 458, "No field carries identity, integrity, or freshness. Any host on the segment can build it.", 15, RED, "bold", step=5)
m.save(OUT + "ch20_modbus_frame_v2")

# Redraw: layers of protection
l = Fig(1100, 560, "Layers of protection around a process",
        "Nested bands from the inside out: the process, a tank; the basic process control system loop; alarm plus operator response; "
        "the safety instrumented system; mechanical relief such as a rupture disc or relief valve; and physical containment such as a "
        "dike, bund, or flare. Each layer is credited only if it is independent of the layers around it. The SIS is the last "
        "programmable layer, and the last one an attacker can reach over a network.")
lay = [("Physical containment: dike, bund, flare", "#efe1d1", "factory"), ("Mechanical relief: rupture disc, relief valve", "#e6ddd3", "gear"),
       ("Safety instrumented system (SIS)", "#f5d5c4", "shield"), ("Alarm plus operator response", "#d6e4f0", "hmi"),
       ("Basic process control system loop", "#c9dff0", "plc"), ("The process", "#b5d6ec", "database")]
for i, (name, fill, ic) in enumerate(lay):
    pad = i * 42; st = 6 - i
    l.rect(40 + pad, 60 + pad * 0.82, 640 - 2 * pad, 460 - 2 * pad * 0.82, fill, "#2b3138", 2.4 if i == 2 else 1.4, rx=14, step=st)
    l.icon(ic, 72 + pad, 86 + pad * 0.82, 26, step=st); l.text(92 + pad, 92 + pad * 0.82, name, 14, RED if i == 2 else INK, "bold", "start", step=st)
    l.badge(st, 660 - pad, 78 + pad * 0.82, step=st, color=RED if i == 2 else BLUE)
l.icon("attacker", 900, 230, 70, step=7); l.arrow([(860, 240), (600, 200)], None, RED, step=7, width=2.4, dash=True)
l.text(780, 300, "The SIS is the last programmable layer,", 14, RED, "bold", "start", step=7); l.text(780, 320, "and the last one an attacker", 14, RED, "bold", "start", step=7)
l.text(780, 340, "can reach over a network.", 14, RED, "bold", "start", step=7); l.badge(7, 940, 180, step=7, color=RED)
l.text(780, 400, "The outer mechanical and physical layers", 13, INK, anchor="start", step=7); l.text(780, 418, "need no electricity and no logic.", 13, INK, anchor="start", step=7)
l.text(550, 548, "Each layer is credited only if it is independent of the layers around it (IEC 61511-1 clause 11.2.4 for the control system and the SIS).", 12, MUTED, italic=True, step=8)
l.save(OUT + "ch20_protection_layers_v2")

# Redraw: zones and conduits
z = Fig(1100, 600, "A water treatment plant partitioned into IEC 62443 zones and conduits",
        "Five zones: the enterprise zone with resource planning and the office network at SL-T 1; the industrial DMZ with a historian "
        "replica and remote access broker at SL-T 2; the plant control zone with the SCADA server, consoles, and controllers inside the "
        "fence at SL-T 3; the safety zone with chlorine interlocks, physically separate, at SL-T 3; and the remote station zone with "
        "three pump stations over cellular links at SL-T 3. Conduits: a brokered session to a jump host only, from enterprise to DMZ; "
        "historian data outbound only, from plant control to DMZ; an engineering path only with procedure and key switch, between "
        "safety and plant control; and one polling protocol, one port, one direction, from remote stations to plant control.")
zz = {"ent": (40, 70, "Enterprise zone", "Resource planning,\noffice network", "SL-T 1", "#f2d7d5", "desktop"),
      "dmz": (390, 70, "Industrial DMZ", "Historian replica,\nremote access broker", "SL-T 2", "#fcf3cf", "server"),
      "ctl": (390, 330, "Plant control zone", "SCADA server, consoles,\ncontrollers inside the fence", "SL-T 3", "#d4e6f1", "hmi"),
      "saf": (40, 330, "Safety zone", "Chlorine interlocks,\nphysically separate", "SL-T 3", "#f5d5c4", "shield"),
      "rem": (740, 330, "Remote station zone", "Three pump stations\nover cellular links", "SL-T 3", "#e5ebf2", "tower")}
for k2, (key, (x, y, name, sub, sl, fill, ic)) in enumerate(zz.items()):
    z.rect(x, y, 300, 170, fill, "#2b3138", 1.8, rx=10, step=1 + k2); z.icon(ic, x + 50, y + 85, 60, step=1 + k2)
    z.text(x + 185, y + 36, name, 16, INK, "bold", step=1 + k2); z.text(x + 185, y + 68, sub, 12, INK, step=1 + k2); z.text(x + 185, y + 140, sl, 14, RED, "bold", step=1 + k2)
    z.badge(1 + k2, x + 282, y + 18, step=1 + k2)
B = "#1f4e9c"
z.arrow([(342, 155), (388, 155)], None, B, step=6, width=2.6); z.raw('<line x1="365" y1="165" x2="365" y2="252" stroke="#1f4e9c" stroke-width="1"/>', step=6)
z.text(365, 268, "brokered session", 12, B, "bold", step=6); z.text(365, 284, "to jump host only", 12, B, "bold", step=6)
z.arrow([(540, 328), (540, 242)], None, B, step=7, width=2.6); z.text(550, 280, "historian data,", 12, B, "bold", "start", step=7); z.text(550, 296, "outbound only", 12, B, "bold", "start", step=7)
z.arrow([(342, 415), (388, 415)], None, RED, step=8, width=2.6, dash=True, both=True); z.text(240, 530, "engineering path only,", 12, RED, "bold", step=8); z.text(240, 546, "procedure and key switch", 12, RED, "bold", step=8)
z.raw('<line x1="365" y1="420" x2="300" y2="515" stroke="#c0392b" stroke-width="1"/>', step=8)
z.arrow([(738, 415), (692, 415)], None, B, step=9, width=2.6); z.text(830, 530, "one polling protocol,", 12, B, "bold", step=9); z.text(830, 546, "one port, one direction", 12, B, "bold", step=9)
z.raw('<line x1="715" y1="420" x2="790" y2="515" stroke="#1f4e9c" stroke-width="1"/>', step=9)
for n_, (x, y) in [(6, (365, 130)), (7, (520, 285)), (8, (365, 440)), (9, (715, 440))]: z.badge(n_, x, y, step=n_, color=RED if n_ == 8 else B)
z.text(550, 588, "Five zones, four conduits. Every arrow is a sentence you can test; segment the network is not.", 13, MUTED, italic=True, step=10)
z.save(OUT + "ch20_zones_conduits_v2")
print("ok")
