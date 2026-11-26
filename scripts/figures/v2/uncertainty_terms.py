import os
"""Four words for unpredictability: random, stochastic, aleatoric, intermittent.
One drawing, two label sets: the cybersecurity book (ch05) and the Bedrock book (bk)."""
import sys, math, random
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

LABELS = {
    "ch05_uncertainty_terms": {
        "title": "Four words for unpredictability in security risk work",
        "use": [("Keys need uniform,", "independent bits"),
                ("Monte Carlo loss", "simulation (Section 5.6)"),
                ("Breach count: aleatoric;", "your click rate: epistemic"),
                ("Beacons that sleep", "and wake (Section 12.9)")]},
    "bk_uncertainty_terms": {
        "title": "Four words for unpredictability in a Bedrock application",
        "use": [("Next-token sampling draws", "from a distribution"),
                ("Temperature above 0:", "same prompt, new answer"),
                ("Ambiguous question: aleatoric;", "missing facts: epistemic"),
                ("Throttling errors: retry with", "backoff and jitter")]},
}

def panel(p, x, w, n, name, color, fill, lines, use):
    y, h = 50, 438
    p.zone(x, y, w, h, name, color=color, fill=fill, step=n)
    p.badge(n, x + w - 24, y + 22, step=n, color=color)
    ty = 334
    for i, t in enumerate(lines):
        p.text(x + w / 2, ty + i * 21, t, 13.5 if i == 0 else 12.5, INK if i == 0 else MUTED,
               "bold" if i == 0 else "normal", step=n)
    p.rect(x + 14, 406, w - 28, 66, "#ffffff", color, 1.5, rx=8, step=n)
    p.text(x + w / 2, 432, use[0], 12.5, color, "bold", step=n)
    p.text(x + w / 2, 453, use[1], 12.5, color, "bold", step=n)

def random_art(p, x, w, n):
    # a die and its uniform histogram, then the peaked histogram of two dice: both random
    dx, dy, s = x + 24, 98, 58
    p.rect(dx, dy, s, s, "#ffffff", BLUE, 2.5, rx=10, step=n)
    for cx, cy in [(0.25, 0.25), (0.75, 0.25), (0.5, 0.5), (0.25, 0.75), (0.75, 0.75)]:
        p.circle(dx + cx * s, dy + cy * s, 5, BLUE, BLUE, 1, step=n)
    def hist(hx, base, vals, bw, unit, color, label):
        for i, v in enumerate(vals):
            p.rect(hx + i * (bw + 2), base - v * unit, bw, v * unit, color, color, 1, rx=1.5, step=n, opacity=0.85)
        span = len(vals) * (bw + 2)
        p.raw(f'<line x1="{hx - 3}" y1="{base}" x2="{hx + span}" y2="{base}" stroke="{MUTED}" stroke-width="1.5"/>', step=n)
        p.text(hx + span / 2 - 1, base + 18, label, 12, MUTED, step=n)
    hist(x + 112, 156, [1] * 6, 20, 46, BLUE, "uniform: one die")
    hist(x + 52, 276, [1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1], 13, 11, PURPLE, "not uniform: two dice summed")

def stochastic_art(p, x, w, n):
    cx, cy = x + w / 2, 162
    for r, c in [(62, "#efe7f6"), (44, "#dccbec"), (26, "#c3a6df"), (9, PURPLE)]:
        p.circle(cx, cy, r, c, PURPLE, 1.5, step=n)
    rnd = random.Random(7)
    for _ in range(14):
        a = rnd.uniform(0, 2 * math.pi); d = abs(rnd.gauss(0, 22))
        p.circle(cx + d * math.cos(a), cy + d * math.sin(a), 3.6, INK, "#ffffff", 1, step=n)
    p.text(cx, 246, "arrows land around the aim", 12, MUTED, step=n)
    # bell-shaped histogram of distances
    vals = [4, 10, 19, 27, 30, 27, 19, 10, 4]; bw = 14; hx = cx - len(vals) * (bw + 2) / 2
    for i, v in enumerate(vals):
        p.rect(hx + i * (bw + 2), 296 - v, bw, v, PURPLE, PURPLE, 1, rx=1.5, step=n, opacity=0.85)
    p.raw(f'<line x1="{hx - 4}" y1="296" x2="{hx + len(vals) * (bw + 2)}" y2="296" stroke="{MUTED}" stroke-width="1.5"/>', step=n)

def aleatoric_art(p, x, w, n):
    ox, oy, aw, ah = x + 46, 284, w - 74, 170
    p.raw(f'<polyline points="{ox},{oy - ah} {ox},{oy} {ox + aw},{oy}" fill="none" stroke="{MUTED}" stroke-width="2"/>', step=n)
    p.text(ox + aw / 2, oy + 20, "data collected", 12, MUTED, step=n)
    p.raw(f'<text x="{ox - 12}" y="{oy - ah / 2}" font-family="{FONT}" font-size="12" fill="{MUTED}" text-anchor="middle" '
          f'transform="rotate(-90 {ox - 12} {oy - ah / 2})">uncertainty</text>', step=n)
    floor = oy - 46
    pts = " ".join(f"{ox + t * aw:.1f},{floor - (ah - 60) * math.exp(-4.2 * t):.1f}" for t in [i / 30 for i in range(31)])
    p.raw(f'<polyline points="{pts}" fill="none" stroke="{ORANGE}" stroke-width="2.6" stroke-dasharray="7 5"/>', step=n)
    p.raw(f'<line x1="{ox}" y1="{floor}" x2="{ox + aw}" y2="{floor}" stroke="{ORANGE}" stroke-width="3"/>', step=n)
    p.text(ox + aw - 4, floor + 18, "aleatoric floor", 12, ORANGE, "bold", anchor="end", step=n)
    p.text(ox + 60, oy - ah + 14, "epistemic part", 12, ORANGE, "bold", anchor="start", step=n)
    p.text(ox + 60, oy - ah + 30, "shrinks with data", 12, MUTED, anchor="start", step=n)
    p.icon("database", ox + aw - 22, oy - ah + 22, 34, step=n)

def intermittent_art(p, x, w, n):
    p.icon("clock", x + w / 2, 112, 44, step=n)
    def pulses(y, segs, label):
        p.text(x + 22, y - 26, label, 12, MUTED, anchor="start", step=n)
        x0, x1 = x + 22, x + w - 22
        pts = [(x0, y)]
        for a, b in segs:
            xa, xb = x0 + a * (x1 - x0), x0 + b * (x1 - x0)
            pts += [(xa, y), (xa, y - 22), (xb, y - 22), (xb, y)]
        pts.append((x1, y))
        p.raw('<polyline points="' + " ".join(f"{u:.1f},{v:.1f}" for u, v in pts) + f'" fill="none" stroke="{GREEN}" stroke-width="2.6"/>', step=n)
    pulses(202, [(0.05, 0.17), (0.30, 0.42), (0.55, 0.67), (0.80, 0.92)], "regular: on a schedule")
    pulses(284, [(0.03, 0.10), (0.18, 0.40), (0.62, 0.68), (0.83, 0.97)], "irregular: no fixed schedule")

def draw(name):
    L = LABELS[name]
    p = Fig(1180, 504, L["title"],
            "Four panels. Random: a fair die and two histograms, one uniform and one not, both random. "
            "Stochastic: hits scattered around a target with a bell-shaped spread. Aleatoric: uncertainty falls "
            "with more data until it reaches a floor that more data cannot remove. Intermittent: two on and off "
            "signals over time, one regular and one irregular.")
    W, G, X0 = 278, 16, 16
    xs = [X0 + i * (W + G) for i in range(4)]
    panel(p, xs[0], W, 1, "Random", BLUE, "#eef5fc",
          ["Outcome not known in advance", "Any distribution; uniform is one case"], L["use"][0])
    random_art(p, xs[0], W, 1)
    panel(p, xs[1], W, 2, "Stochastic", PURPLE, "#f6f0fb",
          ["A random process with a model", "Greek stochos: aim, target"], L["use"][1])
    stochastic_art(p, xs[1], W, 2)
    panel(p, xs[2], W, 3, "Aleatoric", ORANGE, "#fdf3e7",
          ["Noise that more data cannot remove", "Latin alea: dice"], L["use"][2])
    aleatoric_art(p, xs[2], W, 3)
    panel(p, xs[3], W, 4, "Intermittent", GREEN, "#edf7ee",
          ["On and off over time", "The schedule can be regular or not"], L["use"][3])
    intermittent_art(p, xs[3], W, 4)
    p.save(OUT + name)

if __name__ == "__main__":
    for nm in LABELS: draw(nm)
    print("ok")
