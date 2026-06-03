import sys, json; sys.path.insert(0,".build")
path="chapters/04_social_engineering/chapter04.ipynb"
nb=json.load(open(path)); cells=nb["cells"]
def find(p):
    for i,c in enumerate(cells):
        if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith(p): return i
def app(p,t):
    i=find(p); cells[i]["source"]=(("".join(cells[i]["source"])).rstrip()+t+"\n").splitlines(keepends=True)

app("## 4.10", r'''

Defenders are not standing still. The same AI techniques aid detection: models can flag the linguistic and
metadata anomalies of machine-generated phishing, voice-liveness and deepfake-detection tools can scrutinize
calls and video, and behavioral analytics can spot the unusual access patterns that follow a successful
deception. But detection will always lag generation to some degree, so policy must not depend on it. The
prudent posture treats every high-stakes request, money movement, credential or access changes, privileged
actions, as requiring provenance that synthetic media cannot forge: a callback to a number already on file,
a shared secret agreed in advance, or a second human approver acting through a separate system. In short,
AI changes the realism of the attack but not its remedy, which remains to anchor trust in verifiable
process rather than in how convincing a message looks or sounds.''')

app("## 4.7", r'''

Operational-technology environments raise the stakes of physical and social attacks further. Supervisory
control and data acquisition (SCADA) systems run power distribution, water treatment, and pipelines, and
because they are often old, infrequently patched, and designed on the assumption of physical isolation,
they may lack basic security controls. A social engineer who gains physical entry to such a facility, or
who talks an operator into an action, can therefore cause consequences in the physical world, not merely
the digital one, which is why critical-infrastructure protection treats physical access control as a
safety issue as much as a security one. This theme is developed fully in Chapter 20.''')

import uuid
for c in cells: c.setdefault("id", uuid.uuid4().hex[:12])
json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="markdown")
codew=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="code")
print(f"chapter04 DONE: {mdw} md words (~{mdw/500:.1f} pg) + {codew} code = {mdw+codew}")
