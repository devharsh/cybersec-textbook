# Appendix I: Protocol Security Reference

This appendix collects every network protocol named in the book into a single reference. For each protocol it
gives the full form, the defining RFC or standard and the year of that document, the default port or ports,
the protocol's usage, the attacks it is commonly subject to, and the defenses that mitigate them.

A few conventions apply throughout. The RFC or standard listed is the primary defining document; many
protocols have been revised, updated, or obsoleted over time, and the original year is noted where it differs
materially from the current document. Ports are the IANA-registered defaults; real deployments may differ.
Some entries are not IETF protocols at all (for example IEEE, OASIS, ISO, Wi-Fi Alliance, or vendor standards),
and the responsible body is named in place of an RFC. Layer-2 and layer-3 protocols, which have no transport
port, are marked accordingly. Cross-references point to the chapters where each protocol is discussed in
context.

## I.1 Internet and Transport Layer

| Protocol (full form) | RFC / standard (year) | Port(s) | Usage | Common attacks | Key defenses |
|------------|---------|-----|------------|------------|------------|
| IP (Internet Protocol) | RFC 791 IPv4 (1981); RFC 8200 IPv6 (2017) | none (layer 3) | Host addressing and packet routing | Address spoofing, fragmentation abuse, option abuse | Ingress/egress filtering (BCP 38), reverse-path checks, IPsec |
| ICMP (Internet Control Message Protocol) | RFC 792 (1981); ICMPv6 RFC 4443 (2006) | none | Diagnostics and error signaling (ping, traceroute) | Ping/Smurf floods, ICMP tunneling, redirect spoofing | Rate-limit, filter unneeded types, drop ICMP redirects |
| ARP (Address Resolution Protocol) | RFC 826 (1982) | none (layer 2) | Maps IPv4 addresses to MAC addresses on a LAN | ARP spoofing/cache poisoning leading to MITM | Dynamic ARP Inspection, DHCP snooping, static entries |
| TCP (Transmission Control Protocol) | RFC 9293 (2022; orig 793, 1981) | n/a (transport) | Reliable, ordered, connection-oriented byte streams | SYN flood, sequence prediction, RST injection/hijacking | SYN cookies, randomized ISNs, TLS, stateful firewalls |
| UDP (User Datagram Protocol) | RFC 768 (1980) | n/a (transport) | Connectionless, low-overhead datagrams | Amplification/reflection DDoS, source spoofing | Source-address validation (BCP 38), response-rate limiting |
| SCTP (Stream Control Transmission Protocol) | RFC 9260 (2022; orig 4960) | n/a (transport) | Multi-stream transport (telecom signaling, SIGTRAN) | Association hijacking, INIT flooding | INIT cookies, firewalling, segmentation |
| IGMP (Internet Group Management Protocol) | RFC 3376 v3 (2002) | none | IPv4 multicast group membership | Spoofed membership reports, flooding | IGMP snooping, filtering at the edge |

Discussed mainly in Chapter 3 (networking) and Chapter 11 (network defense).

## I.2 Naming and Address Assignment

| Protocol (full form) | RFC / standard (year) | Port(s) | Usage | Common attacks | Key defenses |
|------------|---------|-----|------------|------------|------------|
| DNS (Domain Name System) | RFC 1034/1035 (1987) | 53 UDP/TCP | Resolves names to IP addresses | Cache poisoning, spoofing, tunneling, NXDOMAIN flood, DDoS | DNSSEC, DoH/DoT, response-rate limiting, sinkholing |
| DNSSEC (DNS Security Extensions) | RFC 4033/4034/4035 (2005) | 53 | Authenticates DNS records with signatures | Zone walking (NSEC), key mismanagement | NSEC3, key rollover, validating resolvers |
| DoT (DNS over TLS) | RFC 7858 (2016) | 853 TCP | Encrypts DNS queries | Traffic analysis, blocking | TLS, query padding |
| DoH (DNS over HTTPS) | RFC 8484 (2018) | 443 | Encrypts DNS inside HTTPS | Bypass of enterprise DNS controls | Enterprise resolver policy, allowlisting |
| DHCP (Dynamic Host Configuration Protocol) | RFC 2131 (1997); DHCPv6 RFC 8415 (2018) | 67/68 UDP (547/546 v6) | Automatic IP configuration | Rogue DHCP servers, starvation, spoofing | DHCP snooping, port security |
| LLMNR (Link-Local Multicast Name Resolution) | RFC 4795 (2007) | 5355 UDP | Local name resolution fallback | Poisoning and credential theft (Responder) | Disable LLMNR, enforce SMB signing |
| mDNS (Multicast DNS) | RFC 6762 (2013) | 5353 UDP | Zero-configuration local naming | Spoofing, information disclosure | Disable on untrusted networks, segmentation |
| NetBIOS (NetBIOS over TCP/IP) | RFC 1001/1002 (1987) | 137/138 UDP, 139 TCP | Legacy Windows naming and sessions | NBT-NS poisoning, host enumeration | Disable NBT-NS, block ports, SMB signing |

Discussed mainly in Chapters 3, 7, and 11.

## I.3 Web, Transport Security, and Identity

| Protocol (full form) | RFC / standard (year) | Port(s) | Usage | Common attacks | Key defenses |
|------------|---------|-----|------------|------------|------------|
| HTTP (Hypertext Transfer Protocol) | RFC 9110 semantics, 9112 HTTP/1.1 (2022; orig 1945, 1996) | 80 TCP | Web request/response | Sniffing, MITM, injection, request smuggling | HTTPS/TLS, input validation, HSTS |
| HTTP/2 | RFC 9113 (2022) | 443 | Multiplexed binary HTTP | Rapid Reset DDoS (CVE-2023-44487), HPACK abuse | Patching, stream limits, TLS |
| HTTP/3 | RFC 9114 (2022) | 443 UDP | HTTP carried over QUIC | QUIC flooding, amplification | Address validation, rate limiting |
| QUIC | RFC 9000 (2021) | 443 UDP | Encrypted UDP transport with built-in TLS 1.3 | Amplification, connection flooding | Retry/address validation, limits |
| TLS (Transport Layer Security) | RFC 8446 v1.3 (2018); v1.2 RFC 5246 (2008) | application (e.g., 443) | Encrypts and authenticates sessions | Downgrade, BEAST/POODLE (legacy), forged certs | TLS 1.3, HSTS, certificate pinning, strong ciphers |
| SSL (Secure Sockets Layer) | Netscape; deprecated by RFC 7568 (2015) | 443 | Legacy session encryption (predecessor of TLS) | POODLE; all versions are broken | Disable entirely; use TLS 1.2 or 1.3 |
| DTLS (Datagram Transport Layer Security) | RFC 9147 v1.3 (2022); v1.2 RFC 6347 (2012) | application/UDP | TLS for datagram transports (VPN, WebRTC, CoAP) | Amplification, downgrade | DTLS 1.3, cookies |
| HTTPS (HTTP over TLS) | RFC 9110; RFC 2818 (2000) | 443 | Secure web browsing | SSL stripping, mixed content | HSTS, redirect to TLS, secure cookies |
| WebSocket | RFC 6455 (2011) | 80/443 | Full-duplex channel over HTTP | Cross-site hijacking (CSWSH), injection | Origin validation, wss (TLS), auth tokens |
| OAuth 2.0 | RFC 6749 (2012) | application (443) | Delegated authorization | Token theft, redirect/CSRF, phishing | PKCE, exact redirect URIs, short-lived tokens |
| SAML 2.0 | OASIS (2005) | application (443) | Federated single sign-on via XML assertions | Assertion forgery, XML signature wrapping | Validate signatures, audience and time restrictions |
| OpenID Connect | OpenID Foundation (2014) | application (443) | Identity layer on top of OAuth 2.0 | Token replay, identity-provider mix-up | Nonce, validate issuer/audience, PKCE |

Discussed mainly in Chapters 2, 3, 10, and 17.

## I.4 Email

| Protocol (full form) | RFC / standard (year) | Port(s) | Usage | Common attacks | Key defenses |
|------------|---------|-----|------------|------------|------------|
| SMTP (Simple Mail Transfer Protocol) | RFC 5321 (2008; orig 821, 1982) | 25, 587 (submission), 465 (SMTPS) | Sends and relays email | Spoofing, open relay, spam, sniffing | SPF, DKIM, DMARC, STARTTLS, MTA-STS |
| POP3 (Post Office Protocol v3) | RFC 1939 (1996) | 110, 995 (POP3S) | Downloads mail to a client | Cleartext credentials, sniffing | TLS (995), strong authentication |
| IMAP (Internet Message Access Protocol) | RFC 3501 rev1 (2003); RFC 9051 rev2 (2021) | 143, 993 (IMAPS) | Server-side mailbox access | Cleartext credentials, sniffing | TLS (993), OAuth-based auth |

Discussed mainly in Chapters 3 and 4.

## I.5 File Transfer, Remote Access, and Sharing

| Protocol (full form) | RFC / standard (year) | Port(s) | Usage | Common attacks | Key defenses |
|------------|---------|-----|------------|------------|------------|
| FTP (File Transfer Protocol) | RFC 959 (1985) | 21 (control), 20 (data) | File transfer | Cleartext credentials, bounce attack, sniffing | Replace with FTPS/SFTP, disable, restrict |
| FTPS (FTP over TLS) | RFC 4217 (2005) | 21 / 990 | FTP secured with TLS | Misconfiguration, NAT/firewall issues | Explicit TLS, restricted data ports |
| SFTP (SSH File Transfer Protocol) | IETF draft over SSH (RFC 4251 family) | 22 | File transfer tunneled over SSH | Weak keys or credentials | Key-based auth, SSH hardening |
| TFTP (Trivial File Transfer Protocol) | RFC 1350 (1992) | 69 UDP | Simple transfers (PXE boot, device configs) | No authentication, file disclosure/overwrite | Restrict, segment, disable where unused |
| SSH (Secure Shell) | RFC 4251-4254 (2006) | 22 | Secure remote shell and tunneling | Brute force, weak keys, first-connect MITM | Key auth, MFA, fail2ban, verify host keys |
| Telnet | RFC 854 (1983) | 23 | Legacy remote shell | Cleartext, sniffing, session hijacking | Replace with SSH, disable |
| RDP (Remote Desktop Protocol) | Microsoft MS-RDPBCGR | 3389 | Windows remote desktop | BlueKeep (CVE-2019-0708), brute force, MITM | Network Level Authentication, patch, VPN/gateway, MFA |
| VNC / RFB (Remote Framebuffer) | RFC 6143 (2011) | 5900 | Cross-platform remote desktop | Weak or cleartext auth, exposure | Tunnel over SSH/VPN, strong auth |
| SMB (Server Message Block) | Microsoft MS-SMB2 (SMB1 = CIFS) | 445 (139 legacy) | Windows file and printer sharing | EternalBlue (MS17-010), relay, null sessions | Patch, disable SMBv1, signing, block 445 at the edge |
| NFS (Network File System) | RFC 7530 v4 (2015); RFC 1813 v3 (1995) | 2049 | Unix/Linux file sharing | Weak host-based trust, exposure | Kerberos (NFSv4), export restrictions, firewalling |

Discussed mainly in Chapters 3, 9, 11, and 13.

## I.6 Management, Authentication, Time, and Logging

| Protocol (full form) | RFC / standard (year) | Port(s) | Usage | Common attacks | Key defenses |
|------------|---------|-----|------------|------------|------------|
| SNMP (Simple Network Management Protocol) | RFC 1157 v1 (1990); RFC 3411-3418 v3 (2002) | 161, 162 (traps) UDP | Monitoring and managing network devices | Default community strings, info leak, amplification | SNMPv3 (authentication and privacy), ACLs, change defaults |
| LDAP / LDAPS (Lightweight Directory Access Protocol) | RFC 4511 (2006) | 389, 636 (LDAPS) | Directory lookups and authentication | Anonymous bind, LDAP injection, sniffing | LDAPS/StartTLS, restricted binds, input validation |
| Kerberos | RFC 4120 v5 (2005) | 88 | Ticket-based network authentication | Kerberoasting, AS-REP roasting, golden/silver tickets | Strong service-account passwords, AES, PKINIT, monitoring |
| RADIUS (Remote Authentication Dial-In User Service) | RFC 2865 (2000) | 1812/1813 UDP (legacy 1645/1646) | AAA for network access | Shared-secret/MD5 weaknesses (Blast-RADIUS), sniffing | RADSEC (TLS), strong secrets, IPsec |
| TACACS+ (Terminal Access Controller Access-Control System Plus) | RFC 8907 (2020) | 49 TCP | AAA for device administration | Weak body obfuscation, MITM | TLS transport (draft), strong key, management network |
| NTP (Network Time Protocol) | RFC 5905 v4 (2010) | 123 UDP | Time synchronization | Amplification DDoS (monlist), spoofing | NTPv4 hardening, NTS (RFC 8915), restrict queries |
| syslog | RFC 5424 (2009) | 514 UDP (6514 TLS) | Event and log transport | Forged/spoofed logs, cleartext exposure | TLS (RFC 5425), source authentication, segmentation |
| 802.1X / EAP (port access control; Extensible Authentication Protocol) | IEEE 802.1X-2020; EAP RFC 3748 (2004) | EAPOL (layer 2) | Port-based network access control | Rogue supplicant, EAP downgrade, bypass | EAP-TLS, MACsec, certificate-based auth |

Discussed mainly in Chapters 9, 11, and 12.

## I.7 VPN and Tunneling

| Protocol (full form) | RFC / standard (year) | Port(s) | Usage | Common attacks | Key defenses |
|------------|---------|-----|------------|------------|------------|
| IPsec (ESP/AH/IKEv2) | ESP RFC 4303 (2005); IKEv2 RFC 7296 (2014) | IKE 500/4500 UDP; ESP IP proto 50 | Encrypted IP tunnels and VPNs | Aggressive-mode PSK cracking, downgrade | IKEv2, strong DH groups, certificate auth |
| L2TP (Layer 2 Tunneling Protocol) | RFC 2661 (1999); v3 RFC 3931 (2005) | 1701 UDP | Layer-2 tunneling, usually with IPsec | No confidentiality on its own | Always pair with IPsec |
| PPTP (Point-to-Point Tunneling Protocol) | RFC 2637 (1999) | 1723 TCP + GRE | Legacy VPN | MS-CHAPv2 broken, traffic decryptable | Deprecate; use IPsec or WireGuard |
| GRE (Generic Routing Encapsulation) | RFC 2784 (2000) | IP proto 47 | Generic tunneling of arbitrary protocols | No encryption, spoofing | Encrypt with IPsec, apply ACLs |
| PPP (Point-to-Point Protocol) | RFC 1661 (1994) | n/a | Point-to-point link framing and auth | Weak legacy auth (PAP cleartext) | Use CHAP/EAP over secure transports |
| OpenVPN | Open-source project (2001) | 1194 UDP/TCP | TLS-based VPN | Weak configs, certificate issues | Strong TLS, certificates, tls-auth/tls-crypt |
| WireGuard | In-kernel since Linux 5.6 (2020) | 51820 UDP (configurable) | Modern, fast, minimal VPN | Endpoint exposure, key mismanagement | Key rotation, firewalling, least exposure |

Discussed mainly in Chapter 11.

## I.8 Routing, Switching, and Redundancy

| Protocol (full form) | RFC / standard (year) | Port(s) | Usage | Common attacks | Key defenses |
|------------|---------|-----|------------|------------|------------|
| BGP (Border Gateway Protocol) | RFC 4271 BGP-4 (2006) | 179 TCP | Inter-domain Internet routing | Prefix/route hijacking, route leaks | RPKI/ROA, prefix filters, max-prefix limits, BGPsec |
| OSPF (Open Shortest Path First) | RFC 2328 v2 (1998) | IP proto 89 | Intra-domain link-state routing | Spoofed link-state advertisements | HMAC authentication, passive interfaces |
| RIP (Routing Information Protocol) | RFC 2453 v2 (1998) | 520 UDP | Legacy distance-vector routing | Route spoofing/poisoning | Authentication, prefer OSPF, disable |
| STP (Spanning Tree Protocol) | IEEE 802.1D | n/a (layer-2 BPDUs) | Loop prevention in switched LANs | BPDU spoofing, root-bridge takeover | BPDU guard, root guard |
| VLAN / 802.1Q | IEEE 802.1Q | n/a (layer-2 tag) | Network segmentation | VLAN hopping (double-tagging, switch spoofing) | Disable DTP, change native VLAN, VLAN pruning |
| VRRP (Virtual Router Redundancy Protocol) | RFC 5798 (2010) | IP proto 112 | Default-gateway redundancy | Spoofed master takeover | Authentication, control-plane filtering |

Discussed mainly in Chapters 3 and 11.

## I.9 Wireless

| Protocol (full form) | RFC / standard (year) | Port(s) | Usage | Common attacks | Key defenses |
|------------|---------|-----|------------|------------|------------|
| WEP (Wired Equivalent Privacy) | IEEE 802.11 (1997) | n/a (layer 2) | Original Wi-Fi encryption | Completely broken (RC4/IV reuse) | Never use; move to WPA2/WPA3 |
| WPA / WPA2 (Wi-Fi Protected Access) | IEEE 802.11i (2004) | n/a | Wi-Fi link security | KRACK, PMKID/handshake cracking, weak PSK | WPA3, strong passphrase, 802.1X enterprise |
| WPA3 | Wi-Fi Alliance (2018) | n/a | Current Wi-Fi security (SAE handshake) | Dragonblood (early implementations) | Patch, WPA3-only mode, strong configuration |
| WPS (Wi-Fi Protected Setup) | Wi-Fi Alliance (2006) | n/a | Simplified device pairing | PIN brute force (Reaver), Pixie Dust | Disable WPS |

Discussed mainly in Chapters 3, 7, and 11.

## I.10 Multimedia, Messaging, IoT, and Discovery

| Protocol (full form) | RFC / standard (year) | Port(s) | Usage | Common attacks | Key defenses |
|------------|---------|-----|------------|------------|------------|
| SIP (Session Initiation Protocol) | RFC 3261 (2002) | 5060 UDP/TCP, 5061 TLS | VoIP and multimedia call signaling | Toll fraud, eavesdropping, registration hijack | TLS, SRTP, strong authentication |
| RTP / SRTP (Real-time Transport Protocol / Secure RTP) | RFC 3550 (2003) / RFC 3711 (2004) | dynamic UDP | Real-time audio and video transport | Eavesdropping, media injection | SRTP encryption and authentication |
| RTSP (Real-Time Streaming Protocol) | RFC 2326 (1998); v2 RFC 7826 (2016) | 554 | Streaming and IP-camera control | Exposure, missing/weak authentication | Authentication, segmentation, VPN |
| UPnP / SSDP (Universal Plug and Play / Simple Service Discovery Protocol) | UPnP/OCF; SSDP (expired IETF draft) | 1900 UDP | Automatic device discovery | SSDP reflection/amplification DDoS, exposure | Disable on WAN, segment IoT |
| MQTT (Message Queuing Telemetry Transport) | OASIS / ISO-IEC 20922 (2016) | 1883 (8883 TLS) | Lightweight IoT publish/subscribe | Cleartext, no auth, topic abuse | TLS, authentication, topic ACLs |
| CoAP (Constrained Application Protocol) | RFC 7252 (2014) | 5683 UDP (5684 DTLS) | REST-like messaging for constrained IoT | Amplification, spoofing | DTLS, rate limiting |
| AMQP (Advanced Message Queuing Protocol) | OASIS / ISO-IEC 19464 (2014) | 5672 (5671 TLS) | Enterprise message queuing | Cleartext, weak auth | TLS, SASL authentication |
| XMPP (Extensible Messaging and Presence Protocol) | RFC 6120 (2011) | 5222, 5269 | Messaging and presence | Spoofing, sniffing | TLS, SASL |
| IRC (Internet Relay Chat) | RFC 1459 (1993) | 6667 (6697 TLS) | Group chat (and historic botnet C2) | C2 abuse, cleartext | TLS, monitoring, egress control |
| BitTorrent | BEP specifications (no RFC) | 6881-6889 TCP | Peer-to-peer file sharing | Malware distribution, IP exposure | Policy controls, monitoring |

Discussed mainly in Chapters 3, 7, 15, and 17.

## I.11 Industrial Control Systems and Operational Technology

| Protocol (full form) | RFC / standard (year) | Port(s) | Usage | Common attacks | Key defenses |
|------------|---------|-----|------------|------------|------------|
| Modbus | Modbus Organization specification (1979) | 502 TCP | Reading/writing PLC and SCADA registers | No authentication or encryption, replay, command injection | Network segmentation, gateways, deep-packet monitoring |
| DNP3 (Distributed Network Protocol 3) | IEEE 1815-2012 | 20000 TCP/UDP | SCADA telemetry for utilities | Spoofing, replay | DNP3 Secure Authentication, segmentation |
| S7comm | Siemens (proprietary) | 102 TCP | Siemens S7 PLC communication | Replay, command injection (Stuxnet class) | Segmentation, strict access control |
| PROFINET | IEC 61158 / 61784 | 34962-34964 (and layer 2) | Real-time industrial Ethernet automation | Spoofing, denial of service | Segmentation, monitoring |
| BACnet | ASHRAE 135 / ISO 16484-5 | 47808 UDP | Building automation and control | Spoofing, exposure | Segmentation, BACnet/SC (secure connect) |
| OPC UA (OPC Unified Architecture) | IEC 62541 | 4840 TCP | Secure, vendor-neutral industrial interop | Misconfiguration, weak certificates | Security modes, certificate management, hardening |

Discussed mainly in Chapter 20 (and Chapter 17 for IoT).

## I.12 Storage Interfaces

These are storage access protocols rather than general-purpose IETF network protocols, but they appear in the
book (Chapter 17) and carry their own exposure.

| Protocol (full form) | RFC / standard (year) | Port(s) | Usage | Common attacks | Key defenses |
|------------|---------|-----|------------|------------|------------|
| iSCSI (Internet Small Computer Systems Interface) | RFC 7143 (2014; orig 3720, 2004) | 3260 TCP | Block storage over IP networks | Cleartext data, weak CHAP, network exposure | CHAP with IPsec, isolated storage VLAN |
| NVMe / NVMe-oF (Non-Volatile Memory Express over Fabrics) | NVM Express specification | 4420 (NVMe/TCP) | High-performance flash storage and fabrics | Fabric exposure, weak access control | Isolated fabric, DH-HMAC-CHAP, TLS |
| SATA / SAS (Serial ATA / Serial Attached SCSI) | SATA-IO / INCITS T10 | n/a (local bus) | Local drive attachment | Physical access, no transport security | Full-disk encryption, physical security |

## I.13 How to Use This Reference

For defenders, the recurring pattern across this table is unmistakable: protocols designed before security was
a first-class concern (Telnet, FTP, SNMPv1, WEP, the ICS protocols, and the plaintext mail protocols) send
credentials and data in the clear and trust whatever they receive, while their modern replacements (SSH,
SFTP/FTPS, SNMPv3, WPA3, DNS over TLS, and the TLS-protected mail ports) add encryption and authentication.
The single most effective control list, applied across nearly every row above, is to encrypt the channel
(TLS, SSH, IPsec, or DTLS), authenticate both ends, segment management and operational protocols away from
general traffic, filter or disable services that are not needed, and keep implementations patched. Where a
protocol cannot be secured in place (Telnet, SMBv1, PPTP, WEP), the correct defense is replacement, not
mitigation.
