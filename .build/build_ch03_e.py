import sys, pickle, uuid; sys.path.insert(0,".build")
from nbbuild import md, code, write_nb
C=pickle.load(open(".build/_ch03.pkl","rb")); A=C.append

A(code(r'''# Chapter 3 -- Encapsulation: how a message is wrapped down the stack
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

layers = [
    ("Application data", "#d6eaf8", 7.0),
    ("TCP hdr | data  (SEGMENT)", "#aed6f1", 6.0),
    ("IP hdr | TCP hdr | data  (PACKET)", "#85c1e9", 5.0),
    ("Eth hdr | IP hdr | TCP hdr | data | Eth trailer  (FRAME)", "#5dade2", 4.0),
]
fig, ax = plt.subplots(figsize=(9, 4))
for i,(label,color,_) in enumerate(layers):
    y = len(layers)-i
    ax.add_patch(Rectangle((0.5-0.07*i, y), 9*(1+0.03*i)/9*8, 0.7, facecolor=color, edgecolor="black"))
    ax.text(0.6-0.07*i, y+0.35, label, va="center", fontsize=9)
ax.text(4.5, 0.4, "Each layer adds its own header (encapsulation); the receiver strips them in reverse.",
        ha="center", fontsize=9, style="italic")
ax.set_xlim(0, 9); ax.set_ylim(0, 5.5); ax.axis("off")
ax.set_title("Encapsulation down the TCP/IP stack")
plt.tight_layout(); plt.savefig("ch03_encapsulation.png", dpi=110)
print("Saved ch03_encapsulation.png")''' ))

A(md(r'''## Why This Matters

Networking is the connective tissue of every system this book examines, and the layered model is the map
a professional uses to navigate it. When you can place a phenomenon at its layer, an ARP reply at Layer
2, a spoofed IP at Layer 3, a SYN flood at Layer 4, a stolen session cookie at Layer 7, you immediately
know both how the attack works and where to defend. The protocols covered here, IP, TCP, UDP, ICMP, ARP,
and DHCP, were designed decades ago for a small, trusting network, and most of the attacks in this
chapter exploit the authentication those protocols never had. That single insight, that the internet's
foundational protocols trust by default, explains sniffing, spoofing, poisoning, hijacking, and
amplification all at once, and it frames the defensive work of the chapters ahead, which is largely the
project of adding verification back into a system that was built without it.
'''))

A(md(r'''## News in Focus: The Mirai Botnet and the Dyn Attack (2016)

In October 2016, a massive DDoS attack against Dyn, a major Domain Name System (DNS) provider, disrupted
access to many popular websites across the United States and Europe. The attack was driven by the
**Mirai** botnet, which had compromised large numbers of poorly secured Internet-of-Things devices,
such as internet-connected cameras and home routers, by simply trying lists of default usernames and
passwords. Once enrolled, these devices generated enormous volumes of traffic on command.

Seen through this chapter, Mirai ties together several threads. It was a *volumetric* and
*application-layer* DDoS delivered by a *botnet*; it targeted *DNS*, a single dependency whose failure
cascaded into widespread outages; and its root cause was the absence of basic security on networked
devices, default credentials and exposed services, the same hygiene failures discussed in Chapter 1.
Mirai's source code was later published, spawning many variants, and it foreshadowed the even larger
botnet-driven attacks of the 2020s described in this chapter's Current News box. The lesson endures: the
security of the network as a whole depends on the security of its weakest connected device. These
details reflect public reporting and subsequent analysis.
'''))

A(md(r'''## Review Questions

**Q1.** Which OSI layer is responsible for logical IP addressing and routing?
A. Layer 2 Data Link  B. Layer 3 Network  C. Layer 4 Transport  D. Layer 7 Application

**Q2.** The protocol data unit at the Transport layer is called a:
A. Frame  B. Packet  C. Segment  D. Bit

**Q3.** Which range are the well-known ports?
A. 0-1023  B. 1024-49151  C. 49152-65535  D. 0-65535

**Q4.** In the TCP three-way handshake, the server's second packet has which flags set?
A. SYN only  B. ACK only  C. SYN and ACK  D. FIN and ACK

**Q5.** ARP poisoning operates primarily at which layer and enables which attack?
A. Layer 3; routing loop  B. Layer 2; man-in-the-middle  C. Layer 4; SYN flood  D. Layer 7; XSS

**Q6.** Promiscuous mode allows a network card to:
A. Send faster  B. Accept all frames, not just those addressed to it  C. Encrypt traffic  D. Assign IPs

**Q7.** MAC flooding aims to:
A. Crash a router  B. Overflow the switch CAM table so it broadcasts to all ports  C. Spoof an IP  D. Exhaust DHCP

**Q8.** A SYN flood is best classified as which type of DoS attack?
A. Volumetric  B. Protocol / state-exhaustion  C. Application-layer  D. Reflection

**Q9.** Which protocol is connectionless and easier to spoof because it lacks sequence numbers?
A. TCP  B. UDP  C. HTTP  D. SMB

**Q10.** The DHCP lease process is abbreviated:
A. DORA (Discovery, Offer, Request, Acknowledgement)  B. SYN-ACK  C. AAA  D. DALE

**Q11.** Which field in the IP header limits how many router hops a packet may take?
A. Checksum  B. Type of Service  C. Time to Live (TTL)  D. Fragment offset

**Q12.** The primary defense that defeats both sniffing and session hijacking is:
A. Faster switches  B. Encryption (for example TLS)  C. More bandwidth  D. Longer passwords

**Q13.** A Smurf attack achieves amplification by:
A. Sending ICMP echo requests to a broadcast address with the victim's spoofed source  B. Cracking hashes
C. Flooding DHCP  D. Poisoning ARP

**Q14.** Which Wireshark display filter shows only traffic to or from 192.168.0.1?
A. tcp.port==80  B. ip.addr==192.168.0.1  C. http  D. arp

**Q15.** SYN cookies mitigate SYN floods by:
A. Blocking all SYN packets  B. Encoding connection state in the sequence number so no memory is
allocated until the handshake completes  C. Increasing bandwidth  D. Encrypting the handshake

---

### Answer Key

1: B 2: C 3: A 4: C 5: B 6: B 7: B 8: B 9: B 10: A 11: C 12: B 13: A 14: B 15: B
'''))

A(md(r'''## Hands-on Labs

**Lab 3.1 (beginner) - Trace a path.** Use `ping` and `traceroute` (`tracert` on Windows) to reach a
public website you are allowed to test. Identify the TTL behavior, the number of hops, and the last
device before the destination. Explain which ICMP types and codes make `traceroute` work.

**Lab 3.2 (beginner/intermediate) - Read real packets.** Install Wireshark, capture traffic on your own
machine while loading a plain HTTP page and an HTTPS page, and compare. Apply display filters for
`http`, `tcp.flags.syn==1`, and `ip.addr==<your gateway>`. Find the three-way handshake and label each
packet's flags. Confirm that HTTPS content is unreadable while HTTP content is in cleartext.

**Lab 3.3 (intermediate) - Handshake and ports.** Write a short Python script using the `socket` library
that connects to a few common ports on a host you own and reports which are open, then observe the
handshake in Wireshark. Map each open port to its service using the table in Section 3.5.

**Lab 3.4 (advanced) - Safe ARP demonstration in a lab.** In an isolated virtual lab with machines you
own, observe ARP tables before and after running an ARP-spoofing tool, then enable a Layer 2 mitigation
(static ARP entry or dynamic ARP inspection) and show that the attack is blocked. Write up the before,
during, and after states. Perform this only in an isolated lab you control.
'''))

A(md(r'''## References

1. International Organization for Standardization. *ISO/IEC 7498-1: The Basic Reference Model (OSI).*
2. Postel, J. *Transmission Control Protocol.* RFC 793, IETF, 1981.
3. Postel, J. *Internet Protocol.* RFC 791, IETF, 1981.
4. Plummer, D. *An Ethernet Address Resolution Protocol.* RFC 826, IETF, 1982.
5. Droms, R. *Dynamic Host Configuration Protocol.* RFC 2131, IETF, 1997.
6. Deering, S., and Hinden, R. *Internet Protocol, Version 6 (IPv6) Specification.* RFC 8200, 2017.
7. Cloudflare. *DDoS Threat Report for 2025 Q4.* Cloudflare Blog, 2026.
8. Antonakakis, M., et al. "Understanding the Mirai Botnet." *USENIX Security Symposium*, 2017.
9. Kurose, J., and Ross, K. *Computer Networking: A Top-Down Approach.* Pearson.
'''))

for c in C: c.setdefault("id", uuid.uuid4().hex[:12])
write_nb("chapters/03_networking/chapter03.ipynb", C)
