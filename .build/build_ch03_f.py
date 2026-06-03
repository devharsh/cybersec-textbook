import sys, json; sys.path.insert(0,".build")
path="chapters/03_networking/chapter03.ipynb"
nb=json.load(open(path)); cells=nb["cells"]
def find(p):
    for i,c in enumerate(cells):
        if c["cell_type"]=="markdown" and "".join(c["source"]).lstrip().startswith(p): return i
def app(p,t):
    i=find(p); cells[i]["source"]=(("".join(cells[i]["source"])).rstrip()+t+"\n").splitlines(keepends=True)

app("## 3.2", r'''

Each layer is also an attack surface, and naming the threat per layer turns the model into a defensive
checklist. At Layer 1 (Physical), attacks include cable tapping, signal jamming, and physical
destruction. At Layer 2 (Data Link), they include MAC flooding, ARP poisoning, and VLAN hopping. At
Layer 3 (Network), IP spoofing, routing attacks, and ICMP abuse. At Layer 4 (Transport), SYN floods and
TCP session hijacking. At Layers 5 to 7, application attacks such as session hijacking, cross-site
scripting, and protocol-specific exploits. A defender who internalizes this mapping can ask, for any new
technology, "what can go wrong at each layer?" and arrive at a structured threat model rather than an ad
hoc list.''')

app("## 3.3", r'''

### Network Devices and Segments

The layered model also explains what the common network devices do, which matters because each device
defines the boundary of a particular attack. A **hub** is a Layer 1 device that simply repeats every bit
to every port; because it broadcasts, a single hub is one large *collision domain* and one *broadcast
domain*, and it makes passive sniffing trivial. A **switch** is a Layer 2 device that learns which MAC
address lives on which port and forwards frames only to the correct port; each switch port is its own
collision domain, while the switch as a whole is one broadcast domain, which is why sniffing a switched
network requires the active techniques of Section 3.8. A **router** is a Layer 3 device that connects
different networks and makes forwarding decisions based on IP addresses; a router separates broadcast
domains, which is why broadcasts do not cross the internet. *Virtual local area networks (VLANs)* let one
physical switch be partitioned into several logical segments for isolation, though misconfiguration
enables *VLAN hopping* attacks. Understanding these boundaries is practical: it tells an attacker where
they can sniff and a defender where to place monitoring and segmentation.''')

app("## 3.4", r'''

Two mechanisms make IPv4's limited address space workable and appear constantly in assessments.
*Subnetting* divides a network into smaller logical networks using the subnet mask; the mask determines
how many bits identify the network versus the host, which in turn sets the number of available host
addresses (a /24 provides 254 usable hosts, a /16 provides 65,534). Reading Classless Inter-Domain
Routing (CIDR) notation fluently lets a tester scope an engagement and a defender reason about blast
radius. *Network Address Translation (NAT)* lets many hosts using private addresses share one public
address by rewriting address and port information at the gateway; NAT conserves addresses and incidentally
hides internal hosts, but it is not a security control by itself, since inbound connections can still be
forwarded and internal hosts can still initiate malicious outbound traffic. Recognizing private ranges
behind NAT, and the public address they share, is a routine first step in mapping a target network.''')

app("## 3.6", r'''

```{admonition} Going Deeper (graduate/research): TCP sequence-number prediction
:class: tip
The security of an unencrypted TCP connection against off-path attackers rests on the unpredictability
of the 32-bit initial sequence number (ISN). If an attacker who cannot see the traffic can nonetheless
*predict* the ISN, they can forge packets that the server accepts as part of a legitimate connection,
enabling blind session hijacking and connection reset attacks. Early TCP stacks generated ISNs with
simple, predictable increments, and this was exploited in famous attacks (notably the 1994 Mitnick
intrusion). The defensive response, specified in RFC 6528, is to generate ISNs using a cryptographic
function of the connection's four-tuple and a secret, making them unpredictable to off-path attackers
while remaining usable by the endpoints. This is a recurring pattern in protocol security: a field that
was originally a mere bookkeeping value (the sequence number) turns out to be a security boundary, and
hardening it requires importing cryptographic unpredictability into a protocol that had none. It also
explains why on-path attackers (who can simply read the sequence numbers) remain far more powerful than
off-path ones, and why encryption, which hides those numbers, is the durable fix.
```''')

app("## 3.7", r'''

### The Domain Name System (DNS)

A third infrastructure protocol, alongside ARP and DHCP, deserves equal attention because it is both
indispensable and heavily attacked: the **Domain Name System (DNS)**, which translates human-readable
names such as example.com into IP addresses. DNS is a distributed, hierarchical database. When a host
needs an address, its *resolver* queries a *recursive resolver*, which, if it has no cached answer, walks
the hierarchy from the *root* servers to the *top-level domain* (TLD) servers (such as .com) to the
*authoritative* server for the domain, then caches the result for a period set by its *time to live*.
DNS primarily uses UDP port 53 (falling back to TCP for large responses), and it stores several *record
types*: A and AAAA records map names to IPv4 and IPv6 addresses, MX records identify mail servers, NS
records identify name servers, CNAME records create aliases, and TXT records hold arbitrary text (often
used for email authentication and domain verification).

Because DNS is unauthenticated by default and central to reaching every service, it is a favorite target.
In **DNS cache poisoning (DNS spoofing)**, an attacker injects forged records into a resolver's cache so
that victims are silently directed to malicious servers. In **DNS hijacking**, an attacker changes a
domain's configuration or a host's resolver settings to redirect traffic. In **DNS tunneling**, attackers
smuggle data or command-and-control traffic inside DNS queries and responses to bypass firewalls that
permit DNS. DNS is also a powerful *amplification* vector for DDoS, as Section 3.10 describes, because a
small query can trigger a large response. The defensive response includes **DNSSEC (DNS Security
Extensions)**, which digitally signs records so resolvers can verify their authenticity, encrypted
transports such as DNS over HTTPS (DoH) and DNS over TLS (DoT), and careful monitoring of DNS traffic for
the anomalies that tunneling and exfiltration produce. For the penetration tester, DNS is equally a rich
*reconnaissance* source, a theme developed in Chapter 7.''')

app("## 3.8", r'''

Wireless networks add their own sniffing dimension that is worth noting here and developed in Chapter 16
and Chapter 17. Because Wi-Fi is a shared radio medium, an attacker within range can capture frames
without any physical connection by placing the adapter in *monitor mode* (the wireless analog of
promiscuous mode). Whether the captured traffic is readable depends on the link-layer encryption: the
obsolete Wired Equivalent Privacy (WEP) is trivially broken, Wi-Fi Protected Access 2 (WPA2) is strong
when configured with a robust passphrase, and WPA3 further hardens key exchange. This is why open or
weakly secured wireless networks remain a prime sniffing target, and why sensitive traffic should always
carry its own end-to-end encryption regardless of the wireless layer.''')

app("## 3.10", r'''

The largest modern attacks rely on **reflection and amplification**, which deserve a closer look because
they explain the terabit figures in the Current News box. In a reflection attack, the attacker sends
requests to many third-party servers while spoofing the victim's source address, so every server's reply
is "reflected" toward the victim. *Amplification* multiplies this when the reply is much larger than the
request: a small DNS or Network Time Protocol (NTP) query can yield a response tens or hundreds of times
larger, so a modest uplink can generate an overwhelming flood (a form sometimes called a distributed
reflection denial of service, or DrDoS). The defensive responses are collective as much as local:
operators are urged to disable open resolvers and reflectors, to implement source-address validation
(BCP 38 ingress filtering) so spoofed packets cannot leave their networks in the first place, and to rely
on large-scale upstream scrubbing services that can absorb traffic no single organization could.''')

json.dump(nb, open(path,"w"), indent=1, ensure_ascii=True)
mdw=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="markdown")
codew=sum(len("".join(c["source"]).split()) for c in cells if c["cell_type"]=="code")
print(f"chapter03: {len(cells)} cells, {mdw} md words (~{mdw/500:.1f} pg) + {codew} code = {mdw+codew}")
