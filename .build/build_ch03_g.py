import sys, json; sys.path.insert(0,".build")
path="chapters/03_networking/chapter03.ipynb"
nb=json.load(open(path)); cells=nb["cells"]
def find(p):
    for i,c in enumerate(cells):
        if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith(p): return i
def app(p,t):
    i=find(p); cells[i]["source"]=(("".join(cells[i]["source"])).rstrip()+t+"\n").splitlines(keepends=True)

app("## 3.1", r'''

```{note}
If a network feels abstract, picture the postal system. The application is the letter you write; the
transport layer puts it in an envelope and decides whether to pay for tracked delivery (TCP) or a cheap
stamp (UDP); the network layer writes the city-to-city address (IP); the link layer is the local mail
carrier who knows the street (MAC address); and the physical layer is the truck on the road. Every attack
in this chapter is a way of steaming open an envelope, forging a return address, or flooding the post
office until it collapses.
```''')

app("## 3.6", r'''

```{admonition} Knowledge Check
:class: hint
1. Why is UDP easier to spoof than TCP?
2. During a SYN flood, which specific resource on the server is exhausted?

*Answers:* (1) UDP is connectionless and carries no sequence or acknowledgment numbers, so an attacker
need not predict or complete any handshake to forge a packet. (2) The table of half-open connections (the
backlog queue) that the server reserves between receiving a SYN and completing the handshake.
```''')

app("## 3.9", r'''

Defending against man-in-the-middle and hijacking comes down to denying the attacker the two things they
need: a position in the path and usable plaintext. *Encryption with authentication* removes the second:
TLS not only hides sequence numbers and session tokens but verifies the server's identity via
certificates, so an interposed attacker cannot transparently relay traffic without triggering a
certificate error. *Mutual authentication* (for example IPsec or Kerberos between trusted hosts) raises
the bar further. At the network edge, *anti-spoofing filters* that reject packets claiming impossible
source addresses, and *Layer 2 hardening* (dynamic ARP inspection, DHCP snooping, port security), deny
the attacker the path. For web sessions specifically, marking cookies `Secure` and `HttpOnly`, rotating
session identifiers on authentication, and binding sessions to client attributes blunt application-layer
hijacking. The consistent theme is that these attacks exploit *unauthenticated trust*, and each defense
reintroduces authentication at a particular layer.''')

app("## 3.10", r'''

Modern DDoS is industrialized, and understanding the supply chain clarifies the defense. Attackers
assemble *botnets* by infecting large numbers of devices, increasingly insecure Internet-of-Things
gadgets, with malware that connects each victim to a *command-and-control (C2)* server. On command, the
botnet directs traffic at a target. The most powerful attacks combine botnet volume with the reflection
and amplification techniques above, which is how a single operator marshals tens of terabits per second.
Defenders therefore fight DDoS at multiple levels: device makers and users must close the default-credential
and unpatched-service weaknesses that recruit bots in the first place (the Mirai lesson); network operators
must filter spoofed traffic and disable open reflectors; and targets must contract upstream scrubbing
capacity, because absorbing a multi-terabit flood is beyond any single server. The economics also matter:
because booter services make attacks cheap to buy, raising the cost and risk to attackers, through takedowns
and prosecutions, is part of the defensive picture alongside the technical controls.''')

# New section appended to 3.11 area: secure protocols (renumber-free subsection)
app("## 3.11", r'''

### Secure Network Protocols

It is worth knowing the protocols that retrofit security onto the trusting foundation described
throughout this chapter, since they recur in later material. **TLS (Transport Layer Security)** secures
application traffic above the transport layer and is the basis of HTTPS, secure email, and many VPNs, as
detailed in Chapter 2. **IPsec (Internet Protocol Security)** secures traffic at the network layer,
authenticating and optionally encrypting every IP packet; it underlies many site-to-site VPNs and offers
two modes, transport mode (protecting the payload) and tunnel mode (protecting the entire original
packet inside a new one). **SSH (Secure Shell)** replaces insecure remote-access protocols such as Telnet
and rlogin, providing an encrypted, authenticated channel for administration and for tunneling other
protocols. A **virtual private network (VPN)** uses these primitives to extend a private network across a
public one, giving remote users an encrypted tunnel as if they were on the internal network; modern
designs such as WireGuard aim for simplicity and speed. The unifying idea is *tunneling*: wrapping
untrusted-network traffic inside an authenticated, encrypted channel so that the sniffing, spoofing, and
hijacking attacks of this chapter see only ciphertext they cannot use. These protocols, and the zero-trust
architectures that extend their logic, are developed in Chapter 11.

### Going Deeper: Routing Security and BGP Hijacking

```{admonition} Going Deeper (graduate/research): BGP hijacking
:class: tip
The internet's global routing is governed by the Border Gateway Protocol (BGP), through which networks
(autonomous systems) announce which IP address blocks they can deliver. Like ARP on a local network, BGP
was designed for a small community of mutually trusting operators and historically accepted announcements
largely on trust. In a *BGP hijack*, a network announces address blocks it does not own, causing traffic
destined for the victim to be routed to, or through, the attacker, enabling large-scale interception or
denial of service. Real incidents have rerouted significant traffic, sometimes accidentally through
misconfiguration and sometimes maliciously. The defensive response mirrors the rest of this chapter:
adding authentication to a trusting protocol. The Resource Public Key Infrastructure (RPKI) lets address
holders cryptographically authorize which networks may originate their prefixes (Route Origin
Authorizations), and operators increasingly filter invalid announcements. BGP hijacking shows the same
pattern at internet scale that ARP poisoning shows on a LAN: an unauthenticated "who can reach this
address?" mechanism is exploitable until cryptographic origin validation is layered on top.
```

### Network Access Control

A final defensive concept ties the chapter together. **Network Access Control (NAC)** governs which
devices may join a network and what they may reach once admitted, often using the IEEE 802.1X standard to
authenticate a device or user before granting access and to place them on an appropriate segment.
Combined with *segmentation* and the emerging *zero-trust* philosophy, which treats no device as
inherently trusted regardless of its network location, NAC counters the assumption that "inside the
network equals trusted" that so many of this chapter's attacks rely upon. These ideas are the bridge to
Chapter 4, where we turn from attacking the wires to attacking the people who use them, because the most
carefully secured network can still be undone by a convincing phone call.''')

import uuid
for c in cells: c.setdefault("id", uuid.uuid4().hex[:12])
json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="markdown")
codew=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="code")
print(f"chapter03: {len(cells)} cells, {mdw} md words (~{mdw/500:.1f} pg) + {codew} code = {mdw+codew}")
