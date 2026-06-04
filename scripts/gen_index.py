#!/usr/bin/env python3
"""Auto-populate the Sphinx general index from each chapter's Key Terms.
Idempotent: removes prior auto-generated index cells (tagged) and re-adds.
Run before `jupyter-book build`."""
import json, glob, re, os

def key_terms(cells):
    terms=[]
    in_kt=False
    for c in cells:
        if c["cell_type"]!="markdown": continue
        for line in "".join(c["source"]).split("\n"):
            if line.startswith("## "):
                in_kt = line.strip().lower().startswith("## key terms")
                continue
            if in_kt:
                m=re.match(r"\s*[-*]\s+\*\*(.+?)\*\*", line)
                if m:
                    t=m.group(1).strip()
                    # take text before a parenthesis/colon; strip acronym expansions in ()
                    t=re.split(r"\s*\(", t)[0].strip().rstrip(":")
                    if t and len(t)<=60: terms.append(t)
    # dedupe, keep order
    seen=set(); out=[]
    for t in terms:
        k=t.lower()
        if k not in seen: seen.add(k); out.append(t)
    return out

n_files=0; n_terms=0
for path in sorted(glob.glob("chapters/*/*.ipynb")):
    nb=json.load(open(path))
    nb["cells"]=[c for c in nb["cells"] if not c.get("metadata",{}).get("autoindex")]
    terms=key_terms(nb["cells"])
    if not terms: 
        json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True); continue
    terms_clean = [t.replace(",", " ").strip() for t in terms]
    body="```{index} " + ", ".join(terms_clean) + "\n```\n"
    cell={"cell_type":"markdown","metadata":{"autoindex":True},
          "source":body.splitlines(keepends=True)}
    import uuid; cell["id"]=uuid.uuid4().hex[:12]
    nb["cells"].append(cell)
    json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
    n_files+=1; n_terms+=len(terms)
print(f"Indexed {n_terms} key terms across {n_files} chapters into the general index.")
