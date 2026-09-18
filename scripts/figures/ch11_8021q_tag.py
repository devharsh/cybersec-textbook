#!/usr/bin/env python3
"""Generate assets/figures/ch11_8021q_tag.png for Chapter 11, Section 11.24.

The IEEE 802.1Q VLAN tag, drawn in the house style of ch20_modbus_frame.png: a row of
field boxes holding the wire values, a bracket above naming each byte group, field names
below, and a callout carrying the one fact a reader must not get wrong.

Three bands, top to bottom:

  1. An untagged Ethernet frame, so the reader sees what the tag is inserted into.
  2. The same frame tagged, with the four tag bytes in place after the source address.
  3. The four tag bytes expanded into the 16-bit tag protocol identifier and the 16-bit
     tag control information, which splits into a 3-bit priority code point, a 1-bit
     drop eligible indicator, and a 12-bit VLAN identifier.

The worked value is the one Section 11.24 uses in its prose and its exercises: a frame
in VLAN 100 at priority 1, whose tag bytes are 81 00 20 64.  0x2064 is
0010 0000 0110 0100, so the top three bits are 001 (priority 1), the next bit is 0, and
the bottom twelve bits are 0000 0110 0100, which is 0x064, decimal 100.

Run from anywhere:  python3 scripts/figures/ch11_8021q_tag.py
"""

import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, Rectangle

# ---------------------------------------------------------------- house style constants
DPI = 200                     # the book's current export resolution
FIGSIZE = (9.6, 6.4)          # inches, the width the other wide figures in the book use

EDGE = "#333333"              # box outline
BLUE_FILL = "#dce6f0"         # first byte group, as the Modbus figure fills the header
GOLD_FILL = "#f2edcd"         # second byte group, as the Modbus figure fills the unit
GREY_FILL = "#eceff2"         # the surrounding frame, which is context and not the subject
BLUE_INK = "#2b6cb0"          # first group label and annotation
GOLD_INK = "#8a6d1f"          # second group label
GREY_INK = "#444444"          # secondary text
GUIDE = "#7a8b99"             # dashed insertion guide
CALL_FILL = "#fdeaea"         # callout fill
CALL_EDGE = "#c0392b"         # callout border
CALL_INK = "#a02020"          # callout text

NAME_PT = 8.2                 # field name inside a frame box
SIZE_PT = 7.5                 # byte count inside a frame box

OUT = pathlib.Path(__file__).resolve().parents[2] / "assets" / "figures" / "ch11_8021q_tag.png"


def box(ax, x0, x1, y0, y1, fill, lw=1.1, edge=EDGE):
    ax.add_patch(Rectangle((x0, y0), x1 - x0, y1 - y0,
                           facecolor=fill, edgecolor=edge, lw=lw, zorder=2))


def frame_field(ax, x0, x1, y0, y1, name, size, fill=GREY_FILL, lw=1.1, edge=EDGE):
    """A field of the surrounding Ethernet frame: name and byte count, inside the box."""
    box(ax, x0, x1, y0, y1, fill, lw=lw, edge=edge)
    mid = (x0 + x1) / 2
    ax.text(mid, y0 + (y1 - y0) * 0.63, name, ha="center", va="center",
            fontsize=NAME_PT, zorder=3)
    ax.text(mid, y0 + (y1 - y0) * 0.27, size, ha="center", va="center",
            fontsize=SIZE_PT, color=GREY_INK, zorder=3)


def bracket(ax, x0, x1, y, label, color):
    """A span bracket above a group of boxes, with the group name above it."""
    tick = 1.0
    ax.plot([x0, x0, x1, x1], [y - tick, y, y, y - tick],
            color=color, lw=1.4, solid_joinstyle="miter", zorder=3)
    ax.text((x0 + x1) / 2, y + 0.8, label, ha="center", va="bottom",
            fontsize=9.5, color=color, zorder=3)


def main():
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.set_xlim(0, 100)
    ax.set_ylim(3.5, 65.5)
    ax.axis("off")

    ax.text(50, 64.2, "The IEEE 802.1Q tag, and where it goes in the frame",
            ha="center", va="top", fontsize=13, zorder=3)

    # ------------------------------------------------------------- band 1: untagged frame
    ax.text(2, 59.0, "Untagged Ethernet frame, 64 to 1,518 bytes",
            ha="left", va="bottom", fontsize=9.2, color=GREY_INK, zorder=3)

    a0, a1 = 51.5, 57.5
    frame_field(ax, 2, 20, a0, a1, "Destination address", "6 bytes")
    frame_field(ax, 20, 34, a0, a1, "Source address", "6 bytes")
    frame_field(ax, 34, 47, a0, a1, "Type or length", "2 bytes")
    frame_field(ax, 47, 79, a0, a1, "Payload", "46 to 1,500 bytes")
    frame_field(ax, 79, 98, a0, a1, "Frame check sequence", "4 bytes")

    # the insertion point, marked on the exact boundary the tag is pushed into
    # stops above the band 2 caption rather than striking through it
    ax.plot([34, 34], [44.4, 51.5], color=GUIDE, lw=1.0, ls=(0, (4, 3)), zorder=1)
    for y, line in ((50.0, "802.1Q inserts four bytes here, after the source address."),
                    (47.9, "The sender then recomputes the frame check sequence, because"),
                    (45.8, "the frame it altered is no longer the one the old value covered.")):
        ax.text(35.6, y, line, ha="left", va="center", fontsize=9.2,
                color=BLUE_INK, zorder=3)

    # --------------------------------------------------------------- band 2: tagged frame
    ax.text(2, 42.3, "802.1Q tagged frame, four bytes longer, maximum 1,522 bytes",
            ha="left", va="bottom", fontsize=9.2, color=GREY_INK, zorder=3)

    b0, b1 = 36.0, 42.0
    frame_field(ax, 2, 20, b0, b1, "Destination address", "6 bytes")
    frame_field(ax, 20, 34, b0, b1, "Source address", "6 bytes")
    frame_field(ax, 34, 46, b0, b1, "802.1Q tag", "4 bytes", fill=GOLD_FILL,
                lw=1.8, edge=GOLD_INK)
    frame_field(ax, 46, 59, b0, b1, "Type or length", "2 bytes")
    frame_field(ax, 59, 79, b0, b1, "Payload", "46 to 1,500 bytes")
    frame_field(ax, 79, 98, b0, b1, "Frame check sequence", "4 bytes")

    # ------------------------------------------------------------ link down to the detail
    ax.add_patch(FancyArrowPatch((40, 35.4), (40, 31.2),
                                 arrowstyle="-|>", mutation_scale=13,
                                 color=BLUE_INK, lw=1.6, zorder=3))
    ax.text(41.7, 33.3, "the four tag bytes, expanded",
            ha="left", va="center", fontsize=9.2, color=BLUE_INK, zorder=3)

    # -------------------------------------------------------------- band 3: the tag itself
    c0, c1 = 20.0, 26.5
    fields = [
        (4, 28, BLUE_FILL, "81 00", "Tag protocol identifier (TPID)", "16 bits, always 0x8100"),
        (28, 50, GOLD_FILL, "001", "Priority code point (PCP)", "3 bits, here priority 1"),
        (50, 74, GOLD_FILL, "0", "Drop eligible indicator (DEI)", "1 bit, here 0"),
        (74, 97, GOLD_FILL, "0000 0110 0100", "VLAN identifier (VID)",
         "12 bits, 0x064 = VLAN 100"),
    ]
    for x0, x1, fill, value, name, detail in fields:
        box(ax, x0, x1, c0, c1, fill)
        mid = (x0 + x1) / 2
        ax.text(mid, (c0 + c1) / 2, value, ha="center", va="center",
                fontsize=12.5, fontweight="bold", family="monospace", zorder=3)
        ax.text(mid, 18.4, name, ha="center", va="center", fontsize=8.0, zorder=3)
        ax.text(mid, 16.5, detail, ha="center", va="center",
                fontsize=7.6, color=GREY_INK, zorder=3)

    bracket(ax, 4, 28, 28.3, "TPID, 2 bytes", BLUE_INK)
    bracket(ax, 28, 97, 28.3, "TCI, 2 bytes, here 0x2064", GOLD_INK)

    # ------------------------------------------------------------------------- the callout
    box(ax, 1, 99, 5.0, 12.8, CALL_FILL, lw=1.3, edge=CALL_EDGE)
    ax.text(50, 10.3,
            "Twelve bits give 4,096 identifiers, of which 0 and 4,095 are reserved, "
            "leaving 4,094 usable VLAN IDs.",
            ha="center", va="center", fontsize=9.0, color=CALL_INK, zorder=3)
    ax.text(50, 7.5,
            "Identifier 0 carries a priority and no VLAN. The DEI bit was the "
            "canonical format indicator (CFI).",
            ha="center", va="center", fontsize=9.0, color=CALL_INK, zorder=3)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=DPI, bbox_inches="tight", pad_inches=0.12, facecolor="white")
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
