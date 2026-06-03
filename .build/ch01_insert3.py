import json
path="chapters/01_intro/chapter01.ipynb"
nb=json.load(open(path))
addition = r'''

### A Second Case: The SolarWinds Supply-Chain Compromise (2020)

A contrasting example shows the opposite end of the adversary spectrum. In late 2020 it emerged that
attackers had inserted malicious code into a software build of SolarWinds Orion, a widely used network
management product. Because the tampered update was signed and distributed through the vendor's
legitimate channel, it was trusted and installed by thousands of organizations, including government
agencies and major enterprises. The operation has been publicly attributed by the United States
government to a nation-state intelligence service, the hallmark of an advanced persistent threat.

Through this chapter's lens, the contrast with Colonial Pipeline is stark. The **threat actor** was not
a profit-seeking criminal but a patient, well-resourced APT pursuing **espionage**. The **attack
vector** was the **software supply chain**: rather than attacking each target directly, the adversary
compromised a single trusted vendor and let normal update mechanisms carry the implant to victims. The
primary property at risk was **confidentiality**, the covert exfiltration of sensitive information, and
the campaign maintained stealthy, **persistent** access for months before discovery. No firewall rule
or password policy at the victims would have blocked an update they had every reason to trust, which is
precisely why supply-chain attacks are so insidious and why defenses such as software bills of
materials, build-system integrity, and assume-breach detection have risen in prominence. As with the
previous case, these details derive from public reporting and official statements and may be refined as
analysis continues. Taken together, the two incidents illustrate the full range of the adversary model:
an opportunistic criminal exploiting basic hygiene failures, and a strategic state actor subverting the
chain of trust itself.'''
for c in nb["cells"]:
    if c["cell_type"]=="markdown" and "".join(c["source"]).startswith("## News in Focus"):
        c["source"]= (("".join(c["source"])).rstrip()+addition+"\n").splitlines(keepends=True)
        break
json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in nb["cells"] if c["cell_type"]=="markdown")
codew=sum(len("".join(c["source"]).split()) for c in nb["cells"] if c["cell_type"]=="code")
print(f"chapter01: {len(nb['cells'])} cells, {mdw} md words (~{mdw/500:.1f} pg), +{codew} code words")
