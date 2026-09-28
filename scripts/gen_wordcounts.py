import json, glob, re, os, datetime, statistics

CHAP_ORDER = ["00_intro","00_preface"] + [d for d in []]
WORDS_PER_PAGE = 500          # the one page measure used by Appendix G and by the Introduction
INTRO_PATH = "chapters/00_intro/introduction.md"

def md_words(s): return len(s.split())

def chapter_files():
    # order by _toc
    import yaml
    toc=yaml.safe_load(open("_toc.yml"))
    files=[]
    for part in toc.get("parts",[]):
        for ch in part.get("chapters",[]):
            if "file" not in ch:
                continue  # skip external url entries (e.g., General Index link)
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

def compute(files):
    """Word counts for every page in the table of contents except Appendix G itself."""
    rows=[]
    for caption, f, title in files:
        if f.endswith('appendix_g/appendix_g'):
            continue  # do not count the statistics page itself
        h1, sections, tmd, tcode = analyze(f)
        rows.append((title or h1, sections, tmd, tcode))
    return rows

# --- keep the reading-load figures in the Introduction on the same measure as Appendix G ---------
# The Introduction used to carry page counts typed in by hand, and they drifted away from Appendix G
# as chapters grew. Everything numeric about reading load there is now written from the same word
# counts, between BEGIN/END generated markers, every time this script runs (locally and in CI).

def _pages(words): return words / WORDS_PER_PAGE
def _round5(x): return int(5 * round(x / 5.0))
_NUMBER_WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
                 8: "eight", 9: "nine", 10: "ten"}

def _section_words(sections, chapter_no, lo, hi):
    """Words in top-level sections chapter_no.lo through chapter_no.hi, subsections included."""
    total, inside = 0, False
    for hd, lvl, w in sections:
        if lvl == 2:
            m = re.match(rf"{chapter_no}\.(\d+)\b", hd.strip())
            inside = bool(m) and lo <= int(m.group(1)) <= hi
        if inside:
            total += w
    return total

def _last_section(sections, chapter_no):
    nums = [int(m.group(1)) for hd, lvl, w in sections if lvl == 2
            for m in [re.match(rf"{chapter_no}\.(\d+)\b", hd.strip())] if m]
    return max(nums) if nums else None

def _replace_block(text, key, body):
    begin = f"<!-- BEGIN generated:{key}"
    end = f"<!-- END generated:{key} -->"
    i = text.find(begin)
    j = text.find(end)
    if i < 0 or j < 0 or j < i:
        print(f"WARNING: generated:{key} markers not found in {INTRO_PATH}; left unchanged")
        return text
    i = text.index("-->", i) + 3
    return text[:i] + "\n\n" + body.strip() + "\n\n" + text[j:]

def _block(text, key):
    i = text.find(f"<!-- BEGIN generated:{key}")
    j = text.find(f"<!-- END generated:{key} -->")
    if i < 0 or j < 0:
        return None
    return text[text.index("-->", i) + 3:j]

def _course_table(old, ch_pages, chapters_total, book_total):
    out = []
    for line in old.strip().splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 3 or cells[0] == "Course" or set(cells[0]) <= set("-: "):
            out.append(line.strip())
            continue
        name, chapters, _ = cells
        if chapters.lower().startswith("all chapters"):
            pages = f"{chapters_total:.0f} (about {book_total:.0f} with appendices)"
        else:
            counted = [int(n) for n in re.findall(r"\d+", re.sub(r"\([^)]*\)", "", chapters))]
            missing = [n for n in counted if n not in ch_pages]
            if missing:
                print(f"WARNING: course row {name!r} lists unknown chapters {missing}; row left unchanged")
                out.append(line.strip())
                continue
            pages = str(_round5(sum(ch_pages[n] for n in counted)))
        out.append(f"| {name} | {chapters} | {pages} |")
    return "\n".join(out)

def update_intro(rows):
    if not os.path.exists(INTRO_PATH):
        print(f"{INTRO_PATH} not found; skip reading-load figures")
        return False
    ch_pages, ch_sections = {}, {}
    for name, sections, tmd, tcode in rows:
        m = re.match(r"Chapter (\d+):", name)
        if m:
            ch_pages[int(m.group(1))] = _pages(tmd)
            ch_sections[int(m.group(1))] = sections
    book_total = _pages(sum(r[2] for r in rows))
    chapters_total = sum(ch_pages.values())
    text = open(INTRO_PATH).read()
    new = text

    table = _block(new, "course-pages")
    if table is not None:
        new = _replace_block(new, "course-pages", _course_table(table, ch_pages, chapters_total, book_total))

    new = _replace_block(new, "page-basis", (
        f"The page counts are estimates at about {WORDS_PER_PAGE} words of prose per page, the same measure "
        "Appendix G uses, and they count only the listed chapters, not the appendices. Code listings, figures, "
        "and tables are not counted, so a typeset copy will run to a different length. These figures, like "
        "Appendix G, are regenerated from the book source whenever the book is rebuilt. They are a planning aid "
        f"for gauging reading load per course: on the same measure the {len(ch_pages)} chapters come to about "
        f"{chapters_total:.0f} pages, and the whole book, with its front matter and appendices, to about "
        f"{book_total:.0f}. Several courses now exceed a single term's reading if every listed chapter is covered "
        "in full, so the guidance under *Adapting the Reading Load* below on trimming the encyclopedic back "
        "sections of the longer chapters applies directly."))

    ranked = sorted(ch_pages.items(), key=lambda kv: kv[1], reverse=True)
    (a, pa), (b, pb), (c, pc) = ranked[:3]
    if {a, b} != {2, 15}:
        print(f"WARNING: the two longest chapters are now {a} and {b}, not 2 and 15; "
              f"review the reading-load advice written into {INTRO_PATH}")
    (x, px), (y, py) = sorted([(a, pa), (b, pb)])
    median = statistics.median(ch_pages.values())
    times_median = int(min(px, py) // median)
    s15 = ch_sections.get(15, [])
    last15 = _last_section(s15, 15) or 22
    p15_core = _pages(_section_words(s15, 15, 1, 21))
    p15_deep = _pages(_section_words(s15, 15, 22, last15))
    new = _replace_block(new, "outliers", (
        f"**Chapters {x} and {y} are the outliers.** At about {px:.0f} and {py:.0f} pages, they are roughly "
        f"{px / pc:.1f} and {py / pc:.1f} times the length of the next-longest chapter, Chapter {c} (about "
        f"{pc:.0f} pages), and more than {_NUMBER_WORDS.get(times_median, str(times_median))} times the median "
        f"chapter (about {median:.0f} pages), so either one dominates any course that includes it.\n\n"
        "For Chapter 2 in a certification-oriented or introductory course, Sections 2.1 through 2.14 (through the "
        "TLS handshake) plus 2.16 through 2.19b (key management, the attack taxonomy, applied systems, practical "
        "guidance, protecting data in its three states, and tamper-evident mechanisms) carry the examinable "
        "material. Sections 2.15 and 2.15a (advanced and emerging cryptography, including homomorphic encryption "
        "and lattices, and privacy-preserving constructions such as zero-knowledge proofs) and Section 2.20 "
        "(formal security analysis and provable security) are graduate-level and can be assigned as optional "
        "reading; Section 2.21 (post-quantum standards) repays a single lecture even in an introductory course, "
        "because the migration deadlines are now concrete. Appendix J likewise belongs to the advanced track.\n\n"
        f"For Chapter 15, Sections 15.1 through 15.21 (about {p15_core:.0f} pages) carry the malware-analysis "
        "material, including the reverse-engineering overview in Section 15.10. Sections 15.22 through "
        f"15.{last15} (about {p15_deep:.0f} pages) go deeper, mostly into reverse engineering: disassembly, "
        "Windows internals, obfuscation, analysis tooling, and the discipline itself. The *Software Reverse "
        "Engineering* course draws on them, and other courses can assign them as optional reading."))

    if new != text:
        open(INTRO_PATH, "w").write(new)
        print(f"updated reading-load figures in {INTRO_PATH}: chapter 2 {ch_pages.get(2, 0):.1f} pp, "
              f"chapter 15 {ch_pages.get(15, 0):.1f} pp, chapters {chapters_total:.0f} pp, book {book_total:.0f} pp")
        return True
    return False

root, files = chapter_files()
rows = compute(files)
for _ in range(3):                 # the Introduction is itself counted, so settle it before writing G
    if not update_intro(rows):
        break
    rows = compute(files)

out=[]
out.append("# Appendix G: Book Statistics and Word Counts\n")
out.append("This page reports the size of each chapter and of each section within it, measured in markdown "
           "words (the prose; code and figures are additional and reported separately per chapter). It is "
           f"generated automatically from the book source. Approximate pages assume about {WORDS_PER_PAGE} words per "
           f"page.\n\nLast generated: {datetime.date.today().isoformat()}.\n")
grand_md=0; grand_code=0
summary=["## Summary by Chapter\n","| Chapter | Markdown words | Code words | Approx. pages |","|---|---:|---:|---:|"]
detail=[]
for name, sections, tmd, tcode in rows:
    grand_md+=tmd; grand_code+=tcode
    summary.append(f"| {name} | {tmd:,} | {tcode:,} | {_pages(tmd):.1f} |")
    detail.append(f"\n### {name}\n")
    detail.append(f"*{tmd:,} markdown words ({_pages(tmd):.1f} pages); {tcode:,} code words.*\n")
    detail.append("| Section | Words |")
    detail.append("|---|---:|")
    for (hd, lvl, w) in sections:
        if w==0 and hd.strip()=="(front matter)": continue
        detail.append(f"| {hd} | {w:,} |")
summary.append(f"| **TOTAL** | **{grand_md:,}** | **{grand_code:,}** | **{_pages(grand_md):.0f}** |")
out += summary
out.append("\n## Detailed Word Count by Section\n")
out += detail
os.makedirs("chapters/appendix_g", exist_ok=True)
open("chapters/appendix_g/appendix_g.md","w").write("\n".join(out)+"\n")
print(f"Wrote appendix_g.md  | grand md={grand_md:,}  code={grand_code:,}  pages~{_pages(grand_md):.0f}")

# --- stamp "Last updated" into intro.md ---
import datetime as _dt, re as _re
try:
    from zoneinfo import ZoneInfo as _ZI
    _tz = _ZI("America/New_York")
except Exception:
    _tz = _dt.timezone(_dt.timedelta(hours=-5), "EST")
_ts = _dt.datetime.now(_tz).strftime("%m/%d/%Y at %H:%M:%S %Z")
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
