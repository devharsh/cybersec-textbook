#!/usr/bin/env python3
"""Generate assets/figures/ch11_segmentation_zones.png for Chapter 11, Section 11.23.

The worked segmentation of the 250-person engineering firm, drawn in the house style of
ch20_zones_conduits.png: one box per zone, one arrow per permitted flow, each arrow
labeled with what it carries, and a line underneath giving the arithmetic that the
section argues is the real cost of the project.

Every zone, VLAN number, address range, and permitted flow below is taken from the
tables in Section 11.23. Nothing is added. The eight zones give 8 x 7 = 56 directed
zone-to-zone pairs, and each zone has an outbound and an inbound internet path, so
56 + 8 + 8 = 72 directions need a decision. Ten are permitted, so 62 are denied.

Run from anywhere:  python3 scripts/figures/ch11_segmentation_zones.py
"""

import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

# ---------------------------------------------------------------- house style constants
DPI = 200                     # the book's current export resolution
FIGSIZE = (9.6, 7.0)          # inches, the width the other wide figures in the book use

EDGE = "#333333"              # zone outline
FLOW = "#2e6094"              # permitted flow, the steel blue the zones figure uses
GREY_INK = "#444444"          # secondary text
NAME_PT = 9.0                 # zone name
DETAIL_PT = 8.2               # VLAN number and address range
FLOW_PT = 7.8                 # flow label

# Fills follow the zones-and-conduits figure: untrusted in red, the demilitarized zone in
# yellow, the most tightly held zone in peach, ordinary internal zones in blue tints.
UNTRUSTED = "#f0d4d4"
GUESTISH = "#f7e3e3"
DMZ_FILL = "#f5f0cf"
GUARDED = "#f7e0cf"
BLUE_1 = "#c9e1f0"
BLUE_2 = "#dbe7f2"
BLUE_3 = "#e4ecf4"

OUT = (pathlib.Path(__file__).resolve().parents[2]
       / "assets" / "figures" / "ch11_segmentation_zones.png")

# Column spans. The gaps either side of the server column are wide, because the two
# horizontal flows are labeled inside them.
COL = [(1.0, 16.0), (24.0, 39.0), (54.0, 69.0), (84.0, 99.0)]
ROW_A = (43.0, 54.0)
ROW_B = (22.0, 33.0)
NET = (60.0, 66.0)

# (column, row, name lines, VLAN, address range, fill)
ZONES = [
    (0, ROW_A, ["Guest"], "VLAN 170", "10.0.70.0/24", GUESTISH),
    (1, ROW_A, ["Users"], "VLAN 110", "10.0.10.0/23", BLUE_2),
    (2, ROW_A, ["Servers"], "VLAN 100", "10.0.0.0/24", BLUE_1),
    (3, ROW_A, ["Demilitarized", "zone"], "VLAN 200", "203.0.113.0/24", DMZ_FILL),
    (0, ROW_B, ["Print"], "VLAN 130", "10.0.30.0/24", BLUE_3),
    (1, ROW_B, ["Out-of-band", "management"], "VLAN 160", "10.0.60.0/24", GUARDED),
    (2, ROW_B, ["Voice"], "VLAN 120", "10.0.20.0/24", BLUE_2),
    (3, ROW_B, ["Building", "systems"], "VLAN 140", "10.0.40.0/24", BLUE_3),
]


def zone_box(ax, x0, x1, y0, y1, fill, lw=1.3):
    ax.add_patch(FancyBboxPatch((x0, y0), x1 - x0, y1 - y0,
                                boxstyle="round,pad=0,rounding_size=0.6",
                                facecolor=fill, edgecolor=EDGE, lw=lw, zorder=2))


def arrow(ax, points):
    """A flow: one straight arrow, or an elbow drawn as plain segments plus a head."""
    for (xa, ya), (xb, yb) in zip(points, points[1:-1]):
        ax.plot([xa, xb], [ya, yb], color=FLOW, lw=1.9, solid_capstyle="round", zorder=3)
    ax.add_patch(FancyArrowPatch(points[-2], points[-1], arrowstyle="-|>",
                                 mutation_scale=13, color=FLOW, lw=1.9, zorder=3))


def flow_label(ax, x, y, lines, ha="left"):
    for n, line in enumerate(lines):
        ax.text(x, y - n * 1.9, line, ha=ha, va="center",
                fontsize=FLOW_PT, color=FLOW, zorder=4)


def main():
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.set_xlim(0, 100)
    ax.set_ylim(6.0, 71.5)
    ax.axis("off")

    ax.text(50, 70.5, "A 250-person firm in eight zones, and the ten flows that are permitted",
            ha="center", va="top", fontsize=13, zorder=4)

    # ------------------------------------------------------------------ the outside world
    zone_box(ax, 1.0, 99.0, NET[0], NET[1], UNTRUSTED)
    ax.text(50, 64.2, "Internet", ha="center", va="center",
            fontsize=NAME_PT + 0.8, fontweight="bold", zorder=4)
    ax.text(50, 61.9, "outside every zone, reached only on the paths below",
            ha="center", va="center", fontsize=DETAIL_PT, color=GREY_INK, zorder=4)

    # ------------------------------------------------------------------------- the zones
    for col, row, names, vlan, cidr, fill in ZONES:
        x0, x1 = COL[col]
        y0, y1 = row
        zone_box(ax, x0, x1, y0, y1, fill)
        mid = (x0 + x1) / 2
        if len(names) == 1:
            ax.text(mid, y0 + 8.0, names[0], ha="center", va="center",
                    fontsize=NAME_PT, fontweight="bold", zorder=4)
        else:
            ax.text(mid, y0 + 8.8, names[0], ha="center", va="center",
                    fontsize=NAME_PT, fontweight="bold", zorder=4)
            ax.text(mid, y0 + 6.9, names[1], ha="center", va="center",
                    fontsize=NAME_PT, fontweight="bold", zorder=4)
        ax.text(mid, y0 + 4.6, vlan, ha="center", va="center",
                fontsize=DETAIL_PT, color=GREY_INK, zorder=4)
        ax.text(mid, y0 + 2.4, cidr, ha="center", va="center",
                fontsize=DETAIL_PT, color=GREY_INK, zorder=4)

    # ------------------------------------------------- the ten flows the matrix permits
    # Guest to the internet
    arrow(ax, [(8.5, 54.0), (8.5, 60.0)])
    flow_label(ax, 9.7, 57.0, ["TCP 80, 443"])

    # Users to the internet, through the proxy
    arrow(ax, [(31.5, 54.0), (31.5, 60.0)])
    flow_label(ax, 32.7, 57.0, ["TCP 80, 443 via proxy"])

    # Servers to the internet, for updates and licensing
    arrow(ax, [(60.0, 54.0), (60.0, 60.0)])
    flow_label(ax, 61.2, 57.9, ["TCP 443 to named", "destinations"])

    # The internet to the public site in the demilitarized zone
    arrow(ax, [(93.0, 60.0), (93.0, 54.0)])
    flow_label(ax, 91.8, 57.9, ["TCP 80, 443 to", "203.0.113.10"], ha="right")

    # Users to servers: file shares and directory
    arrow(ax, [(39.0, 48.5), (54.0, 48.5)])
    flow_label(ax, 46.5, 52.5, ["TCP 445, 88,", "389, 636, 3268"], ha="center")

    # Demilitarized zone to one database on one port
    arrow(ax, [(84.0, 48.5), (69.0, 48.5)])
    flow_label(ax, 76.5, 52.5, ["TCP 5432 to", "10.0.0.50 only"], ha="center")

    # Users to print
    arrow(ax, [(27.0, 43.0), (27.0, 38.0), (8.5, 38.0), (8.5, 33.0)])
    flow_label(ax, 17.7, 39.3, ["TCP 9100, 631"], ha="center")

    # Users to the management zone, from named administrative hosts only
    arrow(ax, [(35.0, 43.0), (35.0, 33.0)])
    flow_label(ax, 36.2, 40.0, ["TCP 22, 443", "from named", "admin hosts"])

    # Voice to servers: call control and media
    arrow(ax, [(63.0, 33.0), (63.0, 43.0)])
    flow_label(ax, 61.8, 38.5, ["UDP 5060, media"], ha="right")

    # Servers to the cameras, because a camera never starts a conversation
    arrow(ax, [(67.0, 43.0), (67.0, 41.0), (91.0, 41.0), (91.0, 33.0)])
    flow_label(ax, 79.0, 39.3, ["TCP 554, 80 to", "the camera range"], ha="center")

    # ------------------------------------------------------------- the arithmetic beneath
    ax.text(50, 14.6,
            "Eight zones give 8 x 7 = 56 directed pairs, plus 8 outbound and 8 inbound "
            "internet paths: 72 decisions.",
            ha="center", va="center", fontsize=8.8, color=GREY_INK, zorder=4)
    ax.text(50, 11.6,
            "Ten are permitted above. The other 62 are denied, including users to users "
            "and guest to anything internal.",
            ha="center", va="center", fontsize=8.8, color=GREY_INK, zorder=4)

    OUT.parent.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT, dpi=DPI, bbox_inches="tight", pad_inches=0.12, facecolor="white")
    plt.close(fig)
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
