# Build Progress: Cybersecurity Textbook Expansion

Targets: 10 ch @ 15pg (7,500w) | 5 ch @ 20pg (10,000w) | 5 ch @ 25pg (12,500w)
Page basis: ~500 words/page (markdown words only; code/figures additional).

## Page-tier assignment (confirmed with user)
- 25pg / 12,500w: 02 Cryptography, 05 Risk, 09 Exploitation, 10 Web Security, 19 Governance
- 20pg / 10,000w: 03 Networking, 06 Pentest Methodology, 13 Forensics, 14 Incident Response, 18 Privacy & Law
- 15pg / 7,500w: 01, 04, 07, 08, 11, 12, 15, 16, 17, 20

## Illustrations: matplotlib (data/charts) + Mermaid (flow/architecture)

## Status legend: [ ] todo  [~] in progress  [x] done (meets target)

| Ch | Title | Target words | Current | Status |
|----|-------|-------------|---------|--------|
| 01 | Introduction | 7500 | 7783 | [x] DONE (+transitions) |
| 02 | Cryptography | 12500 | 11976 md +1219 code | [x] DONE |
| 03 | Networking | 10000 | 9418 md +223 code | [x] DONE |
| 04 | Social Engineering | 7500 | 7297 md +203 code | [x] DONE |
| 05 | Risk Management | 12500 | 2218 | [ ] |
| 06 | Pentest Methodology | 10000 | 1909 | [ ] |
| 07 | Reconnaissance | 7500 | 1922 | [ ] |
| 08 | Scanning | 7500 | 1821 | [ ] |
| 09 | Exploitation | 12500 | 1957 | [ ] |
| 10 | Web Security | 12500 | 2019 | [ ] |
| 11 | Network Defense | 7500 | 1984 | [ ] |
| 12 | IDS/IPS | 7500 | 1832 | [ ] |
| 13 | Forensics | 10000 | 2033 | [ ] |
| 14 | Incident Response | 10000 | 1994 | [ ] |
| 15 | Malware | 7500 | 2196 | [ ] |
| 16 | CTF | 7500 | 1839 | [ ] |
| 17 | Emerging Topics | 7500 | 1936 | [ ] |
| 18 | Privacy & Law | 10000 | 2085 | [ ] |
| 19 | Governance & Compliance | 12500 | 2164 | [ ] |
| 20 | ICS/OT Security | 7500 | 2210 | [ ] |
| C  | Appendix C: Cert Mapping | n/a | 1323 | [x] DONE |

## Resume notes
- Notebooks built via .build/nbbuild.py helper (append/replace cells).
- After each chapter: run word count, update this table, git add+commit.

## Session 1 log (2026-06-02)
- Infra, Mermaid, research (cert_domains.md, source_books.md), STYLE_GUIDE.md done.
- Appendix C complete with full coverage matrix.
- Ch01 fully expanded to 7,399 md words + 2 figures + 2 mermaid + worked example + 12 MCQ + 4 labs.
- LAYERED pedagogy now required (high-school to postdoc): see STYLE_GUIDE.md. Apply to ch02-20 and retrofit ch01 'Going Deeper' box next pass.
- NEXT: Ch02 Cryptography (12,500w) using attached notebooks + Nakov + Boneh-Shoup.

## Session 2 log (2026-06-02)
- CITATION.cff added (v1.1.0).
- Ch02 Cryptography complete: 11,976 md words + 1,219 code (~25 pg). Covers classical/modern crypto, randomness, AES/modes, hashing, MAC/AEAD, KDF/passwords, RSA/DH/ECC, signatures/PKI, TLS, key management, attack taxonomy, applied systems, practical guidance, advanced (HE/FE/MPC/ORAM/ZKP/stego/PQC). Reused attached lab notebooks' concepts.
- Transitions added to Ch01 (incl. 1.6->1.7 fix) and Ch02 per user request; rule added to STYLE_GUIDE.
- Appendix C: added SY0-701 weights, numbering 1-5.
- Appendix titles fixed in _toc.yml: A=Security Command Reference, B=Glossary (match notebook content).
- NEXT: Ch03 Networking (10,000w).

## Session 3 log (2026-06-02)
- Logo: assets/hacker-logo.jpg (from user) embedded centered at top of intro.md (landing = intro.html).
- PPTX coverage mapped (.build/pptx_coverage.md): all crypto topics already in Ch02; networking/DoS/SYN-flood/IDS/Snort/tools queued for Ch03, Ch08, Ch12, Ch06 builds.
- Added MD5 (Wang/Yu 2004-2005) collision specifics to Ch02 per deck.
- Preface fixed: removed "peer-reviewed" claim.

## Session 4 log (2026-06-02)
- Extracted all 20 COSC 489 decks -> .build/course_decks.txt; mapped in .build/deck_chapter_map.md.
- Ch03 Networking DONE: ~9,418 md words + 3 figures + 2 mermaid. OSI/TCP-IP, addressing, ports/protocols, TCP handshake/headers, ARP/DHCP/DNS, sniffing, spoofing/MITM/session hijacking, DoS/DDoS (verified Cloudflare 2025 news), secure protocols, wireless, NAC. Folded decks 4 + 13 + 101 DoS content. Knowledge checks + in-class exercise + current news included.
- Global fixes: disabled JB auto-numbering (_toc numbered:false) so manual section numbers render cleanly; Appendix C numbering -> CISSP D1-D8, Security+ 1.0-5.0, CEH D1-D9, CISA D1-D5, CGRC P1-P7; 'Camp Note' -> plain Note.
- NEXT: Ch04 Social Engineering (deck 18) 7,500w.

## Session 5 log (2026-06-02)
- Ch04 Social Engineering DONE (~7,297 md). Folded deck 18. Psychology (Cialdini+biases), lifecycle, full attack taxonomy (phishing family + pretexting/baiting/tailgating/etc + watering hole/BEC/scareware), vectors+OSINT, identifying phishing (+code checker), physical security (locks/bypass/facility/mantrap/environmental/MTBF-MTTR-SLA), auth factors (FAR/FRR/CER), defenses (awareness/policies/help-desk/SPF-DKIM-DMARC/FIDO2), AI-enabled SE. Current news: Scattered Spider 2025 + Arup deepfake (verified). News in Focus: Twitter 2020. Knowledge checks + in-class exercise included.
- NEXT: Ch05 Risk Management (12,500w).
