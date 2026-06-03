import sys, pickle; sys.path.insert(0,".build")
from nbbuild import md, code
C=pickle.load(open(".build/_ch03.pkl","rb")); A=C.append

A(md(r'''## 3.10 Denial-of-Service and Distributed Denial-of-Service Attacks

The attacks so far targeted confidentiality and integrity by listening or impersonating. Denial-of-service
attacks target the third pillar of the CIA triad, *availability*, by exhausting a resource until
legitimate users cannot be served. A **denial-of-service (DoS)** attack comes from one source; a
**distributed denial-of-service (DDoS)** attack comes from many compromised machines at once, typically
a *botnet* of malware-infected devices under one attacker's control. Alarmingly, DoS capability is now a
cheap commodity: so-called *booter* or *stresser* services sell attacks online for a few dollars, payable
by credit card or cryptocurrency, which is why the barrier to launching one has collapsed.

DoS and DDoS attacks fall into three categories, and recognizing the category points to the defense.
**Volumetric** attacks consume raw bandwidth, drowning the link in traffic. **Protocol (or
state-exhaustion)** attacks consume connection-tracking resources in servers, firewalls, and load
balancers. **Application-layer** attacks consume the resources a specific application needs, often with
modest traffic that mimics legitimate requests and is therefore hard to filter.

Several classic techniques illustrate the categories. The **SYN flood** is the archetypal protocol
attack: the attacker sends many SYN packets with spoofed source addresses, leaving the server with a
backlog of *half-open* connections that fills its connection table and blocks legitimate clients;
spoofing the source also hides the attacker. The **Ping of Death** sends a fragmented ICMP packet that,
once reassembled, exceeds the maximum legal size and crashes older systems. **Teardrop** sends
overlapping, oversized fragments that the target cannot reassemble. The **Land** attack sends a packet
whose source and destination address and port are identical, confusing the target. **Smurf** and
**Fraggle** are amplification attacks: Smurf sends ICMP echo requests to a network's broadcast address
spoofing the victim's source so all replies flood the victim, while Fraggle does the same with UDP echo
packets to port 7. Amplification and *reflection* using DNS, the Network Time Protocol (NTP), and
similar UDP services let a small request generate a huge response aimed at the victim, which is how
modern record-breaking volumetric attacks reach tens of terabits per second. **DHCP starvation**, seen
earlier, is a DoS on the address pool itself.

The defenses mirror the categories. For SYN floods specifically, six well-known mitigations exist:
*increasing the backlog queue* so more half-open connections can be held; *recycling the oldest half-open
connection* when the queue fills; *micro blocks*, allocating a tiny record rather than a full connection
object per SYN; *SYN cookies*, in which the server encodes connection state in the sequence number and
allocates no memory until the handshake completes; *RST cookies*, which deliberately send an invalid
SYN-ACK to verify a real client; and *stack tweaking*, reducing connection timeouts. Broadly, volumetric
attacks are absorbed by upstream scrubbing and content-delivery networks, protocol attacks by SYN cookies
and stateful filtering, and application attacks by rate limiting and behavioral analysis.
'''))

A(md(r'''```{admonition} Current News: the terabit era of DDoS (2025-2026)
:class: important
Distributed denial of service has scaled to once-unimaginable size. According to Cloudflare's Q4 2025
DDoS Threat Report, the company mitigated a record volumetric attack that peaked at **31.4 terabits per
second (Tbps)** and lasted only about 35 seconds, the culmination of a year in which a series of records
fell in quick succession, including attacks of 7.3, 11.5, 22.2, and 29.7 Tbps (the last attributed to a
botnet known as AISURU). Cloudflare reported mitigating roughly **47.1 million DDoS attacks** across
2025, an average of several thousand per hour, with the largest absorbed automatically by autonomous
defenses. These figures, drawn from vendor reporting, illustrate two themes from this chapter: modern
volumetric DDoS is driven by large botnets and amplification, and defense has shifted to always-on,
automated scrubbing at internet scale rather than per-incident human response.
```
'''))

A(code(r'''# Chapter 3 -- Visualizing the 2025 escalation in record DDoS attack size
# Source: Cloudflare DDoS threat reports, 2025 (figures as publicly reported).
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

events = ["May\n7.3", "Sep\n11.5", "Late Sep\n22.2", "Q4\n29.7", "Q4 peak\n31.4"]
tbps   = [7.3, 11.5, 22.2, 29.7, 31.4]
fig, ax = plt.subplots(figsize=(8, 4))
bars = ax.bar(events, tbps, color="#2c7fb8")
ax.set_ylabel("Peak attack size (Tbps)")
ax.set_title("Record DDoS attacks mitigated by Cloudflare during 2025 (as reported)")
for b, v in zip(bars, tbps):
    ax.text(b.get_x()+b.get_width()/2, b.get_height()+0.3, f"{v}", ha="center", fontsize=9)
ax.set_ylim(0, 35)
plt.tight_layout(); plt.savefig("ch03_ddos_2025.png", dpi=110)
print("Saved ch03_ddos_2025.png")
print("Each record stood for only weeks, illustrating the DDoS arms race of 2025.")''' ))

A(md(r'''## 3.11 Securing the Network: A Preview

This chapter has shown, layer by layer, how networks are observed and disrupted. The corresponding
defenses are developed fully in Chapters 11 and 12, but it is worth naming them here so the attacks do
not end on a note of helplessness. At Layer 2, *port security*, *dynamic ARP inspection*, and *DHCP
snooping* counter MAC flooding, ARP poisoning, and rogue DHCP servers. At Layer 3 and above,
*ingress and egress filtering* reject packets with forged or impossible source addresses, blunting
spoofing and reflection. *Network segmentation* limits how far an attacker who gains a foothold can
move. *Encryption*, above all universal TLS, defeats sniffing and session hijacking by denying the
attacker usable plaintext. And *firewalls* and *intrusion detection and prevention systems*, the
subjects of Chapters 11 and 12, watch and filter the very packets this chapter taught you to read. The
recurring lesson is that most network attacks exploit protocols that were designed for a smaller, more
trusting internet, and that defense consists largely of adding the authentication and validation those
protocols originally lacked.
'''))
print("part D:", len(C))
pickle.dump(C, open(".build/_ch03.pkl","wb"))
