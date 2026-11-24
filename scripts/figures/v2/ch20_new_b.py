import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# Purdue model
p = Fig(1100, 620, "The Purdue model: distance from the thing that moves",
        "Levels from the bottom: Level 0 field devices such as sensors, actuators, motors, and valves; Level 1 control with PLCs, RTUs, "
        "and safety systems; Level 2 supervisory with SCADA servers, DCS, and HMIs; Level 3 manufacturing operations with historians, "
        "MES, and engineering workstations; Level 3.5 the industrial DMZ with data diodes, jump servers, and protocol converters; and "
        "Level 4 business logistics with ERP, email, and the internet. A failure at the bottom can injure somebody; at the top it is "
        "expensive. Cellular modems and vendor remote access can bypass every level.")
lv = [("4", "Business logistics", "ERP, email, internet", ["desktop", "envelope", "cloud"], "#d6e9f8"),
      ("3.5", "Industrial DMZ", "data diodes, jump servers, protocol converters", ["firewall", "server"], "#fcf3cf"),
      ("3", "Manufacturing operations", "historian, MES, engineering workstations", ["database", "desktop"], "#e8f5e9"),
      ("2", "Supervisory", "SCADA servers, DCS, HMIs", ["server", "hmi"], "#e8f5e9"),
      ("1", "Control", "PLCs, RTUs, safety systems", ["plc", "shield"], "#fae5d3"),
      ("0", "Field", "sensors, actuators, motors, valves", ["gear", "factory"], "#f5d5c4")]
for i, (n_, name, sub, ics, fill) in enumerate(lv):
    y = 60 + i * 86; st = 6 - i
    p.rect(40, y, 820, 76, fill, "#5b6570", 1.6, rx=8, step=st)
    p.circle(84, y + 38, 26, "#2b3138", "#2b3138", 1, step=st); p.text(84, y + 44, n_, 15 if n_ != "3.5" else 13, "#ffffff", "bold", step=st)
    p.text(126, y + 32, name, 16, INK, "bold", "start", step=st); p.text(126, y + 54, sub, 13, INK, anchor="start", step=st)
    for k, ic in enumerate(ics): p.icon(ic, 660 + k * 70, y + 38, 50, step=st)
    p.badge(st, 846, y + 16, step=st)
p.raw('<line x1="30" y1="228" x2="870" y2="228" stroke="#c0392b" stroke-width="2.4" stroke-dasharray="9 5"/>', step=6); p.text(866, 222, "IT/OT boundary", 12, RED, "bold", "end", step=6)
p.arrow([(900, 560), (900, 80)], None, MUTED, step=7, width=2.4)
p.text(920, 110, "failure is", 12, MUTED, "bold", "start", step=7); p.text(920, 126, "expensive", 12, MUTED, "bold", "start", step=7)
p.text(920, 520, "failure can", 12, RED, "bold", "start", step=7); p.text(920, 536, "injure people", 12, RED, "bold", "start", step=7)
p.icon("tower", 990, 330, 50, step=8); p.arrow([(990, 302), (868, 98)], None, RED, step=8, dash=True, width=2); p.arrow([(990, 358), (868, 470)], None, RED, step=8, dash=True, width=2)
p.text(1000, 390, "cellular modem or", 11, RED, "bold", step=8); p.text(1000, 404, "vendor access:", 11, RED, "bold", step=8); p.text(1000, 418, "skips every level", 11, RED, "bold", step=8)
p.badge(8, 1040, 300, step=8, color=RED)
p.save(OUT + "ch20_purdue")

# ICS components and HMI deception
c = Fig(1100, 520, "ICS components, and how a compromised HMI deceives the operator",
        "Field sensors and actuators connect to PLCs, which scan inputs, execute logic, and write outputs in milliseconds, often with no "
        "authentication. RTUs at remote sites report over a wide-area network to the SCADA server, and operators watch the HMI. A "
        "compromised HMI can show normal values while the process runs out of bounds, which is what Stuxnet did with centrifuge "
        "speeds.")
c.icon("gear", 90, 400, 56, "Motor, valve", step=1, label_size=12); c.icon("chip", 210, 400, 50, "Sensor", step=1, label_size=12)
c.icon("plc", 160, 260, 70, "PLC", "scan, logic, outputs in ms", step=2); c.arrow([(110, 368), (140, 334)], None, INK, step=2, both=True); c.arrow([(205, 372), (180, 334)], None, INK, step=2, both=True)
c.icon("tower", 450, 400, 56, "Remote site", step=3, label_size=12); c.icon("plc", 450, 260, 60, "RTU", step=3)
c.icon("cloud", 600, 300, 100, "WAN, cellular, satellite", step=3, label_size=12); c.arrow([(480, 260), (560, 290)], None, INK, step=3)
c.icon("server", 760, 180, 70, "SCADA server", step=4); c.arrow([(200, 230), (720, 180)], None, INK, step=4); c.arrow([(640, 290), (722, 200)], None, INK, step=4)
c.icon("hmi", 960, 180, 80, "HMI", "operator's view", step=5); c.arrow([(800, 180), (912, 180)], None, INK, step=5)
c.icon("user", 960, 320, 60, "Operator", step=5)
for n_, (x, y) in enumerate([(50, 360), (110, 210), (410, 210), (720, 130), (920, 120)], 1): c.badge(n_, x, y, step=n_)
c.rect(700, 390, 380, 110, "#fdecea", RED, 1.6, rx=8, step=6); c.badge(6, 700, 390, step=6, color=RED)
c.text(716, 416, "Compromised HMI:", 14, RED, "bold", "start", step=6)
c.text(716, 440, "shows: speed normal", 13, GREEN, "bold", "start", step=6); c.text(716, 462, "reality: spinning at damaging speeds", 13, RED, "bold", "start", step=6)
c.text(716, 484, "as Stuxnet did with centrifuges", 12, INK, anchor="start", step=6, italic=True)
c.save(OUT + "ch20_ics_components")

# Stuxnet
s = Fig(1100, 460, "Stuxnet: sabotage that reported normal operation",
        "Delivered across an air gap by insider or supply-chain means rather than over the internet, Stuxnet reached the Siemens "
        "S7-315 PLCs controlling uranium enrichment centrifuges. It commanded the centrifuges to spin at damaging speeds while the "
        "SCADA system was shown normal readings. It was the first publicly documented cyberweapon designed to cause physical damage.")
s.icon("usb", 100, 170, 70, "Insider or", "supply-chain delivery", step=1); s.icon("bug", 130, 130, 26, step=1)
s.raw('<line x1="220" y1="70" x2="220" y2="300" stroke="#52606d" stroke-width="3" stroke-dasharray="10 6"/>', step=1); s.text(220, 320, "air gap", 13, MUTED, "bold", step=1)
s.icon("desktop", 340, 170, 70, "Plant network", "air-gapped", step=2); s.arrow([(140, 170), (300, 170)], "crosses it", RED, step=2, size=12, width=2.4)
s.icon("plc", 560, 170, 80, "Siemens S7-315", "PLC", step=3); s.arrow([(380, 170), (514, 170)], None, RED, step=3, width=2.4)
for k in range(4): s.icon("gear", 760 + k * 70, 120, 50, step=4); s.icon("warning", 780 + k * 70, 96, 18, step=4)
s.text(865, 175, "centrifuges at damaging speeds", 13, RED, "bold", step=4); s.arrow([(606, 160), (730, 130)], None, RED, step=4, width=2.4)
s.icon("hmi", 865, 290, 70, step=5); s.text(865, 352, "SCADA shows: normal", 14, GREEN, "bold", step=5); s.arrow([(606, 190), (826, 280)], "reports normal readings", ORANGE, step=5, size=12, width=2.2, dash=True)
for n_, x in enumerate([60, 300, 520, 740, 820], 1): s.badge(n_, x, 110 if n_ < 4 else (80 if n_ == 4 else 250), step=n_, color=RED if n_ > 2 else BLUE)
s.text(550, 420, "Lesson: air gaps are not absolute, and the operator's screen is part of the attack surface.", 14, INK, "bold", step=6)
s.save(OUT + "ch20_stuxnet")

# Active scanning versus passive monitoring
a = Fig(1100, 520, "Active scanning can stop a plant; passive monitoring listens instead",
        "Left: a scanner sends unsolicited probes to controllers whose fixed loops and untested stacks were never sized for them; a "
        "controller faults, a ping sweep moved a standby robotic arm 180 degrees, and another destroyed fifty thousand dollars of "
        "wafers. Right: a tap copies existing traffic to a passive sensor, which builds an inventory from protocol payloads and flags a "
        "write from a host that only ever read and any device never seen before. Limits: it cannot see silent devices or read "
        "encrypted traffic, and it can take days.")
a.zone(20, 60, 520, 380, "Active scanning", RED, "#fdf2f1", step=1); a.badge(1, 522, 76, step=1, color=RED)
a.icon("laptop", 90, 200, 70, "Scanner", step=1)
for k, y in enumerate([130, 230, 330]):
    a.icon("plc", 400, y, 56, step=1); a.arrow([(130, 200), (366, y)], None, RED, step=1, width=1.8)
a.icon("warning", 440, 230, 28, step=2); a.icon("cross", 440, 130, 24, step=2)
a.text(270, 398, "stack faults, loop overruns, or a probe", 12, RED, "bold", step=2); a.text(270, 414, "is a real command the device obeys", 12, RED, "bold", step=2)
a.badge(2, 470, 200, step=2, color=RED)
a.zone(560, 60, 520, 380, "Passive monitoring", GREEN, "#eef8ef", step=3); a.badge(3, 1062, 76, step=3, color=GREEN)
a.icon("hmi", 640, 150, 56, step=3); a.icon("plc", 900, 150, 56, step=3); a.arrow([(672, 150), (868, 150)], None, INK, step=3, both=True)
a.rect(760, 138, 26, 24, "#f5b041", "#8a6d1a", 1.2, rx=3, step=3); a.text(773, 128, "tap", 11, ORANGE, "bold", step=3)
a.icon("eye", 773, 270, 56, "Passive sensor", "adds nothing to the wire", step=4); a.arrow([(773, 164), (773, 236)], None, ORANGE, step=4, dash=True)
a.badge(4, 720, 250, step=4, color=GREEN)
a.text(600, 380, "+ inventory from payloads: model, firmware", 12, GREEN, "bold", "start", step=5)
a.text(600, 398, "+ alerts: a write from a read-only host, a new device", 12, GREEN, "bold", "start", step=5)
a.text(600, 416, "- cannot see silent devices or encrypted traffic", 12, ORANGE, "bold", "start", step=5); a.badge(5, 580, 360, step=5, color=GREEN)
a.text(550, 476, "NIST SP 800-82r3 records a ping sweep that swung a standby robotic arm 180 degrees, and one that destroyed", 13, MUTED, italic=True, step=6)
a.text(550, 496, "fifty thousand dollars of wafers. Prefer a tap to a mirror port, which drops frames under load.", 13, MUTED, italic=True, step=6)
a.save(OUT + "ch20_passive_active")
print("ok")
