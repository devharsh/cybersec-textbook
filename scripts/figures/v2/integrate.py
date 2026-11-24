"""Swap an {image} block in a notebook for the new animated figure, and keep the
old figure below it in a collapsed dropdown, so both versions stay in the book."""
import json, re, shutil

def lines(t):
    L = t.split("\n"); return [l + "\n" for l in L[:-1]] + ([L[-1]] if L[-1] else [])

def swap(nb_path, old_png, new_name, alt=None, width="95%"):
    nb = json.load(open(nb_path)); n = 0
    pat = re.compile(r"```\{image\} (\.\./\.\./assets/figures/" + re.escape(old_png) + r")\n((?::[^\n]*\n)*)```\n?")
    for c in nb["cells"]:
        if c["cell_type"] != "markdown": continue
        s = "".join(c["source"])
        if "figures/v2/" + new_name in s: continue
        m = pat.search(s)
        if not m: continue
        opts = m.group(2)
        old_alt = re.search(r":alt: ([^\n]*)", opts)
        a = alt or (old_alt.group(1) if old_alt else new_name)
        new = (f"```{{image}} ../../assets/figures/v2/{new_name}.*\n:alt: {a}\n:width: {width}\n:align: center\n:class: anim-fig\n```\n\n"
               f"````{{admonition}} Earlier version of this figure\n:class: dropdown\n"
               f"```{{image}} {m.group(1)}\n{opts}```\n````\n")
        s = s[:m.start()] + new + s[m.end():]
        c["source"] = lines(s); n += 1
    if n:
        open(nb_path, "w").write(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
    return n

def publish(src_no_ext, book_root, name):
    for ext in (".svg", ".png"):
        shutil.copy(src_no_ext + ext, f"{book_root}/assets/figures/v2/{name}{ext}")
