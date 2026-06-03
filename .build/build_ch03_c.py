import sys, pickle; sys.path.insert(0,".build")
from nbbuild import md, code
C=pickle.load(open(".build/_ch03.pkl","rb")); A=C.append

A(md(r'''## 3.7 ARP and DHCP: Convenience and Its Abuse

Two helper protocols quietly make local networks usable, and both are routinely abused, which is why
they deserve close attention immediately after the core protocols. The **Address Resolution Protocol
(ARP)** solves a basic problem: to deliver a frame on a local network, a device needs the recipient's
MAC address, but it usually knows only the IP address. ARP bridges the two with two message types: an
*ARP request* ("Who has this IP address?") broadcast to the network, and an *ARP reply* ("I have that
IP; my MAC address is XYZ") returned by the owner. Results are cached in an ARP table for efficiency.

The weakness is that ARP has no authentication, so any host can send unsolicited replies. In **ARP
poisoning (ARP spoofing)**, an attacker floods the switch and victims with forged ARP replies that map
the attacker's MAC address to another device's IP, typically the default gateway. Once the victims'
caches are poisoned, traffic destined for the gateway flows through the attacker instead, enabling
man-in-the-middle interception, traffic recording for later replay, and credential theft. Tools such as
Ettercap, Cain and Abel, arpspoof, and WinARPAttacker automate this. Because ARP poisoning operates at
Layer 2, the standard defenses are also at Layer 2: *dynamic ARP inspection* on managed switches,
*port security*, and static ARP entries for critical hosts.

The **Dynamic Host Configuration Protocol (DHCP)** automatically assigns and manages IP addresses,
eliminating manual configuration and reducing address conflicts. A client obtains a *lease* through a
four-step process abbreviated **DORA**: Discovery (the client broadcasts a request), Offer (a DHCP
server offers an address), Request (the client requests the offered address), and Acknowledgement (the
server confirms). DHCP uses UDP port 67 for servers and 68 for clients. It is abused in two ways. In
**DHCP starvation**, an attacker, using tools such as Yersinia or Gobbler, floods the server with
requests using spoofed MAC addresses until the address pool is exhausted, denying service to legitimate
clients. The attacker may then introduce a **rogue DHCP server** that hands out its own machine as the
default gateway, achieving a man-in-the-middle position. Defenses include *DHCP snooping*, which permits
only authorized DHCP servers and tracks legitimate IP-to-port bindings, and MAC filtering.

```{admonition} In-Class Exercise: map your own network
:class: note
On a network you own (your home network or a lab), open a terminal and run, depending on your operating
system, `arp -a` to view your ARP table and `ipconfig /all` (Windows) or `ip addr` / `ifconfig`
(Linux/macOS) to view your interfaces. Identify (1) your own IP and MAC address, (2) your default
gateway's IP, and (3) the MAC address your machine has cached for the gateway. Discuss in pairs: if an
attacker performed ARP poisoning, which entry in your table would change, and what would that let them
do? Do this only on networks you are authorized to inspect.
```
'''))

A(md(r'''## 3.8 Sniffing: Listening on the Wire

Having seen how addressing works, we can now understand how an attacker listens to it. A **sniffer**
(also called a packet analyzer, network analyzer, or protocol analyzer) is software or hardware that
intercepts and logs traffic crossing a network. To capture traffic not addressed to it, a sniffer puts
the network interface card into **promiscuous mode**, in which the card accepts all frames it sees rather
than only those bearing its own MAC address. Sniffers operate at the data link layer (Layer 2).

How much an attacker can capture depends on the network hardware, which is why the distinction between
passive and active sniffing matters. **Passive sniffing** suffices on a *hub*, because a hub broadcasts
every frame to every port, so the attacker simply listens. Modern networks use *switches*, which forward
each frame only to the port of its intended recipient, so capturing other hosts' traffic requires
**active sniffing**, the attacker must actively manipulate the switch. One legitimate method is the
*Switch Port Analyzer (SPAN)*, also called port mirroring, which an administrator (or an attacker who has
compromised the switch) configures so that traffic is copied to a monitoring port. Attackers without
that access turn to **MAC flooding**: overwhelming the switch's Content-Addressable Memory (CAM) table,
which maps MAC addresses to ports, with a flood of frames bearing fake source MAC addresses. When the
CAM table fills, many switches "fail open" and begin broadcasting all frames to all ports, letting the
attacker sniff everything, at the cost of generating very noisy traffic. Tools such as macof and
EtherFlood perform MAC flooding; ARP poisoning, from the previous section, is the other common way to
sniff a switched network.

The dominant analyzer is **Wireshark**, whose graphical interface presents three panes: a one-line
summary per packet, a detailed decode of the selected packet, and a raw hexadecimal-and-ASCII view where
plaintext usernames and passwords are often visible. Wireshark's power lies in its *filters*, of which
there are two kinds: *capture filters* limit what is recorded in the first place (for example, capturing
only HTTP), while *display filters* narrow what is shown after capture (for example, `ip.addr==192.168.0.1`,
`tcp.port==23`, or `tcp.flags.syn==1`). Filters are validated as you type, green for valid and red for
invalid. Command-line analyzers include **tcpdump** (Linux) and **WinDump** (Windows), which are ideal
for quickly displaying header information. Defenders detect sniffing by restricting physical access,
enabling port security and DHCP snooping, and using tools such as Arpwatch, which tracks MAC-to-IP
pairings and reports suspicious changes.
'''))

A(md(r'''## 3.9 Spoofing, Man-in-the-Middle, and Session Hijacking

Sniffing only observes; the attacks in this section *interfere*. Building directly on sniffing and ARP
poisoning, they let an attacker impersonate hosts, sit between communicating parties, and seize live
sessions. **Spoofing** is the forgery of an identity field: *IP spoofing* forges a source IP address
(easy with UDP, which lacks sequence numbers), *MAC spoofing* forges a hardware address (often to bypass
port security, using tools such as SMAC), and *ARP spoofing* forges ARP replies as described above. A
**man-in-the-middle (MITM)** attack uses spoofing or ARP poisoning to insert the attacker between two
parties so that all traffic passes through them, to be read, recorded, or altered before being relayed.
This is the very attack that authenticated key exchange in Chapter 2 was designed to defeat.

**Session hijacking** goes one step further than sniffing: the attacker actively injects packets to take
over an already-authenticated connection, stealing the trust the legitimate user has established. Timing
is essential, the attacker must strike after the victim has authenticated (so a valid session exists)
but before it ends. There are two families. **Transport-layer (TCP) hijacking** follows four steps:
find an active session, predict the sequence number, take one party offline, and take control. Sequence
prediction is easy when the attacker shares the network segment and can sniff the sequence and
acknowledgment numbers; when they cannot, *blind hijacking* must guess them, which is far harder and
often blocked at the firewall. To remove the legitimate user, the attacker may launch a denial of
service, use source routing, or send a TCP reset; a side effect can be an **ACK storm**, an endless
exchange of acknowledgments as the confused hosts each reply with the sequence number they expect. Tools
such as Ettercap and Hunt assist sequence prediction and hijacking.

**Application-layer hijacking** instead targets the *session identifier (session ID)*, the unique token a
web server assigns a user for the duration of a visit, stored in a cookie, form field, or URL. If a
server generates session IDs with a predictable pattern, an attacker who captures several can predict the
next and impersonate the user. Related techniques include *session sniffing*, *man-in-the-browser*
attacks, *client-side attacks* (cross-site scripting, where the victim trusts the site, and cross-site
request forgery, where the site trusts the victim, both developed in Chapter 10), and *session fixation*,
in which the attacker plants a known session ID and waits for the victim to authenticate with it. Tools
such as Firesheep and Hamster historically made cookie-stealing trivial on open networks. The primary
defense against all of these is **encryption**: end-to-end TLS denies the attacker the plaintext sequence
numbers and session tokens these attacks require, which is why universal HTTPS has done more to curb
session hijacking than any other single measure, supplemented by unpredictable session IDs, short
session lifetimes, and binding sessions to additional attributes.
'''))
print("part C:", len(C))
pickle.dump(C, open(".build/_ch03.pkl","wb"))
