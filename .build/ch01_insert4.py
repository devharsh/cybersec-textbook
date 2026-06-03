import json
path="chapters/01_intro/chapter01.ipynb"
nb=json.load(open(path))
extra = r'''

It is also worth noting how recently this field matured. Through the 1970s and 1980s, computer security
was largely the concern of governments and a handful of researchers; the famous Morris Worm of 1988,
which disrupted a large fraction of the early internet, was a wake-up call that networked systems
created entirely new categories of risk. The commercialization of the internet in the 1990s, the rise
of e-commerce, the explosion of mobile and cloud computing in the 2000s and 2010s, and the more recent
spread of connected devices and artificial intelligence have each enlarged the attack surface and
drawn in new adversaries. Cybersecurity today is thus a young, fast-moving discipline in which the
fundamentals endure even as the specific technologies and threats turn over rapidly, which is exactly
why this book emphasizes durable principles alongside current practice.'''
for c in nb["cells"]:
    if c["cell_type"]=="markdown" and "".join(c["source"]).startswith("## 1.1 What Is Cybersecurity?"):
        c["source"]=(("".join(c["source"])).rstrip()+extra+"\n").splitlines(keepends=True)
        break
json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in nb["cells"] if c["cell_type"]=="markdown")
print(f"chapter01: {mdw} md words (~{mdw/500:.1f} pg)")
