# Appendix G: Book Statistics and Word Counts

This page reports the size of each chapter and of each section within it, measured in markdown words (the prose; code and figures are additional and reported separately per chapter). It is generated automatically from the book source. Approximate pages assume about 500 words per page.

Last generated: 2026-06-06.

## Summary by Chapter

| Chapter | Markdown words | Code words | Approx. pages |
|---|---:|---:|---:|
| Introduction | 816 | 0 | 1.6 |
| Preface | 391 | 0 | 0.8 |
| Chapter 1: Introduction to Cybersecurity | 8,936 | 361 | 17.9 |
| Chapter 2: Cryptography | 28,882 | 1,994 | 57.8 |
| Chapter 3: Networking and Network Attacks | 14,610 | 374 | 29.2 |
| Chapter 4: Social Engineering and the Human Element | 7,218 | 203 | 14.4 |
| Chapter 5: Risk Management | 11,833 | 469 | 23.7 |
| Chapter 6: Penetration Testing Methodology | 9,639 | 265 | 19.3 |
| Chapter 7: Reconnaissance and Open-Source Intelligence | 6,606 | 253 | 13.2 |
| Chapter 8: Scanning and Enumeration | 6,849 | 816 | 13.7 |
| Chapter 9: Exploitation and Post-Exploitation | 5,225 | 316 | 10.4 |
| Chapter 10: Web Application Security | 4,376 | 202 | 8.8 |
| Chapter 11: Network Defense and Hardening | 5,075 | 258 | 10.2 |
| Chapter 12: Intrusion Detection and Prevention Systems | 3,620 | 377 | 7.2 |
| Chapter 13: Digital Forensics | 3,803 | 300 | 7.6 |
| Chapter 14: Incident Response | 3,556 | 373 | 7.1 |
| Chapter 15: Malware Analysis | 3,727 | 339 | 7.5 |
| Chapter 16: Capture the Flag and Competitive Security | 3,305 | 366 | 6.6 |
| Chapter 17: Emerging Threats and Future Challenges | 9,993 | 598 | 20.0 |
| Chapter 18: Privacy, Law, and Information Governance | 3,728 | 387 | 7.5 |
| Chapter 19: Security Governance, Policy, and Culture | 3,519 | 482 | 7.0 |
| Chapter 20: Industrial Control Systems and OT Security | 2,086 | 442 | 4.2 |
| Appendix A: Security Command Reference | 1,653 | 0 | 3.3 |
| Appendix B: Glossary | 2,319 | 0 | 4.6 |
| Appendix C: Certification Mapping | 1,277 | 0 | 2.6 |
| Appendix D: ABET Outcomes and Bloom's Taxonomy Mapping | 775 | 0 | 1.6 |
| Appendix E: Selected Works by the Author | 1,506 | 0 | 3.0 |
| Appendix F: Companion Code and Repositories | 1,169 | 0 | 2.3 |
| Appendix H: Capstone and Group Project Ideas | 833 | 0 | 1.7 |
| **TOTAL** | **157,325** | **9,175** | **315** |

## Detailed Word Count by Section


### Introduction

*816 markdown words (1.6 pages); 0 code words.*

| Section | Words |
|---|---:|
| Course Mapping | 157 |
| What Every Chapter Contains | 64 |
| How to Cite This Book | 158 |
| Accessibility | 310 |
| License | 27 |

### Preface

*391 markdown words (0.8 pages); 0 code words.*

| Section | Words |
|---|---:|
| About This Textbook | 38 |
| Who This Book Is For | 49 |
| How This Book Is Organised | 127 |
| Ethical Commitment | 65 |
| Using This Book in a Course | 57 |
| A Note on Currency | 55 |

### Chapter 1: Introduction to Cybersecurity

*8,936 markdown words (17.9 pages); 361 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 179 |
| Key Terms | 252 |
| 1.1 What Is Cybersecurity? | 636 |
| 1.2 The CIA Triad and Its Extensions | 649 |
|     The DIE Model: A Modern Complement to CIA | 254 |
| 1.3 The Anatomy of an Attack | 593 |
| 1.4 Threat Actors and the Adversary Model | 529 |
| 1.5 Defense in Depth and Security Controls | 488 |
| 1.6 Hardware Foundations: Rings, Modes, and the Trusted Computing Base | 561 |
| 1.7 The NIST Cybersecurity Framework | 403 |
| 1.8 Quantifying Risk in Monetary Terms | 375 |
| 1.9 The Saltzer and Schroeder Design Principles | 641 |
|     The Principle of Least Privilege (PoLP) | 246 |
| 1.10 The Security Mindset, Ethics, and the Law | 369 |
| 1.11 A Taxonomy of Threats and a Roadmap to This Book | 547 |
| Chapter Summary | 240 |
| Why This Matters | 133 |
| News in Focus: The Colonial Pipeline Ransomware Incident (2021) | 215 |
|     A Second Case: The SolarWinds Supply-Chain Compromise (2020) | 266 |
| News in Focus: Cyber Warfare and the US-Iran Cyber Conflict | 531 |
| Review Questions | 349 |
|     Answer Key | 39 |
| Hands-on Labs | 248 |
| References | 154 |

### Chapter 2: Cryptography

*28,882 markdown words (57.8 pages); 1,994 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 170 |
| Key Terms | 648 |
| 2.1 What Cryptography Is and What It Promises | 387 |
|     Encoding versus Encryption versus Hashing | 316 |
| 2.2 Classical Ciphers and Why They Fall | 604 |
|     Classical versus Modern Ciphers | 295 |
|     A Classification of Ciphers | 226 |
|     Classical Ciphers in Code | 294 |
| 2.3 Perfect Secrecy and the One-Time Pad | 633 |
|     XOR, the One-Time Pad, and Perfect Secrecy, Formally | 698 |
|     From Information-Theoretic to Computational Security | 311 |
|     Game-Based (Provable) Security and Ciphertext Indistinguishability | 2,292 |
|     Real-World Case: The ANC's One-Time Pad and Operation Vula | 441 |
| 2.4 Randomness: True, Pseudo, and Cryptographically Secure | 517 |
|     Insecure versus Cryptographically Secure Randomness in Code | 168 |
| 2.5 Symmetric Encryption: Stream and Block Ciphers | 850 |
|     The Feistel Network: A Blueprint for Block Ciphers | 222 |
| 2.6 Block Cipher Modes of Operation | 540 |
|     AES Modes in Code: ECB versus CTR | 324 |
| 2.7 Cryptographic Hash Functions | 626 |
|     The Merkle-Damgard Construction | 215 |
|     Hashing in Code, and Why a CRC Is Not a Hash | 213 |
|     Error Detection versus Error Correction: CRC and Hamming Codes | 205 |
| 2.8 Message Authentication Codes and Authenticated Encryption | 585 |
|     Hash, MAC, and Digital Signature Compared | 490 |
|     Wrong-Key Behavior: Garbage Output versus Null Rejection | 526 |
|     The Three-Behavior Hierarchy of Incorrect Decryption | 2,298 |
|     Computing an HMAC in Code | 98 |
|     Authenticated Encryption in Practice: Encrypt-then-MAC | 190 |
| 2.9 Key Derivation and Password Storage | 510 |
| 2.10 Public-Key Cryptography and RSA | 686 |
| 2.11 Diffie-Hellman Key Exchange | 519 |
|     ElGamal Encryption | 277 |
|     ElGamal in Code | 266 |
| 2.12 Elliptic-Curve Cryptography | 495 |
|     Elliptic Curves Up Close: Group Law, the ECDLP, and the Curve Zoo | 776 |
| 2.13 Digital Signatures, Certificates, and PKI | 619 |
|     Generating a Digital Signature in Code | 145 |
| 2.14 Putting It Together: The TLS Handshake | 354 |
| 2.15 Advanced and Emerging Cryptography | 824 |
|     Computing Paradigms: Mainframes, Classical, DNA, and Quantum | 395 |
|     Searchable, Deniable, and Functional Encryption | 341 |
|     The Algebra Beneath Cryptography: Finite Fields, Abelian and Non-Abelian Groups | 470 |
| 2.16 Key Management | 530 |
|     Key Management Services and Key Escrow | 347 |
| 2.17 A Taxonomy of Cryptographic Attacks | 348 |
| 2.18 Applied Cryptographic Systems | 392 |
| 2.19 Practical Guidance: Choosing and Using Cryptography | 380 |
| 2.19a Protecting Data in All Three States | 289 |
| 2.19b Tamper-Evident and Tamper-Proof Mechanisms | 207 |
| 2.20 Formal Security Analysis and Provable Security | 125 |
|     The Anatomy of a Security Definition | 331 |
|     Hardness Assumptions and the Random Oracle Model | 234 |
|     The Zoo of Security Notions | 251 |
|     Simulation-Based Security and Universal Composability | 234 |
|     Symbolic Models: Dolev-Yao and Automated Verification | 316 |
|     A Taxonomy of Security Properties | 326 |
|     Writing a Security Analysis: Proof Sketches and Experimental Evaluation | 372 |
| Why This Matters | 161 |
| News in Focus: Heartbleed (2014) | 202 |
| Review Questions | 433 |
|     Answer Key | 106 |
| Hands-on Labs | 375 |
| References | 826 |

### Chapter 3: Networking and Network Attacks

*14,610 markdown words (29.2 pages); 374 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 152 |
| Key Terms | 407 |
| 3.1 Why Networking Is the Battleground | 359 |
| 3.2 The OSI Model | 550 |
|     Mapping the OSI and TCP/IP Models | 270 |
| 3.3 The TCP/IP Model and Encapsulation | 293 |
|     Network Devices and Segments | 194 |
|     Routing and the Route Table | 250 |
| 3.4 IP Addressing: IPv4 and IPv6 | 508 |
|     Subnetting, CIDR, and Network versus Host Addresses | 332 |
|     Network Scopes and Hardware: NIC, LAN, WLAN, and WAN | 410 |
|     Special and Reserved Addresses | 233 |
|     IP Address Management and Internet Registries | 212 |
| 3.5 Ports and Common Protocols | 434 |
|     Application Protocols and Their Security Posture | 383 |
|     Secure versus Insecure Protocols | 319 |
| 3.6 The Core Protocols: TCP, UDP, ICMP, and Their Headers | 793 |
|     Sockets: Programming the Transport Layer | 216 |
|     Sockets in Code: A TCP Server, Client, and a Tiny Web Server | 586 |
| 3.7 ARP and DHCP: Convenience and Its Abuse | 472 |
|     The Domain Name System (DNS) | 548 |
| 3.8 Sniffing: Listening on the Wire | 530 |
|     Wireless Networking Fundamentals | 250 |
|     Traffic Analysis and Network Monitoring | 158 |
|     Syslog and Centralized Logging | 354 |
| 3.9 Spoofing, Man-in-the-Middle, and Session Hijacking | 613 |
|     Packet Capture, On-Path Attacks, and SSL Stripping | 315 |
|     Hands-On: Capturing a Plaintext Password, Then Encrypting It | 501 |
| 3.10 Denial-of-Service and Distributed Denial-of-Service Attacks | 1,068 |
|     Access Control Lists, NACLs, and Security Groups | 515 |
| 3.11 Securing the Network: A Preview | 173 |
|     Secure Network Protocols | 203 |
|     Going Deeper: Routing Security and BGP Hijacking | 180 |
|     Network Access Control | 144 |
| Chapter Summary | 215 |
| Why This Matters | 153 |
| News in Focus: The Mirai Botnet and the Dyn Attack (2016) | 186 |
| Review Questions | 384 |
|     Answer Key | 30 |
| Hands-on Labs | 393 |
| References | 254 |

### Chapter 4: Social Engineering and the Human Element

*7,218 markdown words (14.4 pages); 203 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 115 |
| Key Terms | 169 |
| 4.1 Why People Are the Weakest Link | 394 |
| 4.2 The Psychology of Influence | 468 |
| 4.3 The Social-Engineering Attack Lifecycle | 463 |
| 4.4 The Taxonomy of Social-Engineering Attacks | 813 |
| 4.5 Vectors and the Role of Open-Source Intelligence | 429 |
| 4.6 Recognizing and Analyzing Phishing | 472 |
| 4.7 Physical Security as Social Engineering's Partner | 363 |
|     Environmental and Availability Threats | 338 |
| 4.8 Authentication Factors | 386 |
| 4.9 Defending Against Social Engineering | 315 |
|     Technical Controls That Reinforce the Human Defenses | 216 |
|     Measuring and Sustaining the Human Firewall | 359 |
| 4.10 Social Engineering in the Age of Artificial Intelligence | 441 |
| News in Focus: The 2020 Twitter Account Takeover | 185 |
| Why This Matters | 169 |
| Chapter Summary | 219 |
| Review Questions | 396 |
|     Answer Key | 30 |
| Hands-on Labs | 243 |
| References | 143 |

### Chapter 5: Risk Management

*11,833 markdown words (23.7 pages); 469 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 155 |
| Key Terms | 160 |
| 5.1 Risk as the Organizing Principle of Security | 395 |
| 5.2 The Vocabulary of Risk | 607 |
| 5.3 The Risk-Management Lifecycle | 399 |
| 5.4 Risk Identification | 275 |
|     Asset and Data Classification | 239 |
|     A Worked Risk Register | 281 |
| 5.5 Qualitative Risk Assessment | 346 |
| 5.6 Quantitative Risk Assessment | 682 |
| 5.7 Risk Treatment | 740 |
| 5.8 Threat Modeling | 565 |
| 5.9 Risk Frameworks and Standards | 329 |
|     The NIST RMF Steps in Detail | 170 |
|     CSF Tiers and Profiles, and ISO 27001 | 413 |
| 5.10 The Security Program: Policies, Standards, and Controls | 306 |
|     Control Catalogs and Foundational Control Principles | 344 |
| 5.11 Business Continuity and Disaster Recovery | 328 |
|     Resilience Engineering: Backups, Redundancy, and Plan Testing | 441 |
| 5.12 Third-Party and Supply-Chain Risk | 223 |
| 5.13 Assurance Evaluation | 337 |
| 5.14 Security Roles, Responsibilities, and Accountability | 251 |
| 5.15 Measuring Risk: Metrics, KPIs, and KRIs | 236 |
| 5.16 Managing Risk Across the System Lifecycle | 244 |
| 5.17 Compliance as a Risk Driver | 303 |
| 5.18 Insider Risk and Human Factors | 279 |
| 5.19 Emerging Risks: AI, Quantum, and the Expanding Attack Surface | 293 |
| 5.20 Bringing It Together: An End-to-End Risk Scenario | 431 |
| 5.21 Common Pitfalls in Risk Management | 274 |
| News in Focus: Repeat Breaches at Neiman Marcus | 467 |
| Why This Matters | 164 |
| Chapter Summary | 242 |
| Review Questions | 364 |
|     Answer Key | 30 |
| Hands-on Labs | 210 |
| References | 178 |

### Chapter 6: Penetration Testing Methodology

*9,639 markdown words (19.3 pages); 265 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 117 |
| Key Terms | 147 |
| 6.1 Why Methodology Matters | 409 |
| 6.2 What Penetration Testing Is, and Is Not | 584 |
| 6.3 Hats and Team Colors | 273 |
| 6.4 Knowledge Levels: Black, Grey, and Crystal Box | 284 |
| 6.5 The Phases of a Penetration Test | 561 |
| 6.6 Types of Penetration Tests | 411 |
| 6.6 Pre-Engagement: Scope and the Rules of Engagement | 520 |
| 6.7 The Legal Framework | 500 |
| 6.8 Ethics and Professional Conduct | 529 |
| 6.9 Vulnerability Disclosure | 725 |
|     Worked Example: CVE and CVSS in Practice (the Log4Shell case) | 513 |
| 6.10 The Test Environment and Toolkit | 494 |
| 6.11 Threat Modeling and Intelligence in the Engagement | 183 |
| 6.12 Post-Exploitation, Pivoting, and Operational Discipline | 470 |
| 6.13 Compliance-Driven and Standards-Based Testing | 232 |
| 6.11 Reporting | 530 |
| 6.14 Professional Certifications for Penetration Testers | 206 |
| 6.15 An End-to-End Engagement, Start to Finish | 354 |
| 6.16 Limitations, Pitfalls, and Misconceptions | 307 |
| Why This Matters | 156 |
| Chapter Summary | 221 |
| Review Questions | 388 |
|     Answer Key | 30 |
| Hands-on Labs | 218 |
| References | 151 |

### Chapter 7: Reconnaissance and Open-Source Intelligence

*6,606 markdown words (13.2 pages); 253 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 93 |
| Key Terms | 153 |
| 7.1 Why Reconnaissance Comes First | 501 |
| 7.2 Footprinting: Passive and Active | 338 |
| 7.3 Open-Source Intelligence (OSINT) | 606 |
| 7.4 Search-Engine Reconnaissance ("Google Dorking") | 416 |
| 7.5 WHOIS and the Regional Internet Registries | 455 |
| 7.6 DNS Reconnaissance | 436 |
| 7.7 Email Harvesting, Metadata, and Social-Media Profiling | 211 |
| 7.8 Reconnaissance of Cloud and Modern Infrastructure | 345 |
| 7.9 The Intelligence Cycle and Organizing Findings | 377 |
| 7.10 Reconnaissance Tools | 383 |
| 7.11 Passive Fingerprinting | 265 |
| 7.12 Defending Against Reconnaissance | 485 |
| News in Focus: Mass Scraping of Public Profiles (2021) | 388 |
| Why This Matters | 132 |
| Chapter Summary | 206 |
| Review Questions | 372 |
|     Answer Key | 30 |
| Hands-on Labs | 185 |
| References | 109 |

### Chapter 8: Scanning and Enumeration

*6,849 markdown words (13.7 pages); 816 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 152 |
| Key Terms | 161 |
| 8.1 From Reconnaissance to Active Probing | 301 |
| 8.2 The Scanning Taxonomy and the Tyranny of Time | 168 |
|     Why Scanning Time Dominates Planning | 304 |
| 8.3 A TCP/IP Refresher for Scanners | 214 |
|     The Six Nmap Port States | 280 |
| 8.4 Host Discovery and Network Sweeps | 164 |
|     What Nmap Probes by Default | 130 |
| 8.5 Network Mapping: Traceroute, Firewalking, and Nmap | 209 |
|     Firewalking, LFT, and Nmap's Smarter Traceroute | 219 |
| 8.6 Port Scanning with Nmap | 132 |
|     TCP Scan Types | 288 |
|     UDP Scanning, Timing, and Output | 355 |
| 8.7 hping3: Crafting Packets by Hand | 289 |
| 8.8 Always Sniff the Wire | 176 |
| 8.9 Operating-System Fingerprinting | 202 |
| 8.10 Service and Version Scanning, and Enumeration | 216 |
| 8.11 Vulnerability Scanning | 314 |
| 8.12 The Nmap Scripting Engine (NSE) | 160 |
| 8.13 Detection and Evasion | 309 |
| 8.14 Scanning Safely, Legally, and Within Scope | 195 |
|     Automated Discovery and Mapping Tools | 142 |
|     Scanning IPv6 | 143 |
|     The Pentester's Toolkit: Kali and BackTrack | 262 |
| Why This Matters | 125 |
| News in Focus: Internet-Scale Scanning as an Early-Warning Signal (2025-2026) | 253 |
| Review Questions (MCQ) | 310 |
|     Answer Key | 82 |
| Hands-on Labs | 315 |
| References | 163 |

### Chapter 9: Exploitation and Post-Exploitation

*5,225 markdown words (10.4 pages); 316 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 91 |
| Key Terms | 166 |
| What Exploitation Is (and Is Not) | 0 |
|     In a Penetration Test | 53 |
|     Ethical Boundaries | 64 |
| Common Vulnerability Classes | 0 |
|     Injection Vulnerabilities | 121 |
|     Memory Corruption | 161 |
|     Authentication and Session Vulnerabilities | 33 |
| From Source to Machine Code: The Compilation Pipeline | 247 |
| Memory Corruption: The Stack, the Heap, and Buffer Overflows | 344 |
|     Stack Exhaustion and Heap Problems | 249 |
| From Stack Smashing to Return-Oriented Programming | 513 |
| Programming Survival Skills for Exploitation | 302 |
| Shellcode and Shellcode Strategies | 276 |
| The Exploit-Development Workflow | 351 |
|     Inside the Metasploit Framework | 281 |
| Passive and Static Analysis: Reverse Engineering for Exploitation | 208 |
|     Privilege Escalation in Depth | 193 |
|     Post-Exploitation, Lateral Movement, and Defense Evasion | 346 |
| Metasploit Framework | 0 |
|     Structure | 51 |
|     Responsible Use | 46 |
| Privilege Escalation | 0 |
|     Linux Privilege Escalation | 142 |
|     Windows Privilege Escalation | 85 |
| Lateral Movement | 0 |
|     Pass-the-Hash | 58 |
|     Pass-the-Ticket | 60 |
| Persistence | 0 |
|     Common Persistence Mechanisms and Their Detection Signatures | 93 |
| Why This Matters | 62 |
| News in Focus | 78 |
| Review Questions (MCQ) | 285 |
| Lab Assignment | 189 |
| References | 58 |

### Chapter 10: Web Application Security

*4,376 markdown words (8.8 pages); 202 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 105 |
| Key Terms | 153 |
| How the Web Works: HTTP, Sessions, and the Same-Origin Policy | 234 |
| The OWASP Top 10 | 38 |
|     Broken Access Control | 164 |
|     The OWASP Top 10:2025 | 256 |
| Injection Attacks | 0 |
|     SQL Injection in Depth | 179 |
|     Cross-Site Scripting | 150 |
|     Cross-Site Request Forgery | 99 |
|     Server-Side Request Forgery | 65 |
| SQL Injection in Depth | 434 |
| Cross-Site Scripting (XSS) | 378 |
| Broken Access Control, CSRF, SSRF, and Other High-Impact Flaws | 224 |
| Authentication and Session Management | 0 |
|     Broken Authentication | 142 |
| Authentication, Sessions, and the Insufficient-Session-Expiration Flaw | 145 |
| Security Misconfigurations | 41 |
|     Security Headers | 64 |
| The Web-Application Testing Toolkit | 279 |
| Application Security Testing: SAST, DAST, IAST, and DevSecOps | 429 |
| Web Application Firewalls and Their Limits | 40 |
|     WAF Bypass Techniques | 76 |
| Why This Matters | 79 |
| News in Focus | 78 |
| Review Questions (MCQ) | 314 |
| Lab Assignment | 154 |
| References | 37 |

### Chapter 11: Network Defense and Hardening

*5,075 markdown words (10.2 pages); 258 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 86 |
| Key Terms | 202 |
| Firewalls | 0 |
|     Firewall Types and Evolution | 144 |
|     Writing Firewall Rules | 154 |
| Firewall Types and Topologies | 399 |
|     Physical and Virtual Firewalls | 174 |
|     Stateless and Stateful Packet Filtering | 362 |
| Network Segmentation | 0 |
|     DMZ Architecture | 89 |
|     VLAN and Micro-Segmentation | 60 |
| Zero-Trust Architecture | 0 |
|     The Zero-Trust Principle | 152 |
| DNS Security | 0 |
|     DNSSEC | 44 |
|     DNS over HTTPS and DNS over TLS | 53 |
|     DNS Sinkholing | 55 |
| VPNs and Remote Access | 0 |
|     IPsec and WireGuard | 57 |
|     Split Tunnelling and Its Risks | 64 |
| Proxies, VPNs, and Tor | 284 |
| Network Access Control and 802.1X | 49 |
|     802.1X Operation | 54 |
| DDoS and Mitigation | 0 |
|     DDoS Attack Categories | 41 |
|     DDoS Mitigation | 60 |
| Authentication, Identity, and Access | 351 |
|     Biometrics and the Reality of False Positives and Negatives | 392 |
| Network Monitoring and Visibility | 201 |
| Deception: Honeypots, Honeynets, and Honeytokens | 175 |
| Network Forensics in Defense | 154 |
| CVE Case Study: When the Firewall Is the Door (CVE-2024-3400) | 242 |
| Capstone and Group Project Ideas (Network Defense) | 265 |
| Why This Matters | 72 |
| News in Focus | 64 |
| Review Questions (MCQ) | 299 |
| Lab Assignment | 159 |
| References | 85 |

### Chapter 12: Intrusion Detection and Prevention Systems

*3,620 markdown words (7.2 pages); 377 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 97 |
| Key Terms | 152 |
| Detection System Types | 0 |
|     Network-Based IDS and IPS | 135 |
|     Host-Based IDS | 48 |
| Detection Methods | 0 |
|     Signature-Based Detection | 133 |
|     Anomaly-Based Detection | 116 |
|     Stateful Protocol Analysis | 50 |
| SIEM and Log Aggregation | 0 |
|     SIEM Architecture | 110 |
|     SIEM Challenges | 59 |
| UEBA and Threat Hunting | 0 |
|     User and Entity Behaviour Analytics | 58 |
|     Threat Hunting | 186 |
| Intrusion Detection Systems: What They Watch | 211 |
| Intrusion Prevention Systems: From Alert to Action | 238 |
| Detection Methods: Signature, Heuristic, and Anomaly | 467 |
| The Cyber Kill Chain and MITRE ATT&CK | 221 |
| SIEM, SOAR, XDR, and EDR: The Detection Stack | 269 |
| Detection Engineering, Threat Hunting, and Deception | 349 |
| Why This Matters | 85 |
| News in Focus | 69 |
| Review Questions (MCQ) | 306 |
| Lab Assignment | 183 |
| References | 59 |

### Chapter 13: Digital Forensics

*3,803 markdown words (7.6 pages); 300 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 99 |
| Key Terms | 244 |
| Forensic Principles | 0 |
|     The Locard Exchange Principle | 69 |
|     Forensic Soundness | 124 |
| Evidence Acquisition | 0 |
|     Write Blockers | 64 |
|     Forensic Imaging | 107 |
|     Hash Verification | 62 |
| File System Forensics | 0 |
|     NTFS Artefacts | 125 |
|     Deleted Files and Unallocated Space | 60 |
| Memory Forensics | 0 |
|     Why Memory Matters | 54 |
|     Acquiring Memory | 53 |
|     Analysing Memory with Volatility | 91 |
| Network Forensics | 0 |
|     PCAP Analysis | 95 |
| Anti-Forensics | 85 |
|     Countermeasures | 55 |
| Artificial Intelligence in Digital Evidence Triage | 224 |
| IoT Forensics and Explainable AI | 244 |
| AI-Driven Cybercrime Analytics and Attribution | 369 |
| The Forensic Process, Order of Volatility, and Chain of Custody | 228 |
| Disk, Memory, and Mobile Forensics in Practice | 289 |
| Legal Admissibility and Reporting | 285 |
| Why This Matters | 76 |
| News in Focus | 70 |
| Review Questions (MCQ) | 298 |
| Lab Assignment | 172 |
| References | 127 |

### Chapter 14: Incident Response

*3,556 markdown words (7.1 pages); 373 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 103 |
| Key Terms | 137 |
| Incidents Versus Events | 63 |
|     Incident Severity Classification | 96 |
| The NIST SP 800-61 Lifecycle | 13 |
|     Preparation | 119 |
|     Detection and Analysis | 160 |
|     Containment | 107 |
|     Eradication | 117 |
|     Recovery | 87 |
|     Post-Incident Activity | 110 |
| Legal and Regulatory Obligations | 0 |
|     Breach Notification Laws | 60 |
|     Law Enforcement and Evidence Preservation | 68 |
| The Assume-Breach Mindset | 133 |
| Before, During, and After: An Operational IR Playbook | 375 |
| Case Study: The Locky Ransomware Incident | 281 |
| NIST SP 800-61 Rev. 3 and the CSF 2.0 Framing | 139 |
| The CSIRT, Roles, and Communication | 152 |
| Triage, Severity, Containment, and Recovery in Depth | 288 |
| Postmortem, Metrics, and Exercises | 199 |
| Why This Matters | 75 |
| News in Focus | 88 |
| Review Questions (MCQ) | 320 |
| Lab Assignment | 176 |
| References | 72 |

### Chapter 15: Malware Analysis

*3,727 markdown words (7.5 pages); 339 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 97 |
| Key Terms | 162 |
| Malware Taxonomy | 0 |
|     Viruses and Worms | 81 |
|     Trojans and RATs | 53 |
|     Ransomware | 107 |
|     Rootkits | 65 |
|     Botnets and C2 | 75 |
| Analysis Environment Setup | 0 |
|     Safe Lab Requirements | 94 |
|     REMnux and FlareVM | 41 |
| Static Analysis | 0 |
|     File Identification | 86 |
|     PE Analysis | 93 |
|     YARA Rules | 77 |
| Dynamic Analysis | 0 |
|     Behavioural Monitoring Tools | 75 |
|     Common Malware Behaviours to Watch | 92 |
| Anti-Analysis and Evasion Techniques | 0 |
|     VM and Sandbox Detection | 64 |
|     Packers and Obfuscators | 55 |
|     Fileless Malware | 42 |
| Malware Analysis Report Structure | 130 |
| Antivirus and Antimalware Defenses | 387 |
|     The Anti-* Family: Beyond Antivirus | 326 |
| A Field Guide to Malware Types | 262 |
| The Malware Lifecycle and a Ransomware Deep Dive | 250 |
| News in Focus: WannaCry and the Worm That Used a Leaked Exploit (2017) | 286 |
| Why This Matters | 61 |
| News in Focus | 68 |
| Review Questions (MCQ) | 335 |
| Lab Assignment | 176 |
| References | 74 |

### Chapter 16: Capture the Flag and Competitive Security

*3,305 markdown words (6.6 pages); 366 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 89 |
| Key Terms | 112 |
| What Is a CTF? | 46 |
|     Jeopardy Format | 146 |
| Category Deep Dives | 0 |
|     Web Challenges | 136 |
|     Forensics Challenges | 147 |
|     Cryptography Challenges | 122 |
|     Binary Exploitation (Pwn) | 93 |
|     Reverse Engineering | 130 |
| The National Cyber League (NCL) | 81 |
|     Structure of a Season | 146 |
|     Challenge Categories | 78 |
|     Scoring and the NICE Framework | 175 |
|     How to Prepare and Compete Well | 176 |
| CTF Platforms for Learning | 84 |
| CTF Skills and Professional Mapping | 103 |
| Formats: Jeopardy, Attack-Defense, and King-of-the-Hill | 120 |
| Category Deep Dives and Tooling | 355 |
| Why CTFs Build Real Skill | 279 |
| Why This Matters | 62 |
| News in Focus | 58 |
| Review Questions (MCQ) | 312 |
| Lab Assignment | 164 |
| References | 77 |

### Chapter 17: Emerging Threats and Future Challenges

*9,993 markdown words (20.0 pages); 598 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 88 |
| Key Terms | 149 |
| 17.1 Post-Quantum Cryptography | 0 |
|     The Quantum Threat to Current Cryptography | 60 |
|     NIST PQC Standardisation | 162 |
|     Quantum Key Distribution and the Quantum Horizon | 168 |
| 17.2 AI-Enabled Attacks and Defences | 0 |
|     Offensive AI | 85 |
|     Defensive AI | 77 |
|     Privacy in LLM Chat and AI Agents | 367 |
| 17.3 Pattern Matching, Machine Learning, and Deep Learning in Security | 63 |
|     Pattern Matching: Rules and Signatures | 123 |
|     Machine Learning: Learning Patterns from Data | 189 |
|     Deep Learning: Neural Networks at Scale | 229 |
|     Adversarial Machine Learning | 398 |
| 17.8 Privacy-Preserving and Collaborative Machine Learning | 338 |
|     Case Study: A Privacy-Preserving ML Research Program (SigML, SplitML, Fairis) | 1,645 |
|     Applied Privacy and Trust Systems | 842 |
| 17.9 Anomaly Detection Across Domains | 271 |
| 17.10 Modeling, Simulation, and Control for Security | 275 |
| 17.11 Probability Distributions in Security | 319 |
| 17.4 Supply Chain Attacks | 0 |
|     Why Supply Chain Is a High-Value Target | 32 |
|     Notable Supply Chain Attack Patterns | 98 |
|     SBOM and Dependency Management | 55 |
| 17.5 Cloud Security | 0 |
|     The Shared Responsibility Model | 94 |
|     Cloud-Native Threats | 32 |
|     Control Plane and Data Plane | 159 |
|     Static and Dynamic Stability | 165 |
|     Availability and Durability Risk | 205 |
|     Cloud Compute Audit and Security | 181 |
|     VPC and Cloud Network Isolation | 264 |
|     Cloud Compute Models: VMs, Containers, Serverless, and Edge | 348 |
|     Cloud Service Scope, Resiliency, and Data Protection | 304 |
|     Reliability Properties: Availability, Resiliency, Reliability, Scalability, Elasticity, Durability | 269 |
|     Load Balancers, Hypervisors, and Content Delivery | 253 |
|     Cloud Security Services and the Cost of DDoS | 230 |
|     Event-Driven Architecture: Queues, Pub/Sub, and Event Buses | 220 |
| 17.6 Internet of Things Security | 0 |
|     The IoT Attack Surface | 47 |
|     Consequences | 58 |
| 17.7 Zero-Day Markets and Disclosure | 0 |
|     The Zero-Day Economy | 54 |
|     Responsible Disclosure and Bug Bounties | 48 |
| Why This Matters | 71 |
| News in Focus | 72 |
| Review Questions (MCQ) | 342 |
| Lab Assignment | 192 |
| References | 336 |

### Chapter 18: Privacy, Law, and Information Governance

*3,728 markdown words (7.5 pages); 387 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 101 |
| Key Terms | 170 |
| Foundational Privacy Principles | 0 |
|     The 1973 HEW Report and Fair Information Practice Principles | 91 |
|     The OECD Privacy Guidelines | 109 |
| GDPR | 0 |
|     Scope and Jurisdiction | 70 |
|     Lawful Bases for Processing | 115 |
|     Data Subject Rights | 131 |
|     GDPR Breach Notification | 57 |
| US Privacy Law | 0 |
|     HIPAA | 102 |
|     CCPA and CPRA | 60 |
|     FERPA and COPPA | 45 |
| PCI DSS | 0 |
|     Scope and Requirements | 43 |
|     Scoping and Cardholder Data Environment | 59 |
| Privacy by Design | 0 |
|     The Seven Foundational Principles | 60 |
|     Data Protection Impact Assessments | 70 |
| The Fourth Amendment and the Reasonable Expectation of Privacy | 54 |
|     The Katz Reasonable-Expectation-of-Privacy Test | 198 |
|     The Third-Party Doctrine and Its Erosion | 147 |
|     Current Issue: Geofence Warrants and Chatrie v. United States | 281 |
|     What the Chatrie Oral Argument Signaled | 592 |
| Entrapment versus Enticement in Investigations | 481 |
| Why This Matters | 50 |
| News in Focus | 76 |
| Review Questions (MCQ) | 325 |
| Lab Assignment | 203 |
| References | 6 |

### Chapter 19: Security Governance, Policy, and Culture

*3,519 markdown words (7.0 pages); 482 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 97 |
| Key Terms | 128 |
| What Security Governance Is | 48 |
|     Why Governance Matters | 50 |
| The CISO Role | 0 |
|     Strategic Responsibilities | 44 |
|     Organisational Models | 83 |
|     Reporting Lines and Independence | 62 |
| The Policy Hierarchy | 0 |
|     Policy | 92 |
|     Standard | 47 |
|     Procedure | 54 |
|     Guideline | 44 |
| Board-Level Security Reporting | 0 |
|     Communicating Risk in Business Language | 68 |
|     Key Metrics for Board Reporting | 78 |
|     Key Risk Indicators | 47 |
| Security Culture | 0 |
|     What Culture Is and Why It Matters | 89 |
|     Tone at the Top | 66 |
|     Building a Positive Security Culture | 115 |
| Common Compliance Frameworks | 121 |
| NIST Cybersecurity Framework 2.0 and the Govern Function | 268 |
| Cybersecurity Governance at the Municipal Level | 135 |
|     Benchmarking Readiness with Automated Policy Analytics | 305 |
|     Governance and Supply-Chain Gaps | 350 |
|     Compliance Reports, Certifications, and Agreements | 341 |
| Why This Matters | 63 |
| News in Focus | 67 |
| Review Questions (MCQ) | 368 |
| Lab Assignment | 190 |
| References | 74 |

### Chapter 20: Industrial Control Systems and OT Security

*2,086 markdown words (4.2 pages); 442 code words.*

| Section | Words |
|---|---:|
| Learning Objectives | 104 |
| Key Terms | 148 |
| IT Versus OT: A Fundamental Difference in Priorities | 75 |
|     Safety as the Overriding Priority | 57 |
| ICS Components | 0 |
|     Programmable Logic Controllers | 67 |
|     SCADA Systems | 53 |
|     Human-Machine Interfaces | 60 |
| The Purdue Model and Network Segmentation | 96 |
|     The Industrial DMZ | 57 |
|     Air Gaps and Their Limitations | 66 |
| OT-Specific Security Challenges | 0 |
|     Legacy Equipment and Long Lifecycles | 69 |
|     Availability Requirements | 51 |
|     Protocol Insecurity | 65 |
| ICS Malware Case Studies | 0 |
|     Stuxnet (2010) | 69 |
|     Industroyer/CRASHOVERRIDE (2016) | 44 |
|     TRITON/TRISIS (2017) | 56 |
| IEC 62443 and NIST SP 800-82 | 0 |
|     IEC 62443 | 49 |
|     NIST SP 800-82 | 41 |
| OT Defence-in-Depth | 102 |
| Why This Matters | 81 |
| News in Focus | 88 |
| Review Questions (MCQ) | 372 |
| Lab Assignment | 193 |
| References | 6 |

### Appendix A: Security Command Reference

*1,653 markdown words (3.3 pages); 0 code words.*

| Section | Words |
|---|---:|
| Network Scanning and Enumeration | 0 |
|     Nmap | 80 |
|     DNS Enumeration | 39 |
|     Web Enumeration | 37 |
| Password and Credential Tools | 54 |
| Forensics | 82 |
| Network Analysis | 49 |
| Cryptography | 72 |
| Python One-Liners | 42 |
| Security Tools Reference | 30 |
|     Metasploit Framework (exploitation -- Chapter 9) | 39 |
|     Wireshark / tshark (packet analysis -- Chapters 3, 8) | 36 |
|     hping3 (packet crafting / testing -- Chapters 3, 8) | 40 |
|     LOIC (Low Orbit Ion Cannon) (DoS demonstration -- Chapter 3) | 27 |
|     Nmap (scanning and mapping -- Chapters 7, 8) | 36 |
|     John the Ripper (password cracking -- Chapters 9, 12) | 22 |
|     Hashcat (GPU password cracking -- Chapters 9, 12) | 31 |
|     Aircrack-ng (wireless auditing -- Chapters 3, 16) | 35 |
|     Snort (intrusion detection/prevention -- Chapters 12, 17) | 50 |
|     Zeek (network security monitoring -- Chapters 12, 17) | 54 |
|     pfSense (firewall / router -- Chapters 11, 17) | 103 |
| OWASP Tools and Projects | 43 |
|     OWASP ZAP (Zed Attack Proxy) (web app testing -- Chapter 10) | 74 |
|     OWASP WebGoat (deliberately vulnerable app -- Chapters 6, 10) | 43 |
|     OWASP Juice Shop (deliberately vulnerable app -- Chapter 10) | 27 |
|     OWASP Amass (attack-surface discovery -- Chapter 7) | 33 |
|     OWASP Dependency-Check (software composition analysis -- Chapters 5, 10) | 80 |
| Reverse Engineering with Ghidra | 365 |

### Appendix B: Glossary

*2,319 markdown words (4.6 pages); 0 code words.*

| Section | Words |
|---|---:|
| Cloud and Infrastructure Terminology | 1,464 |

### Appendix C: Certification Mapping

*1,277 markdown words (2.6 pages); 0 code words.*

| Section | Words |
|---|---:|
| C.1 (ISC)2 CISSP - 8 Domains | 177 |
| C.2 CompTIA Security+ SY0-701 - 5 Domains | 129 |
| C.3 EC-Council CEH v13 - 9 Domains | 175 |
| C.4 ISACA CISA - 5 Domains | 140 |
| C.5 (ISC)2 CGRC / CAP - 7 Job Practice Areas (NIST RMF) | 167 |
| C.6 Chapter-to-Certification Coverage Matrix | 378 |

### Appendix D: ABET Outcomes and Bloom's Taxonomy Mapping

*775 markdown words (1.6 pages); 0 code words.*

| Section | Words |
|---|---:|
| ABET Student Outcomes (computing programs, Criterion 3) | 99 |
| Bloom's Revised Cognitive Taxonomy (lowest to highest order) | 93 |
| Chapter Mapping | 382 |
| Coverage Summary | 137 |

### Appendix E: Selected Works by the Author

*1,506 markdown words (3.0 pages); 0 code words.*

| Section | Words |
|---|---:|
| Cryptography and Privacy-Preserving Computation | 231 |
| Privacy-Preserving Machine Learning and Emerging Topics | 146 |
| Security Analytics, Monitoring, and Detection | 68 |
| Networking, Wireless, and Packet Analysis | 121 |
| Offensive Security, Social Engineering, and Capture the Flag | 135 |
| Software, Systems, Data, and Governance | 313 |
| Additional Notes, Talks, and Early Works (by topic) | 405 |

### Appendix F: Companion Code and Repositories

*1,169 markdown words (2.3 pages); 0 code words.*

| Section | Words |
|---|---:|
| Worked Code Examples in This Book | 375 |
| Author Repositories (github.com/devharsh) | 191 |
| Computer Tips Organization (github.com/com-puter-tips) | 182 |
| Companion Blog Tutorials (com.puter.tips) | 347 |

### Appendix H: Capstone and Group Project Ideas

*833 markdown words (1.7 pages); 0 code words.*

| Section | Words |
|---|---:|
| H.1 Deliverables and Scholarly Lifecycle | 85 |
| H.2 Track 1: Advanced Research, Innovation, and Privacy-Preserving Systems | 170 |
| H.3 Track 2: Autonomous Threats, AI Security, and Offensive Security | 77 |
| H.4 Track 3: Specialized Technical Tools and Ethical Hacking | 152 |
| H.5 Track 4: Defensive Security, Detection, and Digital Forensics | 88 |
| H.6 GitHub Submission Standards | 71 |
| H.7 Approved Preprint Servers for DOI Generation | 34 |
