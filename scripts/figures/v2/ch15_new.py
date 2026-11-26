import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# 1. Malware taxonomy
t = Fig(1100, 470, "Malware by how it spreads and what it does",
        "Six families as cards. A virus needs a host file and spreads when it runs. A worm spreads on its own across networks, like "
        "WannaCry with EternalBlue. A Trojan poses as legitimate software, and a RAT adds remote control. Ransomware encrypts files and "
        "often steals them first for double extortion. A rootkit hides from the operating system. A botnet is many infected machines "
        "steered through command and control.")
fam = [("document", "Virus", "needs a host file;\nspreads when run", PURPLE), ("nodes", "Worm", "spreads by itself;\nWannaCry, EternalBlue", RED),
       ("certificate", "Trojan / RAT", "looks legitimate;\nRAT adds remote control", ORANGE), ("lock", "Ransomware", "encrypts, often steals\nfirst: double extortion", RED),
       ("eye", "Rootkit", "hides files, processes,\nconnections from the OS", "#2b3138"), ("bot", "Botnet", "many machines under\none C2: DDoS, spam", BLUE)]
for i, (ic, name, sub, col) in enumerate(fam):
    x = 30 + (i % 3) * 355; y = 60 + (i // 3) * 200
    t.card(x, y, 330, 180, ic, name, sub, col, step=i + 1, icon_size=70, title_size=17); t.badge(i + 1, x + 14, y + 20, step=i + 1, color=col)
t.save(OUT + "ch15_taxonomy")

# 2. Safe analysis lab
l = Fig(1100, 520, "A safe malware analysis lab: isolated, snapshotted, with a fake internet",
        "The analyst's host runs a Windows analysis VM with FlareVM tools and a REMnux VM on an isolated host-only network with no "
        "route to production or the real internet. REMnux runs INetSim, which answers DNS, HTTP, SMTP, and IRC so the sample behaves "
        "normally. A clean snapshot is taken before each run and restored afterward.")
l.zone(30, 60, 1040, 340, "Analyst workstation (hypervisor)", BLUE, "#eef5fc")
l.zone(70, 100, 640, 270, "Isolated host-only network", GREEN, "#eef8ef", step=1, dash=True); l.badge(1, 692, 116, step=1, color=GREEN)
l.icon("desktop", 200, 220, 90, "Windows analysis VM", "FlareVM: x64dbg, Ghidra", step=2); l.icon("bug", 235, 180, 30, step=2); l.badge(2, 140, 150, step=2)
l.icon("server", 560, 220, 90, "REMnux VM", "INetSim: fake DNS, HTTP,\nSMTP, IRC", step=3); l.badge(3, 500, 150, step=3)
l.arrow([(250, 210), (510, 210)], "sample's traffic", ORANGE, step=3, size=12, width=2.4); l.arrow([(510, 236), (250, 236)], "fake answers", GREEN, step=3, size=12, width=2.4, label_dy=20)
l.icon("clock", 880, 170, 60, "Clean snapshot", "taken before each run", step=4); l.arrow([(840, 158), (252, 158)], None, MUTED, step=4, dash=True, width=1.6)
l.icon("gear", 880, 300, 50, "revert after", step=5, label_size=13); l.badge(4, 840, 120, step=4); l.badge(5, 840, 270, step=5)
l.icon("cloud", 900, 460, 80, step=6); l.icon("rack", 600, 460, 56, step=6); l.text(600, 505, "production", 12, MUTED, "bold", step=6); l.text(900, 505, "real internet", 12, MUTED, "bold", step=6)
l.arrow([(400, 372), (580, 440)], None, RED, step=6, dash=True, width=2); l.arrow([(400, 372), (860, 450)], None, RED, step=6, dash=True, width=2)
l.icon("cross", 530, 420, 26, step=6); l.icon("cross", 760, 432, 26, step=6); l.badge(6, 330, 440, step=6, color=RED)
l.text(200, 470, "no route out", 14, RED, "bold", step=6)
l.save(OUT + "ch15_analysis_lab")

# 3. Ransomware lifecycle
r = Fig(1100, 440, "The modern ransomware lifecycle: encryption comes last",
        "Seven stages: initial access through phishing or an exposed service; execute and persist; escalate and spread; exfiltrate "
        "data; disable backups and security tools; encrypt everything; and demand a ransom with a threat to leak the stolen data. "
        "Defenses map onto each stage, and tested offline or immutable backups make encryption a recoverable outage.")
st = [("envelope", "Initial access", "phishing, exposed\nservice", ORANGE), ("gear", "Execute,\npersist", "", ORANGE), ("nodes", "Escalate,\nspread", "", ORANGE),
      ("cloud", "Exfiltrate", "data stolen first", RED), ("database", "Disable backups\nand tools", "", RED), ("lock", "Encrypt", "everything", RED),
      ("money", "Ransom +\nleak threat", "double extortion", "#922b21")]
for i, (ic, name, sub, col) in enumerate(st):
    x = 80 + i * 157
    r.circle(x, 150, 54, "#ffffff", col, 3.2, step=i + 1); r.icon(ic, x, 146, 60, step=i + 1)
    r.text(x, 230, name, 14, col, "bold", step=i + 1); r.text(x, 268 if "\n" in name else 250, sub, 12, INK, step=i + 1); r.badge(i + 1, x - 44, 106, step=i + 1, color=col)
    if i < 6: r.arrow([(x + 56, 150), (x + 99, 150)], None, col, step=i + 2, width=2.6)
r.rect(30, 310, 1040, 100, "#e8f5e9", GREEN, 1.6, rx=8, step=8); r.icon("shield", 70, 360, 44, step=8); r.badge(8, 30, 310, step=8, color=GREEN)
r.text(104, 344, "Defenses by stage: phishing-resistant MFA and training; patching and least privilege; EDR to catch staging;", 13, GREEN, "bold", "start", step=8)
r.text(104, 366, "and, decisively, tested offline or immutable backups. Paying funds the ecosystem, may be legally restricted,", 13, GREEN, "bold", "start", step=8)
r.text(104, 388, "and does not guarantee recovery.", 13, GREEN, "bold", "start", step=8)
r.save(OUT + "ch15_ransomware_lifecycle")

# 4. End-to-end analysis walkthrough
a = Fig(1100, 560, "An end-to-end malware analysis, from hash to report",
        "Triage the sample by hash, file type, and threat intelligence. Run static analysis of strings, imports, PE sections, and "
        "entropy. If it is packed, unpack it by running to the original entry point and dumping it. Disassemble or decompile it in "
        "Ghidra. Run it in a sandbox and watch API calls, files, registry, and network. Extract indicators and write YARA and network "
        "signatures. Report capabilities, indicators, and severity.")
nodes = [("search", "Triage", "hash, file type,\nthreat intel", 90, 140), ("document", "Static", "strings, imports,\nsections, entropy", 300, 140),
         ("warning", "Packed?", "high entropy,\nfew imports", 510, 140), ("gear", "Unpack", "run to OEP, dump", 510, 370),
         ("code", "Disassemble", "Ghidra", 730, 140), ("desktop", "Dynamic", "sandbox: API, files,\nregistry, network", 940, 140),
         ("checklist", "IOCs + YARA", "and network\nsignatures", 830, 360), ("logbook", "Report", "capabilities, IOCs,\nseverity", 1010, 360)]
for i, (ic, name, sub, x, y) in enumerate(nodes):
    a.circle(x, y, 50, "#ffffff", BLUE if i != 2 else ORANGE, 3, step=i + 1); a.icon(ic, x, y - 2, 56, step=i + 1)
    a.text(x, y + 74, name, 15, BLUE if i != 2 else ORANGE, "bold", step=i + 1); a.text(x, y + 92, sub, 12, INK, step=i + 1)
    a.badge(i + 1, x - 40, y - 40, step=i + 1, color=BLUE if i != 2 else ORANGE)
for (x1, y1, x2, y2, st, lab) in [(142, 140, 248, 140, 2, None), (352, 140, 458, 140, 3, None), (562, 140, 678, 140, 5, "no"), (510, 258, 510, 316, 4, "yes"),
                                  (556, 348, 694, 178, 5, None), (782, 140, 888, 140, 6, None), (905, 252, 852, 312, 7, None), (882, 360, 958, 360, 8, None)]:
    a.arrow([(x1, y1), (x2, y2)], lab, ORANGE if lab else BLUE, step=st, width=2.4, size=12, label_anchor="start" if lab == "yes" else "middle", label_dy=4 if lab == "yes" else -8)
a.save(OUT + "ch15_analysis_flow")

# 5. Rootkits and the trust anchor
k = Fig(1100, 560, "Rootkits hide by sitting below the tools that look for them",
        "A stack from top to bottom: applications and security tools, user-mode libraries, the operating system kernel, the boot "
        "process with the MBR or UEFI, firmware and device controllers, and hardware with a TPM. A user-mode rootkit hooks library "
        "calls; a kernel-mode rootkit changes kernel structures so tools that ask the kernel are blind; a bootkit loads before the "
        "operating system; firmware implants are deepest. Secure Boot and measured boot anchored in a TPM verify each stage, because a "
        "monitor can be trusted only if it sits below what it monitors.")
layers = [("Applications and security tools", "desktop", "#d6e9f8", None), ("User-mode libraries", "code", "#d6e9f8", "user-mode rootkit: hooks library calls"),
          ("Operating system kernel", "gear", "#aed6f1", "kernel-mode rootkit: edits kernel structures"), ("Boot: MBR or UEFI", "key", "#fcf3cf", "bootkit: loads before the OS"),
          ("Firmware, device controllers", "chip", "#fae5d3", "firmware implant: deepest, hardest to remove"), ("Hardware with a TPM", "lock", "#d5f5e3", None)]
for i, (name, ic, fill, atk) in enumerate(layers):
    y = 60 + i * 72
    k.rect(40, y, 560, 62, fill, "#5b6570", 1.6, rx=8, step=1); k.icon(ic, 80, y + 31, 40, step=1); k.text(110, y + 37, name, 15, INK, "bold", "start", step=1)
    if atk:
        k.arrow([(600, y + 31), (628, y + 31)], None, RED, step=i + 1, width=2)
        k.icon("devil", 646, y + 31, 34, step=i + 1); k.badge(i + 1, 680, y + 31, step=i + 1, color=RED); k.text(700, y + 37, atk, 13, RED, "bold", "start", step=i + 1)
k.badge(1, 40, 60, step=1)
k.arrow([(20, 476), (20, 76)], None, GREEN, step=6, width=4); k.text(38, 520, "Secure Boot and measured boot: each stage verified from the TPM up", 14, GREEN, "bold", "start", step=6)
k.badge(6, 18, 515, step=6, color=GREEN)
k.text(830, 520, "Trust anchor: a monitor is trustworthy only below what it watches.", 13, INK, step=6, italic=True)
k.save(OUT + "ch15_rootkit_layers")

# 6. Worms, botnets, supply chain
w = Fig(1100, 520, "Three ways malware reaches many machines at once",
        "A worm spreads from host to host on its own by exploiting a vulnerability, like WannaCry over SMB; patching and segmentation set "
        "its blast radius. A botnet is many compromised machines under one command-and-control server, rented out for DDoS, spam, and "
        "credential stuffing. Supply-chain malware rides a trusted, signed update to thousands of customers, as with SolarWinds.")
w.zone(20, 60, 340, 400, "Worm", RED, "#fdf2f1", step=1); w.badge(1, 342, 76, step=1, color=RED)
pos = [(190, 130), (90, 230), (290, 230), (90, 350), (190, 380), (290, 350)]
for k2, (x, y) in enumerate(pos):
    w.icon("desktop", x, y, 50, step=1 + (k2 > 0)); w.icon("bug", x + 18, y - 20, 18, step=1 + (k2 > 0))
for a_, b_ in [(0, 1), (0, 2), (1, 3), (2, 5), (3, 4)]:
    w.arrow([pos[a_], pos[b_]], None, RED, step=2, width=1.8)
w.text(190, 440, "SMB exploit, no user action", 12, RED, "bold", step=2)
w.zone(380, 60, 340, 400, "Botnet", ORANGE, "#fef5e7", step=3); w.badge(3, 702, 76, step=3, color=ORANGE)
w.icon("server", 550, 140, 64, "C2 server", step=3); w.icon("attacker", 640, 120, 44, step=3)
for k2, x in enumerate([440, 510, 590, 660]):
    w.icon("bot", x, 290, 44, step=3); w.arrow([(550, 184), (x, 262)], None, ORANGE, step=3, width=1.4, dash=True)
w.icon("server", 550, 400, 54, "victim: DDoS, spam", step=4, label_size=12)
for x in [440, 510, 590, 660]: w.arrow([(x, 318), (550, 368)], None, RED, step=4, width=1.6)
w.badge(4, 420, 390, step=4, color=RED)
w.zone(740, 60, 340, 400, "Supply chain", PURPLE, "#f5eef8", step=5); w.badge(5, 1062, 76, step=5, color=PURPLE)
w.icon("gear", 840, 150, 56, "vendor build", step=5); w.icon("certificate", 980, 150, 56, "signed update", step=5); w.icon("bug", 860, 118, 22, step=5)
w.arrow([(870, 150), (948, 150)], None, PURPLE, step=5, width=2.2)
for k2, x in enumerate([800, 870, 940, 1010]):
    w.icon("desktop", x, 330, 44, step=6); w.arrow([(980, 202), (x, 304)], None, PURPLE, step=6, width=1.4)
w.text(910, 400, "thousands of trusting customers", 12, PURPLE, "bold", step=6); w.badge(6, 760, 300, step=6, color=PURPLE)
w.text(550, 496, "Defenses: patch and segment; take down C2 with legal partners; SBOM, build integrity, and monitoring of trusted vendors.", 13, GREEN, "bold", step=7)
w.save(OUT + "ch15_worm_botnet")
print("ok")
