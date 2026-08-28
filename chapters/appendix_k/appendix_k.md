# Appendix K: Course Materials, Coverage Map, and Sample Assignments

This appendix is a resource for instructors. It maps common lecture topics to the chapters that cover them, gives
three ready-to-adapt lecture-module outlines, and lists sample assignments and group projects. It complements
Appendix H (capstone and group-project ideas) and Appendix F (companion code); where the material overlaps, this
appendix cross-references rather than repeats. The outlines and projects are written to be institution-neutral, so
they can be dropped into a syllabus and adjusted to local constraints.

## K.1 Source-Materials Coverage Map

A typical undergraduate ethical-hacking or computer-security course is taught from a sequence of topic lectures.
The table below maps those standard topics to the chapters of this book, so an instructor moving from an existing
slide deck can find the corresponding reading, worked examples, exercises, and labs. It doubles as a coverage
check: every topic in a conventional sequence is treated somewhere in the text.

| Lecture topic | Book chapter(s) |
|---|---|
| Introduction to ethical hacking; penetration-testing methodology; rules of engagement; PTES and NIST testing | 6 |
| Professional ethics; the legal system; proper and responsible disclosure | 1, 6, 18 |
| Cryptography: classical ciphers, symmetric and public-key, hashing, signatures, HTTPS and TLS | 2 |
| The OSI model, ports, ARP, DHCP, the TCP handshake; sniffing, Wireshark, session hijacking | 3 |
| Reconnaissance and intelligence gathering; OSINT; Google dorking; log and SIEM review | 7 |
| Port scanning and network mapping; enumeration; OS fingerprinting; vulnerability scanning (Nessus, NSE) | 8 |
| Exploitation, Kali and Metasploit; Linux and Windows exploitation; shellcode; passive analysis and reversing | 9, 15 |
| Password cracking; Windows security (SAM, SID/RID, LM/NTLM, Active Directory, LDAP, NetBIOS, SMB); rootkits | 9, 15 |
| Programming survival skills: C, assembly, gdb, Python for security | 9, 15 |
| Web application attacks: the OWASP Top 10, SQL injection, XSS, Nikto, session flaws | 10 |
| Mobile, wireless, and IoT attacks (WEP/WPA/WPA2/WPA3, evil twin, deauthentication) | 3, 17, 20 |
| Malware: viruses, worms, trojans, RATs; antivirus and antimalware; detection methods | 12, 15 |
| Firewalls and their types; intrusion detection and prevention; honeypots and deception | 11, 12 |
| Physical security and social engineering | 4, 11, 20 |
| Incident response: before, during, and after the attack; "attacks are inevitable" | 14 |
| Virtualization and its security | 17 |
| Capture-the-flag competitions: platforms and tooling | 16 |
| Formal adversary and threat models | Appendix J |
| Companion source code (cryptography, networking, exploitation) | Appendix F, `code/` |

### K.1.1 Software Reverse Engineering: A Malware-Analysis Course Map

A common Software Reverse Engineering course is organized around a hands-on malware-analysis textbook and a
fifteen-week laboratory sequence. The mapping below aligns that standard progression to the chapters and sections
of this book, so an instructor using such a syllabus can assign the corresponding reading. It also serves as a
coverage check for the reverse-engineering track (Chapters 9 and 15, with networking analysis from Chapter 3).

| Weekly topic (typical SRE sequence) | Book section(s) |
|---|---|
| What reverse engineering is: discipline, domains, law, and careers | 15.39 |
| How software is built; toolchains, artifacts, and malware versus software | 15.38, 15.1 |
| Basic static techniques | 15.3, 15.4 |
| Malware analysis in virtual machines (safe lab) | 15.21, 15.2 |
| Basic dynamic analysis | 15.25, 15.4 |
| x86 assembly and IDA Pro | 9.27, 15.22, 15.35 |
| C code in assembly; malicious Windows programs | 15.22, 15.23 |
| Debugging and OllyDbg/x64dbg | 9.28, 15.25, 15.35 |
| Malware behavior | 15.13 to 15.17 |
| Covert launching and data encoding | 15.33, 15.24 |
| Network signatures and anti-disassembly | 15.34, 15.30 |
| Anti-debugging | 15.30, 15.35 |
| Anti-virtual-machine techniques | 15.30 |
| Packers and unpacking; shellcode analysis | 15.5, 15.25, 9.25 |
| C++ analysis | 15.32 |
| 64-bit malware | 15.22, 15.27 |
| Linux-only analysis workflow (pev, gdb, edb, crackmes) | 15.37, 15.27 |
| AI-assisted reverse engineering | 15.36 |
| Competitive practice: the CTF reverse engineering category | 16.12, 16.2 |
| Final project: analyze real-world malware | 15.11, 15.19, 15.29, 15.31 |

The standard reference for such a course is Sikorski and Honig's *Practical Malware Analysis* (No Starch Press,
2012), and a concise scholarly overview is Cipresso and Stamp's "Software Reverse Engineering" chapter in the
*Handbook of Information and Communication Security* (Springer, 2010).

### K.1.2 Three Systems- and Network-Security Course Maps

Three further course maps align this book to a twelve-week sequence for an introductory computer-security course,
a Security+ oriented advanced network-security course, and an advanced systems-security course. Each row is one
weekly lecture in the order a syllabus would teach it, so an instructor can assign the corresponding reading. The
sequences are institution-neutral and pair one graded midterm, one final, and one semester-long group research
project.

Introductory Computer Security:

| Weekly lecture | Book chapter(s) |
|---|---|
| Security overview and cryptographic tools | 1, 2 |
| User authentication and access control | 11, 1 |
| Denial-of-service attacks, intrusion detection, and honeypots | 3, 12 |
| Malicious software and countermeasures | 15, 4 |
| Software security: buffer overflows and safe coding | 9, 10 |
| Operating-system security and human-resources security | 11, 19 |
| Application security: OWASP Top 10, sessions, TLS, SSH | 10, 2 |
| Browser attacks and web security principles | 10 |
| Database security and SQL injection | 10, 19 |
| Security development methodologies: SDL, CLASP, SAMM, BSIMM | 10, 19 |
| IT security management and risk assessment | 5, 19 |
| Cloud security, IoT, electronic voting, and cyber warfare | 17, 20, 18 |

Advanced Network Security (CompTIA Security+ oriented):

| Weekly lecture | Book chapter(s) |
|---|---|
| Introduction to security and access-control models | 1, 11 |
| Threats: malware, social engineering, and application attacks | 4, 15, 10 |
| Identifying and mitigating threats | 4, 9 |
| Policies, network plans, risk management, and incident response | 5, 19, 14 |
| Physical security, tailgating, and breaking into a system | 4, 11 |
| Cryptography | 2 |
| Denial of service, DNS attacks, and firewalls | 3, 11 |
| Virtual private networks | 11, 2 |
| Securing network devices and file-server security | 3, 11 |
| Web application attacks, browsers, and wireless security | 10, 3 |
| Data defenses: redundancy, backup, and file encryption | 5, 2, 11 |
| Assessment and audit techniques, penetration testing, and log management | 6, 8, 12 |

Advanced Systems Security:

| Weekly lecture | Book chapter(s) |
|---|---|
| Access controls and the identity-management life cycle | 11 |
| Security concepts and asset management | 1, 5 |
| Documenting and operating controls; change and patch management | 19, 11 |
| Risk management | 5 |
| Security assessment activities | 6, 8 |
| Monitoring systems and security analytics | 12 |
| Cryptography and key management | 2 |
| Network and communications security | 3, 11 |
| Endpoint device security: HIDS, TPM, and mobile device management | 11, 15 |
| Cloud security | 17 |
| Data-warehouse and big-data security | 10, 17 |
| Software-defined networks, clustering, and virtualization | 17, 11 |

## K.2 Sample Lecture Modules

The three outlines below are complete single-topic modules distilled to their teaching structure. Each can be
delivered as one or two lectures and pairs with the chapter noted.

### K.2.1 Social Engineering and the Human Attack Surface (pairs with Chapter 4)

A module on why humans, not technology, remain the most consistently exploited attack surface.

1. The unpatchable vulnerability. Modern attackers increasingly log in with stolen credentials and manipulated
   approvals rather than breaking in; the user becomes the attack vector, and one click or approval can nullify
   expensive technical defenses.
2. The cognitive science of the attack. Humans rely on mental shortcuts (heuristics) to function; social
   engineering is engineered to exploit them. Introduce dual-process thinking (fast, automatic System 1 versus
   slow, analytical System 2) and how attackers keep victims in System 1 through urgency and emotion.
3. The levers of influence. Authority, urgency, scarcity, social proof, reciprocity, and fear, with a worked
   example of each in a phishing or pretexting lure.
4. Attack forms. Phishing and spear phishing, vishing and smishing, pretexting, baiting, and business email
   compromise (Section 4 and Section 14 for the incident-response side).
5. Building resilient systems. Because human error is inevitable, design for it: verification workflows,
   out-of-band approval for high-risk actions, least privilege, and phishing-resistant multi-factor
   authentication, plus a culture in which reporting a mistake is safe.

### K.2.2 Ethical Hacking Foundations (pairs with Chapters 1, 5, and 6)

An opening module that establishes vocabulary and mindset before any hands-on work.

1. The CIA triad. Confidentiality, integrity, and availability as the goals every control ultimately serves,
   each with a concrete breach example.
2. The DAD triad. Disclosure, alteration, and destruction as the attacker's mirror image of CIA, defining what a
   malicious actor is trying to achieve.
3. The anatomy of an attack. Vulnerability (the weakness), threat (the danger), and exploit (the mechanism), the
   vocabulary used throughout the book, tied to the risk material of Chapter 5.
4. Authorization and ethics first. Rules of engagement, scope, written authorization, and responsible
   disclosure, so that every later technique is practiced legally (Chapter 6).
5. The attacker's process. A preview of the reconnaissance, scanning, exploitation, and post-exploitation
   sequence developed in Chapters 7 through 9.

### K.2.3 Intrusion Detection and Prevention Systems (pairs with Chapters 11 and 12)

A module on the security-monitoring stack and where each component fits.

1. Why dedicated security devices exist, and how they fit a defense-in-depth strategy.
2. The monitoring stack. Distinguish SIEM, SOAR, XDR, and EDR and place each in the workflow of a security
   operations center (Section 12).
3. The kill chain. Walk the seven stages of the Lockheed Martin Cyber Kill Chain and identify a defensive
   opportunity at each, connecting to MITRE ATT&CK (Section 12).
4. IDS versus IPS. Detection versus prevention, and passive (out-of-band) versus inline deployment and its
   tradeoffs.
5. Sensor placement. Network-based (NIDPS) versus host-based (HIDPS) sensors, and centralized versus distributed
   control strategies.
6. Detection methods. Signature-based, anomaly-based, stateful-protocol, and log-file analysis, with their
   respective strengths and blind spots, plus trap-and-trace and deception (honeypots).

## K.3 Sample Assignments and Group Projects

The projects below are build-oriented and suit teams of two to four students over several weeks. They
deliberately span offense and defense and map to specific chapters; Appendix H offers additional capstone ideas.
Each should be performed only against systems the team owns or is explicitly authorized to test, in an isolated
lab (Chapter 6).

1. Modern phishing simulation and human-risk analysis. Run a multi-stage, controlled phishing campaign against a
   consenting test population: gather OSINT to craft believable lures (Chapter 7), host email templates and a
   spoofed landing page in a contained environment, capture interactions, then compute a phish rate and correlate
   lure sophistication with susceptibility. Tools: an open-source simulation platform (for example GoPhish),
   theHarvester or Maltego. Pairs with Chapters 4 and 14.

2. Mobile or web API vulnerability scanner. Focus on broken access control, especially insecure direct object
   references: intercept client-server traffic with a proxy, then script the systematic modification of object
   identifiers (for example incrementing a user id) to test for horizontal and vertical privilege escalation.
   Deliver a Python tool that automates the parameter injection and reports findings. Pairs with Chapter 10.

3. Automated web-application fuzzer. Build a tool that sends malformed and boundary-case input to a target
   application, monitors responses for errors and crashes, and logs candidate vulnerabilities. Cover mutation
   and generation fuzzing and boundary-value analysis. Tools: Python (requests, a fuzzing library), optionally an
   intercepting proxy. Pairs with Chapters 9 and 10.

4. Network protocol analyzer and sniffer. Develop a capture-and-decode tool that reads live traffic and parses
   packet structure, then extracts security-relevant indicators (credentials in the clear, suspicious
   destinations). Tools: Python (Scapy, libpcap) or C/C++ (libpcap). Pairs with Chapters 3 and 12.

5. Host-based intrusion-detection prototype. Instrument a host to collect process, file, and registry events and
   apply simple signature and anomaly rules to flag suspicious behavior, then measure the true- and false-positive
   rates on benign and malicious activity (Section 12). Pairs with Chapters 12 and 13.

## K.4 Adapting These Materials

The modules and projects are starting points, not prescriptions. Scale them to the term: an introductory course
might use only the foundations module and the phishing or protocol-analyzer project, while an advanced course can
combine the exploitation labs of Chapter 9 with the fuzzer and the intrusion-detection prototype. The guidance in
the introduction on trimming the longer chapters from the back applies here too, keep the hands-on projects and
the case studies when time is short, because those are what students remember. All companion source code
referenced by these assignments is indexed in Appendix F and bundled in the repository's `code/` directory.
