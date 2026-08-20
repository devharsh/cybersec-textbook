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

| Course | Recommended Chapters | Approx. Pages |
|---|---|---|
| Introduction to IT Security | 1, 2, 3, 4, 5, 19 | 180 |
| Computer Security (survey) | 1, 4, 5, 9, 10, 11, 12, 15, 17 | 165 |
| Ethical Hacking | 1, 6, 7, 8, 9, 10, 16 | 120 |
| Software Reverse Engineering | 9, 15 (+ 3) | 32 |
| Computer and Network Security | 2, 3, 5, 11, 12, 17 | 180 |
| Advanced Network Security (Security+ aligned) | 1, 2, 3, 11, 12, 15, 19 | 180 |
| Advanced Systems Security | 5, 6, 8, 11, 12, 17 | 120 |
| Fundamentals of Cryptography | 2, 3, 11, 17 | 145 |
| Incident Response and Digital Forensics | 12, 13, 14, 15 | 45 |
| Cybersecurity and Society | 1, 4, 5, 17, 18, 19, 20 | 135 |
| Capstone or Certification Prep | All chapters | 390 (about 485 with appendices) |

The page counts are approximate and based on the PDF edition, counting only the listed chapters (not the
appendices). They are a planning aid for gauging reading load per course; the full book runs about 485 pages
including all appendices.

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

**Chapter 2 is the outlier.** At roughly 68 pages it is more than twice the length of any other chapter, so it
dominates any course that includes it. For a certification-oriented or introductory course, Sections 2.1
through 2.14 (through the TLS handshake) plus 2.16 through 2.19b (key management, the attack taxonomy, applied
systems, practical guidance, and protecting data in its three states) carry the examinable material. Section
2.15 (advanced and emerging cryptography, including homomorphic encryption and lattices) and Section 2.20
(formal security analysis and provable security) are graduate-level and can be assigned as optional reading;
Section 2.21 (post-quantum standards) repays a single lecture even in an introductory course, because the
migration deadlines are now concrete. Appendix J likewise belongs to the advanced track.

**Trim from the back of a chapter, not the middle.** Every chapter ends with a summary, a "Why This Matters"
section, one or more "News in Focus" case studies, review questions, and a lab assignment. The case studies
and labs are the most valuable material to keep when time is short, because they are what students remember;
the encyclopedic middle sections of the longer chapters are the safer cut.

The appendices map every chapter to the CISSP, Security+, CEH, CISA, and CGRC certification domains
(Appendix C) and to ABET student outcomes and Bloom's taxonomy levels (Appendix D), and they provide a
command reference, a glossary, pointers to companion publications and code, and a protocol security reference
(Appendices A, B, E, F, I).

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
