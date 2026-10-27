#!/usr/bin/env python3
"""Generate the three Section 16.14 figures for the CyberChef workshop.

assets/figures/ch16_classify.png   how the five Part 1 challenges sort into encoding,
                                    encryption and hashing by two questions
assets/figures/ch16_keyspace.png    time to try every key at a trillion guesses a second
assets/figures/ch16_case_chain.png  the Part 2 evidence chain, from five artifacts to a briefing

Every value drawn here comes from the challenge data in Section 16.14 or from arithmetic
stated beside it. Keyspace times: keys / 10^12 per second; one year = 365.25 days.

Run from anywhere:  python3 scripts/figures/ch16_workshop.py
"""

import math
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

DPI = 200
FIG_DIR = pathlib.Path(__file__).resolve().parents[2] / "assets" / "figures"

INK = "#222222"
GREY = "#555555"
ENC_FILL, ENC_EDGE = "#dbe7f7", "#1f5fc4"      # encode: blue
CRY_FILL, CRY_EDGE = "#f7ead4", "#a9630f"      # encrypt: amber
HSH_FILL, HSH_EDGE = "#ece0f7", "#7c33c2"      # hash: violet
Q_FILL, Q_EDGE = "#f2f2f2", "#555555"          # questions
RED = "#b23a3a"


def box(ax, x, y, w, h, fill, edge, lines, size=8.6, weight_first=True, align="center"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=1.2",
                                fc=fill, ec=edge, lw=1.3))
    n = len(lines)
    for i, t in enumerate(lines):
        yy = y + h - (i + 1) * h / (n + 1)
        tx = x + w / 2 if align == "center" else x + 1.5
        ax.text(tx, yy, t, ha=align, va="center", fontsize=size, color=INK,
                fontweight="bold" if (i == 0 and weight_first) else "normal")


def arrow(ax, p, q, label=None, color=INK, rad=0.0, lpos=0.5, loff=(0, 1.6), size=8.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=12, lw=1.2, color=color,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))
    if label:
        mx = p[0] + (q[0] - p[0]) * lpos + loff[0]
        my = p[1] + (q[1] - p[1]) * lpos + loff[1]
        ax.text(mx, my, label, ha="center", va="center", fontsize=size, color=color,
                fontweight="bold")


def classify():
    fig, ax = plt.subplots(figsize=(9.6, 5.6))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 58)
    ax.axis("off")
    box(ax, 2, 22, 17, 14, "#ffffff", INK, ["A scrambled", "string"], size=9.5, weight_first=False)
    box(ax, 25, 22, 22, 14, Q_FILL, Q_EDGE, ["Question 1", "Is it meant to be undone", "without a secret?"], size=8.6)
    box(ax, 55, 40, 43, 16, ENC_FILL, ENC_EDGE,
        ["ENCODING: the bottle", "1  Base64: one click back, no key", "2  ROT13: called a cipher, but no key"], size=8.4)
    box(ax, 25, 2, 22, 14, Q_FILL, Q_EDGE, ["Question 2", "Can the right key", "undo it?"], size=8.6)
    box(ax, 55, 15, 43, 18, CRY_FILL, CRY_EDGE,
        ["ENCRYPTION: the napkin", "3  XOR, one-byte key: 256 keys, tried at once",
         "4  AES-128: $2^{128}$ keys, no way to try them all"], size=8.4)
    box(ax, 55, 0.5, 43, 12, HSH_FILL, HSH_EDGE,
        ["HASHING: milk into curd", "5  SHA-256: always 256 bits, check it, never undo it"], size=8.4)
    arrow(ax, (19, 29), (25, 29))
    arrow(ax, (47, 33), (55, 47), "yes", color=ENC_EDGE, lpos=0.45, loff=(-2.5, 1.5))
    arrow(ax, (36, 22), (36, 16), "no", color=INK, lpos=0.5, loff=(2.2, 0))
    arrow(ax, (47, 11), (55, 23), "yes", color=CRY_EDGE, lpos=0.45, loff=(-2.5, 1.5))
    arrow(ax, (47, 5), (55, 6), "no, never", color=HSH_EDGE, lpos=0.5, loff=(-1.2, 2.2))
    ax.text(2, 52, "Same look, different promises", fontsize=11, fontweight="bold", color=INK)
    ax.text(2, 47.5, "Sort each Part 1 challenge by two\nquestions, never by how scrambled it looks.",
            fontsize=8.6, color=GREY, va="top")
    fig.savefig(FIG_DIR / "ch16_classify.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def human(seconds):
    year = 365.25 * 24 * 3600
    if seconds < 1e-6:
        return f"{seconds * 1e9:.2g} nanoseconds"
    if seconds < 1:
        return f"{seconds * 1e3:.2g} milliseconds"
    if seconds < 3 * 24 * 3600:
        return f"{seconds / 3600:.0f} hours"
    years = seconds / year
    exp = math.floor(math.log10(years))
    mant = years / 10 ** exp
    return f"about {mant:.1f} \u00d7 $10^{{{exp}}}$ years"


def keyspace():
    rate = 1e12
    rows = [("XOR, one-byte key (challenge 3)", 8, CRY_EDGE),
            ("XOR, four-byte key", 32, CRY_EDGE),
            ("DES, 56-bit key", 56, GREY),
            ("AES-128 (challenge 4)", 128, CRY_EDGE),
            ("AES-256", 256, CRY_EDGE)]
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    ys = list(range(len(rows)))[::-1]
    for y, (name, bits, col) in zip(ys, rows):
        sec = 2 ** bits / rate
        ax.barh(y, math.log10(sec) + 11, left=-11, color=col, alpha=0.85, height=0.55)
        ax.text(math.log10(sec) + 1.2, y, f"$2^{{{bits}}}$ keys: {human(sec)}", va="center",
                fontsize=8.6, color=INK, bbox=dict(fc="white", ec="none", pad=1.5))
    ax.set_yticks(ys)
    ax.set_yticklabels([r[0] for r in rows], fontsize=8.8)
    universe = math.log10(13.8e9 * 365.25 * 24 * 3600)
    for x, lab in [(0, "1 second"), (universe, "age of the universe")]:
        ax.axvline(x, color=RED if "universe" in lab else "#999999", lw=1, ls="--")
        ax.text(x + 0.4, len(rows) - 0.45, lab, fontsize=8, color=RED if "universe" in lab else GREY,
                va="bottom")
    ax.set_xlim(-11, 98)
    ax.set_ylim(-0.6, len(rows) - 0.1)
    ax.set_xlabel("Seconds to try every key, as a power of ten (log scale), at $10^{12}$ guesses a second",
                  fontsize=8.8)
    ax.set_xticks(range(-10, 100, 10))
    ax.set_xticklabels([f"$10^{{{t}}}$" for t in range(-10, 100, 10)], fontsize=8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title("Each added key bit doubles the work", fontsize=11, fontweight="bold", loc="left")
    fig.savefig(FIG_DIR / "ch16_keyspace.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def case_chain():
    fig, ax = plt.subplots(figsize=(9.6, 7.8))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    rows = [
        ("E1  Chat log", "Base64, an encoding", "From Base64", "The injected instruction:\nignore policy, export the customer table", ENC_FILL, ENC_EDGE),
        ("E2  Outbound request", "hex, an encoding", "From Hex", "Data posted to exfil.staging.invalid\nas customers.enc", ENC_FILL, ENC_EDGE),
        ("E3  Leaked config", "XOR, one-byte key 5a", "From Hex, XOR", "AES key and IV in a config\nbackup, rotate=never", CRY_FILL, CRY_EDGE),
        ("E4  Stolen file", "AES-128-CBC", "AES Decrypt with E3's key", "The exported record (synthetic)", CRY_FILL, CRY_EDGE),
        ("E5  Integrity seal", "SHA-256 in the ticket", "SHA-256 over the E4 record", "Digest matches: the record\nwas not altered", HSH_FILL, HSH_EDGE),
    ]
    top, step, h = 93, 17, 10.5
    ax.text(2, 97.5, "Evidence", fontsize=9, fontweight="bold", color=GREY)
    ax.text(37, 97.5, "Recipe", fontsize=9, fontweight="bold", color=GREY)
    ax.text(66, 97.5, "What it reveals", fontsize=9, fontweight="bold", color=GREY)
    ys = []
    for i, (name, form, recipe, reveal, fill, edge) in enumerate(rows):
        y = top - i * step - h
        ys.append(y)
        box(ax, 2, y, 29, h, fill, edge, [name, form], size=8.6)
        box(ax, 37, y, 23, h, "#ffffff", edge, [recipe], size=8.4, weight_first=False)
        box(ax, 66, y, 32, h, "#ffffff", edge, reveal.split("\n"), size=8.2, weight_first=False)
        arrow(ax, (31, y + h / 2), (37, y + h / 2))
        arrow(ax, (60, y + h / 2), (66, y + h / 2))
    y3, y4, y5 = ys[2], ys[3], ys[4]
    for (ya, yb, lab, col) in [(y3, y4, "key and IV", CRY_EDGE), (y4, y5, "hash the record", HSH_EDGE)]:
        arrow(ax, (74, ya), (52, yb + h), color=col)
        ax.text(63, (ya + yb + h) / 2, lab, ha="center", va="center", fontsize=8.0, color=col,
                fontweight="bold", bbox=dict(fc="white", ec="none", pad=1.5))
    ax.add_patch(FancyBboxPatch((2, 0.5), 96, 10, boxstyle="round,pad=0.02,rounding_size=1.2",
                                fc="#fbeaea", ec=RED, lw=1.3))
    ax.text(50, 7.6, "Two weak links: prompt injection opened the door, and the AES key sat in a config backup.",
            ha="center", va="center", fontsize=8.8, color=INK, fontweight="bold")
    ax.text(50, 3.4, "Briefing: what happened, impact, root cause, three recommendations, the ask.",
            ha="center", va="center", fontsize=8.6, color=INK)
    fig.savefig(FIG_DIR / "ch16_case_chain.png", dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


if __name__ == "__main__":
    classify()
    keyspace()
    case_chain()
    print("wrote ch16_classify.png, ch16_keyspace.png, ch16_case_chain.png")
