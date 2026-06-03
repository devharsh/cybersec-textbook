import sys, json, uuid; sys.path.insert(0,".build")
from nbbuild import md
path="chapters/04_social_engineering/chapter04.ipynb"
nb=json.load(open(path)); cells=nb["cells"]
def find(p):
    for i,c in enumerate(cells):
        if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith(p): return i
def app(p,t):
    i=find(p); cells[i]["source"]=(("".join(cells[i]["source"])).rstrip()+t+"\n").splitlines(keepends=True)

app("## 4.1", r'''

It is worth dispelling a common misconception that social engineering is merely "lying to people." In
reality it is a disciplined craft that blends reconnaissance, psychology, and performance, and its
practitioners rehearse pretexts, prepare for objections, and exploit organizational structure. The same
skills, applied lawfully and with authorization, are a legitimate part of professional penetration
testing, where social-engineering assessments measure how well an organization's people and procedures
resist manipulation. The ethical line, as throughout this book, is *authorization*: testing an
organization's susceptibility under a written engagement is a service, while the same actions without
permission are fraud. Understanding the attacker's craft in depth is what allows the defender, and the
authorized tester, to anticipate and blunt it.''')

app("## 4.7", r'''

### Environmental and Availability Threats

Physical security also encompasses the environment that keeps systems running, because availability can be
lost to a power event or a fire as surely as to an attacker. **Power anomalies** form a spectrum: a
*power failure* is a total loss of utility power; a *sag* is a brief low voltage; a *surge* or *spike* is
a brief high voltage; a *brownout* is reduced voltage over a longer period (common when summer cooling
demand peaks); and an *over-voltage* is extended high voltage. Defenses include uninterruptible power
supplies (UPS), surge protectors, and backup generators. **Fire** is managed through prevention training,
detection (heat-activated and smoke-activated sensors), and suppression matched to the fire class (Class
A for ordinary combustibles, B for flammable liquids, C for gases, D for metals, and electrical fires
that demand non-conductive agents), with data centers favoring clean-agent systems over water.

Two metrics quantify equipment reliability and recovery and recur in risk and operations planning. The
**mean time between failures (MTBF)** estimates how long a device is expected to operate before failing,
so higher is better, while the **mean time to repair (MTTR)** estimates how long restoration takes, so
lower is better. Organizations often bound MTTR contractually through **service level agreements (SLAs)**
that cap how long a provider may take to repair or replace a system. These ideas connect physical
security to the availability and resilience planning developed in Chapters 5 and 14.''')

app("## 4.8", r'''

Biometric systems are evaluated by their error rates, which a security professional should be able to
interpret. The *false acceptance rate (FAR)* is the proportion of impostors wrongly accepted, a security
failure, while the *false rejection rate (FRR)* is the proportion of legitimate users wrongly rejected, a
usability failure. Tuning a system's sensitivity trades one against the other, and the *crossover error
rate (CER)*, the point where FAR equals FRR, is a common single-number measure of overall accuracy, with
a lower CER indicating a better system. Because biometrics cannot be changed once compromised and raise
privacy concerns, they are best used as one factor within multi-factor authentication rather than as a
sole credential.''')

# News in Focus historical case (Twitter 2020) before Why This Matters
news=md(r'''## News in Focus: The 2020 Twitter Account Takeover

In July 2020, attackers seized control of dozens of high-profile Twitter accounts, including those of
public figures and major companies, and used them to post a cryptocurrency scam. According to subsequent
public investigations, the intrusion did not begin with a software exploit but with **phone spear
phishing (vishing)**: the attackers called Twitter employees, impersonated internal information-technology
staff, and persuaded targets to enter credentials on a convincing look-alike site, ultimately gaining
access to powerful internal account-management tools.

Read through this chapter, the incident is a near-perfect illustration of its themes. The attackers used
*OSINT* to identify employees, *pretexting* and *authority* to impersonate IT, *vishing* as the vector,
and the captured access to reach internal tools no outsider should touch. It also underscores why the
help desk and employees with privileged tooling are prime targets, and why *phishing-resistant
multi-factor authentication* and strict internal-tool access controls matter so much: technical
defenses around those tools could have contained an attack that human deception had already begun. These
details reflect public reporting and an official investigation report, and they preview the
help-desk-focused campaigns described in this chapter's Current News box.
''')
news.setdefault("id", uuid.uuid4().hex[:12])
wi=find("## Why This Matters")
cells[wi:wi]=[news]

for c in cells: c.setdefault("id", uuid.uuid4().hex[:12])
json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="markdown")
codew=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="code")
print(f"chapter04 FINAL: {len(cells)} cells, {mdw} md words (~{mdw/500:.1f} pg) + {codew} code = {mdw+codew}")
