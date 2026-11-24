"""Compose book figures from icons, boxes, arrows, and numbered steps.
Each element can carry a step number; the SVG builds in step order once,
like a slide build, and shows everything at once when motion is reduced."""
import html, math, subprocess
import icons

FONT = "Helvetica, Arial, sans-serif"
INK, MUTED = "#1f2933", "#52606d"
BLUE, RED, GREEN, ORANGE, PURPLE = "#1f4e9c", "#c0392b", "#2e7d32", "#d9822b", "#6a3d9a"

def esc(t): return html.escape(str(t), quote=True)

class Fig:
    def __init__(self, w, h, title=None, desc="", step_gap=0.9):
        self.w, self.h, self.title, self.desc = w, h, title, desc
        self.items, self.used, self.colors = [], [], set()
        self.step_gap, self.max_step = step_gap, 0

    def _add(self, svg, step):
        if step:
            self.max_step = max(self.max_step, step)
            svg = f'<g class="st s{step}">{svg}</g>'
        self.items.append(svg)

    def icon(self, name, x, y, size=70, label=None, sub=None, step=None, label_color=INK, label_size=15):
        if name not in self.used: self.used.append(name)
        s = f'<use href="#i-{name}" x="{x - size/2:.1f}" y="{y - size/2:.1f}" width="{size}" height="{size}"/>'
        ty = y + size/2 + 15
        if label:
            s += self._text(x, ty, label, label_size, label_color, "bold")
            ty += label_size + 2
        if sub:
            for line in sub.split("\n"):
                s += self._text(x, ty, line, 12, MUTED); ty += 14
        self._add(s, step)

    def _text(self, x, y, t, size=13, color=INK, weight="normal", anchor="middle", italic=False):
        st = ' font-style="italic"' if italic else ""
        return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" fill="{color}" '
                f'font-weight="{weight}" text-anchor="{anchor}"{st}>{esc(t)}</text>')

    def text(self, x, y, t, size=13, color=INK, weight="normal", anchor="middle", step=None, italic=False):
        lines = str(t).split("\n")
        self._add("".join(self._text(x, y + i*(size+3), l, size, color, weight, anchor, italic) for i, l in enumerate(lines)), step)

    def box(self, x, y, w, h, text, step=None, kind="process", size=14, color=INK):
        fills = {"process": ("url(#g-box)", "#4a6fa5"), "note": ("#fff8e1", "#d9a400"),
                 "danger": ("#fdecea", RED), "ok": ("#e8f5e9", GREEN), "plain": ("#ffffff", "#9aa5b1")}
        f, stroke = fills[kind]
        s = (f'<rect x="{x:.1f}" y="{y:.1f}" width="{w}" height="{h}" rx="6" fill="{f}" stroke="{stroke}" stroke-width="1.6" filter="url(#f-drop)"/>')
        lines = str(text).split("\n")
        y0 = y + h/2 - (len(lines)-1)*(size+3)/2 + size*0.35
        for i, l in enumerate(lines):
            s += self._text(x + w/2, y0 + i*(size+3), l, size, color, "bold" if i == 0 else "normal")
        self._add(s, step)

    def zone(self, x, y, w, h, label, color="#5b9bd5", fill="#eef5fc", step=None, dash=False):
        d = ' stroke-dasharray="7 5"' if dash else ""
        s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="14" fill="{fill}" stroke="{color}" stroke-width="2"{d}/>'
             + self._text(x + 14, y + 22, label, 14, color, "bold", "start"))
        self._add(s, step)

    def arrow(self, pts, label=None, color=INK, step=None, dash=False, width=2.2, label_at=0.5, label_dy=-8,
              label_color=None, both=False, size=13, label_anchor="middle"):
        self.colors.add(color)
        cid = color.strip("#")
        d = "M" + " L".join(f"{px:.1f} {py:.1f}" for px, py in pts)
        dash_attr = ' stroke-dasharray="7 6"' if dash else ""
        start = f' marker-start="url(#a-{cid})"' if both else ""
        s = (f'<path d="{d}" fill="none" stroke="{color}" stroke-width="{width}"{dash_attr}{start} '
             f'marker-end="url(#a-{cid})" stroke-linejoin="round"/>')
        if label:
            # place the label at a fraction of the total path length
            segs = list(zip(pts, pts[1:])); lens = [math.dist(a, b) for a, b in segs]
            target, acc = sum(lens) * label_at, 0
            for (a, b), L in zip(segs, lens):
                if acc + L >= target:
                    t = (target - acc) / L if L else 0
                    lx, ly = a[0] + (b[0]-a[0])*t, a[1] + (b[1]-a[1])*t
                    break
                acc += L
            lc = label_color or color
            for i, line in enumerate(str(label).split("\n")):
                s += self._text(lx, ly + label_dy + i*(size+2), line, size, lc, "bold", label_anchor)
        self._add(s, step)

    def badge(self, n, x, y, step=None, color=BLUE):
        s = (f'<circle cx="{x}" cy="{y}" r="12" fill="{color}" stroke="#fff" stroke-width="2"/>'
             + self._text(x, y + 4.6, str(n), 13, "#fff", "bold"))
        self._add(s, step if step is not None else n)

    def raw(self, svg, step=None): self._add(svg, step)

    def svg(self):
        markers = "".join(
            f'<marker id="a-{c.strip("#")}" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" '
            f'orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 Z" fill="{c}"/></marker>' for c in sorted(self.colors))
        delays = "".join(f".s{k}{{animation-delay:{(k-1)*self.step_gap:.2f}s}}" for k in range(1, self.max_step + 1))
        style = ("<style>@media (prefers-reduced-motion: no-preference){"
                 ".st{animation:fig-in .7s ease-out both}" + delays + "}"
                 "@keyframes fig-in{from{opacity:0}to{opacity:1}}</style>")
        extra = ('<linearGradient id="g-box" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#f3f8fe"/>'
                 '<stop offset="1" stop-color="#c9ddf4"/></linearGradient>'
                 '<filter id="f-drop" x="-10%" y="-10%" width="130%" height="140%"><feDropShadow dx="1.5" dy="2" '
                 'stdDeviation="1.6" flood-color="#000" flood-opacity=".18"/></filter>')
        head = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" '
                f'role="img" aria-labelledby="t d"><title id="t">{esc(self.title or "")}</title><desc id="d">{esc(self.desc)}</desc>')
        body = [head, style, icons.defs(self.used).replace("<defs>", "<defs>" + extra + markers, 1),
                f'<rect width="{self.w}" height="{self.h}" fill="#ffffff"/>']
        if self.title:
            body.append(self._text(self.w/2, 30, self.title, 19, INK, "bold"))
        body += self.items + ["</svg>"]
        return "\n".join(body)

    def save(self, path_no_ext, png_width=None):
        open(path_no_ext + ".svg", "w").write(self.svg())
        subprocess.run(["rsvg-convert", "-w", str(png_width or self.w * 2), path_no_ext + ".svg",
                        "-o", path_no_ext + ".png"], check=True)

def _card(self, x, y, w, h, icon, title, sub=None, color=BLUE, step=None, icon_size=None, title_size=16):
    """A colored card with an icon, a bold title, and an optional subtitle."""
    if icon and icon not in self.used: self.used.append(icon)
    isz = icon_size or min(w * 0.5, h * 0.45)
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="10" fill="#ffffff" stroke="{color}" stroke-width="2.2" filter="url(#f-drop)"/>'
         f'<rect x="{x}" y="{y}" width="{w}" height="8" rx="4" fill="{color}"/>')
    cy = y + 14
    if icon:
        s += f'<use href="#i-{icon}" x="{x + w/2 - isz/2:.1f}" y="{cy:.1f}" width="{isz:.1f}" height="{isz:.1f}"/>'
        cy += isz + 6
    s += self._text(x + w/2, cy + title_size*0.8, title, title_size, color, "bold")
    cy += title_size + 8
    if sub:
        for line in sub.split("\n"):
            s += self._text(x + w/2, cy + 10, line, 13, INK); cy += 16
    self._add(s, step)
Fig.card = _card

def _poly(self, pts, fill="none", stroke=INK, width=2, step=None, opacity=1, dash=False):
    d = ' stroke-dasharray="7 5"' if dash else ""
    self._add(f'<polygon points="{" ".join(f"{a:.1f},{b:.1f}" for a, b in pts)}" fill="{fill}" stroke="{stroke}" '
              f'stroke-width="{width}" fill-opacity="{opacity}"{d}/>', step)
Fig.poly = _poly

def _circle(self, cx, cy, r, fill="none", stroke=INK, width=2, step=None, opacity=1):
    self._add(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" fill-opacity="{opacity}" stroke="{stroke}" stroke-width="{width}"/>', step)
Fig.circle = _circle

def _rect(self, x, y, w, h, fill="none", stroke=INK, width=1.5, rx=4, step=None, opacity=1, dash=False):
    d = ' stroke-dasharray="6 4"' if dash else ""
    self._add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{opacity}" '
              f'stroke="{stroke}" stroke-width="{width}"{d}/>', step)
Fig.rect = _rect

def _bars(self, x0, y0, w, h, labels, values, ymax, tick, ylabel=None, colors=None, icons=None, fmt="{:g}",
          first_step=1, bar_w=None, label_size=13):
    """Vertical bar chart; each bar is its own build step. (x0, y0) is the bottom-left of the plot area."""
    n = len(values); slot = w / n; bw = bar_w or slot * 0.55
    self.raw(f'<line x1="{x0}" y1="{y0}" x2="{x0 + w}" y2="{y0}" stroke="#52606d" stroke-width="2"/>')
    v = 0
    while v <= ymax + 1e-9:
        y = y0 - h * v / ymax
        self.raw(f'<line x1="{x0}" y1="{y:.1f}" x2="{x0 + w}" y2="{y:.1f}" stroke="#e4e7eb"/>')
        self.text(x0 - 8, y + 4, fmt.format(v), 12, MUTED, anchor="end"); v += tick
    if ylabel:
        cy = y0 - h / 2
        self.raw(f'<text x="{x0 - 52}" y="{cy}" font-family="{FONT}" font-size="13" fill="{MUTED}" text-anchor="middle" '
                 f'transform="rotate(-90 {x0 - 52} {cy})">{esc(ylabel)}</text>')
    for k, (lab, val) in enumerate(zip(labels, values)):
        cx = x0 + slot * (k + .5); hh = h * val / ymax; st = first_step + k
        col = (colors[k] if isinstance(colors, list) else colors) or BLUE
        self.rect(cx - bw / 2, y0 - hh, bw, hh, col, col, 1, rx=3, step=st)
        top = y0 - hh
        if icons and icons[k]:
            self.icon(icons[k], cx, top - 26, 40, step=st); top -= 48
        self.text(cx, top - 8, fmt.format(val), 14, INK, "bold", step=st)
        for i, line in enumerate(str(lab).split("\n")):
            self.text(cx, y0 + 20 + i * 16, line, label_size, INK, "bold" if i == 0 else "normal", step=st)
Fig.bars = _bars
