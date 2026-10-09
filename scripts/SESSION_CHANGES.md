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

- Done: after the Claude GitHub App was installed, the change was pushed to main as 74de5b0 on
  2026-09-30, the Build and Deploy Jupyter Book run succeeded, and 15.44 is live. The patch files
  delivered to Downloads earlier (v1 and v2) are now redundant; do not apply them.
- The build here ran in a fresh cloud venv. The venv path recorded from earlier work,
  /Users/devharsh/Downloads/venv311/bin, no longer exists (Downloads is empty), so rebuild with your
  current local environment.

## 2026-10-05: new Section 11.26, SMB file sharing on Windows and macOS

Chapter 11 gains Section 11.26, "SMB File Sharing on Windows and macOS, and How to Secure It", after 11.25
and before the Chapter Summary. It began from a reader's note on what SMB is, how to share a folder in Windows,
and how to turn on SMB sharing in macOS. Every claim in the note was checked before anything was written, and
the section adds what the note lacked: the security settings that decide whether a share is safe.

Corrections to the source note, each now stated correctly in the section:

- SMB is not a LAN protocol. It runs over any IP network, Microsoft describes SMB 3 improvements for branch
  offices on WAN links, and SMB over QUIC carries it across the internet on UDP 443.
- TCP 445 is right for direct-hosted SMB, but the legacy NetBIOS ports (UDP 137 and 138, TCP 139) are only
  needed by SMB 1, and the note did not mention QUIC.
- The Windows steps omitted the conditions that make sharing safe: enable discovery only on the Private
  profile, keep password-protected sharing on (Microsoft's own troubleshooting page says to turn it off, with no
  warning), and remember that share and NTFS permissions both apply.
- The macOS steps were right, but left out Apple's own warning that passwords for Windows File Sharing accounts
  may be stored less securely, and that those accounts should be deselected before turning file sharing off.
- The note's numbered sources were bare domains, not pages, and could not be verified. The section cites
  primary pages instead.

What the section adds: how SMB works (ports, dialects from MS-SMB2 Appendix A, SMB 2.0.2 shipping with Windows
Vista SP1), Windows and macOS sharing steps for Windows 11 and macOS 27 Golden Gate, a measured lab table, the
attack techniques (MS17-010, CVE-2020-0796, CVE-2021-34527, ATT&CK T1135, T1021.002, T1187 with its WebDAV
fallback, T1557.001), and hardening lists for both platforms built from Microsoft's current defaults (signing,
encryption, guest logons, SMB 1, dialect floor, NTLM deprecation and the September 2026 retirement FAQ, firewall,
SMB over QUIC) and Apple's documented client and server settings (nsmb.conf protocol_vers_map, port445,
signing_required; ProtocolVersionMap on the server).

The lab table comes from a real run: Samba 4.19.5 on loopback, observed with smbstatus. At defaults an SMB 3.1.1
session was neither encrypted nor fully signed, anonymous share listing succeeded, and SMB 1 was refused;
restrict anonymous = 2, server signing = mandatory and server smb encrypt = required fixed all three, imposed
protection even on a client run with --client-protection=off, and refused an SMB 2.1 client.

Also changed: Chapter 11 learning objective 14 and key terms SMB signing and SMB over QUIC; references 27 to 52;
one-sentence cross-references in Sections 3.5 and 8.10 and in Appendix I's SMB row; regenerated word counts
(Chapter 11 about 45 pages, just under Chapter 9, and the book about 646).

Checks: check_acronyms.py 0 failures; no dead links (samba.org returns an anti-bot 403 to the checker but was read
directly); jupyter-book build succeeds with only the two older asm-lexer warnings; no em dashes, curly quotes,
prose quotation marks or non-ASCII characters in the new text.

An independent agent re-verified every claim and found eleven precision problems, all checked and fixed before
publishing: guest-logon defaults by edition, the WebDAV fallback when outbound SMB is blocked, Microsoft's
Guest or Everyone wording as an instruction, SMB 1 on Windows 10, Vista SP1, the NTLM wording, Apple's warning
placement and the Firewall Options path, lab wording, Linux's kernel SMB client and ksmbd, and reference dates
and URLs.

### Still left for you

- No Microsoft page states the Windows 11 Home guest-logon default for version 24H2 and later, so the section
  names only the editions Microsoft documents.
- Microsoft's PrintNightmare workaround page is JavaScript-only, so the section's advice stays general (share
  printers only where needed, patch).
- The macOS nsmb.conf keys come from Apple support articles and the macOS 15.2 manual page; Apple's open-source
  SMB repository is from the 2013 era and was not relied on.

## 2026-10-08: workshop coverage in Chapters 2, 3 and 16

The two-part CyberChef workshop for the CyberNinjas club (Encode, Encrypt, or Hash? and Crack the Case) now
cites the book section by section, so every concept the workshop teaches had to be in the book first. Most
already were: Sections 2.1 to 2.9, 2.13, 2.15a, 2.16, 2.17, 13.2, 13.14, 13.22, 14.2, 14.10, 14.22, 14.27,
15.24, 15.42, 16.1, 16.2, 16.10, 17.2, 17.4 and 17.12. The gaps were filled as follows.

- Section 2.1: the kitchen picture gains its third limit. Water keeps its amount, while Base64 output runs about
  a third longer than its input.
- Section 2.2: ROT13, the Caesar cipher with its shift fixed at 13, has no key, so by the two questions of
  Section 2.1 it sits with the encodings even though it is usually listed among the classical ciphers.
- Section 2.3: single-byte XOR has only 256 keys and the work is recognizing the right one; cribs, the
  known-plaintext attack, and why a crib reveals nothing beyond itself under a one-time pad.
- Section 2.5: the 2 to the 128th arithmetic (about 3.4 times 10 to the 38th keys, on the order of 10 to the
  19th years at a trillion guesses a second), why practical attacks go after the key, the implementation and the
  mode instead, and the Grover caveat that points to Section 2.15.
- Section 2.16: deleting a leaked key does not un-leak it; GitHub's revoke-or-rotate guidance, push protection
  and its limits (off by default for repositories, bypassable), and CWE-798.
- Section 3.7: reserved names from RFC 2606 and RFC 6761, why names under .invalid never resolve, and why
  .localhost and the example domains still do.
- Section 16.9: new subsection, Case Study Competitions: When the Deliverable Is a Recommendation, with the
  Cybersecurity Case Competition of ISACA's New York Metropolitan Chapter as the example.
- Section 16.10: CyberChef 11.5.0 (September 18, 2026) ships 505 operations; the project's statement that no
  recipe or input reaches its web server, and the two operations that contact outside servers by design.

Also changed: key terms ROT13, Crib, Reserved domain names and Case study competition, also added to each
chapter's static index cell; Chapter 2 references 62 to 64 (and the blank line that loosened the list removed);
Chapter 3 references 14 and 15; a new Chapter 16 reference group for Sections 16.9 and 16.10 with five entries;
regenerated word counts (Chapter 2 about 76 pages, the book about 649).

Sources were read directly: the ISACA chapter's competition overview and Past Winners pages, the Stevens
(May 31, 2023) and Baruch Zicklin (June 26, 2024) articles, GitHub Docs on removing sensitive data and on push
protection, MITRE CWE-798, RFC 2606 and RFC 6761, and CyberChef's README, CHANGELOG and Categories.json at tags
v11.3.0, v11.4.0 and v11.5.0 (501, 504 and 505 distinct operations; gchq.github.io/CyberChef serves 11.5.0).

Checks: check_acronyms.py 0 failures for Chapters 2, 3 and 16; new links return 200 except two the container
cannot test (the Baruch host fails TLS verification from the shell and was read through a fetcher, and
github.com/gchq/CyberChef is the canonical repository); jupyter-book build in a CI-mirror copy succeeds with only
the two older asm-lexer warnings; no em dashes, curly quotes, prose quotation marks or non-ASCII characters in
the new text.

An independent agent re-verified every claim and found precision problems, all checked and fixed before
publishing: the ROT13 classification wording, the Section 16.2 and 15.24 cross-references, an AES sentence that
contradicted Section 2.17, GitHub's stated reason for rotating and the limits of push protection, a claim that
reserved names can never exist, CyberChef's client-side wording, the competition's official name, an unsupported
time span, a phrase copied from the ISACA page, and the grouping of the new Chapter 16 references.

### Still left for you

- The lecture decks' bottle picture does not yet carry the third limit now stated in Section 2.1.
- CyberChef releases often; the version and operation count in Section 16.10 will need a refresh.
- The ISACA chapter's overview says Over six years (2020 to 2025 on its Past Winners page); when it updates the
  totals, Section 16.9 should follow.

## 2026-10-08: skateboard risk analogy (Section 5.7) and everyday distributions (Section 17.7)

Two additions requested in one note: a skateboard analogy for the risk treatments, and everyday examples for
the probability distributions (a fair die for uniform, student grades for normal, wealth for Poisson).

Correction to the request, made before writing: wealth across a population is not Poisson distributed. A
Poisson quantity has variance equal to its mean, so wealth with a mean of 100,000 dollars would have a standard
deviation of about 316 dollars. Wealth is heavy tailed, and its upper tail is commonly modeled with a Pareto
distribution. The section therefore uses wealth as the Pareto example and gives Poisson its own correct
examples (horse-kick deaths, failed logins per hour, phishing clicks per day, annualized rates of occurrence),
with a short paragraph explaining why wealth fails the Poisson test. Standard normal is explained as the one
bell curve with mean 0 and standard deviation 1, not a synonym for normal.

Chapter 5, Section 5.7: new subsection A Worked Analogy: The Skateboard and the Scraped Knee, after the
existing bicycle paragraph and encryption example. It states the risk in Section 5.2 terms, maps each element
to an organizational counterpart, and walks through avoidance (whole and partial; AAP advice that children
under 5 not ride), mitigation split into likelihood and impact controls (AAOS gear functions: knee and elbow
pads against scrapes, wrist guards against fractures, helmet), transfer (deductible, coinsurance, out-of-pocket
maximum, and the cyber equivalents: retention, sublimits, conditions, policy limits), acceptance (decision by
the risk owner, appetite by severity, revisit when conditions change), a combined plan table, residual risk,
and secondary risk (risk compensation, Morrongiello et al. 2007). A worked-numbers subsection with a code cell
computes the Poisson chance of at least one clinic visit, the ALE and ROSI of the gear, and the insurance split,
and notes that likelihood versus impact depends on how the loss event is defined. Six exercises with an answer
key, learning objective 9, two key terms, review questions 16 and 17, references 10 to 13, index terms, and a
pointer to Section 17.7 in the Section 5.6 admonition.

Chapter 17, Section 17.7: new subsection Four Distributions from Everyday Life (fair die and uniform, with
the chi-square fairness test, Diceware and modulo bias; student grades and the normal curve, with z-scores, the
68-95-99.7 rule, the central limit theorem and its finite-variance condition, and base-rate false alarms; Poisson
counts with the Bortkiewicz data, the law of rare events and negative binomial burstiness; wealth and the
Pareto distribution with Fed DFA 2026 Q2 shares, SCF 2022 mean and median, the 80/20 tail index, the Clauset et
al. tests, and heavy-tailed breach losses), a comparison table, a code cell, and a new four-panel figure
(assets/figures/ch17_everyday_distributions.png). The existing soliton paragraph is unchanged under a new
heading. Eight exercises with an answer key, learning objective 9, six key terms, review questions 11 and 12,
references 14 to 27, and index terms.

Also changed: one-sentence cross-references in Section 2.4 (randomness) and Section 12.2 (anomaly thresholds);
eight glossary entries in Appendix B (heavy tail, modulo bias, normal distribution, Pareto distribution, Poisson
distribution, risk compensation, uniform distribution, z-score); regenerated word counts (book about 665 pages).

Sources were read directly: AAOS OrthoInfo Skateboarding Safety; HealthCare.gov glossary (deductible,
out-of-pocket maximum, 2026 limits); NIST CSRC glossary (risk response) and NISTIR 8286 wording; ISO 31000:2018
treatment options (secondary sources, the standard is paywalled); Morrongiello et al. via PubMed and Crossref;
NIST/SEMATECH e-Handbook; EFF Diceware post and dice page; NIST SP 800-22 Rev. 1a; Python secrets docs and the
CPython randbelow source; FRED series WFRBST01134, WFRBSN09161, WFRBSN40188 and WFRBSB50215 (updated September
18, 2026); the October 2023 SCF bulletin; Pareto, Poisson and Bortkiewicz bibliographic records; Newman 2005;
Clauset et al. 2009 (arXiv full text); Edwards et al. 2016 (OUP); Maillart and Sornette 2010 (arXiv, Crossref).
The PubMed search page for a 1996 in-line skating gear study returned HTTP 429 and was not used.

Checks: every number recomputed in code; check_acronyms.py 0 failures book-wide (FRED expanded); the 18 new
links return OK or a redirect, except three publisher DOIs that refuse scripts (verified through Crossref and
publisher pages) and FRED, which timed out from the shell but was read through a fetcher; clean jupyter-book
build with only the two older asm-lexer warnings; rendered pages screenshotted; no em dashes, curly quotes,
prose quotation marks or emojis in the new text.

An independent agent reviewed all new text and found 2 errors and 17 precision problems, all verified and
fixed before publishing, including: a sample sequence that was not actually uniform; the helmet wrongly called
the only gear AAOS says to wear every time; the Clauset et al. result misstated (it rejected a power law for
its wealth data); sample means said never to settle for any tail index of 2 or less; the central limit
theorem stated without its finite-variance condition; steep hills attributed to AAOS; nonces said to require
uniformity; EFF's short lists overlooked; the Pareto share formula given without its alpha greater than 1
condition; and answer letters rotated so the new questions are not all B.

### Still left for you

- The Chapter 5 answer key leans toward B for the original questions (10 of 15).
- The DFA shares change every quarter; refresh the 2026 Q2 figures in Section 17.7 when you next revise.

Follow-up the same day: two older passages had the same overstatements the review caught in the new text, and
were fixed. Section 5.7 twice said insurance never transfers reputational harm; it now says some policies pay
costs that follow reputational damage (crisis communications, lost profits), but the loss of trust itself and,
usually, legal accountability stay with the organization. The opening of Section 17.7 and the Section 17.6
figure called the uniform distribution the ideal for nonces; they now say keys, tokens and randomly generated
nonces, and assets/figures/ch17_distributions.png was regenerated from its own code cell with the new title.

## 2026-10-09: answer keys, reference numbering, privilege rings, and the times sign

Four problems reported by the reader, each fixed wherever it occurs in the book after a full audit.

MCQs inside answer keys: only Chapter 2 had this. Questions 17 and 18 (ElGamal) sat below the Answer Key
heading with their own key line; they now sit with the other questions and the key reads 1 to 18.

Reference numbering: Chapters 2 and 17 placed the related-work-by-the-author block in the middle of the
numbered list, so the list stopped and resumed (61 to 64 in Chapter 2, 13 to 27 in Chapter 17). The block now
follows the whole list in both. Chapter 16 had one numbered item followed by three unnumbered groups; it is now
one list numbered 1 to 19 with a sentence saying which items belong to which section. Chapter 8's item 14 was a
see-also note, not a reference, and is now a note after the list. Every chapter's references now run 1 to N.

Privilege rings: Section 1.6 drew the x86 rings as four rectangles in a mermaid graph, while its own text said
concentric circles. Two new figures replace it (scripts/figures/ch01_privilege_rings.py): the x86 rings as
concentric disks with the negative rings below ring 0 (ring -1 hypervisor, ring -2 System Management Mode,
ring -3 security processor), an SGX enclave and a TDX confidential VM marked as isolation rather than rank, a
firmware TPM in the security processor and a discrete TPM as a separate chip; and the Arm exception levels as
concentric disks split into the TrustZone normal and secure worlds with EL3 at the center. The text was
rewritten to match, quotation marks around the ring names removed, two new paragraphs explain where TPMs and
TEEs fit, and references 9 to 18, three key terms, index terms and learning objective 9 were added.

Times sign: x used for multiplication now uses the multiplication sign in Chapters 1, 5, 12, 17 and 19 and in
Appendix B, in two Chapter 5 code cells (outputs rerun), and in the text drawn inside the Chapter 11
segmentation figure (regenerated). Hex values such as 0x80, the ElGamal secret key x and a shell loop
variable were left alone.

Sources read directly: Tereshkin and Wojtczuk, Black Hat USA 2009; Domas, Black Hat USA 2015; Buhren and
Eichner, Black Hat USA 2020; Intel Community, Choose the Right TPM Type (2022); Trusted Computing Group TPM
summary; Costan and Devadas, Intel SGX Explained (ePrint 2016/086); Cheng et al., Intel TDX Demystified
(arXiv 2303.15540); Arm, Learn the architecture: AArch64 Exception Model (102412, version 1.3); Arm, SMC
Calling Convention (2013); Mann, Arm Community blog (2018). Intel's own SGX and TDX pages and the Linux kernel
SGX page could not be fetched from this session and were not used.

Checks: check_acronyms.py 0 failures book-wide; new links OK or redirect except the TCG page and the Arm blog,
which refuse scripts and were read through a fetcher; clean jupyter-book build; rendered pages screenshotted;
figure colors pass the dataviz ordinal ramp checks; word counts regenerated (book about 667 pages).

### Still left for you

- Nothing from this list: the plain-text formulas it named were typeset in the next entry.

## 2026-10-09: formulas typeset as math, and money no longer read as math

The reader asked for the plain-text formulas to be typeset. A book-wide audit (powers written with a caret,
products with an asterisk, subscripts with an underscore, spelled-out Greek letters, digit-suffixed variables
such as m0, and the same inside admonitions, which earlier audits had skipped) found them in Chapters 2, 3, 15,
17 and 19 and Appendices B, F and J. All are now MyST math: the one-time pad, the two-time pad (now a display
equation), the IND-CPA game, hash properties and length extension, the Feistel round, RSA, Diffie-Hellman and
the man in the middle, ElGamal and its C++ recap, elliptic-curve point arithmetic and the ECDLP, CDH and DDH,
GF(2^8) and the abelian-group identity, the lattice and Ring-LWE notation, the noise-flooding formula and its
parameters, the Fairis weights and bound, (epsilon, delta) for differential privacy, the deterrence factor, the
corruption thresholds, and every worked example and answer in Appendix J. Chapter 15's answer key now writes the
C conditions as code, as its body text does. Diagram labels use real subscripts and superscripts (Feistel,
IND-CPA game, Chapter 17 research map, Appendix J layers), and the Chapter 17 distributions figure reads
lambda = 4 in math type (assets/figures/ch17_distributions.png regenerated from the notebook code).

Notation: the decryption-oracle notion is written IND-CPA with a superscript D, as Li and Micciancio named it,
in every chapter and appendix; the glossary adds that it is also written IND-CPA-D, which the index entries
use, and the key-recovery notion is written KR with a superscript D. Reference titles keep their published
spelling.

Money read as math: with dollar math on, two dollar signs in one paragraph became a math span, so text such as
Q9 in Chapter 1 rendered as run-together italics on the live site. Every currency amount is now escaped (Chapters
1, 5, 16 and 19, including a Chapter 5 knowledge check and the Chapter 19 budget table), the MongoDB operators in
Chapter 10 and the NTFS journal names in Chapter 13 are code, and a parse of every cell with the book's own
MyST settings, admonition bodies included, finds no accidental math left. Three times signs hidden inside those
spans or diagrams were also fixed (Chapter 1 Q9 worked, Chapter 19 answer 2, the Chapter 5 and Appendix J
diagrams).

Corrections found while checking the typeset passages against the sources: the KR-D notion is defined by Li,
Micciancio, Schultz and Sorrell (CRYPTO 2022, Appendix A), not by Li and Micciancio (2021), and the proof that
Gaussian noise flooding achieves IND-CPA-D with nearly matching bounds is also from the 2022 paper; Chapter 2
and its reference notes now say so. Reference 30 of Chapter 2 adds its venue (ACM CCS 2024), reference 31 uses
the published title (IND-CPA-D and KR-D Security With Reduced Noise from the HintLWE Problem), and reference
33 now gives the repository's own description. Appendix J Example J.3 claimed that 2 active plus 2 passive
corruptions of 10 parties is feasible, but Fitzi, Hirt and Maurer (CRYPTO 1998) give perfect security if and
only if 3 t_a + 2 t_p + t_f < n, and 6 + 4 = 10 is not below 10; the example now uses 1 active plus 3 passive
(9 < 10) against 4 active (12 > 10), and the Mixed Adversaries paragraph states the condition. Three
cross-references sent readers to Section 2.8 for the IND-CPA-D material, which lives in Section 2.3 (the
Chapter 2 notions table and two places in Chapter 17); they now point to Section 2.3.

Sources read directly: ePrint 2020/1533 (Li and Micciancio, page and paper), 2022/816 (Li, Micciancio, Schultz
and Sorrell, page and paper), 2024/127 (Cheon et al., page and paper), 2025/1618 (Ogilvie); the
ucsd-crypto/DynamicEstimationAttack repository page; Fitzi, Hirt and Maurer (1998) from the ETH Zurich
publications server.

Checks: check_acronyms.py 0 failures; all notebooks validate; MyST token scan finds no accidental math;
jupyter-book build clean apart from the two existing asm lexer notices in Chapter 15; rendered pages
screenshotted (Chapters 1, 2, 3, 5, 13, 17, 19, Appendices B and J, all changed diagrams); word counts
regenerated.

## 2026-10-09: the policy hierarchy told through Claude's abuse rule (Section 19.3)

The reader asked for policy, process and procedure to be explained with the news that Anthropic's 2026 Usage
Policy update bans sustained abuse of its models and that Claude can end abusive chats, with the policy as the
high-level rule and the procedure as the exact steps and technology Claude uses.

Section 19.3 now has a Process level between Standard and Procedure, defined from ISO 9000:2015 (a process is a
set of interrelated or interacting activities that use inputs to deliver an intended result; a procedure is a
specified way to carry out an activity or a process) and illustrated with the Chapter 14 incident response
lifecycle and its playbooks. A new worked example, When Claude Ends an Abusive Chat, sorts Anthropic's public
statements into the five levels: the one-line Usage Policy prohibition (policy, including the trap that
Anthropic files it under a heading called Universal Usage Standards), the published conditions for ending a
conversation (standard), the Safeguards loop from writing the policy through training, pre-release testing,
enforcement, feedback and revision (process), the six steps inside one conversation, ending with the
end-conversation action shown in the Claude Opus 4 system card and the app closing the thread (procedure),
and the feedback advice and scope note (guideline). It closes with a five-level table, two exercises and an
answer key. Learning objective 3, a Process key term, the opening of Section 19.15, the chapter summary, review
questions 16 and 17 (answers C and A), references 22 to 30 and index terms were updated to match.

Where the procedure describes mechanics Anthropic has not published, the text says so: the system card's test
transcript shows the action as end_conversation, and the developer documentation explains that a tool call is
returned by the model and executed by the application, so the section calls the action a tool on that basis
and states that the product wiring is not public.

Sources read directly: Anthropic, 2026 Usage Policy update (October 8, 2026); Anthropic Usage Policy effective
November 12, 2026; Anthropic, Claude Opus 4 and 4.1 can now end a rare subset of conversations (August 15,
2025); Anthropic, Building safeguards for Claude (August 12, 2025); System Card: Claude Opus 4 & Claude Sonnet 4,
Section 5.7 and Transcript 5.7.A; the published Claude Opus 5.5 system prompt (September 22, 2026); Anthropic's
tool use documentation; Brandom, TechCrunch (October 8, 2026); the NIST glossary entry reproducing ISO 9000:2015
3.4.5. The Gadgets Now article the reader linked could not be fetched from this session and is not cited.

Checks: check_acronyms.py 0 failures; the nine new reference links return 200; no accidental math in the
chapter; jupyter-book build clean; the new section, table, exercises and questions screenshotted; word counts
regenerated (book about 672 pages).
