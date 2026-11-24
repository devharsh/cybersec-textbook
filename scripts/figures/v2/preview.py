"""Make a GIF that shows the build, step by step, from a figure SVG."""
import re, subprocess, sys, io
from PIL import Image
def gif(svg_path, gif_path, width=1000, step_ms=1000, hold_ms=3000):
    svg = open(svg_path).read()
    n = max(int(k) for k in re.findall(r'class="st s(\d+)"', svg))
    frames = []
    for k in range(0, n + 1):
        hide = "".join(f".s{j}{{opacity:0}}" for j in range(k + 1, n + 1))
        v = re.sub(r"<style>.*?</style>", f"<style>{hide}</style>", svg, flags=re.S)
        png = subprocess.run(["rsvg-convert", "-w", str(width)], input=v.encode(), capture_output=True, check=True).stdout
        frames.append(Image.open(io.BytesIO(png)).convert("RGB"))
    durs = [step_ms] * n + [hold_ms]
    frames[0].save(gif_path, save_all=True, append_images=frames[1:], duration=durs, loop=0, optimize=True)
    return n
if __name__ == "__main__":
    for p in sys.argv[1:]:
        print(p, gif(p, p.replace(".svg", "_build.gif")))
