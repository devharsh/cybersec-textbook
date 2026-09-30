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

## 2026-09-27: reading-load figures in the Introduction follow Appendix G

The Introduction said Chapter 2 ran about 68 pages and was nearly twice the length of the next-longest
chapters, while Appendix G reported 74.1 pages for it and 73.3 for Chapter 15. The Introduction's page
figures were typed by hand against an older edition and had drifted; the course table understated
every course by 10 to 70 pages, and the stated book length was about 570 pages against 628.

- `scripts/gen_wordcounts.py` now also writes the Introduction's Approx. Pages column, the page-basis
  paragraph and the outliers paragraph, between `generated:` markers, from the same word counts and
  the same 500 words per page as Appendix G. It settles the Introduction before writing Appendix G,
  because the Introduction is itself counted. Course names and chapter lists stay editable in the
  Introduction; chapters in parentheses are optional and not counted.
- The outliers paragraph now names Chapters 2 and 15 and gives trimming guidance for both. The
  script warns if the two longest chapters ever stop being 2 and 15.
- The Appendix C sentence listed CGRC twice and omitted SSCP, CC and GREM; it now lists the eight
  certifications Appendix C maps.

## 2026-09-30: new Section 15.44, Launching versus Attaching

Chapter 15 gains Section 15.44, "Launching Versus Attaching: How a Debugger Takes Control," inserted
after 15.43 and before the Chapter Summary. It started from a reader's uploaded note that compared
launching a debugger with attaching to a process; the note was expanded into a full section and every
claim in it was checked against primary sources before anything was written.

Two claims in the source note were wrong or too loose and are corrected in the section:

- The note implied Ctrl+Alt+P is the Attach-to-Process shortcut in both Visual Studio and the
  JetBrains IDEs. It is Visual Studio only. IntelliJ IDEA uses Ctrl+Alt+F5 in its default Windows
  keymap, Ctrl+Alt+5 in its Linux keymaps and Option+Shift+F5 on macOS (read from the keymap files
  in the intellij-community repository); Rider adds Ctrl+Alt+Shift+F5 to reattach. The section
  states this and Exercise 7 makes students correct it.
- The note said disconnecting the debugger leaves the app running safely, stated unconditionally. On
  Windows the default is the opposite: DebugSetProcessKillOnExit's KillOnExit parameter defaults to
  TRUE, and DebugActiveProcess's own documentation says exiting the debugger also exits the target
  unless that default is cleared. The section explains that IDEs and WinDbg (qd, .detach) opt out of
  the kill-on-exit default, and that q closes the target.

What the section adds beyond the note: the operating-system mechanism and permission check behind each
path. Linux ptrace (PTRACE_TRACEME for launch, PTRACE_ATTACH/PTRACE_SEIZE for attach), the
one-tracer-per-thread rule, GDB's attach-stops / detach-continues / exit-detaches / run-kills behavior,
Yama ptrace_scope 0 to 3 and CAP_SYS_PTRACE; Windows DebugActiveProcess, SeDebugPrivilege, Session 0
and w3wp.exe, and the WinDbg -p/-pn/-pv/-o options; macOS task ports, the com.apple.security.cs.debugger
entitlement, get-task-allow and SIP; the cooperative attach of language runtimes (JDWP suspend and
binding, the Node.js inspector, Python debugpy); and a security section covering the startup gap for
packed samples, detach safety for live analysis, anti-debugging (MITRE ATT&CK T1622), and the debugger
interface itself as an attack surface (unauthenticated JDWP and exposed Node inspectors as
remote-code-execution exposures).

Every command transcript in the section (launch, attach, detach, quit-while-attached, the self-trace
anti-debugging check, cross-user attach, lldb wait-for-launch, JDWP suspend and interface binding, the
Node inspector) was reproduced in a Linux lab (GDB 15.1, LLDB 18.1.3, OpenJDK 21, Node 22) rather than
recalled. YouTube links from the source note were not reachable to verify and are not used; the section
cites primary documentation instead (GDB manual, ptrace(2), Yama, Microsoft Learn, JetBrains, Node.js,
Oracle JPDA, Apple, MITRE, Wiz).

Other files touched, all mechanical:

- references.bib is not used by Chapter 15; the chapter keeps its own numbered list, which gains
  entries 44 to 69 for the primary sources above.
- Appendix B gains a JDWP glossary entry.
- Chapter 9 (Section 9.28) and Section 15.35 gain one-sentence cross-references to 15.44.
- gen_wordcounts.py was re-run, so the Introduction and Appendix G now read Chapter 15 at about 83
  pages and the book at about 637, and the Introduction's deep-material range reads 15.22 through 15.44
  (about 58 pages).

Checks: check_acronyms.py passes with 0 failures; check_links.py finds no dead links among the new
references (GitHub and a few others return anti-bot 403s, as before); jupyter-book build succeeds with
only the two pre-existing asm-lexer warnings in older Chapter 15 cells, none from the new section.

An independent agent that had not seen the drafting re-verified every claim against primary sources and
found no factual errors; its two minor precision notes (the per-thread nature of the tracer limit, and
the JDWP example binding) were folded in.

### Second pass, same day

The note was sent again, and the section was re-reviewed and extended where the first pass was thin.
Every new claim was checked against primary documentation and, where possible, in the lab:

- 15.44.1 now says that both modes give the same core tools once connected; that a launched program
  inherits the debugger's permissions (a sample detonated from an elevated debugger runs elevated);
  that code optimized before an attach can hide local variables; that building is a separate step
  (the VS Code preLaunchTask) except where the debugger builds the program itself (Go's Delve); the
  Start Debugging keys (F5 in Visual Studio and VS Code, Shift+F9 for Debug in IntelliJ IDEA); and that
  PIDs are reused (pid_max). The table gains a While connected row, a corrected Gate on use row
  (Yama 2 and 3 can refuse even launch-mode tracing) and a clearer On disconnect row, and a new
  paragraph covers GDB's all-stop mode and the cost of pausing a live service.
- New 15.44.6, Remote hosts and containers: gdbserver launch and attach, Visual Studio's msvsmon.exe,
  and the gdbserver no-security warning. A lab run found that `gdbserver 127.0.0.1:2345` still listens
  on every interface (the manual says the host part is ignored), so the section recommends a firewall
  or the manual's stdio-over-ssh route, which opens no port. For containers: Docker's default seccomp
  profile and CAP_SYS_PTRACE, the VS Code dev container guidance, and `kubectl debug --target`, with
  the general profile's SYS_PTRACE grant to the ephemeral container and the baseline Pod Security
  Standard that forbids it. The former 15.44.6 is now 15.44.7.
- Exercise 9 and its answer, and references 57 to 69.
- References 45 and 62 now credit the Linux man-pages project, maintained by Alejandro Colomar since
  2020 (release 5.09 onward), with the man7.org HTML rendering by Michael Kerrisk. Reference 37,
  which predates this work, still names Kerrisk as editor without a version. That is accurate for
  pages up to 5.13, so it is left for you to decide.
- A second independent review of the changed passages found no errors in the core claims. Its
  precision corrections were each verified before being applied.

### Still left for you

- The push could not be made from this environment (no GitHub credentials here). The change is
  committed locally; apply the delivered patch on your Mac and push with scripts/sync.sh.
- The build here ran in a fresh cloud venv. The venv path recorded from earlier work,
  /Users/devharsh/Downloads/venv311/bin, no longer exists (Downloads is empty), so rebuild with your
  current local environment.
