#!/usr/bin/env python3
"""Figures for the October 2026 news additions and the landmark-bugs section.

assets/figures/ch02_emudhra_response.png   the eMudhra trust chain and the four layers of response
assets/figures/ch09_bug_lifetimes.png      how long landmark bugs stayed hidden before disclosure
assets/figures/ch10_oct2026_chains.png     the PHP2Shell and GitLab org-mode attack paths
assets/figures/ch14_japan_timeline.png     Japan's national response, October 2026
assets/figures/ch17_litellm_timeline.png   the LiteLLM 1.107.0 compromise, May to October 2026
assets/figures/ch17_agent_access.png       shared password versus delegated token for an AI agent

Every date and number drawn here appears, with its source, in the section text that embeds the figure.

Run from anywhere:  python3 scripts/figures/news_2026_10.py
"""

import datetime as dt
import pathlib

import matplotlib

matplotlib.use("Agg")
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch

DPI = 200
FIG_DIR = pathlib.Path(__file__).resolve().parents[2] / "assets" / "figures"

INK = "#222222"
GREY = "#555555"
BLUE, BLUE_F = "#1f5fc4", "#dbe7f7"
AMBER, AMBER_F = "#a9630f", "#f7ead4"
VIOLET, VIOLET_F = "#7c33c2", "#ece0f7"
RED, RED_F = "#b23a3a", "#fbeaea"
GREEN, GREEN_F = "#2e7d4f", "#e3f2e8"
Q_F = "#f2f2f2"


def box(ax, x, y, w, h, fill, edge, lines, size=8.4, bold_first=True):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.02,rounding_size=1.0",
                                fc=fill, ec=edge, lw=1.2))
    n = len(lines)
    for i, t in enumerate(lines):
        ax.text(x + w / 2, y + h - (i + 1) * h / (n + 1), t, ha="center", va="center", fontsize=size,
                color=INK, fontweight="bold" if (i == 0 and bold_first) else "normal")


def arrow(ax, p, q, color=INK, label=None, loff=(0, 1.4), size=7.8, rad=0.0):
    ax.add_patch(FancyArrowPatch(p, q, arrowstyle="-|>", mutation_scale=11, lw=1.1, color=color,
                                 connectionstyle=f"arc3,rad={rad}", shrinkA=2, shrinkB=2))
    if label:
        ax.text((p[0] + q[0]) / 2 + loff[0], (p[1] + q[1]) / 2 + loff[1], label, ha="center",
                va="center", fontsize=size, color=color, fontweight="bold",
                bbox=dict(fc="white", ec="none", pad=1.0))


def canvas(w=9.6, h=6.0):
    fig, ax = plt.subplots(figsize=(w, h))
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis("off")
    return fig, ax


def save(fig, name):
    fig.savefig(FIG_DIR / name, dpi=DPI, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def emudhra():
    fig, ax = canvas(9.6, 6.4)
    box(ax, 22, 82, 56, 15, RED_F, RED, ["emSign ECC Root CA - G3", "cross-signs the G3 TLS and code-signing sub-roots;",
                                       "distrust announced October 20, Chrome removal scheduled October 27"])
    box(ax, 2, 56, 44, 16, AMBER_F, AMBER, ["8 weak intermediates (P-384)",
                                           "6 TLS, 2 code signing; private keys below 256",
                                           "issued no customer certificates"])
    box(ax, 54, 56, 44, 16, BLUE_F, BLUE, ["Sibling intermediates under the same root",
                                          "about 30,800 unexpired precertificates (Chrome)",
                                          "had to move to another hierarchy"])
    arrow(ax, (40, 82), (26, 72))
    arrow(ax, (60, 82), (74, 72))
    layers = [("1  Revocation by the CA", "October 18: all eight revoked, CA compromise"),
              ("2  Browser blocklists", "Oct 17: Chrome CRLSet 19:45, Firefox OneCRL 22:59 UTC; Windows list, Oct 20"),
              ("3  Root removal", "Oct 20: Mozilla announces it; Chrome follows; Windows drops G3 roots, Oct 26"),
              ("4  Collateral", "customers under the root migrate; eMudhra exits the TLS business, October 22")]
    for i, (a, b) in enumerate(layers):
        y = 40 - i * 11
        ax.add_patch(FancyBboxPatch((2, y), 96, 9, boxstyle="round,pad=0.02,rounding_size=1.0",
                                    fc=Q_F, ec=GREY, lw=1.0))
        ax.text(4, y + 4.5, a, ha="left", va="center", fontsize=8.6, fontweight="bold", color=INK)
        ax.text(32, y + 4.5, b, ha="left", va="center", fontsize=8.2, color=INK)
    ax.text(2, 50.5, "Response, from narrowest to widest (2026, UTC)", fontsize=9, fontweight="bold", color=GREY)
    save(fig, "ch02_emudhra_response.png")


def lifetimes():
    D = dt.date
    rows = [("Shellshock (Bash)", D(1989, 8, 5), D(2014, 9, 24), BLUE),
            ("Heartbleed (OpenSSL)", D(2011, 12, 15), D(2014, 4, 7), BLUE),
            ("Log4Shell (Log4j 2)", D(2013, 9, 14), D(2021, 12, 10), BLUE),
            ("GitLab org-mode regex", D(2014, 6, 20), D(2026, 10, 21), AMBER),
            ("regreSSHion (OpenSSH)", D(2020, 10, 1), D(2024, 7, 1), BLUE)]
    fig, ax = plt.subplots(figsize=(9.6, 4.2))
    for i, (name, a, b, col) in enumerate(rows):
        y = len(rows) - i
        ax.plot([a, b], [y, y], color=col, lw=9, solid_capstyle="butt", alpha=0.85)
        years = (b - a).days / 365.25
        ax.text(b + dt.timedelta(days=120), y, f"about {years:.0f} years",
                va="center", fontsize=8.4, color=INK)
    ax.plot([D(2006, 9, 27)], [1], marker="o", color=GREY, ms=5)
    ax.text(D(2006, 9, 27), 0.55, "first fixed 2006", ha="center", fontsize=7.6, color=GREY)
    ax.axvline(D(2038, 1, 19), color=RED, lw=1, ls="--")
    ax.text(D(2037, 9, 1), len(rows) + 0.45, "2038: signed 32-bit time runs out", ha="right", fontsize=7.8, color=RED)
    ax.set_yticks(range(1, len(rows) + 1))
    ax.set_yticklabels([r[0] for r in rows][::-1], fontsize=8.6)
    ax.set_ylim(0.2, len(rows) + 0.9)
    ax.set_xlim(D(1987, 1, 1), D(2040, 1, 1))
    ax.xaxis.set_major_locator(mdates.YearLocator(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.tick_params(axis="x", labelsize=8)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.set_title("From the commit or release that introduced the bug to its public disclosure",
                 fontsize=10, fontweight="bold", loc="left")
    save(fig, "ch09_bug_lifetimes.png")


def chains():
    fig, ax = canvas(9.6, 6.6)
    ax.text(2, 97, "PHP2Shell (CVE-2026-109618 and CVE-2026-109619)", fontsize=9.4, fontweight="bold", color=INK)
    steps = [("Request 1", "multipart body", "passes size check,", "exhausts memory"),
             ("Out of memory", "PHP aborts", "mid-operation;", "state half built"),
             ("Stale state", "worker keeps", "pointers into", "freed memory"),
             ("Request 2", "same worker", "reuses the", "stale state"),
             ("Code execution", "before any", "application code", "runs (mod_php)")]
    for i, lines in enumerate(steps):
        x = 2 + i * 19.6
        box(ax, x, 66, 17, 24, AMBER_F if i < 4 else RED_F, AMBER if i < 4 else RED, list(lines), size=7.6)
        if i:
            arrow(ax, (x - 2.6, 78), (x, 78))
    ax.text(2, 52, "GitLab org-mode rendering (CVE-2026-110264)", fontsize=9.4, fontweight="bold", color=INK)
    steps = [("Org-mode file", "declares its own", "task keyword", "with #+TODO:"),
             ("org-ruby", "escapes it for one", "pattern, pastes it", "raw into another"),
             ("Regex compiler", "attacker text", "becomes pattern", "syntax"),
             ("Onigmo engine", "too many repeats", "overflow an", "internal ID counter"),
             ("Code execution", "on the GitLab", "server, no login", "(CVSS 10.0)")]
    for i, lines in enumerate(steps):
        x = 2 + i * 19.6
        box(ax, x, 20, 17, 24, BLUE_F if i < 4 else RED_F, BLUE if i < 4 else RED, list(lines), size=7.6)
        if i:
            arrow(ax, (x - 2.6, 32), (x, 32))
    ax.text(50, 8, "Both: untrusted input reaches a native component below a memory-safe or interpreted layer.",
            ha="center", fontsize=8.6, color=GREY)
    save(fig, "ch10_oct2026_chains.png")


def japan():
    D = dt.date
    events = [(D(2026, 10, 1), "Active Cyber Defense powers\nand reporting take effect", 1.0),
              (D(2026, 10, 7), "IDC Frontier ransomware reported;\n495 companies and local governments", -1.0),
              (D(2026, 10, 9), "National Cybersecurity Office advisory;\nLDP official: an emergency in cyberspace", 1.6),
              (D(2026, 10, 20), "LDP emergency proposals:\na headquarters under the PM's office", -1.6),
              (D(2026, 10, 23), "PM: the National Cybersecurity\nOffice is the command center", 1.0),
              (D(2026, 10, 24), "GMO asks for active cyber defense;\nup to 26,739 servers may be affected", -1.0),
              (D(2026, 10, 26), "PM orders emergency measures\nby the end of the next week", 2.2)]
    fig, ax = plt.subplots(figsize=(9.6, 4.6))
    ax.axhline(0, color=INK, lw=1.2)
    for d, label, yy in events:
        ax.plot([d, d], [0, yy * 0.8], color=GREY, lw=0.9)
        ax.plot([d], [0], marker="o", color=RED if "ransomware" in label else BLUE, ms=6)
        ax.text(d, yy, label, ha="center", va="center", fontsize=7.6, color=INK,
                bbox=dict(fc="white", ec="#cccccc", pad=2.0))
    ax.set_ylim(-2.4, 2.9)
    ax.set_xlim(D(2026, 9, 27), D(2026, 10, 30))
    ax.xaxis.set_major_locator(mdates.DayLocator(bymonthday=[1, 7, 9, 20, 23, 26]))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.tick_params(axis="x", labelsize=8)
    ax.get_yaxis().set_visible(False)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.set_title("Japan, October 2026: from a breach wave to a national response", fontsize=10,
                 fontweight="bold", loc="left")
    save(fig, "ch14_japan_timeline.png")


def litellm():
    fig, ax = canvas(9.6, 5.8)
    ax.text(2, 97, "Months of exposure, minutes of compromise, hours of exposure again", fontsize=9.8,
            fontweight="bold", color=INK)
    left = [("May 27", "master key committed to a public", "repository; force-pushed over, never revoked"),
            ("Oct 10, 21:27 UTC", "the key returns an organization", "owner's GitHub token, not scoped down"),
            ("Oct 10, 22:11 UTC", "workflow runs send more", "maintainer tokens to an outside endpoint")]
    for i, lines in enumerate(left):
        y = 72 - i * 24
        box(ax, 2, y, 36, 18, AMBER_F, AMBER, list(lines), size=7.9)
        if i:
            arrow(ax, (20, y + 24), (20, y + 18))
    right = [("Oct 21, 10:08 to 11:40", "branch protection overridden; release", "built from the fork Berri-AI/litellm"),
             ("11:39 to 11:47", "signed wheels on PyPI; images on", "Docker Hub and GHCR, including latest"),
             ("about 11:47", "Socket flags the wheels,", "about seven minutes after publication"),
             ("13:23 to 14:20", "PyPI frozen, tags pulled:", "live about two hours"),
             ("16:20 to 17:01", "stolen AWS credentials tested,", "consistent with LLMjacking (Wiz)")]
    for i, lines in enumerate(right):
        y = 78 - i * 17
        col, fill = (RED, RED_F) if i in (1, 4) else (BLUE, BLUE_F)
        box(ax, 50, y, 48, 13, fill, col, list(lines), size=7.7)
        if i:
            arrow(ax, (74, y + 17), (74, y + 13))
    arrow(ax, (38, 33), (50, 84), color=GREY, rad=-0.2)
    ax.text(41, 60, "11 days", fontsize=8.2, color=GREY, fontweight="bold", rotation=62)
    save(fig, "ch17_litellm_timeline.png")


def agents():
    fig, ax = canvas(9.6, 5.6)
    box(ax, 2, 40, 16, 20, Q_F, GREY, ["Customer", "asks an AI agent", "to act"], size=8.2)
    box(ax, 30, 66, 22, 22, RED_F, RED, ["Agent with the", "customer's password", "logs in as the customer"], size=8.0)
    box(ax, 30, 12, 22, 22, GREEN_F, GREEN, ["Agent with a", "delegated token", "named, scoped, revocable"], size=8.0)
    box(ax, 68, 66, 30, 22, RED_F, RED, ["Bank sees: the customer", "full read and write", "cannot reliably tell agent from user"], size=8.0)
    box(ax, 68, 12, 30, 22, GREEN_F, GREEN, ["Bank sees: this agent", "read-only, or payments with", "approval; cut off by revoking"], size=8.0)
    arrow(ax, (18, 55), (30, 76), color=RED, label="shares password", loff=(-3, 3))
    arrow(ax, (18, 45), (30, 24), color=GREEN, label="grants consent", loff=(-3, -3))
    arrow(ax, (52, 77), (68, 77), color=RED)
    arrow(ax, (52, 23), (68, 23), color=GREEN)
    ax.text(65, 50, "A hidden instruction in a web page or an email can steer either agent;\nonly the lower path limits what the agent can then do.",
            ha="center", va="center", fontsize=8.2, color=GREY)
    save(fig, "ch17_agent_access.png")


if __name__ == "__main__":
    emudhra()
    lifetimes()
    chains()
    japan()
    litellm()
    agents()
    print("wrote ch02_emudhra_response, ch09_bug_lifetimes, ch10_oct2026_chains, ch14_japan_timeline, "
          "ch17_litellm_timeline, ch17_agent_access")
