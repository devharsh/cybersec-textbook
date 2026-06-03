"""Helper to assemble Jupyter notebooks for the textbook.
Usage from a chapter build script:
    from nbbuild import md, code, write_nb
    cells = [md(\"\"\"# Chapter ...\"\"\"), code(\"...\"), ...]
    write_nb("chapters/01_intro/chapter01.ipynb", cells)
"""
import json, os, sys, uuid

def md(text):
    return {"cell_type":"markdown","id":uuid.uuid4().hex[:12],"metadata":{},"source":text.splitlines(keepends=True)}

def code(text):
    return {"cell_type":"code","id":uuid.uuid4().hex[:12],"metadata":{},"execution_count":None,"outputs":[],
            "source":text.splitlines(keepends=True)}

def write_nb(path, cells):
    nb={"cells":cells,
        "metadata":{"kernelspec":{"display_name":"Python 3","language":"python","name":"python3"},
                    "language_info":{"name":"python"}},
        "nbformat":4,"nbformat_minor":5}
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path,"w") as f: json.dump(nb,f,indent=1,ensure_ascii=True)
    mdw=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="markdown")
    print(f"wrote {path}: {len(cells)} cells, {mdw} markdown words (~{mdw/500:.1f} pages)")
    return mdw
