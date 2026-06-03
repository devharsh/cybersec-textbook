import sys, json; sys.path.insert(0,".build")
path="chapters/04_social_engineering/chapter04.ipynb"
nb=json.load(open(path)); cells=nb["cells"]
def find(p):
    for i,c in enumerate(cells):
        if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith(p): return i
def app(p,t):
    i=find(p); cells[i]["source"]=(("".join(cells[i]["source"])).rstrip()+t+"\n").splitlines(keepends=True)

app("## 4.3", r'''

A concrete walkthrough makes the lifecycle vivid. Suppose an attacker targets a mid-size company's
finance team. In *research*, they read the company's website and LinkedIn to learn that Jordan is the
chief financial officer and Sam is an accounts-payable clerk, and they note from a press release that the
firm recently engaged a named construction vendor. In the *hook*, they register a look-alike domain for
that vendor and email Sam a polite note referencing the real project, establishing context and rapport. In
the *play*, a follow-up message, apparently from Jordan and marked urgent, instructs Sam to pay an updated
invoice to new bank details before end of day, combining authority, urgency, and the established pretext.
In the *exit*, once the transfer clears, the attacker goes silent, and the fraud may not surface until the
real vendor asks why it has not been paid. Every defensive control in this chapter maps onto a step: less
public detail would have weakened the research; sender authentication and user suspicion would have caught
the hook; and a policy requiring out-of-band verification and dual approval for changes to payment details
would have stopped the play even after the deception succeeded.''')

app("## 4.6", r'''

Business-email-compromise messages deserve special vigilance because they often lack the crude tells of
mass phishing. They may come from a genuinely compromised or convincingly spoofed account, contain no
link or attachment at all, and consist only of a plausible, well-written business request. The reliable
indicators shift accordingly: an unexpected *change to payment details or banking information*, pressure
to bypass normal procedures, a request to keep the matter confidential, a slightly altered reply-to
address, and timing that exploits when an executive is known to be traveling or unreachable. The defense
is procedural rather than perceptual: any change to payment instructions or any large or unusual transfer
should require verification through a previously known channel and a second approver, regardless of how
authentic the request appears.''')

app("## 4.9", r'''

### Measuring and Sustaining the Human Firewall

A security-awareness program is only as good as its results, so mature organizations measure it. Common
metrics include the *phishing-simulation click rate* (the share of employees who click a simulated lure),
the *report rate* (the share who report it), and the time to first report, since a fast report can trigger
defenses before an attack spreads. The goal is not to punish those who click, which breeds fear and
silence, but to drive the report rate up and the click rate down over time, and to identify roles that
need targeted training. Sustained programs combine periodic training, realistic and varied simulations,
clear and frictionless reporting (such as a one-click "report phishing" button), positive reinforcement
for good catches, and metrics reviewed by leadership. Treating awareness as an ongoing business
investment with measurable outcomes, rather than a one-time compliance checkbox, is what turns a workforce
from the most exploited attack surface into a distributed sensor network, the so-called human firewall,
that complements every technical control in this book.''')

import uuid
for c in cells: c.setdefault("id", uuid.uuid4().hex[:12])
json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="markdown")
codew=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="code")
print(f"chapter04 FINAL2: {mdw} md words (~{mdw/500:.1f} pg) + {codew} code = {mdw+codew}")
