# Chapter Style Guide (apply to every chapter)

Goal: each chapter must serve high-school summer-camp learners through postdocs. Achieve this with
explicit LAYERED depth, not by dumbing down or by being obscure.

## Layered pedagogy (every chapter)
1. Plain-language on-ramp: open each major section with an intuition/analogy a motivated high-schooler
   can follow. No jargon before it is defined.
2. Rigorous core (bachelor/master): precise definitions, formulas (MyST $...$ / $$...$$), worked
   numerical examples, and runnable Python in code cells.
3. Advanced/research depth (doctoral/postdoc): a clearly marked "Going Deeper" admonition per chapter
   with formal definitions, security proofs/reductions where relevant, threat-model nuance, open
   problems, and pointers to primary literature (papers, RFCs, NIST SPs).

Use MyST admonitions to signal level, e.g.:
  ```{admonition} Going Deeper (graduate/research)
  :class: tip
  ...advanced content...
  ```
  ```{note}
  :class: note
  ...analogy...
  ```

## Required structure per chapter (.ipynb cells)
- Title + epigraph quote
- Learning Objectives (Bloom verbs), Key Terms (acronyms expanded on first use)
- Numbered sections N.1, N.2 ... with subsections; detailed PROSE (no bullet-only sections)
- >=2 matplotlib figures (saved as chNN_*.png) AND >=1 Mermaid diagram
- >=1 worked numerical example with output
- "Why This Matters"
- "News in Focus" (documented, real incidents only; hedge with "per public reporting"; NO fabricated
  facts, dates, CVEs, attributions)
- Review Questions (>=12 MCQ) + Answer Key with worked solutions
- Hands-on Labs (3-4, ranging beginner to advanced/research)
- References (real, verifiable: NIST SPs, RFCs, OWASP, primary papers, the 3 source books)

## Word targets (markdown words; figures/code are extra)
25pg=12,500w: ch02,05,09,10,19 | 20pg=10,000w: ch03,06,13,14,18 | 15pg=7,500w: rest

## Integrity rules (user + global CLAUDE.md)
- No em-dashes, no decorative quotes, no emojis in book content.
- Do NOT invent papers, conferences, awards, funding, CVE numbers, dates, or attributions. If unsure,
  describe generically or omit. Verify against fetched sources.
- Reuse attached lab notebooks in Ch02 (randomness, modes, RSA, integrity, cryptanalysis) and the CTF
  RTFs in Ch16.

## Advanced topics to weave in (user request)
homomorphic encryption, post-quantum crypto, functional encryption, steganography, AI/LLM security,
hardware security, CPU rings, TEEs (SGX/TrustZone/SEV), sandboxes, return-oriented programming,
oblivious computation (ORAM/OT/MPC). Placement recorded in source_books.md.

## Build/save discipline
- Build via .build/ python scripts using nbbuild.py (emits cell ids). Save after each chapter.
- After each chapter: run `python3 .build/wc.py` and update PROGRESS.md table.
- git commit may fail (sandbox lock on .git); files persist on disk regardless. Retry commit by
  removing stale locks; if it fails, disk save is the source of truth.

## Transitions (REQUIRED, user request)
- Every section and subsection must OPEN with a one to three sentence bridge that explains why we move
  here from the previous topic. No abrupt topic jumps (e.g., do not jump from 1.6 Rings to 1.7 NIST CSF
  without a connecting sentence).
- Each chapter ENDS with a forward-looking sentence/paragraph pointing to the next chapter, and the next
  chapter OPENS by referencing where we just were.
- Bridges should be motivational ("having established X, we now need Y because...") not mechanical.

## Accuracy correction (user)
- The book is NOT peer-reviewed. Never describe it as peer-reviewed or refereed. Use "free,
  open-source" / "open educational resource" instead.

## Course-deck integration + added requirements (user, session 4)
Source: 20 COSC 489 decks in .build/course_decks.txt, mapped in .build/deck_chapter_map.md. Fold the
mapped deck content into each chapter as it is built. Per chapter, additionally include:
- FULL FORMS + DEFINITIONS: expand every acronym on first use and define key terms inline (the decks
  list many; carry them over). Keep the Key Terms block AND define inline.
- KNOWLEDGE CHECK: short "Knowledge Check" callout(s) mid-chapter (2-4 quick Q+A) in addition to the
  end-of-chapter MCQ bank.
- IN-CLASS EXERCISE: at least one "In-Class Exercise" callout (hands-on, doable in a class session),
  separate from the longer end-of-chapter Labs.
- CURRENT NEWS: a dated, real, verified recent incident/development (use WebSearch to verify; cite
  source; hedge as "per reporting"). NEVER fabricate incidents, CVEs, dates, or attributions.
- IMAGES/ARCHITECTURE DIAGRAMS: matplotlib figures for data + Mermaid for architecture/flow (OSI stack,
  TCP handshake, kill chain, network topology, etc.).
- FULL SENTENCES + transitions throughout (no telegraphic slide-style fragments).
- VERIFY all facts; do not hallucinate.
