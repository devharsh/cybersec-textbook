#!/usr/bin/env python3
"""Generate the three worked-example figures for Chapter 9, Section 9.27, from the gdb traces in
scripts/figures/data: assets/figures/ch09_example1_sp_tos_bp.png, ch09_example2_bp_chain.png and
ch09_example3_red_zone.png. The trace tables printed by --tables are the ones the section quotes.

Every number drawn or printed is read from a trace, and asserts check the facts the section states
in words, so a figure cannot drift away from its text. SP is the stack pointer, TOS the top of stack
(the slot SP points at) and BP the base pointer.

The same figures appear on the COSC 332 week 5 slides, drawn by a twin of this script from the same
traces. Change both or neither.

Run from anywhere:  python3 scripts/figures/ch09_worked_examples.py [--tables]
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon, FancyArrowPatch

HERE = os.path.dirname(os.path.abspath(__file__))
TR = os.environ.get("WE_TRACES", os.path.join(HERE, "data"))
OUTDIR = os.environ.get("WE_OUT", os.path.normpath(os.path.join(HERE, "..", "..", "assets", "figures")))
PREFIX = os.environ.get("WE_PREFIX", "ch09")
NAVY, INK, GREY = "#14284B", "#1F2937", "#6B7280"
SP_C, BP_C, CHG = "#1D4ED8", "#C2410C", "#B91C1C"
FILL = {"arg": ("#DBEAFE", "#1D4ED8"), "ret": ("#FEE2E2", "#B91C1C"), "bp": ("#FEF3C7", "#B45309"),
        "local": ("#DCFCE7", "#15803D"), "unused": ("#F3F4F6", "#9CA3AF"), "free": ("#FFFFFF", "#CBD5E1"),
        "caller": ("#F1F5F9", "#94A3B8"), "red": ("#FFF1F2", "#E11D48")}
MONO = "DejaVu Sans Mono"
W, H = 8.10, 4.30


def load(name):
    t = json.load(open(os.path.join(TR, name)))
    for s in t:
        s["r"] = {k: int(v, 16) for k, v in s["regs"].items()}
        s["m"] = {int(k, 16): v for k, v in s["stack"].items()}
    return t


def at(t, pc):
    hits = [s for s in t if int(s["pc"], 16) == pc]
    assert len(hits) == 1, (hex(pc), len(hits))
    return hits[0]


def after(t, pc):
    """The state right after the instruction at pc ran: the next state in the trace."""
    i = [k for k, s in enumerate(t) if int(s["pc"], 16) == pc]
    assert len(i) == 1, hex(pc)
    return t[i[0] + 1]


def word(s, addr, size=4):
    """Read a 4-byte value out of the trace's stack words (4- or 8-byte words)."""
    for base, v in s["m"].items():
        span = 8 if max(s["m"]) - min(s["m"]) > 0 and all((a - min(s["m"])) % 8 == 0 for a in s["m"]) else 4
        if base <= addr < base + span:
            off = addr - base
            return (v >> (8 * off)) & ((1 << (8 * size)) - 1)
    raise KeyError(hex(addr))


def tidy(insn):
    s = insn.replace("DWORD PTR ", "").replace("QWORD PTR ", "").replace(",", ", ")
    s = s.split(" <")[0]
    for a, b in (("call   ", "call "), ("0x8049017", "add3"), ("0x8049013", "add3"), ("0x804902f", "twice"),
                 ("0x40101d", "add3")):
        s = s.replace(a, b)
    parts = s.split()
    if parts and parts[0] == "call" and len(parts) > 1 and parts[1].startswith("0x"):
        pass
    return " ".join(parts).replace("push 0x", "push ").replace("[ebp+0x8]", "[ebp+8]").replace("[ebp-0x4]", "[ebp-4]")


def box(ax, x, y, w, h, kind, text="", dashed=False, bold=False, fs=6.6, tc=INK):
    fc, ec = FILL[kind]
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.02", fc=fc, ec=ec,
                                lw=0.9, ls="--" if dashed else "-"))
    if text:
        ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=fs, color=tc,
                family=MONO, weight="bold" if bold else "normal")


def tri_right(ax, x, yc, color, s=0.055):
    ax.add_patch(Polygon([[x - s * 1.3, yc - s], [x - s * 1.3, yc + s], [x, yc]], closed=True, fc=color, ec="none"))


def tri_left(ax, x, yc, color, s=0.055):
    ax.add_patch(Polygon([[x + s * 1.3, yc - s], [x + s * 1.3, yc + s], [x, yc]], closed=True, fc=color, ec="none"))


# ------------------------------------------------------------------------------------ example 1
def ex1_facts():
    t = load("trace_ex1_add3_32.json")
    call_pc, entry = 0x8049006, 0x8049017
    s_call = after(t, call_pc)
    assert s_call["r"]["eip"] == entry
    assert s_call["m"][s_call["r"]["esp"]] == 0x804900b, "TOS after call is the return address"
    s_mov = after(t, 0x8049018)
    assert s_mov["r"]["esp"] == s_mov["r"]["ebp"], "after mov ebp, esp both point at the saved ebp"
    bp = s_mov["r"]["ebp"]
    s_leave_before = at(t, 0x8049031)
    assert word(s_leave_before, bp - 4) == 6 and s_leave_before["r"]["eax"] == 6
    assert [word(s_leave_before, bp + k) for k in (8, 12, 16)] == [1, 2, 3]
    assert word(s_leave_before, bp + 4) == 0x804900b and word(s_leave_before, bp) == 0
    s_after_leave = after(t, 0x8049031)
    assert s_after_leave["r"]["esp"] == bp + 4 and s_after_leave["r"]["ebp"] == 0
    assert word(s_after_leave, bp - 4) == 6, "the released local still holds 6"
    s_after_ret = after(t, 0x8049032)
    assert s_after_ret["r"]["eip"] == 0x804900b and s_after_ret["r"]["esp"] == bp + 8
    return t, bp


def ex1_table(t):
    lines = ["; add3(1, 2, 3), 32-bit, gcc -m32 -O0: registers after each instruction",
             "; addr     instruction           esp       ebp       eax  edx  [ebp-4]  TOS"]
    for i, s in enumerate(t[:-1]):
        n = t[i + 1]
        r = n["r"]
        bpv = r["ebp"]
        loc = str(word(n, bpv - 4)) if bpv else "-"
        tos = n["m"].get(r["esp"])
        lines.append(f"  {s['pc']:>8}  {tidy(s['insn']):<20}  {r['esp']:08x}  {r['ebp']:08x}  {r['eax']:<3}  "
                     f"{r['edx']:<3}  {loc:<7}  {tos:08x}")
    return lines


def marker(ax, x_right, yc, text, color, dy=0.0):
    """A right-pointing triangle ending at x_right, with its label to the left of it."""
    tri_right(ax, x_right, yc + dy, color, s=0.048)
    ax.text(x_right - 0.085, yc + dy, text, ha="right", va="center", fontsize=6.2, weight="bold", color=color)


def ex1_figure(t, bp):
    slots = [bp + 16, bp + 12, bp + 8, bp + 4, bp, bp - 4, bp - 8, bp - 12, bp - 16]
    role = {bp + 16: ("arg", "arg 3 = {v}"), bp + 12: ("arg", "arg 2 = {v}"), bp + 8: ("arg", "arg 1 = {v}"),
            bp + 4: ("ret", "ret {v:08x}"), bp: ("bp", "saved ebp {v}"), bp - 4: ("local", "sum = {v}")}
    moments = [("1", "call add3", after(t, 0x8049006), "call pushed the return address", False),
               ("2", "mov ebp, esp", after(t, 0x8049018), "BP now anchors the frame", False),
               ("3", "mov eax, [ebp-4]", after(t, 0x804902e), "body done, eax = 6", False),
               ("4", "leave", after(t, 0x8049031), "released, not erased", True)]
    fig = plt.figure(figsize=(W, H), dpi=220)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    ax.text(W / 2, H - 0.13, "Worked example 1: add3(1, 2, 3), 32-bit. SP, TOS and BP at four moments",
            ha="center", va="center", fontsize=9.6, weight="bold", color=NAVY)
    pw = W / 4
    prev = at(t, 0x8049006)
    for k, (num, instr, s, note, released) in enumerate(moments):
        x0 = k * pw
        esp, ebp = s["r"]["esp"], s["r"]["ebp"]
        ax.add_patch(FancyBboxPatch((x0 + 0.05, 0.08), pw - 0.10, H - 0.36, boxstyle="round,pad=0,rounding_size=0.05",
                                    fc="#FFFFFF", ec="#E5E7EB", lw=0.8))
        ax.text(x0 + pw / 2, H - 0.40, f"{num}.  after", ha="center", va="center", fontsize=7.4, color=GREY)
        ax.text(x0 + pw / 2, H - 0.58, instr, ha="center", va="center", fontsize=8.2, family=MONO, weight="bold", color=INK)
        ax.text(x0 + pw / 2, H - 0.76, note, ha="center", va="center", fontsize=6.9, color=GREY, style="italic")
        top, rh = H - 0.93, 0.245
        ax_addr, cx, cw = x0 + 0.86, x0 + 0.90, 1.02
        for j, a in enumerate(slots):
            y = top - (j + 1) * rh
            yc = y + rh / 2
            ax.text(ax_addr, yc, f"{a & 0xffff:04x}", ha="right", va="center", fontsize=6.1, family=MONO, color=GREY)
            kind, fmt = role.get(a, ("unused", "{v}"))
            v = word(s, a)
            if a >= esp:
                box(ax, cx, y + 0.02, cw, rh - 0.04, kind, fmt.format(v=v), fs=6.2,
                    tc=INK if kind != "unused" else GREY)
            elif released and a in role:
                box(ax, cx, y + 0.02, cw, rh - 0.04, "free", fmt.format(v=v), dashed=True, fs=6.2, tc="#94A3B8")
            else:
                box(ax, cx, y + 0.02, cw, rh - 0.04, "free", "", dashed=True)
            same = (a == esp and a == ebp)
            if a == esp:
                marker(ax, ax_addr - 0.31, yc, "SP, TOS", SP_C, dy=0.058 if same else 0.0)
            if a == ebp:
                marker(ax, ax_addr - 0.31, yc, "BP", BP_C, dy=-0.058 if same else 0.0)
        if ebp == 0:
            ax.text(cx + cw / 2 - 0.25, top - 9 * rh - 0.10, "BP = 0, outside the stack", ha="center", va="center",
                    fontsize=6.3, color=BP_C, weight="bold")
        ry = 0.20
        ax.add_patch(FancyBboxPatch((x0 + 0.20, ry), pw - 0.40, 0.76, boxstyle="round,pad=0,rounding_size=0.04",
                                    fc="#F8FAFC", ec="#CBD5E1", lw=0.8))
        for i, n in enumerate(("eip", "esp", "ebp", "eax")):
            v = s["r"][n]
            changed = prev["r"][n] != v
            ax.text(x0 + 0.34, ry + 0.64 - i * 0.16, n, ha="left", va="center", fontsize=7.0, family=MONO, color=GREY)
            ax.text(x0 + pw - 0.34, ry + 0.64 - i * 0.16, f"{v:08x}", ha="right", va="center", fontsize=7.0,
                    family=MONO, color=CHG if changed else INK, weight="bold" if changed else "normal")
        prev = s
    ax.text(W / 2, 0.035, "Red register values changed since the panel before (panel 1 compares with the moment before the call).",
            ha="center", va="bottom", fontsize=6.2, color=GREY)
    out = os.path.join(OUTDIR, f"{PREFIX}_example1_sp_tos_bp.png")
    fig.savefig(out, dpi=220); plt.close(fig)
    return out


# ------------------------------------------------------------------------------------ example 2
def ex2_facts():
    t = load("trace_ex2_nested_32.json")
    in_twice = after(t, 0x8049030)          # after twice's mov ebp, esp
    bp_twice = in_twice["r"]["ebp"]
    s = at(t, 0x804902d)                    # inside add3, just before its leave
    bp_add3 = s["r"]["ebp"]
    assert word(s, bp_add3) == bp_twice, "add3's saved ebp is twice's ebp"
    assert word(s, bp_twice) == 0, "twice's saved ebp is 0, the end of the chain"
    assert word(s, bp_add3 + 4) == 0x8049042 and word(s, bp_twice + 4) == 0x8049007
    assert [word(s, bp_add3 + k) for k in (8, 12, 16)] == [5, 5, 0]
    assert word(s, bp_add3 - 4) == 10 and s["r"]["eax"] == 10
    return t, s, bp_twice, bp_add3


def ex2_table(t):
    keep = {0x8049000, 0x8049002, 0x804902f, 0x8049030, 0x8049032, 0x8049035, 0x8049037, 0x804903a, 0x804903d,
            0x8049013, 0x8049014, 0x8049016, 0x804902d, 0x804902e, 0x8049042, 0x8049045, 0x8049048, 0x804904b,
            0x804904c, 0x8049007}
    lines = ["; twice(5) calls add3(5, 5, 0), 32-bit: registers after each instruction",
             "; addr     instruction           esp       ebp       eax  TOS"]
    skipped = False
    for i, s in enumerate(t[:-1]):
        pc = int(s["pc"], 16)
        if pc not in keep:
            if not skipped:
                lines.append("  ...       add3's body: sum = 5 + 5 + 0 = 10 at [ebp-4]")
                skipped = True
            continue
        r = t[i + 1]["r"]
        tos = t[i + 1]["m"].get(r["esp"])
        lines.append(f"  {s['pc']:>8}  {tidy(s['insn']):<20}  {r['esp']:08x}  {r['ebp']:08x}  {r['eax']:<3x}  {tos:08x}")
    return lines


def ex2_figure(t, s, bp_twice, bp_add3):
    esp = s["r"]["esp"]
    addrs = list(range(bp_twice + 8, esp - 4, -4))
    label = {bp_twice + 8: ("arg", "x = 5, twice's argument"), bp_twice + 4: ("ret", "return into _start"),
             bp_twice: ("bp", "twice's saved ebp"), bp_twice - 4: ("local", "twice's r"),
             bp_add3 + 16: ("arg", "c = 0"), bp_add3 + 12: ("arg", "b = 5"), bp_add3 + 8: ("arg", "a = 5"),
             bp_add3 + 4: ("ret", "return into twice"), bp_add3: ("bp", "add3's saved ebp"),
             bp_add3 - 4: ("local", "add3's sum")}
    fig = plt.figure(figsize=(W, H), dpi=220)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    ax.text(W / 2, H - 0.13, "Worked example 2: twice(5) calls add3(5, 5, 0). Two frames, one chain of saved BPs",
            ha="center", va="center", fontsize=9.4, weight="bold", color=NAVY)
    ax.text(W / 2, H - 0.32, "32-bit, inside add3 just before its leave; every value read from the gdb trace",
            ha="center", va="center", fontsize=7.0, color=GREY, style="italic")
    top, rh = H - 0.46, 0.205
    ax_addr, cx, cw = 2.05, 2.12, 1.25
    lane = cx + cw + 0.55
    rows = {}
    for j, a in enumerate(addrs):
        y = top - (j + 1) * rh
        rows[a] = y + rh / 2
        kind, text = label.get(a, ("unused", ""))
        v = word(s, a)
        shown = f"{v:08x}" if kind in ("ret", "bp") else (str(v) if kind in ("arg", "local") else "")
        ax.text(ax_addr, y + rh / 2, f"{a:08x}", ha="right", va="center", fontsize=6.3, family=MONO, color=GREY)
        box(ax, cx, y + 0.017, cw, rh - 0.034, kind, shown, fs=6.8)
        if text:
            ax.text(lane + 0.05, y + rh / 2, text, ha="left", va="center", fontsize=6.7, color=INK)
    def bracket(a_hi, a_lo, name, color):
        y1, y2 = rows[a_hi] + rh / 2 - 0.02, rows[a_lo] - rh / 2 + 0.02
        x = 0.42
        ax.plot([x + 0.06, x, x, x + 0.06], [y1, y1, y2, y2], color=color, lw=1.3)
        ax.text(x - 0.06, (y1 + y2) / 2, name, ha="right", va="center", fontsize=7.0, color=color, weight="bold", rotation=90)
    bracket(bp_twice + 4, bp_add3 + 8, "twice's frame", "#7C3AED")
    bracket(bp_add3 + 4, esp, "add3's frame", "#0F766E")
    marker(ax, ax_addr - 0.62, rows[esp], "SP, TOS", SP_C)
    marker(ax, ax_addr - 0.62, rows[bp_add3], "BP", BP_C)
    ax.add_patch(FancyArrowPatch((cx + cw + 0.03, rows[bp_add3]), (cx + cw + 0.03, rows[bp_twice]),
                                 connectionstyle="arc3,rad=0.35", arrowstyle="-|>", mutation_scale=10,
                                 color=BP_C, lw=1.5))
    rx, ry = 5.95, 0.50
    ax.add_patch(FancyBboxPatch((rx, ry), 1.95, 1.05, boxstyle="round,pad=0,rounding_size=0.04", fc="#F8FAFC",
                                ec="#CBD5E1", lw=0.8))
    for i, (n, v) in enumerate((("eip", s["r"]["eip"]), ("esp", esp), ("ebp", bp_add3), ("eax", s["r"]["eax"]))):
        ax.text(rx + 0.15, ry + 0.87 - i * 0.215, n, ha="left", va="center", fontsize=7.4, family=MONO, color=GREY)
        ax.text(rx + 1.80, ry + 0.87 - i * 0.215, f"{v:08x}", ha="right", va="center", fontsize=7.4, family=MONO, color=INK)
    ax.text(rx + 0.975, ry + 1.19, "registers at this moment", ha="center", va="center", fontsize=6.8, color=GREY)
    ax.text(rx + 0.975, 3.45, "Walk the chain by hand:", ha="center", va="center", fontsize=7.2, color=BP_C, weight="bold")
    ax.text(rx + 0.975, 3.02, f"ebp = {bp_add3:08x}\n[{bp_add3:08x}] = {bp_twice:08x}\n[{bp_twice:08x}] = 00000000",
            ha="center", va="center", fontsize=6.9, family=MONO, color=BP_C, linespacing=1.4)
    ax.text(rx + 0.975, 2.42, "Each saved ebp holds the caller's\nebp, so the saved values link the\nframes; a zero ends the chain.",
            ha="center", va="center", fontsize=6.6, color=GREY, linespacing=1.3)
    out = os.path.join(OUTDIR, f"{PREFIX}_example2_bp_chain.png")
    fig.savefig(out, dpi=220); plt.close(fig)
    return out


# ------------------------------------------------------------------------------------ example 3
def ex3_facts():
    t = load("trace_ex3_add3_64.json")
    s = at(t, 0x40103e)                     # just before pop rbp: body done
    rsp, rbp = s["r"]["rsp"], s["r"]["rbp"]
    assert rsp == rbp, "the leaf never moved rsp below its saved rbp"
    q = lambda a: word(s, a, 4)
    assert q(rbp - 0x4) == 6 and q(rbp - 0x14) == 1 and q(rbp - 0x18) == 2 and q(rbp - 0x1c) == 3
    assert word(s, rbp + 8, 8) == 0x401014 and word(s, rbp, 8) == 0
    assert s["r"]["rax"] == 6
    return t, s


def ex3_table(t):
    lines = ["; add3(1, 2, 3), 64-bit System V, gcc -O0: registers after each instruction",
             "; addr    instruction            rsp           rbp           edi esi edx eax"]
    for i, s in enumerate(t[:-1]):
        r = t[i + 1]["r"]
        lines.append(f"  {s['pc']:>6}  {tidy(s['insn']):<21}  {r['rsp']:012x}  {r['rbp']:012x}  "
                     f"{r['rdi'] & 0xffffffff:<3} {r['rsi'] & 0xffffffff:<3} {r['rdx'] & 0xffffffff:<3} {r['rax'] & 0xffffffff:<3}")
    return lines


def ex3_figure(t, s):
    rsp, rbp = s["r"]["rsp"], s["r"]["rbp"]
    fig = plt.figure(figsize=(W, H), dpi=220)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    ax.text(W / 2, H - 0.13, "Worked example 3: add3(1, 2, 3), 64-bit. The leaf keeps its data below SP",
            ha="center", va="center", fontsize=9.6, weight="bold", color=NAVY)
    ax.text(W / 2, H - 0.32, "just before pop rbp; arguments arrived in edi, esi and edx, and rsp never moved",
            ha="center", va="center", fontsize=7.0, color=GREY, style="italic")
    rows = [(rbp + 8, 8, "ret", f"{word(s, rbp + 8, 8):016x}", "return address"),
            (rbp, 8, "bp", f"{word(s, rbp, 8):016x}", "saved rbp"),
            (rbp - 0x4, 4, "local", str(word(s, rbp - 0x4, 4)), "[rbp-0x4]  sum"),
            (rbp - 0x8, 4, "unused", "", ""), (rbp - 0xc, 4, "unused", "", ""), (rbp - 0x10, 4, "unused", "", ""),
            (rbp - 0x14, 4, "arg", str(word(s, rbp - 0x14, 4)), "[rbp-0x14]  a, spilled from edi"),
            (rbp - 0x18, 4, "arg", str(word(s, rbp - 0x18, 4)), "[rbp-0x18]  b, spilled from esi"),
            (rbp - 0x1c, 4, "arg", str(word(s, rbp - 0x1c, 4)), "[rbp-0x1c]  c, spilled from edx")]
    top, rh, cx, cw = H - 0.52, 0.30, 2.25, 1.75
    ymap = {}
    for j, (a, size, kind, txt, lab) in enumerate(rows):
        y = top - (j + 1) * rh
        ymap[a] = y + rh / 2
        ax.text(cx - 0.08, y + rh / 2, f"{a:012x}", ha="right", va="center", fontsize=6.6, family=MONO, color=GREY)
        box(ax, cx, y + 0.025, cw, rh - 0.05, kind, txt, fs=7.0)
        if lab:
            ax.text(cx + cw + 0.14, y + rh / 2, lab, ha="left", va="center", fontsize=7.0, color=INK, family=MONO if lab.startswith("[") else None)
    # red zone band: everything below rsp
    y_top_red = ymap[rbp - 0x4] + rh / 2 + 0.01
    y_bot_red = ymap[rbp - 0x1c] - rh / 2 - 0.01
    ax.add_patch(FancyBboxPatch((cx - 1.68, y_bot_red), 0.26, y_top_red - y_bot_red, boxstyle="round,pad=0,rounding_size=0.03",
                                fc=FILL["red"][0], ec=FILL["red"][1], lw=1.0))
    ax.text(cx - 1.55, (y_top_red + y_bot_red) / 2, "red zone: below SP", rotation=90, ha="center", va="center",
            fontsize=7.0, color=FILL["red"][1], weight="bold")
    marker(ax, cx - 1.02, ymap[rbp], "SP, TOS", SP_C, dy=0.07)
    marker(ax, cx - 1.02, ymap[rbp], "BP", BP_C, dy=-0.07)
    rx, ry = 6.15, 0.35
    ax.add_patch(FancyBboxPatch((rx, ry), 1.80, 1.50, boxstyle="round,pad=0,rounding_size=0.04", fc="#F8FAFC",
                                ec="#CBD5E1", lw=0.8))
    for i, (n, v) in enumerate((("rip", s["r"]["rip"]), ("rsp", rsp), ("rbp", rbp), ("edi", s["r"]["rdi"]),
                                ("esi", s["r"]["rsi"]), ("edx", s["r"]["rdx"]), ("eax", s["r"]["rax"]))):
        vv = (f"{v:x}" if n == "rip" else f"{v:012x}") if n in ("rip", "rsp", "rbp") else str(v & 0xffffffff)
        ax.text(rx + 0.12, ry + 1.36 - i * 0.19, n, ha="left", va="center", fontsize=7.0, family=MONO, color=GREY)
        ax.text(rx + 1.68, ry + 1.36 - i * 0.19, vv, ha="right", va="center", fontsize=7.0, family=MONO, color=INK)
    ax.text(0.25, 0.30, "The System V ABI keeps the 128 bytes below rsp safe from signal and interrupt handlers, "
            "so a leaf function\nmay skip sub rsp. A function that calls another must move rsp first, or the call "
            "would overwrite this data.", fontsize=6.7, color=GREY, va="center")
    out = os.path.join(OUTDIR, f"{PREFIX}_example3_red_zone.png")
    fig.savefig(out, dpi=220); plt.close(fig)
    return out


def main():
    t1, bp1 = ex1_facts()
    t2, s2, bpt, bpa = ex2_facts()
    t3, s3 = ex3_facts()
    print("facts: all asserts hold")
    if "--check" in sys.argv:
        return
    tables = {"ex1": ex1_table(t1), "ex2": ex2_table(t2), "ex3": ex3_table(t3)}
    if "--tables" in sys.argv:
        for k, v in tables.items():
            print(f"\n[{k}]")
            print("\n".join(v))
    for f in (ex1_figure(t1, bp1), ex2_figure(t2, s2, bpt, bpa), ex3_figure(t3, s3)):
        print("wrote", f)


if __name__ == "__main__":
    main()
