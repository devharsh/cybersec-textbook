"""Put the new animated figure above an existing {image} block in a notebook.
The old figure stays right below it, so readers see both versions."""
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
               f"```{{image}} {m.group(1)}\n{opts}```\n")
        s = s[:m.start()] + new + s[m.end():]
        c["source"] = lines(s); n += 1
    if n:
        open(nb_path, "w").write(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
    return n

def publish(src_no_ext, book_root, name):
    for ext in (".svg", ".png"):
        shutil.copy(src_no_ext + ext, f"{book_root}/assets/figures/v2/{name}{ext}")


def unwrap(nb_path):
    """Turn earlier collapsed dropdowns back into a plain image shown below the new figure."""
    nb = json.load(open(nb_path)); n = 0
    pat = re.compile(r"````\{admonition\} Earlier version of this figure\n:class: dropdown\n(```\{image\}[^`]*```\n)````\n")
    for c in nb["cells"]:
        if c["cell_type"] != "markdown": continue
        s = "".join(c["source"]); s2, k = pat.subn(lambda m: m.group(1), s)
        if k: c["source"] = lines(s2); n += k
    if n: open(nb_path, "w").write(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
    return n

def add_new(nb_path, heading, name, alt, width="95%", after_text=None, after_block=False):
    """Append a new animated figure to the first markdown cell of the section whose heading starts with `heading`
    (for example '## 3.7 '), or right after the paragraph containing `after_text` if given."""
    nb = json.load(open(nb_path))
    if any("figures/v2/" + name + "." in "".join(c["source"]) for c in nb["cells"]): return 0
    block = (f"\n\n```{{image}} ../../assets/figures/v2/{name}.*\n:alt: {alt}\n:width: {width}\n:align: center\n"
             f":class: anim-fig\n```\n")
    for c in nb["cells"]:
        if c["cell_type"] != "markdown": continue
        s = "".join(c["source"])
        if after_text:
            i = s.find(after_text)
            if i < 0: continue
            if after_block:  # place after the fenced block (for example a mermaid diagram) that contains after_text
                j = s.find("\n```", i); j = s.find("\n", j + 4); j = len(s) if j < 0 else j
            else:
                j = s.find("\n\n", i); j = len(s) if j < 0 else j
            s = s[:j] + block.rstrip("\n") + "\n" + s[j:]
        elif s.lstrip().startswith(heading):
            s = s.rstrip("\n") + block
        else:
            continue
        c["source"] = lines(s)
        open(nb_path, "w").write(json.dumps(nb, indent=1, ensure_ascii=False) + "\n")
        return 1
    raise ValueError(f"no place for {name} in {nb_path}")


def md_block(prefix, name, alt, width="95%"):
    return (f"```{{image}} {prefix}_static/figures/{name}.*\n:alt: {alt}\n:width: {width}\n:align: center\n:class: anim-fig\n```\n")


def md_add(md_path, name, alt, after_text, prefix="../", width="95%"):
    """Insert an animated figure after the paragraph (or fenced block, if after_text is inside one) containing after_text."""
    s = open(md_path).read()
    if f"_static/figures/{name}." in s: return 0
    i = s.find(after_text)
    if i < 0: raise ValueError(f"anchor not found for {name}: {after_text}")
    fence = s.rfind("```", 0, i); inside = fence >= 0 and s.count("```", 0, i) % 2 == 1
    if inside:
        j = s.find("\n```", i); j = s.find("\n", j + 4)
    else:
        j = s.find("\n\n", i)
    j = len(s) if j < 0 else j
    s = s[:j] + "\n\n" + md_block(prefix, name, alt, width).rstrip("\n") + s[j:]
    open(md_path, "w").write(s); return 1


def md_swap(md_path, old_ref, name, alt, prefix="../", width="95%"):
    """Show the new animated figure directly above an existing figure directive that references old_ref."""
    s = open(md_path).read()
    if f"_static/figures/{name}." in s: return 0
    i = s.find(old_ref)
    if i < 0: raise ValueError(f"old figure not found: {old_ref}")
    k = s.rfind("```{", 0, i)
    s = s[:k] + md_block(prefix, name, alt, width) + "\n" + s[k:]
    open(md_path, "w").write(s); return 1
