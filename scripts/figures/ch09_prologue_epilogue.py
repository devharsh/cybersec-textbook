#!/usr/bin/env python3
"""Generate assets/figures/ch09_prologue_epilogue.png for Chapter 9, Section 9.27.

The prologue and epilogue of a 32-bit cdecl function, one instruction at a time: nine snapshots of
the same nine stack slots, from the moment before the call to the moment after the caller removes
its arguments. Every address and value is read from data/trace_ex1_add3_32.json, a gdb trace of
add3(1, 2, 3) built with gcc -m32 -O0. Released slots are drawn dashed and keep their old contents,
because that is what the trace shows: after leave, the old local still reads 6.

The same figure appears on the COSC 332 week 5 slides, drawn by a twin of this script from the same
trace, because the book and the decks carry the same pictures. Change both or neither.

Run from anywhere:  python3 scripts/figures/ch09_prologue_epilogue.py
"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Polygon

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(HERE, "..", "..", "assets", "figures", "ch09_prologue_epilogue.png"))
NAVY, INK, GREY = "#14284B", "#1F2937", "#6B7280"
ESP_C, EBP_C = "#1D4ED8", "#C2410C"
KIND = {  # face, edge, text
    "arg": ("#DBEAFE", "#1D4ED8", INK), "ret": ("#FEE2E2", "#B91C1C", INK),
    "ebp": ("#FEF3C7", "#B45309", INK), "sum": ("#DCFCE7", "#15803D", INK),
    "unused": ("#F3F4F6", "#9CA3AF", GREY), "free": ("#FFFFFF", "#CBD5E1", "#94A3B8"),
    "empty": ("#FFFFFF", "#E5E7EB", INK),
}
MONO = "DejaVu Sans Mono"
W, H = 8.10, 4.30

TRACE = os.path.join(HERE, "data", "trace_ex1_add3_32.json")


def _trace():
    import json
    t = json.load(open(TRACE))
    for st in t:
        st["r"] = {k: int(v, 16) for k, v in st["regs"].items()}
        st["m"] = {int(k, 16): v for k, v in st["stack"].items()}
    return t


_T = _trace()


def _at(pc):
    return [st for st in _T if int(st["pc"], 16) == pc][0]


def _after(pc):
    i = [k for k, st in enumerate(_T) if int(st["pc"], 16) == pc][0]
    return _T[i + 1]


BP = _after(0x8049018)["r"]["ebp"]
RET = _at(0x8049031)["m"][BP + 4]
ADDR = [f"{BP + d:08x}" for d in (16, 12, 8, 4, 0, -4, -8, -12, -16)]
LIVE = {ADDR[0]: ("arg", "arg 3 = 3"), ADDR[1]: ("arg", "arg 2 = 2"), ADDR[2]: ("arg", "arg 1 = 1"),
        ADDR[3]: ("ret", "ret addr"), ADDR[4]: ("ebp", "old ebp"), ADDR[5]: ("sum", "sum"),
        ADDR[6]: ("unused", "unused"), ADDR[7]: ("unused", "unused"), ADDR[8]: ("unused", "unused")}
assert [_at(0x8049031)["m"][BP + k] for k in (16, 12, 8, 0, -4)] == [3, 2, 1, 0, 6]


def _regs(st):
    esp, ebp = st["r"]["esp"], st["r"]["ebp"]
    return f"{esp:08x}", (f"{ebp:08x}" if ebp else None)


# (header, instruction, esp, ebp, live slots, released slots, overrides), every esp and ebp from the trace
STEPS = [
    ("caller", "before the call", *_regs(_at(0x8049006)), ADDR[:3], [], {}),
    ("caller", "call add3", *_regs(_after(0x8049006)), ADDR[:4], [], {}),
    ("prologue", "push ebp", *_regs(_after(0x8049017)), ADDR[:5], [], {}),
    ("prologue", "mov ebp, esp", *_regs(_after(0x8049018)), ADDR[:5], [], {}),
    ("prologue", "sub esp, 0x10", *_regs(_after(0x804901a)), ADDR, [], {}),
    ("body", "body runs", *_regs(_at(0x8049031)), ADDR, [], {ADDR[5]: "sum = 6"}),
    ("epilogue", "leave", *_regs(_after(0x8049031)), ADDR[:4], ADDR[4:], {ADDR[5]: "6"}),
    ("epilogue", "ret", *_regs(_after(0x8049032)), ADDR[:3], ADDR[3:], {ADDR[5]: "6"}),
    ("caller", "add esp, 12", *_regs(_after(0x804900b)), [], ADDR, {ADDR[5]: "6"}),
]
BAND = {"caller": ("#E5E7EB", INK), "prologue": ("#DBEAFE", "#1E3A8A"),
        "body": ("#DCFCE7", "#14532D"), "epilogue": ("#FFEDD5", "#9A3412")}


def cell(ax, x, y, w, h, kind, text, dashed=False):
    fc, ec, tc = KIND[kind]
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0,rounding_size=0.025",
                                fc=fc, ec=ec, lw=0.9, ls="--" if dashed else "-"))
    ax.text(x + w / 2, y + h / 2, text, ha="center", va="center", fontsize=6.4, color=tc,
            family=MONO if any(ch.isdigit() for ch in text) and "=" not in text else None)


def figure():
    fig = plt.figure(figsize=(W, H), dpi=220)
    ax = fig.add_axes([0, 0, 1, 1]); ax.set_xlim(0, W); ax.set_ylim(0, H); ax.axis("off")
    ax.text(W / 2, H - 0.14, "The prologue and epilogue, one instruction at a time: add3(1, 2, 3), 32-bit",
            ha="center", va="center", fontsize=9.6, weight="bold", color=NAVY)

    x0, pitch, cw = 0.80, 0.80, 0.58
    top, rh = 3.34, 0.262
    # address axis
    ax.text(0.44, top + 0.10, "address", ha="center", va="bottom", fontsize=6.2, color=GREY)
    for r, a in enumerate(ADDR):
        y = top - (r + 1) * rh
        ax.text(0.44, y + rh / 2, a, ha="center", va="center", fontsize=6.0, family=MONO, color=GREY)
    ax.annotate("", xy=(0.07, top - 9 * rh), xytext=(0.07, top), arrowprops=dict(arrowstyle="-|>",
                color=GREY, lw=0.9))
    ax.text(0.10, top - 9 * rh - 0.07, "lower", fontsize=5.6, color=GREY, va="top")

    # phase bands
    spans = {}
    for i, st in enumerate(STEPS):
        spans.setdefault(st[0] + str(i if st[0] == "caller" else ""), []).append(i)
    runs, cur = [], None
    for i, st in enumerate(STEPS):
        if cur and cur[0] == st[0]:
            cur[2] = i
        else:
            cur = [st[0], i, i]; runs.append(cur)
    for name, a, b in runs:
        fc, tc = BAND[name]
        xa = x0 + a * pitch - 0.02; xb = x0 + b * pitch + cw + 0.14
        ax.add_patch(FancyBboxPatch((xa, 3.84), xb - xa, 0.17, boxstyle="round,pad=0,rounding_size=0.03",
                                    fc=fc, ec="none"))
        ax.text((xa + xb) / 2, 3.925, name, ha="center", va="center", fontsize=7.2, weight="bold", color=tc)

    for i, (phase, instr, esp, ebp, live, freed, over) in enumerate(STEPS):
        cx = x0 + i * pitch + 0.08
        ax.text(cx + cw / 2, 3.60, instr, ha="center", va="center", fontsize=6.6,
                family=MONO if phase != "body" and i else None, weight="bold", color=INK, wrap=True)
        for r, a in enumerate(ADDR):
            y = top - (r + 1) * rh + 0.018
            kind, text = LIVE[a]
            text = over.get(a, text) if (a in live or a in freed) else ""
            if a in freed:
                cell(ax, cx, y, cw, rh - 0.036, "free", text, dashed=True)
            elif a in live:
                cell(ax, cx, y, cw, rh - 0.036, kind, text)
            else:
                cell(ax, cx, y, cw, rh - 0.036, "empty", "")
            if a == esp:
                ax.add_patch(Polygon([[cx - 0.075, y + 0.05], [cx - 0.075, y + rh - 0.086], [cx - 0.012, y + (rh - 0.036) / 2]],
                                     closed=True, fc=ESP_C, ec="none"))
            if ebp and a == ebp:
                ax.add_patch(Polygon([[cx + cw + 0.075, y + 0.05], [cx + cw + 0.075, y + rh - 0.086], [cx + cw + 0.012, y + (rh - 0.036) / 2]],
                                     closed=True, fc=EBP_C, ec="none"))
        if int(esp, 16) > int(ADDR[0], 16):  # above the grid: the caller's stack before the arguments
            ax.add_patch(Polygon([[cx - 0.075, top + 0.02], [cx - 0.075, top + 0.12], [cx - 0.012, top + 0.07]],
                                 closed=True, fc=ESP_C, ec="none"))
        ax.text(cx + cw / 2, top - 9 * rh - 0.10, "esp " + esp[4:], ha="center", va="center", fontsize=6.3,
                family=MONO, color=ESP_C)
        ax.text(cx + cw / 2, top - 9 * rh - 0.25, "ebp " + (ebp[4:] if ebp else "0"), ha="center",
                va="center", fontsize=6.3, family=MONO, color=EBP_C)

    ax.add_patch(Polygon([[0.30, 0.375], [0.30, 0.465], [0.355, 0.42]], closed=True, fc=ESP_C, ec="none"))
    ax.text(0.38, 0.42, "esp points here", fontsize=6.6, va="center", color=INK)
    ax.add_patch(Polygon([[1.52, 0.375], [1.52, 0.465], [1.465, 0.42]], closed=True, fc=EBP_C, ec="none"))
    ax.text(1.56, 0.42, "ebp points here", fontsize=6.6, va="center", color=INK)
    ax.add_patch(FancyBboxPatch((2.62, 0.365), 0.30, 0.11, boxstyle="round,pad=0,rounding_size=0.02",
                                fc="#FFFFFF", ec="#CBD5E1", lw=0.9, ls="--"))
    ax.text(2.97, 0.42, "released: free to reuse, but the old bytes are still there", fontsize=6.6,
            va="center", color=INK)
    ax.text(0.30, 0.215, f"ret addr is {RET:08x}, the instruction after the call; old ebp is 0 because this is the "
            "outermost frame.", fontsize=6.3, va="center", color=GREY)
    ax.text(0.30, 0.085, "leave is mov esp, ebp then pop ebp. Addresses are from one gdb run of gcc -m32 -O0 code; "
            "yours will differ.", fontsize=6.3, va="center", color=GREY)

    fig.savefig(OUT, dpi=220)
    plt.close(fig)
    print("wrote", OUT)


if __name__ == "__main__":
    figure()
