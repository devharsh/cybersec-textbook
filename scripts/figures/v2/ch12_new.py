import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# 1. IDS out of band, IPS inline, HIDS on hosts
d = Fig(1100, 520, "Where detection sits: an IDS watches a copy, an IPS sits in the path, a HIDS lives on the host",
        "Traffic from the internet passes the firewall and an inline IPS, which drops or resets packets that match a rule and forwards "
        "clean ones, at the cost of latency and a possible failure point. A tap or SPAN port on the core switch gives a passive IDS a "
        "copy of the traffic; it can only alert. Host-based agents on servers watch the host itself. Alerts from all of them go to the "
        "SIEM and the analyst.")
d.icon("cloud", 80, 200, 120, "Internet", step=1)
d.icon("firewall", 240, 200, 80, "Firewall", step=1)
d.icon("shield", 410, 200, 74, "Inline IPS", "drop, reset, or forward", step=2)
d.icon("switch", 610, 200, 100, "Core switch", step=3)
for k, y in enumerate([110, 200, 290]): d.icon("server", 880, y, 56, step=3); d.arrow([(664, 200), (848, y)], None, INK, step=3, width=1.8)
d.arrow([(140, 200), (198, 200)], None, INK, step=1, width=2.6); d.arrow([(282, 200), (370, 200)], None, INK, step=2, width=2.6)
d.arrow([(450, 200), (556, 200)], None, GREEN, step=2, width=2.6); d.icon("cross", 410, 140, 26, step=2); d.text(410, 118, "matches a signature or behavior rule: dropped", 12, RED, "bold", step=2)
d.badge(1, 30, 120, step=1); d.badge(2, 360, 140, step=2)
d.icon("eye", 610, 380, 60, "Passive IDS", "copy via SPAN or tap: alert only", step=4)
d.arrow([(610, 274), (610, 346)], "copy", MUTED, step=4, dash=True, size=12, label_anchor="start", label_dy=4); d.badge(4, 560, 360, step=4)
d.icon("memory", 960, 110, 30, step=5); d.icon("memory", 960, 200, 30, step=5); d.icon("memory", 960, 290, 30, step=5)
d.text(1000, 350, "HIDS agents", 13, PURPLE, "bold", step=5); d.badge(5, 990, 80, step=5, color=PURPLE)
d.icon("logbook", 900, 450, 50, "SIEM / analyst", step=6, label_size=13)
d.arrow([(450, 230), (860, 440)], None, ORANGE, step=6, dash=True, width=1.8); d.arrow([(650, 390), (860, 446)], None, ORANGE, step=6, dash=True, width=1.8)
d.arrow([(980, 320), (920, 420)], None, ORANGE, step=6, dash=True, width=1.8); d.badge(6, 830, 470, step=6, color=ORANGE)
d.text(220, 470, "IDS: cheap when wrong, but someone must act.", 13, INK, "bold", step=6)
d.text(220, 490, "IPS: acts alone, so a false positive is an outage.", 13, INK, "bold", step=6)
d.save(OUT + "ch12_ids_ips")

# 2. SIEM pipeline and a correlation rule
s = Fig(1100, 560, "A SIEM: collect, normalize, store, correlate",
        "Logs flow from firewalls, endpoints, servers, applications, cloud APIs, and authentication systems into the SIEM, which "
        "normalizes them into a common schema, stores them, and correlates across sources. Example rule: a failed login to account A, "
        "a successful login to A five minutes later from a different IP, access to a sensitive share, then a transfer to an external "
        "IP. No single event is alarming; the sequence raises one alert.")
src = [("firewall", "Firewalls"), ("desktop", "Endpoints"), ("server", "Servers"), ("code", "Applications"), ("cloud", "Cloud APIs"), ("idcard", "Authentication")]
for k, (ic, lab) in enumerate(src):
    y = 70 + k * 62; s.icon(ic, 70, y, 44, step=1); s.text(100, y + 5, lab, 13, INK, "bold", "start", step=1)
    s.arrow([(200, y), (290, 230)], None, "#9aa5b1", step=1, width=1.6)
s.badge(1, 20, 50, step=1)
stg = [("Collect", "gear"), ("Normalize", "checklist"), ("Store", "database"), ("Correlate", "nodes")]
for i, (lab, ic) in enumerate(stg):
    x = 320 + i * 160
    s.card(x, 160, 130, 140, ic, lab, None, BLUE, step=2 + i, icon_size=60, title_size=15); s.badge(2 + i, x + 12, 172, step=2 + i)
    if i < 3: s.arrow([(x + 132, 230), (x + 158, 230)], None, BLUE, step=3 + i, width=2.6)
s.icon("warning", 1000, 200, 60, step=6); s.icon("user", 1000, 290, 54, "Analyst", step=6, label_size=13)
s.arrow([(932, 230), (966, 210)], None, RED, step=6, width=2.6); s.badge(6, 1040, 160, step=6, color=RED)
ev = [("08:01", "failed login, account A", "idcard"), ("08:06", "login to A succeeds from a new IP", "key"), ("08:09", "A opens the sensitive share", "document"),
      ("08:15", "upload to an external IP", "cloud")]
s.text(40, 430, "One correlation rule, four ordinary events:", 14, INK, "bold", "start", step=7); s.badge(7, 24, 424, step=7, color=RED)
for i, (t, lab, ic) in enumerate(ev):
    x = 40 + i * 260
    s.rect(x, 448, 240, 70, "#ffffff", "#9aa5b1", 1.4, rx=8, step=7); s.icon(ic, x + 30, 483, 36, step=7)
    s.text(x + 56, 474, t, 13, MUTED, "bold", "start", step=7); s.text(x + 56, 494, lab, 12, INK, anchor="start", step=7)
    if i < 3: s.arrow([(x + 242, 483), (x + 258, 483)], None, RED, step=7, width=2)
s.text(550, 546, "credential stuffing, then initial access, then exfiltration: the sequence is the signal", 13, RED, "bold", step=7)
s.save(OUT + "ch12_siem")

# 3. Kill chain with icons
k = Fig(1100, 440, "The cyber kill chain: break any stage, and earlier is cheaper",
        "Seven stages left to right with icons: reconnaissance, weaponization, delivery, exploitation, installation, command and "
        "control, and actions on objectives. Breaking any stage ends the attempt. Detection at reconnaissance costs little; detection "
        "at actions on objectives means loss has already happened. Real intrusions loop and skip, which is why ATT&CK is a matrix.")
st = [("Recon", "search"), ("Weaponize", "bug"), ("Deliver", "envelope"), ("Exploit", "code"), ("Install", "gear"), ("C2", "cloud"), ("Actions on\nobjectives", "database")]
for i, (lab, ic) in enumerate(st):
    x = 80 + i * 157; col = ["#1e8449", "#28b463", "#d4ac0d", "#e67e22", "#d35400", "#c0392b", "#922b21"][i]
    k.circle(x, 150, 56, "#ffffff", col, 3.4, step=i + 1); k.icon(ic, x, 146, 64, step=i + 1)
    k.text(x, 232, lab, 14, col, "bold", step=i + 1); k.badge(i + 1, x - 46, 104, step=i + 1, color=col)
    if i < 6: k.arrow([(x + 58, 150), (x + 98, 150)], None, col, step=i + 2, width=2.6)
k.raw('<defs><linearGradient id="g-cost" x1="0" x2="1"><stop offset="0" stop-color="#2e7d32"/><stop offset=".5" stop-color="#f1c40f"/><stop offset="1" stop-color="#c0392b"/></linearGradient></defs>'
      '<rect x="40" y="300" width="1020" height="22" rx="11" fill="url(#g-cost)"/>', step=8)
k.text(50, 346, "detect here: cheap, nothing lost yet", 13, GREEN, "bold", "start", step=8)
k.text(1050, 346, "detect here: costly, data already gone", 13, RED, "bold", "end", step=8); k.badge(8, 550, 311, step=8)
k.icon("shield", 80, 400, 34, step=9); k.badge(9, 50, 388, step=9, color=GREEN)
k.text(110, 406, "Defenses at every stage, mapped to ATT&CK techniques, because real intrusions loop back and skip stages.", 14, INK, "bold", "start", step=9)
k.save(OUT + "ch12_kill_chain")

# 4. Modern SOC: EDR, XDR, SOAR, detection engineering
o = Fig(1100, 560, "A modern SOC: EDR on the hosts, XDR across layers, SOAR for the routine, detections as code",
        "EDR agents on endpoints record processes, files, registry, and network activity and can isolate a machine. XDR correlates "
        "endpoint, network, identity, email, and cloud signals into one incident. SOAR playbooks enrich indicators, open tickets, and "
        "take pre-approved containment steps. Detection engineers write rules as code, often in Sigma, map them to ATT&CK, and tune "
        "them, which feeds back into every layer.")
sig = [("desktop", "Endpoint (EDR)"), ("router", "Network"), ("idcard", "Identity"), ("envelope", "Email"), ("cloud", "Cloud")]
for i, (ic, lab) in enumerate(sig):
    x = 110 + i * 210
    o.icon(ic, x, 110, 60, lab, step=1, label_size=13); o.arrow([(x, 162), (550, 238)], None, "#9aa5b1", step=2, width=1.6)
o.icon("memory", 130, 80, 26, step=1); o.badge(1, 40, 70, step=1)
o.card(400, 240, 300, 110, "nodes", "XDR: one incident, not five alerts", None, PURPLE, step=2, icon_size=50, title_size=14); o.badge(2, 410, 250, step=2, color=PURPLE)
o.arrow([(550, 352), (550, 392)], None, PURPLE, step=3, width=2.6)
o.card(380, 394, 340, 130, "gear", "SOAR playbook", "enrich indicators, open a ticket,\nisolate the host if pre-approved", ORANGE, step=3, icon_size=46, title_size=15)
o.badge(3, 390, 404, step=3, color=ORANGE)
o.icon("user", 880, 450, 60, "Analyst", "decides the rest", step=4, label_size=13); o.arrow([(722, 450), (842, 450)], None, ORANGE, step=4, width=2.4)
o.badge(4, 800, 420, step=4, color=ORANGE)
o.rect(30, 394, 320, 130, "#1f2933", "#1f2933", 1, rx=8, step=5); o.badge(5, 30, 394, step=5, color=GREEN)
for i, line in enumerate(["title: Encoded PowerShell", "detection:", "  CommandLine|contains: '-enc'", "tags: attack.t1059.001"]):
    o.text(46, 420 + i * 22, line, 12, "#8fd16a" if i == 0 else "#e4e7eb", anchor="start", step=5)
o.text(190, 546, "detection engineering: Sigma rules as code", 13, GREEN, "bold", step=5)
o.arrow([(190, 392), (190, 260), (395, 260)], "tuned, mapped to ATT&CK", GREEN, step=6, dash=True, size=12, width=2, label_at=.75, label_dy=-8)
o.badge(6, 200, 330, step=6, color=GREEN)
o.save(OUT + "ch12_soc_stack")

# 5. Network security monitoring
n = Fig(1100, 560, "Network security monitoring: three kinds of record from one tap",
        "A network tap on the link between the edge router and the core switch feeds an NSM sensor running Zeek. It produces full "
        "packet capture, perfect but expensive and kept briefly; session and flow records such as NetFlow, IPFIX, and Zeek connection "
        "logs, which scale and reveal who talked to whom; and protocol metadata for DNS, HTTP, TLS, and files. Flow analysis shows "
        "beaconing as connections at a fixed interval and exfiltration as a sudden large upload.")
n.icon("router", 160, 130, 80, "Edge router"); n.icon("switch", 560, 130, 96, "Core switch")
n.arrow([(204, 130), (508, 130)], None, INK, width=2.6, both=True)
n.rect(345, 116, 30, 28, "#f5b041", "#8a6d1a", 1.4, rx=4, step=1); n.text(360, 100, "tap", 13, ORANGE, "bold", step=1); n.badge(1, 395, 100, step=1, color=ORANGE)
n.icon("server", 360, 300, 70, "NSM sensor", "Zeek, tcpdump", step=2); n.arrow([(360, 146), (360, 262)], "copy", ORANGE, step=2, size=12, label_anchor="start", label_dy=4)
n.badge(2, 310, 280, step=2)
recs = [("Full packet capture", "every byte; short retention", "memory", 720, 170), ("Session and flow", "NetFlow, IPFIX, Zeek conn", "nodes", 720, 275),
        ("Protocol metadata", "DNS, HTTP, TLS, files", "document", 720, 380)]
for i, (a, b, ic, x, y) in enumerate(recs):
    n.icon(ic, x, y, 48, step=3 + i); n.text(x + 36, y - 4, a, 15, BLUE, "bold", "start", step=3 + i); n.text(x + 36, y + 16, b, 12, INK, anchor="start", step=3 + i)
    n.arrow([(400, 300), (690, y)], None, BLUE, step=3 + i, width=1.8); n.badge(3 + i, x - 40, y - 26, step=3 + i)
X0, Y0 = 60, 490
n.raw(f'<line x1="{X0}" y1="{Y0}" x2="520" y2="{Y0}" stroke="#52606d" stroke-width="2"/>', step=6)
for i in range(9): n.raw(f'<line x1="{X0 + 20 + i * 52}" y1="{Y0 - 30}" x2="{X0 + 20 + i * 52}" y2="{Y0}" stroke="#c0392b" stroke-width="5" stroke-linecap="round"/>', step=6)
n.text(290, Y0 + 26, "beaconing: same destination, fixed interval", 13, RED, "bold", step=6); n.badge(6, X0 - 30, Y0 - 20, step=6, color=RED)
n.raw(f'<line x1="600" y1="{Y0}" x2="1060" y2="{Y0}" stroke="#52606d" stroke-width="2"/>', step=7)
for i, h in enumerate([6, 8, 5, 7, 6, 9, 70, 6, 5]):
    n.raw(f'<rect x="{620 + i * 50}" y="{Y0 - h}" width="30" height="{h}" fill="{RED if h > 50 else "#9aa5b1"}" rx="3"/>', step=7)
n.text(830, Y0 + 26, "exfiltration: a sudden large upload", 13, RED, "bold", step=7); n.badge(7, 590, Y0 - 70, step=7, color=RED)
n.save(OUT + "ch12_nsm")
print("ok")
