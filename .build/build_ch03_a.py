import sys; sys.path.insert(0,".build")
from nbbuild import md, code
import pickle
C=[]; A=C.append

A(md(r'''# Chapter 3: Networking and Network Attacks

> "The network is the computer." -- John Gage, Sun Microsystems

---

Cryptography, the subject of Chapter 2, protects data as it moves. But to understand what it is moving
*through*, how that movement can be observed, redirected, and disrupted, we must understand networks
themselves. This chapter builds the networking foundation every later offensive and defensive technique
depends on, then turns to the classic attacks that target the network directly.

## Learning Objectives

After completing this chapter, you will be able to:

1. Describe the seven layers of the Open Systems Interconnection (OSI) model and the four layers of the
   Transmission Control Protocol/Internet Protocol (TCP/IP) model, and explain encapsulation.
2. Explain Internet Protocol (IP) addressing for IP version 4 (IPv4) and version 6 (IPv6), and the role
   of ports and common protocols.
3. Trace the Transmission Control Protocol (TCP) three-way handshake and four-way termination, and read
   the fields of the IP, TCP, and Internet Control Message Protocol (ICMP) headers.
4. Explain the Address Resolution Protocol (ARP) and the Dynamic Host Configuration Protocol (DHCP), and
   how each is abused (ARP poisoning, DHCP starvation).
5. Distinguish passive and active sniffing and explain promiscuous mode, port mirroring, and Media
   Access Control (MAC) flooding.
6. Explain spoofing, man-in-the-middle (MITM) attacks, and TCP and application-layer session hijacking.
7. Classify denial-of-service (DoS) and distributed denial-of-service (DDoS) attacks and describe their
   mitigations.

## Key Terms

- **OSI (Open Systems Interconnection) model**: a seven-layer conceptual model of network communication.
- **TCP/IP (Transmission Control Protocol/Internet Protocol)**: the four-layer protocol suite of the
  real internet.
- **Protocol data unit (PDU)**: the data unit at a given layer (segment, packet, frame, bit).
- **Encapsulation**: wrapping data with successive headers as it descends the protocol stack.
- **Port**: a 16-bit number identifying an application or process endpoint on a host.
- **ARP (Address Resolution Protocol)**: maps an IP address to a MAC (Media Access Control) address.
- **DHCP (Dynamic Host Configuration Protocol)**: automatically assigns IP addresses to hosts.
- **ICMP (Internet Control Message Protocol)**: a diagnostic/error-reporting protocol (used by ping).
- **Promiscuous mode**: a network-card mode that accepts all frames, not only those addressed to it.
- **Sniffer (packet analyzer)**: software or hardware that captures and logs network traffic.
- **Session hijacking**: taking over an authenticated session by injecting or stealing session state.
- **DoS / DDoS (Distributed Denial of Service)**: attacks that exhaust resources to deny availability.
'''))

A(md(r'''## 3.1 Why Networking Is the Battleground

Almost every attack in this book crosses a network at some point. The reconnaissance of Chapter 7, the
scanning of Chapter 8, the exploitation of Chapter 9, and the web attacks of Chapter 10 all send and
receive packets, and the defenses of Chapters 11 and 12 watch those same packets. A security
professional who does not understand how data is addressed, routed, and delivered cannot reason about
how it is intercepted or forged. This chapter therefore serves two purposes at once: it teaches the
mechanics of networking, and it shows, layer by layer, how each mechanism becomes an attack surface.

The organizing idea is the *layered model*. Networking is too complex to design as one monolithic
system, so engineers divide it into layers, each responsible for one concern and each communicating only
with the layers directly above and below it. This separation is not merely tidy engineering; it is also
a map of where attacks happen. An attacker who poisons an ARP cache operates at Layer 2, one who spoofs
an IP address operates at Layer 3, one who hijacks a TCP session operates at Layer 4, and one who steals
a web session cookie operates at Layer 7. Learning to place an attack at its layer is one of the most
useful diagnostic skills in the field, because the layer usually dictates both the mechanism and the
defense.

We begin with the canonical seven-layer model, then map it onto the four-layer model the real internet
actually uses, before descending into the specific protocols and the attacks that target each one.
'''))

A(md(r'''## 3.2 The OSI Model

The most widely taught framework for understanding networks is the Open Systems Interconnection (OSI)
model, a seven-layer reference model standardized by the International Organization for Standardization
(ISO). No real network implements the OSI model exactly, but it remains the shared vocabulary of the
profession: when an engineer says a problem is "a Layer 1 issue" or "a Layer 7 attack," everyone knows
what is meant. We build up from the foundations of the previous section by giving each layer a precise
responsibility.

From top to bottom, the seven layers are as follows. **Layer 7, Application**, gives programs access to
network services and is where protocols such as the Hypertext Transfer Protocol (HTTP), Simple Mail
Transfer Protocol (SMTP), and Server Message Block (SMB) live. **Layer 6, Presentation**, handles data
representation: translation, compression, and encryption. **Layer 5, Session**, manages the dialogue
between hosts, including full-duplex, half-duplex, and simplex communication. **Layer 4, Transport**,
selects the transport mode and provides either guaranteed delivery (TCP) or fast, best-effort delivery
(the User Datagram Protocol, UDP). **Layer 3, Network**, manages communication across networks through
IP addressing, fragmentation, and routing. **Layer 2, Data Link**, manages communication within a local
network using physical (MAC) addresses and controls access to the shared medium. **Layer 1, Physical**,
transmits raw bits as electrical, optical, or radio signals over Ethernet, digital subscriber line
(DSL), Universal Serial Bus (USB), and similar media.

| Layer | Name | Primary purpose | Examples |
|---|---|---|---|
| 7 | Application | Access to network services | HTTP, Telnet, SMB, SMTP |
| 6 | Presentation | Data representation | Translation, compression, encryption |
| 5 | Session | Manage the dialogue | Full-duplex, half-duplex, simplex |
| 4 | Transport | Select transport mode | Guaranteed (TCP) vs best-effort (UDP) |
| 3 | Network | External (internet) communication | IP addressing, fragmentation, routing |
| 2 | Data Link | Internal (LAN) communication | MAC addressing, media access control |
| 1 | Physical | Bit-level transmission | Ethernet, DSL, USB, RS-232 |

A common mnemonic for remembering the layers from 7 down to 1 is "All People Seem To Need Data
Processing." The diagram below shows the stack and the protocol data unit (PDU) name at each layer.

```{mermaid}
graph TD
    L7["L7 Application - data (HTTP, SMTP, DNS)"] --> L6["L6 Presentation - encryption, compression"]
    L6 --> L5["L5 Session - dialogue control"]
    L5 --> L4["L4 Transport - SEGMENT (TCP/UDP, ports)"]
    L4 --> L3["L3 Network - PACKET (IP, ICMP, routing)"]
    L3 --> L2["L2 Data Link - FRAME (Ethernet, MAC, ARP)"]
    L2 --> L1["L1 Physical - BITS (cable, radio, fiber)"]
```
'''))

A(md(r'''## 3.3 The TCP/IP Model and Encapsulation

The OSI model is the teaching tool, but the internet actually runs on the older and simpler **TCP/IP
model**, which collapses the seven OSI layers into four: the Application layer (OSI 5 to 7), the
Transport layer (OSI 4), the Internet layer (OSI 3), and the Network Access or Link layer (OSI 1 to 2).
Understanding both, and how they correspond, lets you move between textbooks, tools, and certifications
without confusion. Having named the layers, we now follow a single message down the stack to see how
they cooperate, a process called *encapsulation*.

When an application sends data, each layer wraps the data from the layer above in its own header (and
sometimes a trailer), like placing a letter inside successively larger envelopes. The Transport layer
adds a TCP or UDP header, producing a **segment** (or *datagram* for UDP). The Internet layer wraps that
segment in an IP header, producing a **packet**. The Link layer wraps the packet in an Ethernet header
and trailer, producing a **frame**, which the Physical layer finally transmits as **bits**. At the
receiving end the process reverses: each layer strips its own header and hands the contents up. The
naming matters because tools and attacks refer to these PDUs precisely: a TCP segment is carried inside
one or more IP packets, which are each carried inside one or more Ethernet frames.

This nesting is also why an attacker's vantage point determines what they can see and forge. Someone on
the same local segment sees whole Ethernet frames, including MAC addresses; someone who can route
traffic sees IP packets; someone who terminates a connection sees the application data. Encapsulation,
in other words, is simultaneously the engineering that makes the internet work and the structure that
defines each attacker's reach.
'''))
print("part A:", len(C))
pickle.dump(C, open(".build/_ch03.pkl","wb"))
