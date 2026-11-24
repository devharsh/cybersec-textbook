import os
import sys, math; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# Redraw: the reconnaissance funnel
f = Fig(1100, 600, "The reconnaissance funnel: from everything public to a validated target list",
        "Five layers narrowing downward. The public internet holds everything. OSINT narrows it to the target's domains, people, "
        "technology, and documents. WHOIS and the regional internet registries give the IP ranges the target owns. DNS gives hosts, "
        "mail servers, and subdomains. The result is a validated target list that feeds scanning in Chapter 8.")
lv = [("Public internet (everything)", "cloud", "#d6e9f8"), ("OSINT: domains, people, tech, docs", "search", "#aed6f1"),
      ("WHOIS and RIR: owned IP ranges", "database", "#7fb3d5"), ("DNS: hosts, mail, subdomains", "server", "#5499c7"),
      ("Validated target list", "checklist", "#2e86c1")]
top, hgt = 60, 88
for i, (lab, ic, col) in enumerate(lv):
    y = top + i * hgt; w1 = 640 - i * 115; w2 = 640 - (i + 1) * 115
    cx = 360
    f.poly([(cx - w1 / 2, y), (cx + w1 / 2, y), (cx + w2 / 2, y + hgt - 4), (cx - w2 / 2, y + hgt - 4)], col, "#ffffff", 2, step=i + 1)
    f.icon(ic, cx, y + 42, 54 if i < 4 else 48, step=i + 1)
    f.raw(f'<line x1="{cx + w1 / 2 - 10:.0f}" y1="{y + 42}" x2="720" y2="{y + 42}" stroke="#9aa5b1" stroke-width="1.4" stroke-dasharray="4 4"/>', step=i + 1)
    f.text(735, y + 48, lab, 16, INK, "bold", "start", step=i + 1); f.badge(i + 1, 708, y + 42, step=i + 1)
f.text(735, top + 4 * hgt + 70, "passive at the top, active toward the bottom", 13, MUTED, italic=True, anchor="start")
f.arrow([(380, top + 5 * hgt - 6), (520, top + 5 * hgt + 50)], None, GREEN, step=6, width=3); f.text(595, top + 5 * hgt + 56, "to scanning (Chapter 8)", 15, GREEN, "bold", "start", step=6)
f.icon("nodes", 560, top + 5 * hgt + 50, 50, step=6); f.badge(6, 470, top + 5 * hgt + 40, step=6, color=GREEN)
f.save(OUT + "ch07_recon_funnel_v2")

# New: passive versus active footprinting
p = Fig(1100, 540, "Footprinting: passive sources never touch the target; active techniques do",
        "Passive sources on the left: the target's website, social media, job boards, WHOIS and registry data, search-engine "
        "dorking, and document metadata, breach data, and EDGAR filings; none of them sends traffic to the target. Active techniques "
        "on the right touch the target's systems and need authorization: DNS queries and zone-transfer attempts, banner grabbing, "
        "and network range mapping with traceroute, leading into scanning.")
p.icon("user-laptop", 550, 110, 90, "Tester")
p.zone(20, 180, 500, 330, "Passive: no contact with the target", GREEN, "#eef8ef", step=1); p.badge(1, 502, 196, step=1)
srcs = [("browser", "Website"), ("group", "Social media"), ("document", "Job boards"), ("database", "WHOIS, RIRs"), ("search", "Dorking"), ("certificate", "Metadata,\nbreaches, EDGAR")]
for k, (ic, lab) in enumerate(srcs):
    x = 100 + (k % 3) * 160; y = 270 + (k // 3) * 130
    p.icon(ic, x, y, 60, step=1); p.text(x, y + 48, lab, 13, INK, "bold", step=1)
p.arrow([(510, 140), (420, 178)], None, GREEN, step=1, width=2.4)
p.zone(580, 180, 500, 330, "Active: touches the target, needs authorization", RED, "#fdf2f1", step=2); p.badge(2, 1062, 196, step=2)
p.arrow([(590, 140), (680, 178)], None, RED, step=2, width=2.4)
p.icon("firewall", 940, 300, 70, step=2); p.icon("server", 1010, 290, 64, step=2); p.icon("server", 1010, 380, 64, step=2)
p.text(980, 450, "target systems", 13, RED, "bold", step=2)
for k, (lab, y) in enumerate([("DNS queries, zone transfers", 260), ("Banner grabbing", 330), ("Traceroute, range mapping", 400)]):
    p.arrow([(610, y), (896, y + (300 - y) * 0.3)], lab, RED, step=3, size=13, label_at=.42, width=2.2)
p.badge(3, 600, 470, step=3, color=RED)
p.text(830, 490, "leads into scanning (Chapter 8)", 13, RED, italic=True, step=3)
p.save(OUT + "ch07_footprinting")

# New: DNS reconnaissance
d = Fig(1100, 560, "DNS reconnaissance: records, zone transfers, and subdomains",
        "A tester queries the target's DNS with dig or nslookup and learns A, MX, NS, TXT, and other records. An authoritative server "
        "that allows zone transfers to anyone answers an AXFR request with every record in the zone, mapping the whole network; a "
        "correctly configured one transfers only to its authorized secondary. Subdomains also come from certificate-transparency logs, "
        "passive DNS databases, and brute-forcing names. Defenses: restrict zone transfers and sign records with DNSSEC.")
d.icon("user-laptop", 100, 160, 90, "Tester", "dig, nslookup")
d.icon("server", 520, 160, 96, "ns1.example.com", "authoritative DNS")
d.arrow([(150, 140), (470, 140)], "dig example.com MX / NS / TXT", BLUE, step=1, size=13)
d.arrow([(470, 176), (150, 176)], "mail, name servers, SPF and DKIM", BLUE, step=1, size=13, label_dy=-8); d.badge(1, 160, 112, step=1)
d.arrow([(150, 250), (468, 200)], "AXFR example.com", RED, step=2, size=13, width=2.6, label_dy=22); d.badge(2, 150, 250, step=2, color=RED)
d.rect(620, 90, 290, 196, "#1f2933", "#1f2933", 1, rx=8, step=3)
for k, line in enumerate(["; full zone, if AXFR is open", "www     A     203.0.113.10", "vpn     A     203.0.113.20", "mail    MX    10 mx.example.com",
                          "dev     A     10.1.2.30", "admin   A     10.1.2.31", "jira    CNAME vendor.cloud.net"]):
    d.text(636, 114 + k * 24, line, 13, "#8fd16a" if k == 0 else "#e4e7eb", anchor="start", step=3)
d.arrow([(570, 190), (618, 190)], None, RED, step=3, width=2.6); d.badge(3, 920, 96, step=3, color=RED)
d.icon("server", 1010, 160, 70, "ns2", "secondary", step=4)
d.arrow([(914, 240), (980, 210)], None, GREEN, step=4); d.text(1000, 268, "AXFR allowed only here", 12, GREEN, "bold", step=4)
d.badge(4, 1050, 110, step=4, color=GREEN)
d.raw('<line x1="30" y1="330" x2="1070" y2="330" stroke="#d0d6dd" stroke-width="2" stroke-dasharray="6 6"/>')
d.text(40, 360, "Subdomain enumeration", 16, INK, "bold", "start", step=5); d.badge(5, 24, 354, step=5)
for k, (ic, lab, sub) in enumerate([("certificate", "Certificate-transparency logs", "every public TLS certificate is logged"),
                                    ("database", "Passive DNS databases", "historical resolutions"),
                                    ("search", "Brute-force names", "vpn, mail, dev, admin ...")]):
    x = 60 + k * 340
    d.icon(ic, x + 30, 420, 54, step=5); d.text(x + 70, 414, lab, 14, INK, "bold", "start", step=5); d.text(x + 70, 434, sub, 12, MUTED, anchor="start", step=5)
d.rect(30, 480, 1040, 56, "#e8f5e9", GREEN, 1.6, rx=8, step=6); d.icon("shield", 66, 508, 36, step=6); d.badge(6, 30, 480, step=6)
d.text(96, 514, "Defend: allow zone transfers only to authorized secondaries, sign the zone with DNSSEC, and prune stale records.", 14, GREEN, "bold", "start", step=6)
d.save(OUT + "ch07_dns_recon")

# New: cloud and modern infrastructure reconnaissance
c = Fig(1100, 520, "The attack surface is distributed: a hardened perimeter, and everything outside it",
        "The organization's data center sits behind a firewall. Outside it the same data can leak through a publicly readable storage "
        "bucket, an API key committed to a public code repository, a misconfigured cloud function, a container registry, or a "
        "third-party SaaS integration. Attackers find these through bucket-name enumeration, search engines, and "
        "certificate-transparency logs.")
c.zone(30, 60, 300, 330, "Data center", BLUE, "#eef5fc", step=1)
c.icon("firewall", 110, 200, 80, "Hardened", step=1); c.icon("server", 230, 160, 70, step=1); c.icon("database", 230, 270, 70, step=1)
c.icon("check", 300, 90, 28, step=1); c.badge(1, 312, 76, step=1)
c.zone(380, 60, 690, 330, "Outside the perimeter: cloud, SaaS, and code hosting", RED, "#fdf2f1", step=2)
leaks = [("database", "Public storage bucket", "readable by anyone", 490, 170), ("code", "Public repo", "API key committed", 720, 170),
         ("gear", "Cloud function", "misconfigured", 950, 170), ("rack", "Container registry", "images with secrets", 600, 300),
         ("nodes", "SaaS integration", "third-party access", 840, 300)]
for k, (ic, lab, sub, x, y) in enumerate(leaks):
    c.icon(ic, x, y, 60, lab, sub, step=2 + k // 3, label_size=13); c.icon("warning", x + 32, y - 28, 24, step=2 + k // 3)
c.badge(2, 1052, 76, step=2, color=RED); c.badge(3, 520, 280, step=3, color=RED)
c.icon("attacker", 1000, 450, 70, "Attacker", step=4)
for lab, y in [("bucket-name guessing", 410), ("search engines", 440), ("CT logs", 470)]:
    c.text(940, y, lab, 13, RED, "bold", "end", step=4)
c.arrow([(960, 410), (900, 370)], None, RED, step=4, width=2.2); c.badge(4, 960, 500, step=4, color=RED)
c.text(180, 440, "Hardening your own perimeter does not", 14, INK, "bold", step=5); c.text(180, 460, "cover data exposed somewhere else.", 14, INK, "bold", step=5)
c.text(180, 486, "Continuously inventory every external asset.", 13, GREEN, "bold", step=5); c.badge(5, 30, 432, step=5)
c.save(OUT + "ch07_cloud_recon")

# New: the intelligence cycle
g = Fig(1000, 600, "The intelligence cycle turns raw collection into a usable footprint",
        "Five stages in a loop: planning and direction sets the questions from the scope; collection gathers raw data from OSINT, "
        "registries, DNS, and cloud sources; processing deduplicates hosts and resolves names; analysis correlates people, technology, "
        "and exposed hosts, often in a link-analysis tool; dissemination records a structured footprint that drives scanning and "
        "the report, and raises new questions.")
cx, cy, R = 500, 320, 190
g.circle(cx, cy, R, "none", "#c5ccd3", 3)
g.icon("logbook", cx, cy - 10, 80, "Living target profile")
st = [("Planning and direction", "questions from the scope", "checklist", BLUE), ("Collection", "OSINT, registries, DNS, cloud", "search", "#16a085"),
      ("Processing", "deduplicate, resolve, organize", "gear", ORANGE), ("Analysis", "correlate people, tech, hosts", "nodes", RED),
      ("Dissemination", "footprint for scanning and report", "document", PURPLE)]
for i, (name, sub, ic, col) in enumerate(st):
    ang = -90 + i * 72; a = math.radians(ang); x, y = cx + R * math.cos(a), cy + R * math.sin(a)
    g.circle(x, y, 46, "#ffffff", col, 3, step=i + 1); g.icon(ic, x, y - 2, 56, step=i + 1); g.badge(i + 1, x - 36, y - 36, step=i + 1, color=col)
    if ang == -90: tx, ty, ta = x + 62, y - 40, "start"
    elif math.cos(a) > 0.1: tx, ty, ta = x + 58, y - 4, "start"
    else: tx, ty, ta = x - 58, y - 4, "end"
    g.text(tx, ty, name, 16, col, "bold", ta, step=i + 1); g.text(tx, ty + 18, sub, 13, INK, anchor=ta, step=i + 1)
    a2, a3 = math.radians(ang + 17), math.radians(ang + 55)
    g.arrow([(cx + R * math.cos(a2), cy + R * math.sin(a2)), (cx + R * math.cos(a3), cy + R * math.sin(a3))], None, col, step=i + 2, width=3)
g.save(OUT + "ch07_intel_cycle")
print("ok")
