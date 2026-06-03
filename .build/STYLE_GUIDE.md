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
  ```{admonition} Camp Note (beginner intuition)
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
