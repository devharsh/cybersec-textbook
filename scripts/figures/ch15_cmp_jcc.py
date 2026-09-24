#!/usr/bin/env python3
"""Generate assets/figures/ch15_cmp_jcc.png for Chapter 15, Section 15.22.

How cmp and a conditional jump build a branch, traced on the worked example that compares 45 with
72. Left half: what the processor does. cmp subtracts, keeps no result, and leaves four decisive
flags; each jump reads only those flags. Right half: the branch those instructions build, drawn as
a basic block graph, with the path actually taken for 45 and 72 drawn solid.

Every value on the figure was measured, not assumed: gdb shows eflags 0x283 [ CF SF IF ] after the
cmp, jg falls through and jl goes to is_less, and the program exits with status 2.

The same figure appears on the COSC 332 week 5 slides, drawn by a twin of this script, because the
book and the decks carry the same pictures. Change both or neither.

Run from anywhere:  python3 scripts/figures/ch15_cmp_jcc.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "assets", "figures", "ch15_cmp_jcc.png"))
NAVY, INK, GREY, LIGHT = "#14284B", "#1F2937", "#6B7280", "#CBD5E1"
TAKEN, NOT = "#15803D", "#B91C1C"
CODE_FC, CODE_EC = "#EFF6FF", "#1D4ED8"
FLAG_FC, FLAG_EC = "#FEF3C7", "#B45309"
MONO = "DejaVu Sans Mono"
W, H = 8.10, 4.30


def rbox(ax, x, y, w, h, fc, ec, lw=1.1, ls="-"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.04",
                                fc=fc, ec=ec, lw=lw, ls=ls))


def arrow(ax, p, q, color, lw=1.4, ls="-", rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=10, color=color, lw=lw,
                                 ls=ls, connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0))


def code_block(ax, x, y, w, lines, active, line_h=0.155, pad=0.07):
    h = pad * 2 + line_h * len(lines)
    rbox(ax, x, y, w, h, CODE_FC if active else "#F9FAFB", CODE_EC if active else "#9CA3AF",
         lw=1.3 if active else 1.0, ls="-" if active else "--")
    for i, s in enumerate(lines):
        bold = s.endswith(":")
        ax.text(x + 0.09, y + h - pad - line_h * (i + 0.5), s, family=MONO, fontsize=7.6,
                va="center", ha="left", color=INK if active else GREY,
                weight="bold" if bold else "normal")
    return h


def figure():
    fig = plt.figure(figsize=(W, H), dpi=220)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    ax.text(W / 2, H - 0.15, "cmp sets the flags, and each jump reads them: comparing 45 with 72",
            ha="center", va="center", fontsize=10, weight="bold", color=NAVY)
    ax.plot([3.86, 3.86], [0.12, 3.92], color=LIGHT, lw=1.0)

    # ---------------------------------------------------------------- left: the mechanism
    ax.text(0.15, 3.84, "1.  What the processor does", fontsize=8.6, weight="bold", color=NAVY,
            va="center")
    rbox(ax, 0.15, 3.12, 3.55, 0.54, CODE_FC, CODE_EC, lw=1.3)
    ax.text(1.925, 3.475, "cmp  eax, ebx", family=MONO, fontsize=10.5, weight="bold",
            ha="center", va="center", color=INK)
    ax.text(1.925, 3.24, "eax holds 45 and ebx holds 72", fontsize=7.6, ha="center",
            va="center", color=INK)
    arrow(ax, (0.55, 3.10), (0.55, 2.86), NAVY)
    ax.text(0.68, 2.98, "computes 45 - 72 = -27, then discards the result", fontsize=7.6,
            va="center", color=INK)

    cells = [("ZF", "0", "not zero,\nso not equal"), ("SF", "1", "result\nis negative"),
             ("CF", "1", "borrow: 45 is\nbelow 72"), ("OF", "0", "no signed\noverflow")]
    cw, cy, ch = 0.83, 2.02, 0.80
    for i, (name, val, why) in enumerate(cells):
        cx = 0.15 + i * (cw + 0.076)
        rbox(ax, cx, cy, cw, ch, FLAG_FC, FLAG_EC)
        ax.text(cx + cw / 2, cy + ch - 0.13, name, fontsize=8.4, weight="bold", ha="center",
                va="center", color=FLAG_EC)
        ax.text(cx + cw / 2, cy + ch - 0.36, val, fontsize=14, weight="bold", ha="center",
                va="center", color=INK)
        ax.text(cx + cw / 2, cy + 0.16, why, fontsize=6.9, ha="center", va="center", color=INK,
                linespacing=1.05)
    ax.text(1.925, 1.90, "the four status flags a jump reads (cmp also updates AF and PF)", fontsize=7.2,
            ha="center", va="center", color=GREY, style="italic")
    arrow(ax, (0.55, 1.80), (0.55, 1.58), NAVY)
    ax.text(0.68, 1.69, "each jump reads only the flags, never eax or ebx", fontsize=7.6,
            va="center", color=INK)

    rules = [("jg", "taken when ZF = 0 and SF = OF", "SF is 1 and OF is 0: not taken", NOT),
             ("jl", "taken when SF ≠ OF", "1 ≠ 0: taken, to is_less", TAKEN)]
    for i, (op, cond, verdict, col) in enumerate(rules):
        by = 0.98 - i * 0.62
        rbox(ax, 0.15, by, 3.55, 0.54, "#FFFFFF", col, lw=1.3)
        ax.text(0.27, by + 0.36, op, family=MONO, fontsize=10, weight="bold", va="center",
                color=INK)
        ax.text(0.72, by + 0.36, cond, fontsize=7.9, va="center", color=INK)
        ax.text(0.72, by + 0.14, verdict, fontsize=7.9, va="center", color=col, weight="bold")

    # ---------------------------------------------------------------- right: the branch it builds
    ax.text(4.02, 3.84, "2.  The branch it builds, as a basic block graph", fontsize=8.6,
            weight="bold", color=NAVY, va="center")
    code_block(ax, 4.55, 2.93, 2.75, ["mov  eax, [num1]", "mov  ebx, [num2]", "cmp  eax, ebx",
                                        "jg   is_greater"], True)            # top 3.69
    code_block(ax, 4.02, 2.17, 1.62, ["jl   is_less"], True)                 # top 2.465
    code_block(ax, 6.42, 1.96, 1.55, ["is_greater:", "mov  edi, 1", "jmp  done"], False)
    code_block(ax, 4.02, 1.04, 1.45, ["is_equal:", "mov  edi, 0", "jmp  done"], False)
    code_block(ax, 5.62, 1.195, 1.45, ["is_less:", "mov  edi, 2"], True)     # top 1.645
    code_block(ax, 4.62, 0.20, 2.75, ["done:", "mov  eax, 60", "syscall      ; exit status 2"], True)

    # executed path, solid navy; the paths not taken this run, dashed grey
    arrow(ax, (4.83, 2.93), (4.83, 2.475), NAVY, lw=1.8)
    ax.text(4.90, 2.70, "jg not taken", fontsize=7.2, color=NAVY, va="center", weight="bold")
    arrow(ax, (7.05, 2.93), (7.05, 2.44), GREY, lw=1.1, ls="--")
    ax.text(7.12, 2.70, "jg taken", fontsize=7.2, color=GREY, va="center")
    arrow(ax, (5.30, 2.17), (6.05, 1.655), NAVY, lw=1.8)
    ax.text(5.78, 1.99, "jl taken", fontsize=7.2, color=NAVY, va="center", weight="bold")
    arrow(ax, (4.42, 2.17), (4.42, 1.565), GREY, lw=1.1, ls="--")
    ax.text(4.49, 1.86, "not taken", fontsize=7.2, color=GREY, va="center")
    arrow(ax, (4.95, 1.04), (5.20, 0.725), GREY, lw=1.1, ls="--")
    arrow(ax, (6.30, 1.195), (6.10, 0.725), NAVY, lw=1.8)
    arrow(ax, (7.60, 1.96), (7.20, 0.725), GREY, lw=1.1, ls="--")
    ax.text(7.97, 0.11, "solid: the path 45 and 72 take     dashed: paths not taken this run",
            fontsize=6.9, color=GREY, ha="right", va="center", style="italic")

    out = OUT
    fig.savefig(out, dpi=220)
    plt.close(fig)
    print("wrote", out)


if __name__ == "__main__":
    figure()
