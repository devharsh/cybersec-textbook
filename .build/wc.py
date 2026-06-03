import json,glob,sys
pat=sys.argv[1] if len(sys.argv)>1 else "chapters/*/*.ipynb"
tot=0
for nb in sorted(glob.glob(pat)):
    d=json.load(open(nb))
    mdw=sum(len("".join(c.get("source",[])).split()) for c in d["cells"] if c["cell_type"]=="markdown")
    tot+=mdw
    print(f"{nb:46} {mdw:>7} words  ~{mdw/500:>5.1f} pg")
print(f"{'TOTAL':46} {tot:>7} words  ~{tot/500:>5.1f} pg")
