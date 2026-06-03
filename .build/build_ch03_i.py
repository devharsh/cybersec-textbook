import sys, json, uuid; sys.path.insert(0,".build")
from nbbuild import md
path="chapters/03_networking/chapter03.ipynb"
nb=json.load(open(path)); cells=nb["cells"]
def find(p):
    for i,c in enumerate(cells):
        if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith(p): return i
def app(p,t):
    i=find(p); cells[i]["source"]=(("".join(cells[i]["source"])).rstrip()+t+"\n").splitlines(keepends=True)

app("## 3.7", r'''

For the defender and the auditor, DNS is also a rich monitoring opportunity precisely because almost
every connection begins with a name lookup. Logging and analyzing DNS queries can reveal malware reaching
out to command-and-control domains, data being smuggled out through unusually long or frequent queries
(the signature of tunneling), and users being lured to newly registered or look-alike domains used in
phishing. Many organizations now route all DNS through controlled, logged resolvers and block known-bad
domains at that chokepoint, an inexpensive control with broad reach. This dual nature, DNS as both a
prime target and a prime sensor, makes it one of the most strategically important protocols in the entire
stack.''')

app("## 3.8", r'''

### Traffic Analysis and Network Monitoring

The same techniques an attacker uses to sniff are, in defenders' hands, the foundation of network
visibility. *Network traffic analysis* captures and inspects traffic to detect intrusions, troubleshoot
problems, and establish a baseline of normal behavior against which anomalies stand out. Defenders deploy
sensors at chokepoints using SPAN ports or dedicated network taps, feed the data to intrusion detection
systems and to *Security Information and Event Management (SIEM)* platforms, and increasingly retain
*flow records* (such as NetFlow), which summarize who talked to whom, when, and how much, without storing
full packet contents. Even when traffic is encrypted and the payload cannot be read, metadata and
patterns, connection timing, volumes, destinations, and periodic "beaconing" to a command-and-control
server, remain powerful signals. This is why the monitoring concepts introduced here lead directly into
the intrusion-detection material of Chapter 12, and why the line between an attacker's sniffer and a
defender's sensor is one of authorization and intent rather than technology.''')

summary=md(r'''## Chapter Summary

This chapter built the networking foundation that the rest of the book relies on and showed, layer by
layer, how each mechanism becomes an attack surface. The **OSI** and **TCP/IP** models organize
networking into layers, and **encapsulation** wraps data in successive headers as it descends the stack,
producing segments, packets, and frames. **IP addressing** (IPv4 and IPv6), **ports**, and the common
**protocols** identify hosts and services, while **TCP** provides reliable delivery through the three-way
handshake and **UDP** offers fast, spoofable best-effort delivery. The infrastructure protocols **ARP**,
**DHCP**, and **DNS** make networks usable but, lacking authentication by design, are abused through ARP
poisoning, DHCP starvation, and DNS spoofing and tunneling. **Sniffing** (passive and active, with
promiscuous mode, SPAN, and MAC flooding) lets attackers read traffic; **spoofing**,
**man-in-the-middle**, and **session hijacking** (at the transport and application layers) let them
impersonate and seize connections; and **DoS/DDoS** attacks, now reaching tens of terabits per second
through botnets, reflection, and amplification, deny availability. The recurring theme is that the
internet's foundational protocols trust by default, and that defense, encryption, authentication,
filtering, segmentation, and monitoring, consists largely of adding back the verification those protocols
never had. With the wires understood, the next chapter turns to the human layer, where social engineering
attacks bypass all of this technology by targeting people directly.
''')
summary.setdefault("id", uuid.uuid4().hex[:12])
wi=find("## Why This Matters")
cells[wi:wi]=[summary]

for c in cells: c.setdefault("id", uuid.uuid4().hex[:12])
json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="markdown")
codew=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="code")
print(f"chapter03 FINAL: {len(cells)} cells, {mdw} md words (~{mdw/500:.1f} pg) + {codew} code = {mdw+codew}")
