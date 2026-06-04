import json, glob, re, os, datetime

CHAP_ORDER = ["00_intro","00_preface"] + [d for d in []]
def md_words(s): return len(s.split())

def chapter_files():
    # order by _toc
    import yaml
    toc=yaml.safe_load(open("_toc.yml"))
    files=[]
    for part in toc.get("parts",[]):
        for ch in part.get("chapters",[]):
            files.append((part.get("caption",""), ch["file"], ch.get("title")))
    return toc["root"], files

def analyze(path):
    """Return (h1, [(heading, level, words)], total_md, total_code)."""
    if path.endswith(".md") or os.path.exists(path+".md"):
        p = path if path.endswith(".md") else path+".md"
        text=open(p).read()
        cells=[("markdown",text)]
    else:
        p=path+".ipynb"
        nb=json.load(open(p))
        cells=[(c["cell_type"],"".join(c["source"])) for c in nb["cells"] if not c.get("metadata",{}).get("autoindex")]
    h1=None; sections=[]; cur=["(front matter)",2,0]; total_md=0; total_code=0
    started=False
    for ctype,src in cells:
        if ctype=="code":
            total_code+=md_words(src); 
            # attribute code words to current section count? keep separate; skip
            continue
        for line in src.split("\n"):
            if line.startswith("# ") and h1 is None:
                h1=line[2:].strip(); continue
            if line.startswith("## "):
                if started: sections.append(tuple(cur))
                cur=[line[3:].strip(),2,0]; started=True; continue
            if line.startswith("### "):
                if started: sections.append(tuple(cur))
                cur=["    "+line[4:].strip(),3,0]; started=True; continue
            w=md_words(line); cur[2]+=w; total_md+=w
    if started: sections.append(tuple(cur))
    return h1 or os.path.basename(path), sections, total_md, total_code

root, files = chapter_files()
out=[]
out.append("# Appendix G: Book Statistics and Word Counts\n")
out.append("This page reports the size of each chapter and of each section within it, measured in markdown "
           "words (the prose; code and figures are additional and reported separately per chapter). It is "
           "generated automatically from the book source. Approximate pages assume about 500 words per "
           f"page.\n\nLast generated: {datetime.date.today().isoformat()}.\n")
grand_md=0; grand_code=0
summary=["## Summary by Chapter\n","| Chapter | Markdown words | Code words | Approx. pages |","|---|---:|---:|---:|"]
detail=[]
for caption, f, title in files:
    if f.endswith('appendix_g/appendix_g'):
        continue  # do not count the statistics page itself
    h1, sections, tmd, tcode = analyze(f)
    grand_md+=tmd; grand_code+=tcode
    name = title or h1
    summary.append(f"| {name} | {tmd:,} | {tcode:,} | {tmd/500:.1f} |")
    detail.append(f"\n### {name}\n")
    detail.append(f"*{tmd:,} markdown words ({tmd/500:.1f} pages); {tcode:,} code words.*\n")
    detail.append("| Section | Words |")
    detail.append("|---|---:|")
    for (hd, lvl, w) in sections:
        if w==0 and hd.strip()=="(front matter)": continue
        detail.append(f"| {hd} | {w:,} |")
summary.append(f"| **TOTAL** | **{grand_md:,}** | **{grand_code:,}** | **{grand_md/500:.0f}** |")
out += summary
out.append("\n## Detailed Word Count by Section\n")
out += detail
os.makedirs("chapters/appendix_g", exist_ok=True)
open("chapters/appendix_g/appendix_g.md","w").write("\n".join(out)+"\n")
print(f"Wrote appendix_g.md  | grand md={grand_md:,}  code={grand_code:,}  pages~{grand_md/500:.0f}")

# --- stamp "Last updated" into intro.md ---
import datetime as _dt, re as _re
_ts = _dt.datetime.now(_dt.timezone.utc).strftime("%m/%d/%Y at %H:%M:%S UTC")
try:
    _intro = open("intro.md").read()
    _new = _re.sub(r"\*Last updated[^*]*\*", f"*Last updated on {_ts}*", _intro, count=1)
    if _new != _intro:
        open("intro.md","w").write(_new)
        print("stamped intro.md last-updated:", _ts)
    else:
        print("WARNING: last-updated marker not found in intro.md")
except FileNotFoundError:
    print("intro.md not found; skip stamp")
