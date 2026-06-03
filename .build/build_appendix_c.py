import sys; sys.path.insert(0,".build")
from nbbuild import md, write_nb

intro = r"""# Appendix C: Certification Mapping

This appendix demonstrates how the twenty chapters of this textbook cover the official
examination domains of five widely held security certifications: **(ISC)2 CISSP**,
**CompTIA Security+ (SY0-701)**, **EC-Council CEH v13**, **ISACA CISA**, and
**(ISC)2 CGRC** (formerly CAP, aligned to the NIST Risk Management Framework).

Domain titles and weightings below reflect the published exam outlines current as of
2024-2026. Always confirm against the certifying body's latest outline before sitting an
exam, because vendors revise objectives periodically. The mapping is intended to help an
instructor or self-study learner locate the chapters that develop each domain in depth.

A chapter listed in **bold** is the primary home of that domain; lighter listings indicate
supporting coverage.
"""

cissp = r"""## C.1 (ISC)2 CISSP - 8 Domains

| # | CISSP Domain (weight) | Primary chapters | Supporting |
|---|---|---|---|
| 1 | Security and Risk Management (15%) | **5, 19** | 1, 18 |
| 2 | Asset Security (10%) | **5, 18** | 2, 19 |
| 3 | Security Architecture and Engineering (13%) | **2, 11** | 1, 9, 17 |
| 4 | Communication and Network Security (13%) | **3, 11** | 12, 17 |
| 5 | Identity and Access Management (13%) | **11** | 5, 19 |
| 6 | Security Assessment and Testing (12%) | **6, 8** | 7, 9, 10 |
| 7 | Security Operations (13%) | **12, 13, 14** | 11, 15 |
| 8 | Software Development Security (11%) | **10** | 9, 17 |

Cryptographic solutions and cryptanalytic attacks (Domain 3) are developed fully in
Chapter 2, including the advanced primitives (homomorphic, post-quantum, functional
encryption) in Chapters 2 and 17. Site and facility security (Domain 3) appears in
Chapter 11. Investigations and digital forensics (Domains 1 and 7) are in Chapter 13.
"""

secplus = r"""## C.2 CompTIA Security+ SY0-701 - 5 Domains

| # | Security+ Domain | Primary chapters | Supporting |
|---|---|---|---|
| 1.0 | General Security Concepts | **1, 2** | 11, 19 |
| 2.0 | Threats, Vulnerabilities and Mitigations | **4, 9, 15** | 7, 8, 10 |
| 3.0 | Security Architecture | **3, 11** | 2, 17 |
| 4.0 | Security Operations | **12, 13, 14** | 11, 6, 8 |
| 5.0 | Security Program Management and Oversight | **5, 19** | 18 |

The CIA triad and control types (Domain 1.0) are introduced in Chapter 1 and applied
throughout. Cryptographic solutions (Domain 1.0) are in Chapter 2. Zero trust, IoT, OT,
and cloud content updated in SY0-701 appears in Chapters 11, 17, and 20.
"""

ceh = r"""## C.3 EC-Council CEH v13 - 9 Domains

| # | CEH Domain (weight) | Primary chapters | Supporting |
|---|---|---|---|
| 1 | Information Security and Ethical Hacking Overview (6%) | **1, 6** | 5 |
| 2 | Reconnaissance Techniques (17%) | **7, 8** | 6 |
| 3 | System Hacking Phases and Attack Techniques (15%) | **9, 15** | 8 |
| 4 | Network and Perimeter Hacking (24%) | **3, 9, 12** | 11 |
| 5 | Web Application Hacking (14%) | **10** | 9 |
| 6 | Wireless Network Hacking (5%) | **3** | 9, 11 |
| 7 | Mobile, IoT and OT Hacking (10%) | **17, 20** | 9 |
| 8 | Cloud Computing (5%) | **17** | 11 |
| 9 | Cryptography (5%) | **2** | 17 |

The five ethical-hacking phases (recon, scanning, gaining access, maintaining access,
covering tracks) are developed across Chapters 6 through 9. Sniffing, session hijacking,
and DoS (Domain 4) are in Chapters 3 and 9. IDS/firewall/honeypot evasion (Domain 4) is
in Chapters 9 and 12.
"""

cisa = r"""## C.4 ISACA CISA - 5 Domains

| # | CISA Domain (2024 weight) | Primary chapters | Supporting |
|---|---|---|---|
| 1 | Information Systems Auditing Process (18%) | **19** | 5, 6 |
| 2 | Governance and Management of IT (18%) | **19** | 5, 18 |
| 3 | IS Acquisition, Development and Implementation (12%) | **10, 19** | 9, 17 |
| 4 | IS Operations and Business Resilience (26%) | **14** | 11, 12, 13 |
| 5 | Protection of Information Assets (25-26%) | **2, 18** | 11, 13 |

Audit standards and frameworks (COBIT) and internal-controls evaluation (Domain 1) are in
Chapter 19. Business continuity and disaster recovery (Domains 2 and 4) are in Chapters 5
and 14. Encryption and DLP (Domain 5) are in Chapters 2 and 11; privacy and security laws
(Domain 5) are in Chapter 18.
"""

cgrc = r"""## C.5 (ISC)2 CGRC / CAP - 7 Job Practice Areas (NIST RMF)

| # | CGRC Practice Area (weight) | RMF step | Primary chapters | Supporting |
|---|---|---|---|---|
| 1 | Information Security Risk Management Program (16%) | Prepare | **5, 19** | 18 |
| 2 | Scope of the Information System (11%) | Categorize | **5** | 19 |
| 3 | Selection and Approval of Security/Privacy Controls (15%) | Select | **19** | 5, 18 |
| 4 | Implementation of Security/Privacy Controls (16%) | Implement | **11, 19** | 2, 12 |
| 5 | Assessment/Audit of Security/Privacy Controls (16%) | Assess | **6, 19** | 8, 10 |
| 6 | Authorization/Approval of Information System (10%) | Authorize | **19** | 5 |
| 7 | Continuous Monitoring (16%) | Monitor | **12, 14, 19** | 13 |

The full NIST RMF lifecycle (Prepare, Categorize, Select, Implement, Assess, Authorize,
Monitor) is presented as an integrated workflow in Chapter 19, with risk inputs from
Chapter 5 and operational monitoring from Chapters 12 and 14.
"""

coverage = r"""## C.6 Chapter-to-Certification Coverage Matrix

The matrix confirms every chapter contributes to at least one certification and every
certification domain is covered by at least one chapter.

| Ch | Title | CISSP | Sec+ | CEH | CISA | CGRC |
|----|-------|:---:|:---:|:---:|:---:|:---:|
| 1  | Introduction | D1,D3 | 1.0 | D1 | - | - |
| 2  | Cryptography | D3 | 1.0,3.0 | D9 | D5 | P4 |
| 3  | Networking | D4 | 3.0 | D4,D6 | - | - |
| 4  | Social Engineering | D1 | 2.0 | D4 | - | - |
| 5  | Risk Management | D1,D2 | 5.0 | D1 | D1,D2 | P1,P2,P6 |
| 6  | Pentest Methodology | D6 | 4.0 | D1 | D1 | P5 |
| 7  | Reconnaissance | D6 | 2.0 | D2 | - | - |
| 8  | Scanning | D6 | 2.0,4.0 | D2,D3 | - | P5 |
| 9  | Exploitation | D6,D8 | 2.0 | D3,D4,D5 | D3 | - |
| 10 | Web Security | D8 | 2.0 | D5 | D3 | P5 |
| 11 | Network Defense | D3,D4,D5 | 3.0,4.0 | D4 | D4,D5 | P4 |
| 12 | IDS/IPS | D7 | 4.0 | D4 | D4 | P7 |
| 13 | Forensics | D7 | 4.0 | D3 | D4,D5 | P7 |
| 14 | Incident Response | D7 | 4.0 | - | D4 | P7 |
| 15 | Malware | D7 | 2.0 | D3 | - | - |
| 16 | CTF | D6 | 2.0 | D2-D5 | - | - |
| 17 | Emerging Topics | D3 | 3.0 | D7,D8,D9 | D3 | - |
| 18 | Privacy and Law | D1,D2 | 5.0 | - | D1,D2,D5 | P1,P3 |
| 19 | Governance and Compliance | D1 | 5.0 | - | D1,D2,D3 | P1,P3,P5,P6,P7 |
| 20 | ICS/OT Security | D4 | 3.0 | D7 | - | - |

All eight CISSP domains, all five Security+ domains, all nine CEH domains, all five CISA
domains, and all seven CGRC practice areas are covered across the twenty chapters.
"""

cells = [md(intro), md(cissp), md(secplus), md(ceh), md(cisa), md(cgrc), md(coverage)]
write_nb("chapters/appendix_c/appendix_c.ipynb", cells)
