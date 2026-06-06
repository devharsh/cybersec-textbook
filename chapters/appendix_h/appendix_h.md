# Appendix H: Capstone and Group Project Ideas

This appendix collects team-project ideas suitable for a semester-long capstone or final group project in any
cybersecurity course or self-study program. The ideas are organized into research tracks and each is mapped to
the chapters that develop the underlying material, so a team can study, build, and critically evaluate a real
cybersecurity tool or controlled exploit, and reflect on its societal, ethical, legal, and policy implications.
Teams may pick an idea as written or use it as a starting point for an original, instructor-approved topic.

```{note}
Taken together, the tracks below provide at least one project idea mapped to every chapter of the book
(Chapters 1 through 20), so a team can find a capstone aligned with any part of the curriculum.
```

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

- **AI-powered offensive cybersecurity agent** for Capture-the-Flag competitions (an autonomous agent that
  solves CTF challenges and resists prompt injection and code obfuscation). (Ch. 16, Ch. 17)
- **Hybrid privacy-preserving analytics** combining Fully Homomorphic Encryption and Secure Multi-Party
  Computation (for example collaborative fraud detection across institutions). (Ch. 2, Ch. 17)
- **Fully Homomorphic Encryption in distributed tax or audit systems** (privacy-enhanced civic analytics).
  (Ch. 2, Ch. 17)
- **Split-learning architectures** for on-device privacy protection. (Ch. 17)
- **Deepfake detection using polynomial approximation** of facial micro-expressions (an error-detection
  framing). (Ch. 2, Ch. 17)
- **Comparative evaluation of post-quantum cryptography** schemes (lattice-, hash-, and isogeny-based) for
  enterprise migration. (Ch. 2, Ch. 17)
- **Automated malware attribution** using large-language-model embeddings and graph neural networks. (Ch. 15,
  Ch. 17)
- **Adaptive deep-learning systems for real-time fraud detection.** (Ch. 17)
- **Dynamic risk management for third-party and supply-chain vulnerabilities.** (Ch. 5, Ch. 17)
- **Zero-Trust Architecture migration and enterprise design proposal.** (Ch. 11)

## H.3 Track 2: Autonomous Threats, AI Security, and Offensive Security

These map to Chapters 4, 6, 9, and 12.

- **Agentic AI for offensive Capture-the-Flag challenges.** (Ch. 16, Ch. 17)
- **Automated deepfake-detection logic using nonlinear modeling.** (Ch. 17)
- **Modern phishing simulation and human-risk analysis**: a multi-stage spear-phishing campaign using OSINT
  reconnaissance, controlled spoofed landing pages, and phish-rate analytics. (Ch. 4, Ch. 7)
- **Adversary emulation and detection engineering** using MITRE ATT&CK: emulate a known threat and build the
  detections for it. (Ch. 9, Ch. 12)

## H.4 Track 3: Specialized Technical Tools and Ethical Hacking

These map to Chapters 3, 8, 9, 10, 16, and 17.

- **Simplified mobile API vulnerability scanner** for Broken Access Control and IDOR (modify object
  identifiers across API endpoints through an intercepting proxy). (Ch. 10)
- **Mobile application vulnerability analysis** using Frida or mitmproxy. (Ch. 16)
- **Automated web-application fuzzer** (boundary-value, mutation, and generation fuzzing; boofuzz, Atheris).
  (Ch. 10)
- **Network protocol analyzer and packet sniffer** (Scapy, libpcap). (Ch. 3, Ch. 8, Ch. 11)
- **Wi-Fi security auditing tool** for authorized hardware only. (Ch. 16)
- **Hardware security analysis of embedded systems** using firmware extraction. (Ch. 1, Ch. 20)
- **Ethical exploit-development proof of concept** using a controlled stack-based buffer overflow. (Ch. 9)
- **Exploit-development framework** for controlled environments. (Ch. 9)
- **Cloud security misconfiguration auditing** with Infrastructure-as-Code ("shift-left") scanning. (Ch. 17)
- **Container security scanner** for Docker images. (Ch. 17)
- **Cloud security posture assessment tool** across major providers. (Ch. 17)

## H.5 Track 4: Defensive Security, Detection, and Digital Forensics

These map to Chapters 11, 12, 13, and 14.

- **Lightweight SIEM**: ingest logs and flow records, correlate events, and raise alerts. (Ch. 12)
- **Network detection and visibility tool**: build flow analysis or anomaly detection over captured traffic.
  (Ch. 11, Ch. 12)
- **Digital Forensics and Incident Response (DFIR) playbook** for a ransomware (or business-email-compromise)
  scenario, including a tabletop exercise. (Ch. 13, Ch. 14)
- **AI-assisted digital-evidence triage** prototype with explainable outputs. (Ch. 13)
- **Honeypot or deception toolkit** that captures and characterizes attacker interactions. (Ch. 11)

## H.6 Track 5: Penetration Testing, Governance, Privacy, and Society

These map to Chapters 6, 18, and 19, the methodology, legal, and governance dimensions of security.

- **Full-scope penetration test with rules of engagement and a professional report**: plan and execute an
  authorized assessment end to end (scoping, recon, scanning, exploitation, reporting), producing a
  client-grade report with CVSS-rated findings and remediation. (Ch. 6, Ch. 8, Ch. 9, Ch. 10)
- **Coordinated vulnerability-disclosure and computer-crime-law analysis**: design a responsible-disclosure
  policy and analyze the legal boundaries (authorization, CFAA/DMCA) that govern security testing. (Ch. 6,
  Ch. 18)
- **Privacy-compliance assistant**: a tool that checks a data-handling workflow or privacy policy against GDPR
  and CCPA/CPRA requirements (data-subject rights, breach-notification clocks) and flags gaps. (Ch. 18)
- **Data-subject-access-request (DSAR) / breach-notification workflow tool**: automate the intake, tracking,
  and deadline management of privacy requests and breach reporting. (Ch. 18)
- **GRC and security-policy maturity assessment**: map an organization's controls and policies to NIST CSF 2.0
  or ISO/IEC 27001 and produce a maturity-tier scorecard with prioritized recommendations. (Ch. 19)
- **Societal and ethical impact analysis of a security technology**: a scholarly evaluation of a chosen
  technology's effects on privacy, trust, equity, and policy (the cybersecurity-and-society perspective).
  (Ch. 18, Ch. 19)

## H.7 GitHub Submission Standards

A professional repository should contain: a `/src` directory with modular, commented source code and proper
error handling; a `/docs` directory with the report, user manual, and DOI link; a `/tests` directory with unit
and integration tests and sample logs; a `README` with setup instructions, usage examples, and ethical
considerations; a dependencies/`requirements` file; and a `.gitignore` excluding build artifacts and sensitive
data. Use version control with meaningful commits from every team member.

## H.8 Approved Preprint Servers for DOI Generation

To obtain a citable DOI for the preprint deliverable, teams may use, for example: **Zenodo**
(https://zenodo.org), **Preprints.org** (https://www.preprints.org), **ResearchGate**
(https://www.researchgate.net), **arXiv** (https://arxiv.org), and **TechRxiv** (https://www.techrxiv.org).
Always confirm a server's scope and licensing before submitting.
