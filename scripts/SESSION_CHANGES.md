# What changed in this pass, and what is left for you to judge

Five commits: `15caa79` (sidebar), `fa546d9` (two new sections), `51d3dbd` (expansion,
acronyms, facts and links), `398789e` (this file) and `cbe53c8` (the overview, five factual
corrections and the Ch11 figures). The first four are pushed and live. `cbe53c8` is committed
and waiting on you, since this sandbox holds no GitHub credentials.

## The sidebar toggle was two bugs, not one

`sphinx-book-theme.js` binds its handler with `document.querySelector(".primary-toggle")`,
which takes the first match. This build renders two elements with that class: the pydata
navbar icon, hidden above 992px, and the button a desktop reader actually sees. The handler
landed on the invisible one.

Even with the handler attached, the theme's own hide rule never applied: the element matches
`.bd-sidebar-primary.pst-sidebar-hidden`, its media query matches, and computed visibility
stays `visible`.

`_static/sidebar-toggle-fix.js` and `.css` bind to every toggle and hide with their own class.
The hide uses `display: none`, not `width: 0`, because the sidebar's parent is a flex
container and the sidebar sizes from `flex-basis: 20%`. Verified on the deployed site: the
article's left edge moves from 822px to 540px and back.

Both files are safe to leave if the upstream bug is fixed. The theme registers its
capture-phase listener first and calls `stopImmediatePropagation`, so on any element it has
already claimed, its handler runs and ours never fires.

## Four factual corrections

Each was found by checking a claim, not by reading the prose.

| Where | Was | Is |
|---|---|---|
| Ch18 | the Supreme Court "has not yet issued a decision" in Chatrie | decided 29 June 2026; a geofence warrant for Location History is a Fourth Amendment search |
| Ch20 | 230,000 customers attributed to Industroyer, 2016 | that is the December 2015 attack, carried out by operators at a keyboard |
| Ch20 | the Oldsmar intrusion stated as fact | the FBI later said it could not confirm it; now the chapter's attribution lesson |
| Ch19 | SEC enforcement "established" duties for CISOs and boards | SolarWinds was dismissed with prejudice at the SEC's own request, 20 Nov 2025 |

Smaller ones: Log4Shell's affected range ended at 2.14.1 and 2.15.0 is the fix; TLS 1.3 is
now RFC 9846; SP 800-88 is at Revision 2; Cutter is built on Rizin, not radare2; and
`IAST (Interactive AST)` in Ch10 was residue from an earlier mechanical pass.

## Two rendering bugs on the published site

Ch11 had two MyST `{admonition}` fences that opened and never closed. An unclosed fence
swallows the content after it, so material was silently missing from the live page.

## A bug in the deck scanner, found by applying it to the book

The acronym matcher let an acronym match **itself**. `loose_match` anchors the last letter
inside the run's last word, so a run that merely contains the acronym satisfied it. On the
block cipher modes line `ECB CBC CFB OFB CTR GCM CCM`, CCM was reported as expanded by the
run `CBC CFB OFB CTR GCM`. CCM on that slide is the exact term the original complaint named,
and it was passing silently.

The guard is ported back to `LAGCC/_audit/depth/check_acronyms.py`. Re-running the corrected
matcher over the 82 decks surfaced 50 more silent passes, now cleared. **The 871 figure
reported earlier was an undercount.**

## The eleven open items, resolved

Everything in the previous version of this section is now closed. What the checking found:

- **GREM.** Correct as written. giac.org lists exactly 15 objectives, and 36 CPEs over four
  years. No edit.
- **Ch2 Turing Award.** ACM's own press release makes no first claim, so the superlative is
  out and the citation now follows ACM's wording.
- **Binary Ninja Free.** Was stale. The comparison table gives five decompilation
  architectures: x86, x86-64, ARMv7, Thumb2 and ARMv8.
- **Neiman Marcus.** 350,000 cards, not 370,000, per the Seventh Circuit opinion in *Remijas*.
  The settlement was up to 1.6 million dollars, not a payment of it. The 4.6 million customer
  count and the Mandiant attribution are **removed**: no primary source carries either.
- **ISO 31000.** 2018 is current, confirmed from the ANSI catalog record. Ch5 now dates it.
- **OWASP LLM Top 10.** The 2026 PDF was obtained. Ch17 carries the 2026 list, including
  LLM08 Hidden Context Exposure, which replaces 2025's System Prompt Leakage.
- **exploit-db.com.** Still 502 site-wide. The link stays, with a pointer to the GitLab
  repository that does resolve and carries the same `ghdb.xml`.
- **Ch20 redundant blocks.** Removed, 525 words net, after moving the unique material into
  the numbered sections: the Chapter 12 cross-reference, the Knowledge Check, Stuxnet's
  zero-days and the Colonial Pipeline cross-reference.
- **Ch19 19.2.** Softened. It now presents the recommendation as resting on the
  conflict-of-interest argument rather than on outcome evidence, and points to 19.20.
- **Ch11 figures.** Two added, generated by committed scripts: an 802.1Q tag layout and a
  zone diagram for 11.23, both at 200 dpi.
- **FIPS 206.** Checked, not stale. No FIPS 206 entry exists on csrc.nist.gov, so Ch17's
  statement that FN-DSA is still under development is accurate.

## What the checking turned up that nobody had flagged

**Burp Suite was taught as an open-source tool.** It is proprietary: Professional lists at
499 US dollars, and the Community edition is free of charge but not open source. Ch10 section
10.9 now draws the distinction and names ZAP as the one the labs use.

**ZAP has not been an OWASP project since August 2023.** It moved to the Software Security
Project and is maintained today as ZAP by Checkmarx, still open source under Apache 2.0. The
book called it OWASP ZAP in eight places. zaproxy.org runs a page specifically telling people
to stop.

**ISO 27001 appeared bare in ten places**, with no edition and in several cases no ISO/IEC
prefix. Now ISO/IEC 27001, with 2022 given at first use in each chapter.

**A third bug in the acronym checker.** An acronym could match a fragment of a hyphenated
proper name, so FN in the NIST standard FN-DSA was asked to expand as false negative. The
guard is hyphens only: a slash pairs two terms that each stand alone, and suppressing IDS
inside IDS/IPS dropped it from the glossary's defined set and broke two appendices.

**Appendix G is generated.** `scripts/gen_wordcounts.py` rebuilds it from the other chapters'
headings and re-stamps the date in `intro.md`. Anyone who edits a heading must re-run it.

## Still left for you

**Ch20 cell 10** ends with an unnumbered five-bullet term recap after a horizontal rule, which
duplicates the Key Terms cell and looks like the same merge residue as the three blocks that
were removed. It was outside the named scope, so it stays until you say otherwise.

**Ch20's Purdue levels.** One removed block referred in passing to Levels 4-5, the chapter's
only mention of a Level 5, and it conflicts with the chapter's own table, which defines
Levels 0 to 4 plus 3.5. Adding a table row would have meant inventing model content.

**Three tool licenses are stated only as open source**, not by name: Metasploit Framework,
WebGoat and ZAP. GitHub's license detector reports NOASSERTION for the first two.

## Scripts added

- `scripts/check_acronyms.py` plus `scripts/acronyms.json`, so the book checks standalone
- `scripts/check_links.py`, which distinguishes dead links from anti-bot 403s
- `scripts/add_session_sections.py`, which computes and asserts every number in 15.43 and 9.38
- `scripts/_edit_helper.py`, the notebook-safe substitution helper. Delete if unwanted.
- `scripts/figures/ch11_8021q_tag.py` and `ch11_segmentation_zones.py`, the two Ch11 figures
