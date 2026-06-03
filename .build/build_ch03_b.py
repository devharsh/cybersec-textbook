import sys, pickle; sys.path.insert(0,".build")
from nbbuild import md, code
C=pickle.load(open(".build/_ch03.pkl","rb")); A=C.append

A(md(r'''## 3.4 IP Addressing: IPv4 and IPv6

Routing data across the internet requires that every host have an address, which is the job of the
Internet Protocol. Because addressing underlies the scanning and spoofing attacks later in the book, we
pause on it before moving to ports and protocols. An **IPv4 address** is 32 bits, written as four
decimal octets such as 192.168.0.177, giving about 4.3 billion possible addresses, a number the growth
of the internet has exhausted. Addresses are split into a network portion and a host portion by a
*subnet mask* (for example /24 means the first 24 bits identify the network), and certain ranges are
reserved as *private* (10.0.0.0/8, 172.16.0.0/12, and 192.168.0.0/16) for use inside organizations
behind Network Address Translation (NAT). Recognizing private versus public addresses is a basic but
constant task in penetration testing.

To overcome address exhaustion, **IPv6** uses 128-bit addresses, written as eight groups of four
hexadecimal digits separated by colons, for example 2001:0000:3238:DFE1:0063:0000:0000:FEFB. Each
16-bit group is informally called a *hextet* (four hexadecimal digits, or four *nibbles*, where a nibble
is four bits). IPv6 provides a practically inexhaustible address space along with improvements in
autoconfiguration and header design. From a security standpoint, IPv6 is significant because it is often
enabled by default yet overlooked by defenders, creating a parallel, unmonitored network path; a
thorough assessment must consider both IPv4 and IPv6.
'''))

A(md(r'''## 3.5 Ports and Common Protocols

An IP address gets data to the right *host*, but a single host runs many network programs at once, so we
need a finer identifier to reach the right *application*. That identifier is the **port number**, a
16-bit value that, combined with the IP address, uniquely identifies a communication endpoint. Many
applications can therefore share one IP address, each distinguished by its port. There are roughly
65,000 ports, divided into three ranges: **well-known ports (0 to 1023)** assigned to standard services,
**registered ports (1024 to 49151)** assigned to specific applications, and **dynamic or ephemeral ports
(49152 to 65535)** used temporarily by clients.

Memorizing the common ports and their protocols is essential for both certification exams and practical
work, because a port often reveals what service is running before any deeper probing. Each acronym is
expanded for clarity.

| Port(s) | Protocol (full form) |
|---|---|
| 20, 21 | FTP (File Transfer Protocol) |
| 22 | SSH (Secure Shell) |
| 23 | Telnet (insecure remote login) |
| 25 | SMTP (Simple Mail Transfer Protocol) |
| 53 | DNS (Domain Name System), TCP/UDP |
| 67, 68 | DHCP (Dynamic Host Configuration Protocol), UDP |
| 69 | TFTP (Trivial File Transfer Protocol), UDP |
| 80 | HTTP (Hypertext Transfer Protocol) |
| 88 | Kerberos (authentication protocol) |
| 110 | POP3 (Post Office Protocol v3) |
| 135 | MSRPC (Microsoft Remote Procedure Call) |
| 137-139 | NetBIOS (Network Basic Input/Output System) |
| 143 | IMAP (Internet Message Access Protocol) |
| 161, 162 | SNMP (Simple Network Management Protocol), UDP |
| 389 | LDAP (Lightweight Directory Access Protocol) |
| 443 | HTTPS (HTTP over SSL/TLS) |
| 445 | SMB (Server Message Block) |
| 993 / 995 | IMAPS / POP3S (secure IMAP / POP3) |
| 1433 | Microsoft SQL Server |
| 3306 | MySQL database |
| 3389 | RDP (Remote Desktop Protocol) |
| 5900 | VNC (Virtual Network Computing) |
| 8080 | HTTP proxy / alternate HTTP |

```{admonition} Knowledge Check
:class: hint
1. Into which range does port 443 fall, and what service uses it?
2. A scan shows TCP 3389 open. What service is likely running, and why is exposing it to the internet
   risky?

*Answers:* (1) Well-known ports (0 to 1023); HTTPS, that is, HTTP secured with TLS. (2) Remote Desktop
Protocol; exposing RDP directly to the internet invites brute-force and exploitation and is a frequent
ransomware entry point, so it should sit behind a virtual private network (VPN) or be disabled.
```
'''))

A(md(r'''## 3.6 The Core Protocols: TCP, UDP, ICMP, and Their Headers

Ports identify endpoints, but the *behavior* of a connection is governed by the transport protocol and
the structure of its headers. Because attackers forge and manipulate these very fields, we now examine
them in the detail a security professional needs.

The **Transmission Control Protocol (TCP)** provides reliable, ordered, connection-oriented delivery. It
establishes a connection with a *three-way handshake*, guarantees delivery using sequence and
acknowledgment numbers, and closes the connection with an orderly four-step shutdown. The **User
Datagram Protocol (UDP)**, by contrast, performs none of this handshaking: it is connectionless and
best-effort, which makes it faster but less reliable, and notably easier for attackers to spoof because
it carries no sequence or acknowledgment numbers to forge.

The TCP three-way handshake is foundational, both because it underlies every TCP connection and because
the SYN flood attack abuses it directly. The client sends a packet with the **SYN** (synchronize) flag
set and an initial sequence number (ISN). The server replies with a packet that has both the **SYN** and
**ACK** (acknowledge) flags set, acknowledging the client's ISN (by returning it plus one) and supplying
its own ISN. The client then replies with an **ACK**, and the connection is established.

```{mermaid}
sequenceDiagram
    participant C as Client
    participant S as Server
    C->>S: SYN (seq = x)
    S->>C: SYN, ACK (seq = y, ack = x+1)
    C->>S: ACK (ack = y+1)
    Note over C,S: Connection established; data transfer begins
```

A connection is closed by a four-step shutdown using the **FIN** (finish) flag: one side sends FIN/ACK,
the other acknowledges, then sends its own FIN/ACK, and the first side acknowledges. The six common TCP
flags are SYN, ACK, FIN, RST (reset, used to abort a connection abnormally), PSH (push, deliver data
immediately), and URG (urgent). A packet with no flags set is called a NULL packet, a fact scanners
exploit in Chapter 8.

The **IP header** carries the fields that route and reassemble packets: the version (IPv4 or IPv6),
header length, type of service (also called quality of service), total length, an identification tag and
fragment offset used to reassemble fragments, flags including "don't fragment" (DF) and "more fragments"
(MF), the *time to live* (TTL, the number of router hops before the packet is discarded), the upper-layer
protocol (TCP, UDP, or ICMP), a header checksum, and the source and destination addresses. The **TCP
header** carries source and destination ports, the sequence and acknowledgment numbers, the data offset,
the flags, the window size (available buffer space), a checksum, and the urgent pointer. The **Internet
Control Message Protocol (ICMP)** provides feedback and diagnostics; its first byte is a *type* and its
second a *code*. The familiar `ping` uses ICMP echo request (type 8) and echo reply (type 0), while type
3 signals "destination unreachable" and type 11 "time exceeded," which is how `traceroute` maps a path.

Finally, **fragmentation** occurs when a packet exceeds the *maximum transmission unit (MTU)*, the
largest size the receiving link accepts; IP then divides the packet into fragments, each labeled with a
length, an offset, and a "more fragments" bit so the receiver can reassemble them. As we will see,
malformed or overlapping fragments are themselves a class of attack.
'''))
print("part B:", len(C))
pickle.dump(C, open(".build/_ch03.pkl","wb"))
