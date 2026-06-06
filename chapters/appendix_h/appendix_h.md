# Appendix H: Capstone and Group Project Ideas

This appendix collects team-project ideas suitable for a semester-long capstone or final group project, drawn
from the author's Bowie State University courses (COSC 435 Computer and Network Security, COSC 489 Ethical
Hacking, and the COSC 442 Cybersecurity and Society perspective) and a Spring 2026 research-projects catalog.
Projects are mapped to the chapters that develop the underlying material so a team can study, build, and
critically evaluate a real cybersecurity tool or controlled exploit.

```{admonition} Ethical mandate (read first)
:class: warning
All technical work must be conducted **ethically and only within controlled, authorized environments**.
Offensive techniques (exploitation, phishing simulation, Wi-Fi auditing, fuzzing) must target only systems you
own or have explicit written permission to test, in line with the legal and professional-responsibility
material of Chapters 6 and 18. Build deliberately vulnerable labs (DVWA, WebGoat, Metasploitable) or use your
own infrastructure; never test third parties.
```

## H.1 Deliverables and Scholarly Lifecycle

A rigorous capstone mirrors a real research-and-development lifecycle over roughly sixteen weeks: topic
selection, proposal, literature review, methodological design, implementation, evaluation, and dissemination.
Typical required deliverables include:

- a professional scholarly **manuscript** (for example 20+ pages, single-spaced, with a similarity score below
  20 percent);
- a formal **preprint** with a Digital Object Identifier (DOI);
- a **live technical demonstration** of a working proof of concept (for example in Kali Linux);
- a public **GitHub repository** showing professional software-engineering practice and contributions from all
  team members.

## H.2 Track 1: Advanced Research, Innovation, and Privacy-Preserving Systems

These map to Chapters 2 and 17 (cryptography, privacy-preserving machine learning, emerging topics).

- **AI-powered offensive cybersecurity agent** for Capture-the-Flag competitions (autonomous agent that solves
  CTF challenges and resists prompt injection and code obfuscation). (Ch. 16, Ch. 17)
- **Hybrid privacy-preserving analytics** combining Fully Homomorphic Encryption and Secure Multi-Party
  Computation (for example collaborative fraud detection across institutions). (Ch. 2, Ch. 17)
- **Fully Homomorphic Encryption in distributed tax or audit systems** (privacy-enhanced civic analytics).
  (Ch. 2, Ch. 17)
- **Split-learning architectures** for on-device privacy protection. (Ch. 17)
- **Deepfake detection using polynomial approximation** of facial micro-expressions (error-detection framing).
  (Ch. 2, Ch. 17)
- **Comparative evaluation of post-quantum cryptography** schemes (lattice-, hash-, isogeny-based) for
  enterprise migration. (Ch. 2, Ch. 17)
- **Automated malware attribution** using large-language-model embeddings and graph neural networks. (Ch. 15,
  Ch. 17)
- **Adaptive deep-learning systems for real-time fraud detection.** (Ch. 17)
- **Dynamic risk management for third-party and supply-chain vulnerabilities.** (Ch. 5, Ch. 17)
- **Zero-Trust Architecture migration and enterprise design.** (Ch. 11)

## H.3 Track 2: Autonomous Threats, AI Security, and Offensive Security

These map to Chapters 4, 6, 9, and 17.

- **Agentic AI for offensive Capture-the-Flag challenges.** (Ch. 16, Ch. 17)
- **Automated deepfake-detection logic using nonlinear modeling.** (Ch. 17)
- **Modern phishing simulation and human-risk analysis** (multi-stage spear-phishing campaign with phish-rate
  analytics). (Ch. 4)
- **Adversary emulation and detection engineering using MITRE ATT&CK.** (Ch. 9, Ch. 12)

## H.4 Track 3: Specialized Technical Tools and Ethical Hacking

These map to Chapters 3, 8, 9, 10, 16, and 17.

- **Simplified mobile API vulnerability scanner** for Broken Access Control and IDOR. (Ch. 10)
- **Mobile application vulnerability analysis** using Frida or mitmproxy. (Ch. 16)
- **Automated web-application fuzzer** (mutation/generation fuzzing; boofuzz, Atheris). (Ch. 10)
- **Network protocol analyzer and packet sniffer** (Scapy/libpcap). (Ch. 3, Ch. 8, Ch. 11)
- **Wi-Fi security auditing tool** for authorized hardware only. (Ch. 16)
- **Hardware security analysis of embedded systems** using firmware extraction. (Ch. 1, Ch. 20)
- **Ethical exploit development proof of concept** using buffer overflows. (Ch. 9)
- **Exploit-development framework** for controlled environments. (Ch. 9)
- **Cloud security auditing** using Infrastructure-as-Code scanners. (Ch. 17)
- **Container security scanner** for Docker images. (Ch. 17)
- **Lightweight SIEM development.** (Ch. 12)
- **Digital Forensics and Incident Response (DFIR) playbook** for ransomware scenarios. (Ch. 13, Ch. 14)

## H.5 COSC 435 Computer and Network Security: Eight Group Projects

1. **Modern Phishing Simulation and Human Risk Analysis** — a multi-stage (spear-phishing) campaign: OSINT
   reconnaissance (theHarvester, Maltego), controlled execution with spoofed landing pages (GoPhish,
   KingPhisher), and phish-rate analysis. (Ch. 4, Ch. 7)
2. **Simplified Mobile API Vulnerability Scanner** — automate Broken Access Control / IDOR testing by
   modifying object identifiers across API endpoints through an intercepting proxy. (Ch. 10)
3. **Hardware Security Analysis for Embedded Systems** — firmware extraction and analysis from an embedded
   device. (Ch. 1, Ch. 20)
4. **Exploit Development: Ethical Proof-of-Concept** — a controlled stack-based buffer-overflow PoC. (Ch. 9)
5. **Cloud Security Misconfiguration Auditing with IaC** — "shift-left" Infrastructure-as-Code scanning for
   insecure cloud configurations. (Ch. 17)
6. **Adversary Emulation and Detection Engineering** — emulate a known threat (MITRE ATT&CK) and build the
   detections for it. (Ch. 9, Ch. 12)
7. **Zero-Trust Architecture Design Proposal** — a reference ZTA design assuming no implicit trust. (Ch. 11)
8. **Digital Forensics and Incident Response (DFIR) Playbook** — a procedure-driven playbook for a specific
   incident class (for example ransomware). (Ch. 13, Ch. 14)

## H.6 COSC 489 Ethical Hacking: Ten Project Topics

1. **Automated Web Application Fuzzer** (boundary-value, mutation, and generation fuzzing). (Ch. 10)
2. **Network Protocol Analyzer and Sniffer** (Scapy, libpcap, SharpPcap). (Ch. 3, Ch. 8)
3. **Wi-Fi Security Auditing Tool** (authorized hardware only). (Ch. 16)
4. **SIEM Lite** — log ingestion, correlation, and alerting. (Ch. 12)
5. **Exploit Development Framework (simplified).** (Ch. 9)
6. **Mobile Application Vulnerability Scanner (API-focused).** (Ch. 10, Ch. 16)
7. **Phishing Campaign Simulation Tool.** (Ch. 4)
8. **Container Security Scanner.** (Ch. 17)
9. **Hardware Security Analysis Tool (embedded systems).** (Ch. 1, Ch. 20)
10. **Cloud Security Posture Assessment Tool (AWS/Azure/GCP).** (Ch. 17)

## H.7 GitHub Submission Standards

A professional repository should contain: a `/src` directory with modular, commented source code and proper
error handling; a `/docs` directory with the report, user manual, and DOI link; a `/tests` directory with unit
and integration tests and sample logs; a `README` with setup instructions, usage examples, and ethical
considerations; a dependencies/`requirements` file; and a `.gitignore` excluding build artifacts and sensitive
data. Use version control with meaningful commits from every member.

## H.8 Approved Preprint Servers for DOI Generation

To obtain a citable DOI for the preprint deliverable, teams may use, for example: **Zenodo**
(https://zenodo.org), **Preprints.org** (https://www.preprints.org), **ResearchGate**
(https://www.researchgate.net), **arXiv** (https://arxiv.org), and **TechRxiv** (https://www.techrxiv.org).
Always confirm a server's scope and licensing before submitting.
