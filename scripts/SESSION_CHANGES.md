# What changed in this pass, and what is left for you to judge

Three commits: `15caa79` (sidebar), `fa546d9` (two new sections), `51d3dbd` (expansion,
acronyms, facts and links). The first two are pushed and live. The third is committed
and waiting.

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

## Left for you to judge

**Unverifiable claims, left in place and flagged rather than guessed at.** Ch15's "fifteen
exam objectives" for GREM and its continuing-education figure (giac.org renders those with
JavaScript). Ch2's "first Turing Award for work tied to quantum physics" (the award is
confirmed, the superlative is not). Ch16's claim that Binary Ninja Free is limited to x86,
x86-64 and ARMv7. Ch5's Neiman Marcus breach figures. The ISO 31000 edition year, left
undated because iso.org blocks automated access.

**OWASP LLM Top 10.** Ch17 reproduces the 2025 list. A 2026 edition was published on
3 August 2026, but its item names are not available in machine-readable form, so the section
now says which edition it reproduces rather than silently aging.

**exploit-db.com is returning 502 site-wide**, so the GHDB link in Ch7 is down because the
site is down, not because the path moved. Worth a recheck.

**Redundant blocks in Ch20.** Three unnumbered sub-blocks from an earlier automated merge now
restate material the new sections cover properly. Removing them would cut about 500 rendered
words. Cell 11 contains nothing but an HTML comment marker.

**Ch19 section 19.2** still says best practice recommends the CISO not report to the CIO, as
though settled. New section 19.20 says plainly that no public dataset establishes a causal
link. The two read as contradicting each other until one is softened.

**Ch11 has no figures at all.** The two worth adding are an 802.1Q tag layout in the style of
`ch20_modbus_frame.png` and a zone diagram for 11.23.

**Appendix G is generated.** `scripts/gen_wordcounts.py` rebuilds it from the other chapters'
headings and re-stamps the date in `intro.md`. Anyone who edits a heading must re-run it.

## Scripts added

- `scripts/check_acronyms.py` plus `scripts/acronyms.json`, so the book checks standalone
- `scripts/check_links.py`, which distinguishes dead links from anti-bot 403s
- `scripts/add_session_sections.py`, which computes and asserts every number in 15.43 and 9.38
- `scripts/_edit_helper.py`, the notebook-safe substitution helper. Delete if unwanted.
