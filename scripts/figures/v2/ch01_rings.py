import os
import sys; sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

# x86 rings, built from the outside in
x = Fig(1100, 620, "x86 protection rings: the innermost level is the most privileged",
        "Concentric rings built from the outside in. Ring 3 runs user applications. Rings 2 and 1 are defined by the hardware but "
        "rarely used by mainstream operating systems. Ring 0 is the kernel. Ring minus 1 is the hypervisor, ring minus 2 is SMM "
        "firmware, and ring minus 3 is the security processor, Intel CSME or AMD Secure Processor, where a firmware TPM runs. Rings "
        "below 0 are informal names. Trusted execution environments, an SGX enclave in ring 3 and an Intel TDX trust domain, add "
        "isolation rather than a higher rank. The TDX module runs in SEAM, a CPU mode beside the hypervisor's VMX root, not a new ring. "
        "A discrete TPM is a separate chip on the board, outside the CPU rings.")
cx, cy = 470, 330
rings = [(260, "#85b4ee", "Ring 3", "user applications", "desktop", 1), (228, "#5d9be6", "Rings 2, 1", "defined, rarely used", "gear", 2),
         (200, "#2a78d6", "Ring 0", "kernel", "gear", 3), (158, "#f0a070", "Ring -1", "hypervisor", "server", 4),
         (116, "#ea6a35", "Ring -2", "SMM firmware", "chip", 5), (70, "#8e3412", "Ring -3", "security processor", "lock", 6)]
radii = [r for r, *_ in rings] + [0]
for r, col, lab, sub, ic, st in rings:
    x.circle(cx, cy, r, col, "#ffffff", 3, step=st)
for k, (r, col, lab, sub, ic, st) in enumerate(rings):
    mid = (r + radii[k + 1]) / 2 if k < 5 else 0
    x.text(cx, cy - mid + 5, lab, 13 if k < 5 else 14, "#ffffff", "bold", step=st)
    ly = 80 + k * 64
    x.rect(30, ly - 18, 26, 26, col, "#ffffff", 1, rx=4, step=st); x.icon(ic, 82, ly - 5, 30, step=st)
    x.text(104, ly - 6, lab, 13, INK, "bold", "start", step=st); x.text(104, ly + 10, sub, 12, INK, anchor="start", step=st)
    x.badge(st, 22, ly - 22, step=st)
x.circle(cx - 172, cy + 172, 16, "none", "#1f2933", 2.4, step=7); x.text(60, 540, "SGX enclave: ring 3 code whose memory is", 12, INK, "bold", "start", step=7)
x.text(60, 556, "sealed off from ring 0 and the hypervisor", 12, INK, anchor="start", step=7); x.raw(f'<line x1="{cx - 184}" y1="{cy + 184}" x2="200" y2="526" stroke="#52606d"/>', step=7)
x.rect(cx + 170, cy + 60, 80, 24, "none", "#1f2933", 2.2, rx=4, step=7, dash=True); x.text(780, 440, "Intel TDX trust domain: a confidential VM with", 12, INK, "bold", "start", step=7)
x.text(780, 456, "its own rings 3 and 0, sealed off from", 12, INK, anchor="start", step=7); x.text(780, 472, "the hypervisor and the host", 12, INK, anchor="start", step=7); x.raw(f'<line x1="{cx + 250}" y1="{cy + 72}" x2="776" y2="436" stroke="#52606d"/>', step=7)
x.badge(7, 50, 520, step=7)
x.text(780, 150, "Firmware TPM (Intel PTT, AMD fTPM) runs", 12, INK, "bold", "start", step=8); x.text(780, 166, "inside the security processor:", 12, INK, anchor="start", step=8); x.text(780, 182, "Intel CSME or AMD Secure Processor", 12, INK, anchor="start", step=8)
x.raw(f'<line x1="{cx + 40}" y1="{cy - 20}" x2="776" y2="160" stroke="#52606d"/>', step=8); x.badge(8, 762, 140, step=8)
x.rect(800, 270, 70, 40, "#eaecee", "#1f2933", 2, rx=4, step=9); x.text(835, 296, "TPM", 15, INK, "bold", step=9)
x.text(882, 286, "Discrete TPM: a separate", 12, INK, "bold", "start", step=9); x.text(882, 302, "chip outside the CPU rings", 12, INK, anchor="start", step=9); x.badge(9, 790, 262, step=9)
x.rect(cx + 108, cy + 24, 46, 18, "#ffffff", "#1f2933", 1.6, rx=3, step=10); x.text(cx + 131, cy + 37, "SEAM", 10, INK, "bold", step=10)
x.raw(f'<line x1="{cx + 154}" y1="{cy + 33}" x2="776" y2="366" stroke="#52606d"/>', step=10)
x.text(780, 362, "TDX module: runs in SEAM, a CPU mode", 12, INK, "bold", "start", step=10); x.text(780, 378, "beside the hypervisor's VMX root, not a new ring", 12, INK, anchor="start", step=10); x.badge(10, 762, 352, step=10)
x.text(550, 600, "Rings below 0 are informal names, not hardware ring numbers. Dashed outlines mark TEEs, which add isolation rather than rank.", 12, MUTED, italic=True, step=11)
x.save(OUT + "ch01_privilege_rings_x86_v2")

# Arm exception levels and TrustZone
a = Fig(1100, 680, "Arm exception levels and the TrustZone worlds",
        "Two half rings. The normal world on the left: EL0 applications, EL1 a rich operating system such as Linux, and EL2 the "
        "hypervisor. The secure world on the right: S-EL0 trusted applications, S-EL1 the trusted operating system or TEE, and on newer "
        "cores S-EL2, which isolates secure partitions. At the center, EL3 runs firmware and the secure monitor, always in the secure "
        "state, the most privileged level and the gatekeeper between the two worlds. The secure world can reach both worlds' memory; "
        "the normal world reaches only its own.")
cx, cy = 550, 340
def half(r, col, side, st):
    s = 1 if side == "R" else 0
    a.raw(f'<path d="M{cx} {cy - r} A{r} {r} 0 0 {s} {cx} {cy + r} Z" fill="{col}" stroke="#ffffff" stroke-width="3"/>', step=st)
levels = [(250, "#85b4ee", "#f0a070", "EL0", "S-EL0", "applications", "trusted applications", "desktop", "lock", 1),
          (190, "#5d9be6", "#ea6a35", "EL1", "S-EL1", "rich OS, such as Linux", "trusted OS, the TEE", "gear", "shield", 2),
          (130, "#2a78d6", "#c0501f", "EL2", "S-EL2", "hypervisor", "isolates secure\npartitions (newer cores)", "server", "nodes", 3)]
for r, cl, cr, ln, rn, ls, rs, il, ir, st in levels:
    half(r, cl, "L", st); half(r, cr, "R", st)
for r, cl, cr, ln, rn, ls, rs, il, ir, st in levels:
    y = cy - r + 30
    a.text(cx - 40, y, ln, 15, "#ffffff", "bold", step=st); a.text(cx + 40, y, rn, 15, "#ffffff", "bold", step=st)
    a.icon(il, cx - r + 32, cy, 30, step=st); a.icon(ir, cx + r - 32, cy, 30, step=st)
    a.text(cx - 284, cy - 160 + st * 100, ln + ": " + ls, 13, INK, "bold", "end", step=st)
    a.text(cx + 270, cy - 160 + st * 100, rn + ": " + rs, 13, INK, "bold", "start", step=st)
    a.badge(st, cx - 266, cy - 165 + st * 100, step=st)
a.circle(cx, cy, 70, "#8e3412", "#ffffff", 3, step=4); a.icon("key", cx, cy - 20, 34, step=4)
a.text(cx, cy + 14, "EL3", 15, "#ffffff", "bold", step=4); a.text(cx, cy + 32, "secure monitor", 11, "#ffffff", step=4)
a.badge(4, cx + 56, cy - 56, step=4)
a.text(cx - 125, 60, "Normal world", 16, BLUE, "bold", step=1); a.text(cx + 125, 60, "Secure world", 16, "#c0501f", "bold", step=1)
a.text(550, 630, "EL3, always in the secure state, is the most privileged level and the gatekeeper between the worlds.", 13, INK, "bold", step=5)
a.text(550, 654, "The secure world can reach both worlds' memory; the normal world reaches only its own.", 12, MUTED, italic=True, step=5)
a.save(OUT + "ch01_privilege_rings_arm_v2")
print("ok")
