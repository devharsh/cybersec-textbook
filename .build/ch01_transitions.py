import json
path="chapters/01_intro/chapter01.ipynb"
nb=json.load(open(path)); cells=nb["cells"]
bridges={
 "## 1.1": "We start with the most basic question of all, what the field actually is, because every later idea, from cryptography to incident response, is a specialized answer to the problem this section frames.",
 "## 1.2": "Having defined cybersecurity as the management of risk to information, we need to say precisely what property of information we are trying to preserve. That is the job of the CIA triad and its extensions.",
 "## 1.3": "Knowing what we want to protect (the CIA properties) naturally leads to the opposite question: how is that protection lost? To answer it we need a precise vocabulary for the pieces of an attack.",
 "## 1.4": "The previous section treated the threat abstractly. But defenses must be sized to a real opponent, so we now ask who the threat actors actually are and what they can do.",
 "## 1.5": "Once we accept that capable adversaries exist and that no single barrier stops all of them, the design response follows directly: layer many controls so that one failure is not fatal. This section develops that principle and the vocabulary of controls.",
 "## 1.6": "The controls just described are enforced, ultimately, by mechanisms built into the machine itself. Before leaving foundations, we descend to the hardware layer to see what makes any software control trustworthy in the first place.",
 "## 1.7": "We have now covered the building blocks, properties, attacks, adversaries, controls, and hardware foundations. Organizations need a way to assemble these into a coherent program, and that is exactly what a framework provides; the most widely used one is described next.",
 "## 1.8": "A framework tells us what activities to perform, but leadership still must decide where to spend limited money. To make that case we have to express risk in dollars, which is the purpose of the quantitative model in this section.",
 "## 1.9": "Frameworks and risk math operate at the level of programs. Underneath them sit timeless engineering principles for building individual systems securely, articulated decades ago and still authoritative.",
 "## 1.10": "Principles and mechanisms describe how to build secure systems. But the same knowledge can attack as easily as defend, so we close the conceptual core by addressing the mindset, ethics, and law that govern its use.",
 "## 1.11": "With principles, economics, and ethics established, it helps to step back and survey the full range of threats this knowledge must address, which doubles as a roadmap to the chapters ahead.",
}
def find(p):
    for i,c in enumerate(cells):
        if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith(p): return i
for pref,text in bridges.items():
    i=find(pref)
    if i is None: continue
    body="".join(cells[i]["source"])
    if text[:40] in body: continue
    lines=body.split("\n"); head=lines[0]; rest="\n".join(lines[1:]).lstrip("\n")
    cells[i]["source"]=(head+"\n\n"+text+"\n\n"+rest).splitlines(keepends=True)
json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="markdown")
print(f"ch01 transitions added; now {mdw} md words")
