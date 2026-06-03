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
| 01 | Introduction | 7500 | 7399 | [x] DONE |
| 02 | Cryptography | 12500 | 3512 | [ ] |
| 03 | Networking | 10000 | 1839 | [ ] |
| 04 | Social Engineering | 7500 | 2126 | [ ] |
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
