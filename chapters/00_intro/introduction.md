# Introduction

Welcome to an open educational resource that bridges the gap between rigorous theory and hands-on
practice in cybersecurity. This book is designed so that instructors can assemble a course from
self-contained chapters, and so that learners preparing for certifications such as CompTIA Security+,
Certified Ethical Hacker (CEH), and Certified Information Systems Security Professional (CISSP) can
study the relevant material directly. It is written to be read on several levels at once, accessible to a
motivated high-school or summer-camp student, rigorous enough for undergraduate and graduate courses, and
deep enough, through its "Going Deeper" sections, to interest doctoral and postdoctoral readers.

A live, continuously updated web version of this book is available at https://book.com.puter.tips/

## Course Mapping

The chapters map cleanly onto standard three-credit university courses. Instructors can
mix and match chapters to match their exact syllabus.

<!-- BEGIN generated:course-pages. scripts/gen_wordcounts.py rewrites only the Approx. Pages column, from the same word counts as Appendix G. Edit course names and chapter lists here; chapters in parentheses are optional and not counted. -->

| Course | Recommended Chapters | Approx. Pages |
|---|---|---|
| Introduction to IT Security | 1, 2, 3, 4, 5, 19 | 225 |
| Computer Security (survey) | 1, 4, 5, 9, 10, 11, 12, 15, 17 | 335 |
| Ethical Hacking | 1, 6, 7, 8, 9, 10, 16 | 160 |
| Software Reverse Engineering | 9, 15 (+ 3) | 130 |
| Computer and Network Security | 2, 3, 5, 11, 12, 17 | 250 |
| Advanced Network Security (Security+ aligned) | 1, 2, 3, 11, 12, 15, 19 | 325 |
| Advanced Systems Security | 5, 6, 8, 11, 12, 17 | 175 |
| Fundamentals of Cryptography | 2, 3, 11, 17 | 200 |
| Incident Response and Digital Forensics | 12, 13, 14, 15 | 145 |
| Cybersecurity and Society | 1, 4, 5, 17, 18, 19, 20 | 200 |
| Capstone or Certification Prep | All chapters | 625 (about 682 with appendices) |

<!-- END generated:course-pages -->

<!-- BEGIN generated:page-basis. Written by scripts/gen_wordcounts.py; edit the wording in that script. -->

The page counts are estimates at about 500 words of prose per page, the same measure Appendix G uses, and they count only the listed chapters, not the appendices. Code listings, figures, and tables are not counted, so a typeset copy will run to a different length. These figures, like Appendix G, are regenerated from the book source whenever the book is rebuilt. They are a planning aid for gauging reading load per course: on the same measure the 20 chapters come to about 625 pages, and the whole book, with its front matter and appendices, to about 682. Several courses now exceed a single term's reading if every listed chapter is covered in full, so the guidance under *Adapting the Reading Load* below on trimming the encyclopedic back sections of the longer chapters applies directly.

<!-- END generated:page-basis -->

Three of these rows correspond to a common community-college and undergraduate sequence. *Computer Security*
is the introductory survey, covering fundamentals, authentication and access control, attacks, malicious
software, software and application security, operating-system and host hardening, database security and SQL
injection, risk assessment, and cloud security. *Advanced Network Security* goes deep on cryptography,
protocols, and network defense, and is aligned to CompTIA Security+ (the full domain mapping is in
Appendix C.2). *Advanced Systems Security* is the operations-and-architecture course, covering asset,
configuration, change, and patch management, security assessment, monitoring, secure device and endpoint
management, network-based security devices, software-defined networking, clustering, and big-data access
control.

*Software Reverse Engineering* is built on Section 15.10, which develops static and dynamic analysis, x86 and
x86-64 assembly, the PE format and Windows APIs, DLL and process injection, obfuscation and deobfuscation,
anti-disassembly, anti-debugging and anti-VM techniques, packing and unpacking, and shellcode. Chapter 9
supplies the memory-corruption and exploitation foundations it assumes, and Chapter 3 supplies the
networking-attack analysis; the listed page count covers Chapters 9 and 15, with Chapter 3 added where the
network component is emphasized.

### Adapting the Reading Load

Chapters are written so that the foundational sections come first and the advanced material comes last, which
means a chapter can be truncated rather than dropped when a term runs short. Two practical consequences:

<!-- BEGIN generated:outliers. Written by scripts/gen_wordcounts.py; edit the wording in that script. -->

**Chapters 2 and 15 are the outliers.** At about 76 and 83 pages, they are roughly 1.7 and 1.8 times the length of the next-longest chapter, Chapter 9 (about 45 pages), and more than three times the median chapter (about 24 pages), so either one dominates any course that includes it.

For Chapter 2 in a certification-oriented or introductory course, Sections 2.1 through 2.14 (through the TLS handshake) plus 2.16 through 2.19b (key management, the attack taxonomy, applied systems, practical guidance, protecting data in its three states, and tamper-evident mechanisms) carry the examinable material. Sections 2.15 and 2.15a (advanced and emerging cryptography, including homomorphic encryption and lattices, and privacy-preserving constructions such as zero-knowledge proofs) and Section 2.20 (formal security analysis and provable security) are graduate-level and can be assigned as optional reading; Section 2.21 (post-quantum standards) repays a single lecture even in an introductory course, because the migration deadlines are now concrete. Appendix J likewise belongs to the advanced track.

For Chapter 15, Sections 15.1 through 15.21 (about 19 pages) carry the malware-analysis material, including the reverse-engineering overview in Section 15.10. Sections 15.22 through 15.44 (about 58 pages) go deeper, mostly into reverse engineering: disassembly, Windows internals, obfuscation, analysis tooling, and the discipline itself. The *Software Reverse Engineering* course draws on them, and other courses can assign them as optional reading.

<!-- END generated:outliers -->

**Trim from the back of a chapter, not the middle.** Every chapter ends with a summary, a "Why This Matters"
section, one or more "News in Focus" case studies, review questions, and a lab assignment. The case studies
and labs are the most valuable material to keep when time is short, because they are what students remember;
the encyclopedic middle sections of the longer chapters are the safer cut.

The appendices map the chapters to the domains of eight certifications (Appendix C): CISSP, Security+, CEH,
Certified Information Systems Auditor (CISA), Certified in Governance, Risk and Compliance (CGRC), Systems
Security Certified Practitioner (SSCP), Certified in Cybersecurity (CC), and GIAC Reverse Engineering Malware
(GREM). They also map every chapter to ABET student outcomes and Bloom's taxonomy levels (Appendix D), and they provide a
command reference, a glossary, pointers to companion publications and code, and a protocol security reference
(Appendices A, B, E, F, I). For instructors, Appendix K adds a topic-to-chapter coverage map, ready-to-adapt
lecture modules, and sample assignments and group projects, and the companion source code is bundled in the
repository's `code/` directory.

The book is also aligned to the major workforce and framework standards. Its structure and learning
objectives map to the six functions of the NIST Cybersecurity Framework (CSF) 2.0, Govern, Identify,
Protect, Detect, Respond, and Recover, which are treated directly in the governance and defense chapters.
The skills taught correspond to the work roles of the NICE Workforce Framework for Cybersecurity (NIST SP
800-181r1), so instructors can connect chapters to specific job functions. Finally, the learning
objectives and review questions are written against Bloom's taxonomy, progressing from remembering and
understanding toward applying, analyzing, and evaluating, with the full chapter-by-chapter Bloom's mapping
given in Appendix D.

## What Every Chapter Contains

Most chapters are structured around a consistent set of pedagogical features: learning objectives,
key terms with full acronym expansions, detailed prose with figures and architecture diagrams, a
*Why This Matters* section, a *News in Focus* box drawn from documented incidents, worked numerical
examples, knowledge-check questions, multiple-choice questions with answers, executable Python coding
exercises, hands-on lab assignments, in-class exercises, and references in a consistent style.

## How to Cite This Book

If you use this textbook in research, teaching, or writing, please cite it. A machine-readable
`CITATION.cff` file is included in the repository (GitHub displays a "Cite this repository" button that
generates these formats automatically). Replace the year and access date as appropriate for your edition.

The work also has a permanent Digital Object Identifier (DOI) via Zenodo:
**10.5281/zenodo.20575785** (https://doi.org/10.5281/zenodo.20575785). Please cite the DOI where possible.

**APA (7th edition):**

> Trivedi, D. (2026). *Cybersecurity: Theory, Practice, and Ethics.* Zenodo. https://doi.org/10.5281/zenodo.20575785

**IEEE:**

> D. Trivedi, *Cybersecurity: Theory, Practice, and Ethics.* Zenodo, 2026. doi: 10.5281/zenodo.20575785.

**MLA (9th edition):**

> Trivedi, Devharsh. *Cybersecurity: Theory, Practice, and Ethics.* Zenodo, 2026, doi:10.5281/zenodo.20575785.

**Chicago (author-date):**

> Trivedi, Devharsh. 2026. *Cybersecurity: Theory, Practice, and Ethics.* Zenodo. https://doi.org/10.5281/zenodo.20575785.

**BibTeX:**

```bibtex
@book{trivedi2026cybersecurity,
  author    = {Trivedi, Devharsh},
  title     = {Cybersecurity: Theory, Practice, and Ethics},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20575785},
  url       = {https://doi.org/10.5281/zenodo.20575785},
  note      = {Free, open-source textbook, CC BY 4.0}
}
```

To cite a specific chapter, add the chapter title and number, for example: Trivedi, D. (2026).
Cryptography (Chapter 2). In *Cybersecurity: Theory, Practice, and Ethics.* https://book.com.puter.tips

## Accessibility

This book is designed to be usable by everyone, including readers who rely on assistive technology, and it is
published as a live website so that it benefits from the accessibility features of the web. Specific measures
include the following.

- **Semantic structure.** Every page uses a single top-level title followed by a strict, non-skipping heading
  hierarchy, so screen readers (such as NVDA on Windows or VoiceOver on macOS and iOS) can build an accurate
  outline and let readers jump between sections. The sidebar table of contents, the search box, and the
  General Index (linked in the navigation) provide multiple ways to find content without scrolling.
- **Text alternatives for visuals.** Every figure carries descriptive alternative text, and each diagram is
  accompanied by an adjacent prose explanation in the body text, so no information is conveyed by an image
  alone. Architecture and flow diagrams are also provided as text-based diagrams that render as structured
  markup rather than flat pictures.
- **Readable, resizable text.** The site uses a responsive, reflowable layout with relative font sizes, so
  readers can zoom or change the browser font size without losing content, and it ships with a built-in light
  and dark theme. Body text is left-aligned to avoid the uneven spacing that can hinder readers with dyslexia.
- **Language and navigation.** The document declares its language (English) so screen readers use the correct
  pronunciation, links use descriptive text rather than "click here," and all navigation, search, and content
  links are reachable by keyboard alone.
- **Standards.** These choices follow the Web Content Accessibility Guidelines (WCAG), including the
  recommended minimum 4.5:1 contrast ratio for normal text.

If you encounter an accessibility barrier, please open an issue in the book's repository (linked from the
toolbar) so it can be fixed. Because the source is openly licensed (below), readers may also generate
alternative formats to suit their needs.

## License

This textbook is released under the Creative Commons Attribution 4.0 International (CC BY 4.0)
license. You are free to share and adapt the material with appropriate credit.
