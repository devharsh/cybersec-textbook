import os
import sys, datetime as dt; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# Redraw: where each Kerberos attack breaks in
k = Fig(1100, 600, "Where each Kerberos attack breaks in",
        "Top: the three exchanges, the client with the Authentication Server for a Ticket-Granting Ticket, with the Ticket-Granting "
        "Server for a service ticket, and with the service itself. Below: Kerberoasting abuses step 2 with any valid account and "
        "cracks the service ticket offline. Pass-the-ticket reuses a ticket stolen from host memory at steps 2 and 3. A golden "
        "ticket skips step 1 by forging a TGT with the krbtgt key. A silver ticket skips step 2 by forging a service ticket with one "
        "service account key, so the KDC never sees it.")
k.icon("user-laptop", 90, 160, 90, "Client")
k.zone(330, 50, 260, 250, "Key Distribution Center", BLUE, "#eef5fc")
k.icon("server", 460, 115, 70, "AS"); k.icon("server", 460, 225, 70, "TGS")
k.icon("server", 900, 140, 90, "Service")
k.arrow([(140, 125), (420, 115)], "AS-REQ / AS-REP: TGT", BLUE, step=1, size=12, both=True, label_at=.33)
k.arrow([(140, 190), (420, 225)], "TGS: service ticket", BLUE, step=2, size=12, both=True, label_at=.36, label_dy=22)
k.arrow([(90, 230), (90, 315), (900, 315), (900, 214)], "AP-REQ / AP-REP: the KDC is not contacted", BLUE, step=3, size=12, both=True, label_at=.6, label_dy=-8)
k.badge(1, 150, 104, step=1); k.badge(2, 150, 212, step=2); k.badge(3, 70, 300, step=3)
atk = [("Kerberoasting", "against step 2", "any valid account", "request a service ticket,\ncrack it offline", "hourglass", ORANGE, 2),
       ("Pass-the-ticket", "steps 2 and 3", "a ticket from host memory", "reuse a stolen ticket;\nno password needed", "memory", RED, 2.5),
       ("Golden ticket", "skips step 1", "the krbtgt key", "forge any TGT; reset\nkrbtgt twice to undo", "certificate", "#b9770e", 1),
       ("Silver ticket", "skips step 2", "one service account key", "forge a service ticket;\nKDC logs show nothing", "key", PURPLE, 3)]
for i, (name, where, needs, does, ic, col, target) in enumerate(atk):
    x = 30 + i * 265
    k.rect(x, 350, 245, 220, "#ffffff", col, 2.4, rx=10, step=4 + i); k.rect(x, 350, 245, 8, col, col, 1, rx=4, step=4 + i)
    k.icon(ic, x + 50, 404, 58, step=4 + i); k.icon("attacker", x + 196, 404, 50, step=4 + i)
    k.text(x + 122, 460, name, 17, col, "bold", step=4 + i); k.text(x + 122, 480, where, 13, col, "bold", step=4 + i)
    k.text(x + 122, 504, "needs: " + needs, 12, INK, "bold", step=4 + i); k.text(x + 122, 526, does, 12, INK, step=4 + i)
    k.badge(4 + i, x + 227, 366, step=4 + i, color=col)
    tx, ty = {2: (372, 214), 2.5: (420, 321), 1: (500, 126), 3: (880, 200)}[target]
    k.arrow([(x + 122, 350), (tx, ty)], None, col, step=4 + i, dash=True, width=2)
k.text(550, 590, "None breaks the cryptography: each uses a key or ticket the attacker should not hold.", 13, MUTED, italic=True, step=7)
k.save(OUT + "ch09_kerberos_attacks_v2")

# Redraw: bug lifetimes
D = dt.date
rows = [("Shellshock (Bash)", D(1989, 8, 5), D(2014, 9, 24), BLUE), ("Heartbleed (OpenSSL)", D(2011, 12, 15), D(2014, 4, 7), BLUE),
        ("Log4Shell (Log4j 2)", D(2013, 9, 14), D(2021, 12, 10), BLUE), ("GitLab org-mode regex", D(2014, 6, 20), D(2026, 10, 21), ORANGE),
        ("regreSSHion (OpenSSH)", D(2020, 10, 1), D(2024, 7, 1), BLUE)]
b = Fig(1100, 470, "How long landmark bugs hid: from the commit that introduced them to public disclosure",
        "Shellshock lived in Bash from August 1989 to September 2014, about 25 years. Heartbleed from December 2011 to April 2014, "
        "about 2 years. Log4Shell from September 2013 to December 2021, about 8 years. GitLab's org-mode bug from June 2014 to "
        "October 2026, about 12 years. regreSSHion was first fixed in 2006, reintroduced in October 2020, and disclosed in July "
        "2024, about 4 years. A dashed line marks January 2038, when signed 32-bit time runs out.")
X0, X1, Y0 = 230, 1060, 80
xs = lambda d: X0 + (d.year + (d.timetuple().tm_yday - 1) / 365.25 - 1987) / (2040 - 1987) * (X1 - X0)
b.raw(f'<line x1="{X0}" y1="390" x2="{X1}" y2="390" stroke="#52606d" stroke-width="2"/>')
for yr in range(1990, 2041, 5):
    xx = xs(D(yr, 1, 1)); b.raw(f'<line x1="{xx:.1f}" y1="390" x2="{xx:.1f}" y2="396" stroke="#52606d"/><line x1="{xx:.1f}" y1="{Y0}" x2="{xx:.1f}" y2="390" stroke="#eef0f2"/>')
    b.text(xx, 412, str(yr), 12, MUTED)
for i, (name, a, z, col) in enumerate(rows):
    y = Y0 + 30 + i * 60; st = i + 1
    b.text(X0 - 14, y + 5, name, 14, INK, "bold", "end", step=st)
    b.rect(xs(a), y - 9, xs(z) - xs(a), 18, col, col, 1, rx=4, step=st, opacity=.85)
    b.icon("bug", xs(a) - 2, y, 30, step=st); b.icon("warning", xs(z) + 4, y, 24, step=st)
    yrs = (z - a).days / 365.25
    b.text(xs(z) + 22, y + 5, f"about {yrs:.0f} years", 13, INK, anchor="start", step=st)
b.raw(f'<circle cx="{xs(D(2006, 9, 27)):.1f}" cy="{Y0 + 30 + 4 * 60}" r="5" fill="#52606d"/>', step=5)
b.text(xs(D(2006, 9, 27)), Y0 + 30 + 4 * 60 + 26, "first fixed 2006", 12, MUTED, step=5)
x38 = xs(D(2038, 1, 19))
b.raw(f'<line x1="{x38:.1f}" y1="{Y0 - 10}" x2="{x38:.1f}" y2="390" stroke="#c0392b" stroke-width="2" stroke-dasharray="7 5"/>', step=6)
b.icon("clock", x38 - 20, Y0 - 6, 26, step=6); b.text(x38 - 36, Y0 - 2, "2038: signed 32-bit time runs out", 13, RED, "bold", "end", step=6)
b.badge(6, x38 + 14, Y0 - 6, step=6, color=RED)
b.text(550, 450, "bug icon: introduced     warning icon: publicly disclosed", 12, MUTED, italic=True)
b.save(OUT + "ch09_bug_lifetimes_v2")

# New: compilation pipeline
c = Fig(1100, 400, "From source to machine code: four stages, each one inspectable",
        "hello.c is preprocessed with gcc -E into hello.i, compiled with gcc -S into assembly in hello.s, assembled with gcc -c into "
        "the object file hello.o, and linked with gcc into the executable hello, which the CPU runs.")
st = [("hello.c", "source", "code", None), ("hello.i", "one translation unit", "document", "Preprocess\ngcc -E"), ("hello.s", "assembly", "logbook", "Compile\ngcc -S"),
      ("hello.o", "object file", "memory", "Assemble\ngcc -c"), ("hello", "executable", "gear", "Link\ngcc"), ("CPU", "runs the bytes", "chip", None)]
for i, (f, sub, ic, tool) in enumerate(st):
    x = 80 + i * 188
    c.icon(ic, x, 170, 74, step=i + 1); c.text(x, 236, f, 16, INK, "bold", step=i + 1); c.text(x, 256, sub, 12, MUTED, step=i + 1)
    if i: 
        c.arrow([(x - 150, 170), (x - 44, 170)], None, BLUE, step=i + 1, width=2.6)
        if tool: c.text(x - 97, 120, tool, 13, BLUE, "bold", step=i + 1)
        c.badge(i, x - 97, 150, step=i + 1) if tool else None
    if i == 5: c.badge(5, x - 97, 150, step=6)
c.rect(260, 300, 580, 70, "#1f2933", "#1f2933", 1, rx=8, step=3)
c.text(280, 326, "pushq %rbp      ; save caller's base pointer", 13, "#e4e7eb", anchor="start", step=3)
c.text(280, 350, "movq  %rsp, %rbp ; set up this function's frame ... ret", 13, "#e4e7eb", anchor="start", step=3)
c.text(550, 392, "The assembly stage is where the stack frame and the return address become visible.", 12, MUTED, italic=True, step=3)
c.save(OUT + "ch09_compile_pipeline")

# New: the stack and a buffer overflow
o = Fig(1100, 580, "A stack buffer overflow: too much input spills into the neighbors",
        "Left: a process's memory, with text, data and BSS, a heap that grows up, and a stack that grows down. Right: the frame of "
        "buf1_pass.c holds a 15-byte buffer, the pass integer, the saved base pointer, and the return address. gets() copies a long "
        "input with no bounds check; the bytes run past the buffer toward higher addresses, set pass to non-zero so root privileges "
        "are granted without the password, and with enough bytes overwrite the saved return address.")
segs = [("stack (grows down)", "#d6e9f8", 70), ("free space", "#ffffff", 110), ("heap (grows up)", "#e8f5e9", 70), ("data / BSS", "#fef5e7", 50), ("text (code)", "#f4ecf7", 50)]
y = 80; o.text(150, 66, "high addresses", 12, MUTED, step=1)
for name, col, h in segs:
    o.rect(60, y, 180, h, col, "#5b6570", 1.6, rx=0, step=1); o.text(150, y + h / 2 + 5, name, 14, INK, "bold", step=1); y += h
o.text(150, y + 20, "low addresses", 12, MUTED, step=1); o.badge(1, 60, 80, step=1)
o.arrow([(270, 100), (270, 150)], None, BLUE, step=1, width=2.4); o.arrow([(270, 330), (270, 280)], None, GREEN, step=1, width=2.4)
o.arrow([(244, 115), (420, 150)], None, "#9aa5b1", step=2, dash=True)
frame = [("return address", "#fdecea", RED), ("saved rbp", "#fff3e0", ORANGE), ("int pass = 0", "#e8f5e9", GREEN), ("char buff[15]", "#eef5fc", BLUE)]
fy = 110
for k2, (lab, fill, col) in enumerate(frame):
    h = 60 if k2 < 3 else 120
    o.rect(430, fy, 260, h, fill, col, 2, rx=4, step=2); o.text(560, fy + h / 2 + 6, lab, 16, col, "bold", step=2); fy += h
o.text(560, 98, "main's stack frame", 13, MUTED, "bold", step=2); o.badge(2, 430, 110, step=2)
o.text(730, 120, "higher addresses", 12, MUTED, anchor="start", step=2); o.arrow([(720, 410), (720, 130)], None, MUTED, step=2, width=1.6)
o.icon("user-laptop", 1030, 450, 64, "Input", step=3); o.badge(3, 790, 486, step=3)
o.rect(790, 500, 290, 30, "#1f2933", "#1f2933", 1, rx=4, step=3); o.text(935, 520, "AAAAAAAAAAAAAAAAAAAAAAAA", 14, "#8fd16a", "bold", step=3)
o.text(935, 556, "gets(buff): no bounds check", 13, RED, "bold", step=3)
o.arrow([(790, 515), (700, 400)], None, RED, step=3, width=2.6)
o.rect(431, 231, 258, 178, "#f5b7b1", RED, 2, rx=4, step=4); o.text(560, 350, "A A A A A A A A A A A A A A A", 14, RED, "bold", step=4); o.text(560, 380, "buff, full", 13, RED, step=4)
o.text(560, 266, "pass = 0x41414141 (non-zero)", 15, RED, "bold", step=4); o.badge(4, 690, 230, step=4, color=RED)
o.rect(800, 210, 280, 56, "#fdecea", RED, 1.6, rx=6, step=4)
o.text(940, 234, "Root privileges given to the user", 13, RED, "bold", step=4); o.text(940, 254, "without the correct password", 12, INK, step=4)
o.rect(431, 111, 258, 119, "#f5b7b1", RED, 2, rx=4, step=5); o.text(560, 146, "return = 0x4141414141414141", 14, RED, "bold", step=5); o.text(560, 206, "saved rbp = AAAAAAAA", 14, RED, "bold", step=5); o.badge(5, 690, 112, step=5, color=RED)
o.text(800, 150, "With more bytes: saved rbp and the return", 13, RED, "bold", "start", step=5)
o.text(800, 170, "address are overwritten, so ret jumps where", 13, RED, "bold", "start", step=5)
o.text(800, 190, "the attacker chooses.", 13, RED, "bold", "start", step=5)
o.save(OUT + "ch09_stack_overflow")

# New: NX and return-oriented programming, with mitigations
n = Fig(1100, 520, "After the overflow: injected shellcode or reused code, and the mitigations against each",
        "An overflow overwrites the saved return address. If the stack is executable, the attacker injects and runs shellcode. If NX "
        "or DEP makes it non-executable, the attacker reuses existing code through return-to-libc or a chain of ROP gadgets. Against "
        "all of these: ASLR randomizes addresses, a stack canary detects the overwrite, CFI and shadow stacks block bad returns, and "
        "least privilege limits the damage.")
n.card(420, 50, 260, 120, "bug", "Return address overwritten", None, RED, step=1, icon_size=56, title_size=15); n.badge(1, 420, 50, step=1, color=RED)
n.arrow([(470, 172), (250, 230)], None, ORANGE, step=2); n.text(330, 186, "stack executable (no NX)", 13, ORANGE, "bold", "end", step=2)
n.arrow([(630, 172), (850, 230)], None, PURPLE, step=3); n.text(770, 186, "stack not executable (NX / DEP)", 13, PURPLE, "bold", "start", step=3)
n.card(120, 232, 260, 140, "code", "Inject and run shellcode", None, ORANGE, step=2, icon_size=60, title_size=15); n.badge(2, 120, 232, step=2, color=ORANGE)
n.card(720, 232, 260, 140, "gear", "Reuse existing code", "return-to-libc or a\nchain of ROP gadgets", PURPLE, step=3, icon_size=50, title_size=15)
n.badge(3, 720, 232, step=3, color=PURPLE)
mit = [("ASLR", "randomizes addresses"), ("Stack canary", "detects the overwrite"), ("CFI, shadow stack", "blocks bad returns"), ("Least privilege", "limits the impact")]
for i, (a, s2) in enumerate(mit):
    x = 40 + i * 265
    n.rect(x, 410, 245, 80, "#e8f5e9", GREEN, 2, rx=8, step=4); n.icon("shield", x + 36, 450, 44, step=4)
    n.text(x + 66, 444, a, 15, GREEN, "bold", "start", step=4); n.text(x + 66, 466, s2, 13, INK, anchor="start", step=4)
n.arrow([(250, 374), (300, 406)], None, GREEN, step=4); n.arrow([(850, 374), (800, 406)], None, GREEN, step=4); n.badge(4, 40, 410, step=4, color=GREEN)
n.save(OUT + "ch09_nx_rop")

# New: lateral movement with pass-the-hash and pass-the-ticket
l = Fig(1100, 520, "Lateral movement: reusing what was found on one host to reach the next",
        "The attacker controls one workstation and dumps credentials from LSASS memory or the SAM with Mimikatz. Pass-the-hash "
        "presents the NTLM hash itself to other machines, with no cracking. Pass-the-ticket injects a captured or forged Kerberos "
        "ticket; a golden ticket, signed with the krbtgt hash, opens any service in the domain. Defenses: Credential Guard, disabling "
        "NTLM where possible, tiered administration, and rotating krbtgt twice after a compromise.")
l.icon("attacker", 80, 230, 80, "Attacker")
l.icon("desktop", 260, 230, 90, "Workstation 1", "compromised", step=1); l.icon("bug", 290, 190, 30, step=1)
l.arrow([(122, 230), (210, 230)], None, RED, step=1, width=2.6); l.badge(1, 160, 200, step=1, color=RED)
l.icon("memory", 260, 400, 60, "LSASS, SAM", step=2); l.arrow([(260, 314), (260, 366)], None, RED, step=2); l.text(270, 344, "Mimikatz", 12, RED, "bold", "start", step=2)
l.badge(2, 220, 380, step=2, color=RED)
l.rect(360, 330, 200, 60, "#fff3e0", ORANGE, 1.6, rx=6, step=3); l.text(460, 354, "NTLM hash", 14, ORANGE, "bold", step=3); l.text(460, 374, "Kerberos TGT", 14, PURPLE, "bold", step=3)
l.badge(3, 360, 330, step=3, color=ORANGE)
targets = [("server", "File server", 820, 110), ("desktop", "Workstation 2", 820, 260), ("server", "Domain controller", 820, 410)]
for ic, lab, x, y in targets: l.icon(ic, x, y, 80, lab, step=4)
l.arrow([(562, 350), (770, 120)], None, ORANGE, step=4, width=2.6); l.text(630, 226, "pass-the-hash", 13, ORANGE, "bold", "end", step=4)
l.arrow([(562, 360), (770, 260)], None, ORANGE, step=4, width=2.6); l.text(700, 340, "pass-the-hash", 13, ORANGE, "bold", step=4)
l.arrow([(562, 375), (770, 410)], None, PURPLE, step=5, width=2.6); l.text(660, 424, "pass-the-ticket", 13, PURPLE, "bold", step=5)
l.badge(4, 590, 300, step=4, color=ORANGE); l.badge(5, 590, 400, step=5, color=PURPLE)
l.icon("certificate", 960, 410, 50, step=6); l.text(990, 470, "golden ticket:", 12, "#b9770e", "bold", step=6); l.text(990, 486, "any service", 12, "#b9770e", "bold", step=6)
l.badge(6, 990, 380, step=6, color="#b9770e")
l.icon("shield", 80, 470, 40, step=7); l.badge(7, 50, 450, step=7, color=GREEN)
l.text(110, 466, "Credential Guard, disable NTLM, tiered admin,", 13, GREEN, "bold", "start", step=7)
l.text(110, 484, "rotate krbtgt twice after a compromise", 13, GREEN, "bold", "start", step=7)
l.save(OUT + "ch09_lateral_movement")

# New: C2 beaconing
b2 = Fig(1100, 520, "Command and control: an implant beacons home over traffic that looks normal",
         "An implant on the victim checks in with the C2 server at intervals over HTTPS, DNS, or a trusted cloud service, picks up "
         "tasks, and returns results. Jitter varies the interval to evade detection. Frameworks include Cobalt Strike, often cracked "
         "and abused, and open-source Sliver, Mythic, and Havoc. Defenders catch the pattern with network monitoring, endpoint "
         "telemetry, and memory forensics.")
b2.icon("desktop", 120, 170, 90, "Victim", "implant in memory"); b2.icon("bug", 150, 130, 30)
b2.icon("cloud", 540, 160, 150, "HTTPS, DNS, cloud services", step=2)
b2.icon("server", 940, 170, 90, "C2 server", "Cobalt Strike, Sliver,\nMythic, Havoc"); b2.icon("attacker", 1040, 140, 54)
b2.arrow([(172, 150), (462, 150)], "check in", RED, step=1, size=13, width=2.6); b2.arrow([(618, 150), (890, 150)], None, RED, step=1, width=2.6)
b2.arrow([(890, 196), (618, 196)], "task", ORANGE, step=2, size=13, width=2.4, label_dy=20); b2.arrow([(462, 196), (172, 196)], None, ORANGE, step=2, width=2.4)
b2.badge(1, 200, 130, step=1, color=RED); b2.badge(2, 860, 220, step=2, color=ORANGE)
T0, T1 = 90, 1010
b2.raw(f'<line x1="{T0}" y1="370" x2="{T1}" y2="370" stroke="#52606d" stroke-width="2"/>', step=3)
b2.text(T0, 400, "time", 12, MUTED, anchor="start", step=3)
for k3, t in enumerate([0, 60, 118, 183, 240, 297, 362, 420, 478, 541, 600]):
    x = T0 + 30 + t * 1.45
    b2.raw(f'<line x1="{x:.0f}" y1="330" x2="{x:.0f}" y2="370" stroke="#c0392b" stroke-width="4" stroke-linecap="round"/>', step=3)
b2.text(550, 318, "beacons roughly every 60 seconds, with jitter of a few seconds", 13, RED, "bold", step=3); b2.badge(3, 60, 340, step=3, color=RED)
b2.rect(40, 420, 1020, 76, "#e8f5e9", GREEN, 1.6, rx=8, step=4); b2.icon("eye", 80, 458, 44, step=4); b2.badge(4, 40, 420, step=4, color=GREEN)
b2.text(116, 452, "Defenders hunt the rhythm and the behavior: network monitoring for periodic check-ins,", 14, GREEN, "bold", "start", step=4)
b2.text(116, 474, "endpoint telemetry for injection, and memory forensics for in-memory implants.", 14, GREEN, "bold", "start", step=4)
b2.save(OUT + "ch09_c2_beacon")

# New: coverage-guided fuzzing loop
z = Fig(1100, 500, "Coverage-guided fuzzing: mutate, run, keep what reaches new code",
        "Seed inputs form a corpus. The fuzzer picks one, mutates it, and runs the instrumented target built with sanitizers such as "
        "AddressSanitizer. If the input reached new code, it joins the corpus; if the target crashed, the input is saved for triage. "
        "The loop repeats millions of times, steering toward unexplored paths. AFL++ and libFuzzer work this way.")
nodes = [("Corpus", "seed and saved inputs", "database", 110, 220, BLUE), ("Mutate", "flip bits, splice, insert", "gear", 360, 100, ORANGE),
         ("Run target", "instrumented, with ASan\nand UBSan", "chip", 640, 100, PURPLE), ("New coverage?", "a path not seen before", "nodes", 880, 220, GREEN)]
for i, (name, sub, ic, x, y, col) in enumerate(nodes):
    z.circle(x, y, 58, "#ffffff", col, 3, step=i + 1); z.icon(ic, x, y - 4, 64, step=i + 1)
    z.text(x, y + 80, name, 16, col, "bold", step=i + 1); z.text(x, y + 98, sub, 12, INK, step=i + 1); z.badge(i + 1, x - 46, y - 46, step=i + 1, color=col)
z.arrow([(160, 190), (304, 118)], None, BLUE, step=2, width=2.6); z.arrow([(420, 100), (580, 100)], None, ORANGE, step=3, width=2.6)
z.arrow([(694, 124), (836, 190)], None, PURPLE, step=4, width=2.6)
z.arrow([(870, 340), (870, 380), (110, 380), (110, 346)], "yes: add the input to the corpus", GREEN, step=5, width=2.6, label_at=.5)
z.badge(5, 490, 380, step=5, color=GREEN)
z.icon("bug", 640, 300, 54, step=6); z.arrow([(640, 224), (640, 268)], None, RED, step=6, width=2.6); z.text(632, 252, "crash", 13, RED, "bold", "end", step=6)
z.text(600, 306, "save the input for triage", 13, RED, "bold", "end", step=6); z.badge(6, 690, 300, step=6, color=RED)
z.text(550, 470, "Sanitizers turn silent memory corruption into an immediate, diagnosable crash.", 13, MUTED, italic=True, step=6)
z.save(OUT + "ch09_fuzz_loop")
print("ok")
