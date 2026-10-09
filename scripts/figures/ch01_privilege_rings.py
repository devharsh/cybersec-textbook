#!/usr/bin/env python3
"""Generate the two privilege-level figures for Chapter 1, Section 1.6.

assets/figures/ch01_privilege_rings_x86.png
    The x86 protection rings as concentric disks, innermost most privileged: ring 3 (user
    applications), rings 2 and 1 (rarely used), ring 0 (operating-system kernel), and the
    informal negative rings below it: ring -1 (hypervisor), ring -2 (System Management Mode
    firmware) and ring -3 (the platform security processor, Intel CSME or the AMD Secure
    Processor). Callouts place the two components readers look for and that are not rings:
    trusted execution environments (an SGX enclave runs in ring 3 but is sealed off from ring 0
    and the hypervisor; an Intel TDX trust domain is a whole guest with its own rings 3 and 0,
    drawn as a dashed band across them, sealed off from the hypervisor and host, while the TDX
    module runs in Secure Arbitration Mode, SEAM, a mode beside the hypervisor's VMX root rather
    than a new ring) and TPMs (a firmware TPM runs inside the security processor; a discrete TPM
    is a separate chip).

assets/figures/ch01_privilege_rings_arm.png
    Arm exception levels as concentric disks split into the TrustZone normal world (left) and
    secure world (right), with EL3, the secure monitor, at the center as the most privileged
    level and the gatekeeper between the worlds.

Sources for every label are cited in Section 1.6 and its reference list: Tereshkin and
Wojtczuk (2009) and Domas (2015) for the negative rings; Intel (2022) for PTT in the CSME;
Buhren and Eichner (2020) for the AMD Secure Processor and its firmware TPM; Costan and
Devadas (2016) for SGX; Cheng et al. (2023) for TDX and SEAM; Arm's AArch64 Exception Model guide,
the SMC Calling Convention and Mann (2018) for the exception levels and TrustZone.

Colors: one blue ordinal ramp for the processor's own rings and one orange ordinal ramp for
the levels below ring 0 (x86) or the secure world (Arm); both ramps pass the dataviz
validator's ordinal checks (monotone lightness, visible steps, light end at least 2:1).

Run from anywhere:  python3 scripts/figures/ch01_privilege_rings.py
"""

import math
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, FancyBboxPatch, Polygon, Wedge

DPI = 200
FIGSIZE = (9.6, 7.0)
OUTDIR = pathlib.Path(__file__).resolve().parents[2] / "assets" / "figures"

INK, MUTED, SURFACE = "#0b0b0b", "#52514e", "#ffffff"
BLUE = ["#86b6ef", "#5598e7", "#2a78d6"]                 # ring 3, rings 2 and 1, ring 0
ORANGE = ["#f0956a", "#eb6834", "#c24f1f", "#8f3510"]    # ring -1, ring -2, (Arm S-EL2), ring -3 / EL3
GAP = 2.2                                                # white spacer between bands, in points


def band(ax, r_out, width, color, theta1=0, theta2=360):
    ax.add_patch(Wedge((0, 0), r_out, theta1, theta2, width=width, facecolor=color,
                       edgecolor=SURFACE, linewidth=GAP))


def label(ax, x, y, text, color=INK, size=8.6, weight="normal", ha="center"):
    ax.text(x, y, text, ha=ha, va="center", fontsize=size, color=color, fontweight=weight,
            linespacing=1.15)


def callout(ax, xy_mark, xy_text, text, ha="left"):
    ax.annotate(text, xy=xy_mark, xytext=xy_text, ha=ha, va="center", fontsize=8.4, color=INK,
                linespacing=1.25,
                arrowprops=dict(arrowstyle="-", color=MUTED, lw=0.9, shrinkA=2, shrinkB=0))
    ax.add_patch(Circle(xy_mark, 0.045, facecolor=INK, edgecolor="none", zorder=5))


def x86_figure():
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.set_xlim(-6.3, 6.6)
    ax.set_ylim(-4.6, 4.35)
    ax.set_aspect("equal")
    ax.axis("off")

    # (outer radius, width, color, two-line label, text color)
    rings = [
        (3.55, 0.56, BLUE[0], "Ring 3\nuser applications", INK),
        (2.99, 0.24, BLUE[1], "Ring 2", INK),
        (2.75, 0.24, BLUE[1], "Ring 1", INK),
        (2.51, 0.58, BLUE[2], "Ring 0\nkernel", SURFACE),
        (1.93, 0.58, ORANGE[0], "Ring -1\nhypervisor", INK),
        (1.35, 0.55, ORANGE[1], "Ring -2\nSMM firmware", INK),
    ]
    for r_out, w, color, text, tcolor in rings:
        band(ax, r_out, w, color)
        size = 7.2 if w < 0.3 else 8.6
        label(ax, 0, r_out - w / 2, text, color=tcolor, size=size)
    ax.add_patch(Circle((0, 0), 0.80, facecolor=ORANGE[3], edgecolor=SURFACE, linewidth=GAP))
    label(ax, 0, 0.0, "Ring -3\nsecurity\nprocessor", color=SURFACE, size=8.4)

    ax.text(0, 4.15, "x86 protection rings: the innermost level is the most privileged",
            ha="center", va="center", fontsize=11.5, color=INK)

    # rings 1 and 2
    callout(ax, (-2.65 * 0.866, 2.65 * 0.5), (-6.15, 2.85),
            "Rings 1 and 2: defined by the\nhardware, rarely used by\nmainstream operating systems")
    # SGX enclave inside ring 3
    ex, ey = -3.25 * 0.766, -3.25 * 0.643
    ax.add_patch(Circle((ex, ey), 0.2, facecolor=SURFACE, edgecolor=INK, linewidth=1.4,
                        linestyle=(0, (2, 1.2)), zorder=4))
    callout(ax, (ex - 0.2, ey), (-6.15, -3.0),
            "TEE (Intel SGX enclave): runs as\nring 3 code, yet its memory is\nsealed off from ring 0 and\nthe hypervisor")
    # Intel TDX: a trust domain is a guest with its own rings 3 to 0, drawn as a dashed band across
    # them; the TDX module runs in SEAM, a mode beside the hypervisor's VMX root, not a new ring.
    th = math.radians(-16)
    ux, uy = math.cos(th), math.sin(th)
    px, py = -uy, ux
    r1, r2, half = 1.97, 3.50, 0.13
    band_pts = [(r1 * ux + half * px, r1 * uy + half * py), (r2 * ux + half * px, r2 * uy + half * py),
                (r2 * ux - half * px, r2 * uy - half * py), (r1 * ux - half * px, r1 * uy - half * py)]
    ax.add_patch(Polygon(band_pts, closed=True, facecolor=(1, 1, 1, 0.45), edgecolor=INK,
                         linewidth=1.4, linestyle=(0, (2, 1.2)), zorder=4))
    callout(ax, (3.42 * ux, 3.42 * uy), (4.0, -0.30),
            "Intel TDX trust domain: a confidential\nVM with its own rings 3 and 0,\nsealed off from the hypervisor\nand the host")
    sx, sy = 1.63 * math.cos(math.radians(-42)), 1.63 * math.sin(math.radians(-42))
    ax.add_patch(FancyBboxPatch((sx - 0.23, sy - 0.11), 0.46, 0.22, boxstyle="round,pad=0.02",
                                facecolor=SURFACE, edgecolor=INK, linewidth=1.1, zorder=4))
    ax.text(sx, sy, "SEAM", ha="center", va="center", fontsize=6.6, color=INK, fontweight="bold",
            zorder=6)
    callout(ax, (sx + 0.25, sy), (4.0, -1.62),
            "TDX module: runs in SEAM, a CPU\nmode beside the hypervisor's\nVMX root, not a new ring")
    # firmware TPM in the security processor
    callout(ax, (0.56, 0.18), (4.0, 1.35),
            "Firmware TPM (Intel PTT,\nAMD fTPM) runs inside the\nsecurity processor:\nIntel CSME or AMD Secure\nProcessor")
    # discrete TPM, a separate chip outside the rings
    ax.add_patch(FancyBboxPatch((4.0, -3.7), 0.9, 0.62, boxstyle="round,pad=0.04",
                                facecolor="#e9e8e4", edgecolor=MUTED, linewidth=1.2))
    label(ax, 4.45, -3.39, "TPM", size=8.6, weight="bold")
    ax.text(5.1, -3.39, "Discrete TPM: a separate\nchip on the board, outside\nthe CPU rings",
            ha="left", va="center", fontsize=8.4, color=INK, linespacing=1.25)
    ax.text(0, -4.3, "Rings below 0 are informal names, not hardware ring numbers. Dashed outlines mark\n"
            "trusted execution environments, which add isolation rather than a higher rank.",
            ha="center", va="center", fontsize=8.2, color=MUTED, linespacing=1.3)

    out = OUTDIR / "ch01_privilege_rings_x86.png"
    fig.savefig(out, dpi=DPI, bbox_inches="tight", pad_inches=0.12, facecolor=SURFACE)
    plt.close(fig)
    print(f"wrote {out}")


def arm_figure():
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.set_xlim(-6.2, 6.2)
    ax.set_ylim(-4.0, 4.25)
    ax.set_aspect("equal")
    ax.axis("off")

    levels = [  # outer radius, width, normal-world color, secure-world color, tags
        (3.40, 0.80, BLUE[0], ORANGE[0], "EL0", "S-EL0"),
        (2.60, 0.80, BLUE[1], ORANGE[1], "EL1", "S-EL1"),
        (1.80, 0.75, BLUE[2], ORANGE[2], "EL2", "S-EL2"),
    ]
    for r_out, w, cn, cs, tn, ts in levels:
        band(ax, r_out, w, cn, 90, 270)     # normal world on the left
        band(ax, r_out, w, cs, -90, 90)     # secure world on the right
        mid = r_out - w / 2
        light = cn == BLUE[0] or cn == BLUE[1]
        label(ax, -0.62, mid * 0.92, tn, color=INK if light else SURFACE, size=8.6, weight="bold")
        label(ax, 0.62, mid * 0.92, ts, color=INK if cs != ORANGE[2] else SURFACE, size=8.6,
              weight="bold")
    ax.add_patch(Circle((0, 0), 1.05, facecolor=ORANGE[3], edgecolor=SURFACE, linewidth=GAP))
    label(ax, 0, 0, "EL3\nsecure\nmonitor", color=SURFACE, size=8.6)

    ax.text(0, 4.05, "Arm exception levels and the TrustZone worlds", ha="center", va="center",
            fontsize=11.5, color=INK)
    ax.text(-1.75, 3.62, "Normal world", ha="center", va="center", fontsize=9.6, color=INK,
            fontweight="bold")
    ax.text(1.75, 3.62, "Secure world", ha="center", va="center", fontsize=9.6, color=INK,
            fontweight="bold")

    def at(r, deg):
        import math
        return (r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg)))

    callout(ax, at(3.0, 200), (-5.95, -0.55), "EL0: applications")
    callout(ax, at(2.2, 215), (-5.95, -1.55), "EL1: rich operating\nsystem, such as Linux")
    callout(ax, at(1.42, 235), (-5.95, -2.75), "EL2: hypervisor")
    callout(ax, at(3.0, -20), (3.75, -0.55), "S-EL0: trusted applications")
    callout(ax, at(2.2, -35), (3.75, -1.55), "S-EL1: trusted operating\nsystem, the TEE")
    callout(ax, at(1.42, -55), (3.75, -2.75), "S-EL2 (newer cores):\nisolates secure partitions")
    callout(ax, at(0.55, 160), (-5.95, 1.55), "EL3: firmware and secure\nmonitor, always in Secure\nstate, the most privileged\nlevel and the gatekeeper\nbetween the two worlds")
    ax.text(0, -3.82, "The secure world can reach both worlds' memory; the normal world reaches only its own.",
            ha="center", va="center", fontsize=8.2, color=MUTED)

    out = OUTDIR / "ch01_privilege_rings_arm.png"
    fig.savefig(out, dpi=DPI, bbox_inches="tight", pad_inches=0.12, facecolor=SURFACE)
    plt.close(fig)
    print(f"wrote {out}")


if __name__ == "__main__":
    OUTDIR.mkdir(parents=True, exist_ok=True)
    x86_figure()
    arm_figure()
