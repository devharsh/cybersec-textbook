# -*- coding: utf-8 -*-
"""Find acronyms a chapter uses without ever saying what they stand for.

The rule this enforces is a reader's rule, not a book's rule: a student who opens one chapter, and
has only that chapter in front of them, must be able to decode every acronym in it. So an acronym
passes if either

  * the chapter expands it at its first use, in the form `cross-site scripting (XSS)` or
    `XSS (cross-site scripting)`, or
  * Appendix B, the glossary, defines it.

Expanding it in chapter 9 does not help a reader who starts at chapter 15, which is why the check is
per chapter and why "expanded, but only after first use" is reported as its own, milder finding.

WHAT IS NOT AN ACRONYM
----------------------
Most of the work here is not matching, it is refusing to match. `acronyms.json` carries a
human-reviewed `literal` list of about 405 tokens that look like acronyms and are not: MITRE
technique IDs, OWASP category IDs, CPU registers and flags, hex byte values, PE signatures, file
extensions, exam codes, and terms that collide inside this corpus so badly that no automatic pass
can be trusted with them (ANSI is a standards body in one place and a Windows character encoding in
another; CFR is the Code of Federal Regulations in a compliance chapter and the name of a Java
decompiler in a reverse-engineering one). Nothing on that list is ever reported.

On top of the list, this scanner masks out the places where an acronym-shaped token is a piece of
machinery rather than a word: fenced and inline code, HTML tags and comments, URLs and link targets,
math, CVE and CWE and MITRE identifiers, and CVSS vector strings. A CVSS vector is the sharpest of
these. `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` reads as eight unexpanded acronyms and is in fact one
indivisible string that an exercise asks students to interpret; editing inside it destroys the
exercise.

Run:
    python3 scripts/check_acronyms.py                 # report
    python3 scripts/check_acronyms.py --json out.json # machine-readable
    python3 scripts/check_acronyms.py --unknown       # tokens in neither table, for adjudication
    python3 scripts/check_acronyms.py --chapter 10    # one chapter

The matching logic (initialisms, joining words, plurals, mixed case, and the acronyms that are not
derivable from their letters at all) is carried over from the lecture-deck scanner at
_audit/depth/check_acronyms.py so that the book and the decks are held to one standard.
"""
import argparse
import collections
import json
import os
import re
import sys
import unicodedata

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CHAPTERS = os.path.join(ROOT, "chapters")
GLOSSARY = os.path.join(CHAPTERS, "appendix_b", "appendix_b.ipynb")

# The table is authoritative and human-reviewed. A copy lives beside this script so the book checks
# out and runs on its own; the deck tree is the upstream and wins if both are present.
TABLE_PATHS = [
    os.path.expanduser("~/Documents/Teaching/LAGCC/_audit/depth/acronyms.json"),
    os.path.join(HERE, "acronyms.json"),
]


# ---------------------------------------------------------------------------- acronym recognition

ALLCAPS = re.compile(r"\b([A-Z][A-Z0-9]{1,5})\b")
# Mixed-case acronyms are a whole class of term, not an edge case: SoD, IoT, DoS, DDoS, QoS, IPsec,
# mTLS, PaaS, SaaS, NoSQL. A token counts if it is short and carries more than one capital, which
# admits IPsec at five characters with two and excludes ordinary Titlecase words and long product
# names such as PowerShell and VirusTotal.
MIXED = re.compile(r"\b([A-Za-z][A-Za-z0-9]{1,7})\b")


def is_mixed_acronym(tok):
    caps = sum(c.isupper() for c in tok)
    if caps < 2 or tok.isupper() or tok.islower():
        return False
    return (len(tok) <= 6 and caps >= 2) or (len(tok) <= 8 and caps >= 3)


def is_acronym_shaped(tok):
    """True if the token looks like an acronym in its own right, all-caps or mixed.

    Used to tell a hyphenated proper name apart from an acronym glued to an ordinary word:
    the DSA in FN-DSA is acronym-shaped, the injection in SQL-injection is not.
    """
    core = tok.strip("'").rstrip("s") if tok[-1:] == "s" else tok.strip("'")
    if len(core) < 2:
        return False
    return (core.isupper() and any(c.isalpha() for c in core)) or is_mixed_acronym(core)


def singular(tok):
    """The singular of a plural acronym, or the token unchanged.

    ACLs, APIs, VLANs and TGTs are not separate terms from ACL, API, VLAN and TGT. Only a trailing
    lower-case s after a capital counts, so SaaS and DDoS are untouched.
    """
    if len(tok) > 2 and tok.endswith("s") and tok[-2].isupper():
        return tok[:-1]
    return tok


VERSIONED = re.compile(r"^([A-Za-z]{2,6})v\d+$")


def debase(tok):
    """ICMPv6 is ICMP, SNMPv1 is SNMP, CHAPv2 is CHAP. A version suffix is not a new acronym.

    Only the explicit `vN` form is stripped. A bare trailing digit is left alone, because FIDO2,
    PBKDF2, CCA1 and SHA256 are not versions of FIDO, PBKDF, CCA and SHA.
    """
    m = VERSIONED.match(tok)
    return m.group(1) if m else tok


def acronyms_in(text):
    out = list(ALLCAPS.findall(text))
    out += [t for t in MIXED.findall(text) if is_mixed_acronym(t)]
    return [debase(t) for t in out]


SKIP_WORDS = {"of", "the", "and", "with", "for", "in", "on", "to", "a", "an", "by", "at"}

# Assumed known at this level, or not really acronyms. Carried over unchanged from the deck scanner.
ALLOW = {
    "AES", "TLS", "SSL", "HTTP", "HTTPS", "SSH", "FTP", "DNS", "IP", "TCP", "UDP", "URL", "URI",
    "USB", "CPU", "GPU", "RAM", "ROM", "OS", "PDF", "HTML", "XML", "JSON", "CSV", "SQL", "API",
    "IT", "US", "EU", "UK", "PC", "VM", "VPN", "LAN", "WAN", "WIFI", "MAC", "COSC", "AM", "PM",
    "NIST", "ISO", "IEC", "IEEE", "RFC", "CVE", "CWE", "OWASP", "MITRE", "CISA", "FBI", "GDPR",
    "HIPAA", "PCI", "DSS", "SP", "FIPS", "ID", "OK", "NO", "IV", "XOR", "AND", "OR", "NOT",
    "I", "II", "III", "IV", "V", "VI", "Q", "A", "B", "C", "D", "E", "F", "G", "H", "K", "N",
    "RSA", "ECC", "SHA", "MD5", "HMAC", "PKI", "CA", "DES", "RC4", "CIA", "DAD", "AAA", "MFA",
    "TBD", "FAQ", "CEO", "CTO", "CISO", "HR", "QA", "DBA", "SLA", "RTO", "RPO",
    "ATT", "CK", "EC",
    "EB", "FF", "CD", "AB", "BE", "DE", "AD", "BC", "DA", "EF",
    "SY0", "CC", "MCQ",
    "HHS", "DHS", "NSA", "GAO", "FTC", "SEC",
    "AWS", "GCP", "IETF", "IANA", "ICANN", "W3C", "ACM", "USENIX",
    # Book-specific chrome and structure, confirmed by reading the surrounding text:
    "CH", "TOC", "ISBN", "DOI", "BY", "SA", "NC", "ND",         # licence and citation labels
    "AV", "AC", "PR", "UI", "S", "U", "H", "L", "M",            # CVSS vector metric letters
}
# Exercise and question numbers. The deck scanner stopped at Q9 because decks never have more than
# nine questions on a slide; the book's exercise sections run past twenty, and Q10 was the single
# most widely reported "acronym" in the first run, in nineteen chapters.
ALLOW |= {f"Q{i}" for i in range(1, 41)}
ALLOW |= {f"L{i}" for i in range(1, 21)}        # learning-objective labels
ALLOW |= {f"E{i}" for i in range(1, 21)}        # exercise labels
# OWASP Top 10 for LLM Applications category identifiers, the same class of token as A01 to A10.
ALLOW |= {f"LLM{i:02d}" for i in range(1, 11)}

# Tokens this book uses that the deck corpus never did, each read in context before being listed.
# The reason is kept next to the token because a bare list of exclusions rots: the next person needs
# to know whether a term is here because it is not an acronym, because it is a product name, or
# because it means two different things in two different chapters.
BOOK_LITERAL = {
    "DNA": "the molecule, in DNA computing; not an acronym at this level",
    "RIP": "collides: the x86-64 instruction pointer register in Ch. 9, 15, 16; "
           "Routing Information Protocol in Appendix I, where it is already expanded",
    "XP": "collides: Windows XP, and the vendor name XP Cyber; a product name either way",
    "SEAL": "Microsoft SEAL, a library name; the owner does not publish an expansion",
    "HElib": "a library name",
    "HEAAN": "a library name",
    "PALISADE": "a library name",
    "VMware": "a company name",
    "NVMe": "a registered trademark of NVM Express, Inc.; the mark is the name",
    "BACnet": "an ASHRAE standard name, not an initialism of its own words",
    "YARA": "recursive and deliberately unexpanded by its author",
    "SANS": "the SANS Institute; the letters no longer stand for the original phrase",
    "GIAC": "a credential body name, expanded in Appendix C where credentials are listed",
    "STOC": "a conference name in a bibliography entry",
    "PODC": "a conference name in a bibliography entry",
    "TCC": "a conference name in a bibliography entry",
    "PKC": "a conference name in a bibliography entry",
    "LNCS": "a book-series name in a bibliography entry",
    "CCS": "a conference name in a bibliography entry",
    "BFV": "a scheme named for its authors (Brakerski, Fan, Vercauteren); not an initialism",
    "BGV": "a scheme named for its authors (Brakerski, Gentry, Vaikuntanathan)",
    "CKKS": "a scheme named for its authors (Cheon, Kim, Kim, Song)",
    "TFHE": "a library and scheme name",
    "CTXT": "a shorthand for ciphertext used inside notation, not an acronym",
    "PTXT": "a shorthand for plaintext used inside notation, not an acronym",
    "sID": "selective-identity, a notation subscript in a security-game name",
    "vCCA": "a security-notion name built on CCA, defined where it is used",
    "GOD": "guaranteed output delivery, a notation label in a protocol-property table",
    "iOS": "a product name",
    "WPA": "part of the WPA/WPA2/WPA3 family named in full in Appendix I",
    "WPA2": "part of the WPA/WPA2/WPA3 family named in full in Appendix I",
    "WPA3": "part of the WPA/WPA2/WPA3 family named in full in Appendix I",
    "FTPS": "a protocol name given in full in Appendix I",
    "SplitML": "the name of a published system, from its own paper's title",
    "SigML": "the name of a published system, from its own paper's title",
    "ApateDNS": "a tool name",
    "ASCII": "assumed known at this level, like AES and HTTP",
    "NICE": "expanded where it is taught, in Ch. 16; elsewhere it is the framework's proper name",
    # x86-64 registers, flags and instructions, read in the disassembly sections of Ch. 9 and 15.
    "RAX": "x86-64 register", "RBX": "x86-64 register", "RCX": "x86-64 register",
    "RDX": "x86-64 register", "RSI": "x86-64 register", "RDI": "x86-64 register",
    "RBP": "x86-64 register", "RSP": "x86-64 register", "RFLAGS": "x86-64 flags register",
    "CPUID": "an x86 instruction", "RDTSC": "an x86 instruction",
    # Units and quantities.
    "GiB": "a unit", "MiB": "a unit", "KiB": "a unit", "TiB": "a unit",
    "MHz": "a unit", "GHz": "a unit", "TBW": "a drive-endurance unit", "DWPD": "a drive-endurance unit",
    # Tool, library and product names.
    "GCC": "a compiler name", "JADX": "a tool name", "AFL": "a fuzzer name",
    "OpenFHE": "a library name", "IoTeX": "a platform name", "NTRU": "a cryptosystem name",
    "OpenPGP": "a standard's proper name", "BB84": "a protocol named for its authors and year",
    "BLS": "a signature scheme named for its authors (Boneh, Lynn, Shacham)",
    "FHEz": "a library name", "CTFd": "a platform name", "ZIP": "a file format, assumed known",
    "JPEG": "a file format, assumed known", "TRIM": "an ATA command name, not an initialism",
    "COW": "collides: copy-on-write, but every use here is inside the vulnerability name Dirty COW",
    # Publishers, conferences and series in bibliographies.
    "MDPI": "a publisher name", "NDSS": "a conference name", "USENIX": "a conference name",
    "IACR": "a society name", "ACSAC": "a conference name", "RAID": "collides: the storage scheme "
            "and the conference name; both appear, neither is expanded where it is used",
    # Structured labels: exam domains in Appendix C, RFC requirement numbers, Kerberos messages.
    "D1": "a certification domain label", "D2": "a certification domain label",
    "D3": "a certification domain label", "D4": "a certification domain label",
    "D5": "a certification domain label", "D6": "a certification domain label",
    "D7": "a certification domain label", "D8": "a certification domain label",
    "REQ": "collides: an RFC requirement number (REQ-1) and a Kerberos message (AS-REQ)",
    "REP": "a Kerberos message name (AS-REP, TGS-REP, AP-REP)",
    "NTUSER": "part of the file name NTUSER.DAT", "DAT": "a file extension",
    "UA": "only ever appears inside the product name OPC UA, expanded in Appendix I",
    "SAS": "Serial Attached SCSI, a storage bus; given in full in Appendix I",
    "SATA": "a storage bus name, given in full in Appendix I",
    "PCIe": "a bus name, given in full in Appendix I",
    "SMB1": "a version label for SMB", "SMB2": "a version label for SMB",
    "SMB3": "a version label for SMB",
    # Standards bodies and document series named inside a citation, like ISO, IEC and IEEE.
    "ASHRAE": "a standards body named in a standard's citation",
    "INCITS": "a standards body named in a standard's citation",
    "OASIS": "a standards body named in a standard's citation",
    "OCF": "a standards body named in a standard's citation",
    "T10": "an INCITS technical committee number",
    "ETSI": "a standards body named in a standard's citation",
    "ANSI": "collides in this corpus: the standards body and the Windows character encoding",
    "NSEC3": "a record-type version label for NSEC",
    "StartTLS": "a protocol command name, not an initialism",
    "STARTTLS": "a protocol command name, not an initialism",
    "INIT": "the SCTP association-setup chunk, a message name",
    "MS": "a Microsoft protocol document prefix, as in MS-SMB2 and MS-CHAPv2",
    # Chapter 2: schemes and curves named for their authors, notation inside a security game,
    # journal and conference names in the bibliography, and two English digrams.
    "BBS": "a signature scheme named for Boneh, Boyen and Shacham",
    "BLS12": "a pairing-friendly curve family name, as in BLS12-381",
    "BLISS": "a lattice signature scheme name",
    "CGGI": "a scheme named for Chillotti, Gama, Georgieva and Izabachene",
    "DM": "a scheme named for Ducas and Micciancio",
    "FourQ": "a curve name", "GLS254": "a curve name",
    "G1": "a group name in pairing notation", "G2": "a group name in pairing notation",
    "HintLWE": "a lattice problem name", "RLWE": "a lattice problem name, written Ring-LWE in prose",
    "KLM": "the airline, in the one-time pad courier story",
    "LMS": "a hash-based signature scheme name", "XMSS": "a hash-based signature scheme name",
    "M0": "notation for a chosen plaintext in a security game",
    "M1": "notation for a chosen plaintext in a security game",
    "PK": "notation for a public key in a security game",
    "SK": "notation for a secret key in a security game",
    "NI": "part of the instruction-set name AES-NI",
    "NSEC5": "a DNSSEC record-type name",
    "ROBOT": "the published name of an attack, used here as a name",
    "SHA256": "a hash function name", "SCN": "a conference name", "SIAM": "a journal name",
    "BLAKE3": "a hash function name; BLAKE is not an initialism, and the reviewed table already "
              "lists BLAKE2, which stands beside it in the same sentence",
    "TISSEC": "a journal name", "TAA": "part of the paper title k-TAA",
    "UCSD": "an institution name in a bibliography entry",
    "DEV": "the website name DEV Community, in a bibliography entry",
    "VENONA": "a project codename", "X3DH": "a protocol name",
    "ZigBee": "a brand name", "TH": "an English digram in frequency analysis",
    "ER": "an English digram in frequency analysis",
    # Chapter 17: OWASP LLM category IDs, AWS best-practice IDs, dataset, library and venue names.
    "BP04": "an AWS Well-Architected best-practice identifier",
    "REL11": "an AWS Well-Architected reliability-pillar identifier",
    "DBLP": "a bibliographic database name", "TCS": "a journal name in a bibliography entry",
    "CSCML": "a conference name", "MDPI": "a publisher name",
    "FALCON": "a signature scheme name", "SealPIR": "a system name",
    "PriSM": "a system name", "FedAV": "a system name",
    "QEMU": "a product name", "NAND": "a flash-memory type, from the logic gate",
    "NSL": "part of the dataset name NSL-KDD", "KDD": "part of the dataset name NSL-KDD",
    "HDFS": "a dataset and filesystem product name",
    "FV": "a homomorphic scheme named for Fan and Vercauteren",
    "RESTful": "an adjective formed from REST, widely used unexpanded",
    "CAM": "collides badly: computer-aided manufacturing in the reviewed table, cooperative "
           "awareness message in intelligent transport systems, and connected and automated "
           "mobility in EU policy; the book's one use is ambiguous and is left alone",
    # Chapter 15: tool, distribution, company and instruction-set names.
    "MSVC": "a compiler name", "VBScript": "a language name", "AIxCC": "a competition name",
    "ANAB": "an accreditation body name", "ES": "part of the product name OpenGL ES",
    "HC": "part of the cipher name HC-128", "MIPS": "an instruction-set architecture name",
    "MalAPI": "a website name", "NSO": "a company name", "OSED": "an OffSec certification code",
    "PEiD": "a tool name", "PEview": "a tool name", "PSExec": "a tool name",
    "R15": "an x86-64 register", "RunPE": "a technique name",
    "REMnux": "a Linux distribution name", "FlareVM": "a Windows tool collection name",
    "LM": "collides: LAN Manager in Ch. 9, and the product name LM Studio in Ch. 15",
    "PicoCTF": "a platform name",
    "NET": "from .NET, the Microsoft platform name, in Ch. 15 and Ch. 16; the reviewed deck table "
           "lists it as a literal for the same reason",
    # Chapter 3: hex groups inside an IPv6 address, a quiz distractor, a standard and tool name.
    "DFE1": "a hextet inside an example IPv6 address",
    "FEFB": "a hextet inside an example IPv6 address",
    "DALE": "a wrong-answer distractor in a review question",
    "XYZ": "a placeholder in a worked example", "RS": "part of the standard name RS-232",
    "SMAC": "a tool name", "XGS": "part of the standard name XGS-PON",
    "TXT": "a DNS record type, named for the text it carries; the row beside it names A, AAAA, MX "
           "and NS the same way, and Ch. 16 uses it for the same record (Ch. 3, Ch. 16)",
    # Chapter 9: tool names.
    "LinPEAS": "a tool name", "WinPEAS": "a tool name", "PEDA": "a tool name",
    "KLEE": "a tool name", "Z3": "a tool name", "DCSync": "a technique name",
    "EventID": "a Windows event log field name",
    # Chapter 19: citation machinery.
    "FR": "the Federal Register, in a citation such as 88 FR 51896",
    "CHI": "a conference name", "CCSC": "a conference name",
    "PAE": "a judge's initials inside a case docket number",
    "S1": "a journal supplement number, as in Global Policy 9(S1)",
    # Chapter 10: database and product names.
    "MariaDB": "a product name", "DynamoDB": "a product name", "HANA": "a product name",
    "HBase": "a product name", "InfluxDB": "a product name", "InnoDB": "a storage engine name",
    "MyISAM": "a storage engine name", "PostGIS": "an extension name", "RocksDB": "a product name",
    "SAP": "a company name", "RDS": "an Amazon service name", "WiredTiger": "a storage engine name",
    # Chapter 11 and 20: alert and advisory identifiers, product, company and malware names.
    "TA17": "a US-CERT alert identifier", "AA22": "a CISA advisory identifier",
    "MAR": "part of a CISA Malware Analysis Report document number",
    "IOS": "collides: Cisco IOS the router operating system, and Apple iOS; a product name either way",
    "TRISIS": "a malware name", "HatMan": "a malware name", "ESET": "a company name",
    "TRITON": "a malware name, the same malware as TRISIS and HatMan beside it",
    "NATO": "an organization name of the class already allowed above (FBI, NSA, DHS), and every use "
            "is inside the proper name of the NATO Cooperative Cyber Defence Centre of Excellence",
    "eduGAIN": "the name of the GEANT interfederation service, which its own site does not expand; "
               "it stands beside InCommon, which is a name too",
    "OMRON": "a company name", "ISA": "a standards body inside the designation ANSI/ISA-62443",
    # Chapter 13 and 16: tool, dataset, format and platform names, and quiz answer options.
    "AXIOM": "a product name", "SQLite": "a product name", "ALEAPP": "a tool name",
    "iLEAPP": "a tool name", "AVML": "a tool name", "LiME": "a tool name", "PECmd": "a tool name",
    "RunMRU": "a registry key name", "CTU": "part of the dataset name CTU-13",
    "ISDFS": "a conference name", "InC4": "a conference name",
    "CRUD": "a wrong-answer distractor in a review question",
    "ITAR": "a wrong-answer distractor in a review question",
    "CTFtime": "a website name", "rCTF": "a platform name", "FBCTF": "a platform name",
    "CeWL": "a tool name", "BMP": "an image format name", "PNG": "an image format name",
    "ROT": "part of the cipher name ROT13, from rotate", "ROT13": "a cipher name, from rotate",
    # Remaining chapters: product, lab-host, exam-code, author and citation-format names.
    "PRTG": "a product name", "SP2": "a Windows service-pack label",
    "WKS": "a lab host name, as in WKS-7", "TA": "a threat-cluster name prefix, as in TA505",
    "UNC": "a threat-cluster name prefix, as in UNC2452",
    "FOCA": "a tool name", "McGraw": "part of the publisher name McGraw-Hill",
    "JCSC": "a journal abbreviation in a citation",
    "CS0": "a CompTIA exam code", "P6": "a certification practice-area label",
    "APA": "a citation style name", "MLA": "a citation style name",
    "BibTeX": "a citation format name", "NVDA": "a screen reader product name",
    "FreeBSD": "an operating system name", "PowerPC": "a processor architecture name",
}
ALLOW |= set(BOOK_LITERAL)

# Some tokens are literal only where they appear. A venue abbreviation in a bibliography is not an
# acronym the chapter owes the reader, but the same letters elsewhere might be; scoping the exception
# to one file keeps a real finding in another file from being silently suppressed.
CHAPTER_LITERAL = {
    ("13_forensics", "ACID"): "a wrong-answer distractor in a review question",
    ("13_forensics", "CRC"): "one of four algorithm names offered as answer options; expanding only "
                             "this one would signal the answer",
    ("appendix_e", "WLAN"): "inside the title of a cited paper",
    ("appendix_e", "MSRPC"): "inside the title of a cited note",
    ("appendix_e", "NIRMA"): "a university name in a citation",
    ("appendix_e", "CRAN"): "an R package repository name in a paper title",
    ("appendix_e", "MRAN"): "an R package repository name in a paper title",
    ("appendix_e", "PETA"): "a venue abbreviation in a citation",
    ("appendix_e", "SciSec"): "a venue abbreviation in a citation",
    ("appendix_e", "CCWC"): "a venue abbreviation in a citation",
    ("appendix_e", "IJARCS"): "a journal abbreviation in a citation",
    ("appendix_e", "IJCSC"): "a journal abbreviation in a citation",
    ("appendix_e", "IJEDR"): "a journal abbreviation in a citation",
    ("appendix_e", "IJSRD"): "a journal abbreviation in a citation",
    ("appendix_e", "IJTRD"): "a journal abbreviation in a citation",
    ("appendix_h", "INCoS"): "a venue abbreviation in a citation",
    ("appendix_h", "TIFS"): "a journal abbreviation in a citation",
    ("appendix_h", "USEC"): "a venue abbreviation in a citation",
    ("appendix_h", "DSpace"): "a repository platform name",
    ("appendix_h", "OSF"): "a repository platform name",
    ("appendix_h", "PubPub"): "a repository platform name",
    ("appendix_f", "APUE"): "the standard short title of a cited book",
    ("appendix_f", "MP3"): "an audio format name inside a tool name",
    ("appendix_f", "CRC32"): "a named checksum variant inside a notebook name",
}

# Appendix G is generated by scripts/gen_wordcounts.py from the other chapters' section titles.
# Editing it would be undone by the next build, and the acronyms in it are reflections of headings
# that are fixed at their source.
GENERATED = {"appendix_g"}

# Terms the book uses that the deck corpus never had, so the reviewed table never classified them.
# Each is the expansion the book itself now gives, in Appendix B or at first use, which is what makes
# the matcher able to see it: several of these are not derivable from their letters by any rule
# (V2X, CCA1, RIPE NCC), and the rest are here so that one file states what the book means by them.
BOOK_EXPANSIONS = {
    "UC": "universal composability",
    "CTF": "capture the flag",
    "GDB": "GNU debugger",
    "PCAP": "packet capture",
    "MPC": "multi-party computation",
    "SGX": "software guard extensions",
    "V2X": "vehicle-to-everything",
    "HVAC": "heating, ventilation, and air conditioning",
    "RAG": "retrieval-augmented generation",
    "DARPA": "defense advanced research projects agency",
    "DTLS": "datagram transport layer security",
    "LWE": "learning with errors",
    "UAC": "user account control",
    "GF": "galois field",
    "DIE": "distributed, immutable, ephemeral",
    "CCA1": "non-adaptive chosen-ciphertext attack",
    "CCA2": "adaptive chosen-ciphertext attack",
    "RIPE": "reseaux ip europeens",
    "NCC": "network coordination centre",
    "APNIC": "asia-pacific network information centre",
    "LACNIC": "latin american and caribbean network information centre",
    "AFRINIC": "african network information centre",
    "ARIN": "american registry for internet numbers",
    "RIR": "regional internet registry",
    "OPC": "open platform communications",
    "DNP3": "distributed network protocol 3",
    "PFDavg": "average probability of failure on demand",
    "HDD": "hard disk drive",
    "SSD": "solid-state drive",
    "AXFR": "authoritative full zone transfer",
    "COPPA": "children's online privacy protection act",
    "OECD": "organisation for economic co-operation and development",
    "FERPA": "family educational rights and privacy act",
    "HEW": "health, education, and welfare",
    "NYCRR": "new york codes, rules and regulations",
    "CCDC": "collegiate cyber defense competition",
    "NCL": "national cyber league",
    "SEHOP": "structured exception handler overwrite protection",
    "PKCS": "public-key cryptography standards",
    "CFRG": "crypto forum research group",
    "SEV": "secure encrypted virtualization",
    "DOCSIS": "data over cable service interface specification",
    "QAM": "quadrature amplitude modulation",
    "PID": "process identifier",
    "SPN": "service principal name",
    "MSA": "mandatory security assessment",
    "CPS": "cyber-physical system",
    "SBOM": "software bill of materials",
    "FIM": "file integrity monitoring",
    "UEBA": "user and entity behavior analytics",
    # Letter-substitution acronyms, which no initials rule reaches: the X in XMPP is "extensible",
    # the X in XSS is "cross", the 2 in C2 is "to".
    "XMPP": "extensible messaging and presence protocol",
    "PKCE": "proof key for code exchange",
    "SASL": "simple authentication and security layer",
    "AH": "authentication header",
    "ESP": "encapsulating security payload",
    "IKE": "internet key exchange",
    "KRACK": "key reinstallation attack",
    "PMKID": "pairwise master key identifier",
    "SAE": "simultaneous authentication of equals",
    "RADSEC": "radius over tls",
    "NSEC": "next secure record",
    "NTS": "network time security",
    "MTA": "mail transfer agent",
    "MACsec": "media access control security",
    "PKINIT": "public key cryptography for initial authentication in kerberos",
    "PXE": "preboot execution environment",
    "PAP": "password authentication protocol",
    "CHAP": "challenge-handshake authentication protocol",
    "BGPsec": "border gateway protocol security",
    "HPACK": "header compression for http/2",
    "PSK": "pre-shared key",
    "VoIP": "voice over ip",
    "WebRTC": "web real-time communication",
    "VNC": "virtual network computing",
    "CIFS": "common internet file system",
    "BEP": "bittorrent enhancement proposal",
    "CoAP": "constrained application protocol",
    "SMTPS": "smtp over tls",
    "LDAPS": "ldap over tls",
    "POP3S": "pop3 over tls",
    "RFB": "remote framebuffer",
    "STP": "spanning tree protocol",
    "ROA": "route origin authorization",
    "RPKI": "resource public key infrastructure",
    "UPnP": "universal plug and play",
    "mDNS": "multicast dns",
    "NBT": "netbios over tcp/ip",
    "CSWSH": "cross-site websocket hijacking",
    "EAPOL": "eap over lan",
    "IMAPS": "imap over tls",
    "ATA": "at attachment",
    "RST": "reset",
    "WPS": "wi-fi protected setup",
    "SRTP": "secure real-time transport protocol",
    "RTP": "real-time transport protocol",
    "BPDU": "bridge protocol data unit",
    "DTP": "dynamic trunking protocol",
    "SCSI": "small computer system interface",
    "SSDP": "simple service discovery protocol",
    "HSTS": "http strict transport security",
    "POP3": "post office protocol version 3",
    "EUF": "existential unforgeability",
    "SUF": "strong unforgeability",
    "CMA": "chosen-message attack",
    "CCM": "counter with cbc-mac",
    "ORAM": "oblivious ram",
    "XTS": "tweaked codebook mode with ciphertext stealing",
    "E2EE": "end-to-end encryption",
    "EMV": "europay mastercard and visa",
    "CPIR": "computational pir",
    "IMDS": "instance metadata service",
    "iSCSI": "internet small computer systems interface",
    "RTOS": "real-time operating system",
    "OEM": "original equipment manufacturer",
    "SVM": "support vector machine",
    "LSTM": "long short-term memory",
    "BSM": "basic safety message",
    "SQS": "simple queue service",
    "SNS": "simple notification service",
    "ReLU": "rectified linear unit",
    "ATLAS": "adversarial threat landscape for artificial-intelligence systems",
    "RPM": "revolutions per minute",
    "SNI": "server name indication",
    "SWD": "serial wire debug",
    "eMMC": "embedded multimediacard",
    "CMM": "coordinate measuring machine",
    "LGPL": "lesser general public license",
    "SDK": "software development kit",
    "LVM": "logical volume manager",
    "SSID": "service set identifier",
    "IPAM": "ip address management",
    "OFDMA": "orthogonal frequency-division multiple access",
    "MIMO": "multiple input multiple output",
    "MU": "multi-user",
    "MX": "mail exchange",
    "GPON": "gigabit passive optical network",
    "NOP": "no-operation",
    "SMT": "satisfiability modulo theories",
    "BSS": "block started by symbol",
    "UAF": "use-after-free",
    "WinRM": "windows remote management",
    "AST": "abstract syntax tree",
    "PAC": "pointer authentication codes",
    "BSD": "berkeley software distribution",
    "SR": "supply chain risk management",
    "SeBIS": "security behavior intentions scale",
    "NIS2": "network and information security",
    "DORA": "digital operational resilience act",
    "MVCC": "multiversion concurrency control",
    "XXE": "xml external entity",
    "IAST": "interactive application security testing",
    "RASP": "runtime application self-protection",
    "CDO": "chief data officer",
    "COO": "chief operating officer",
    "ACK": "acknowledgment",
    "RCODE": "response code",
    "STUN": "session traversal utilities for nat",
    "VRF": "virtual routing and forwarding",
    "WDAC": "windows defender application control",
    "ZTA": "zero trust architecture",
    "MBAP": "modbus application protocol",
    "NCCIC": "national cybersecurity and communications integration center",
    "MES": "manufacturing execution system",
    "MMS": "manufacturing message specification",
    "ERP": "enterprise resource planning",
    "BES": "bulk electric system",
    "NRC": "nuclear regulatory commission",
    "FERC": "federal energy regulatory commission",
    "SL": "security level",
    "XAI": "explainable ai",
    "CNN": "convolutional neural network",
    "DRAM": "dynamic random-access memory",
    "APFS": "apple file system",
    "ACPO": "association of chief police officers",
    "EXIF": "exchangeable image file format",
    "LSB": "least-significant-bit",
    "ROP": "return-oriented programming",
    "PIE": "position independent executable",
    "CPRA": "california privacy rights act",
    "DSAR": "data subject access request",
    "LGPD": "lei geral de protecao de dados",
    "PIPEDA": "personal information protection and electronic documents act",
    "PIPL": "personal information protection law",
    "POPIA": "protection of personal information act",
    "EEA": "european economic area",
    "GLBA": "gramm-leach-bliley act",
    "QSA": "qualified security assessor",
    "C2PA": "coalition for content provenance and authenticity",
    "FALCPA": "food allergen labeling and consumer protection act",
    "COSE": "cbor object signing and encryption",
    "CBOR": "concise binary object representation",
    "GRC": "governance, risk and compliance",
    "BSIMM": "building security in maturity model",
    "CLASP": "comprehensive, lightweight application security process",
    "SAMM": "software assurance maturity model",
    "SDL": "security development lifecycle",
    "NIDPS": "network-based intrusion detection and prevention system",
    "HIDPS": "host-based intrusion detection and prevention system",
    "RID": "relative identifier",
    "SID": "security identifier",
    "DDP": "distributed data parallel",
    "SEO": "search engine optimization",
    "SNARK": "succinct non-interactive argument of knowledge",
    "STARK": "scalable transparent argument of knowledge",
    "ASIC": "application-specific integrated circuit",
    "RNG": "random number generator",
    "KPI": "key performance indicator",
    "TTP": "tactics, techniques, and procedures",
    "IL": "intermediate language",
    "ISN": "initial sequence number",
    "RAT": "remote access trojan",
    "SCTP": "stream control transmission protocol",
    "UID": "user identifier",
    "LFT": "layer four traceroute",
    "NIDS": "network-based intrusion detection system",
    "HIDS": "host-based intrusion detection system",
    "NIPS": "network-based intrusion prevention system",
    "HIPS": "host-based intrusion prevention system",
    "NGFW": "next-generation firewall",
    "DREAD": "damage, reproducibility, exploitability, affected users, discoverability",
    "COSO": "committee of sponsoring organizations of the treadway commission",
    "EOL": "end of life",
    "IC3": "internet crime complaint center",
    "EDGAR": "electronic data gathering, analysis, and retrieval",
    "ISECOM": "institute for security and open methodologies",
    "GPEN": "giac penetration tester",
    "SOA": "selective-opening security",
    "CySA": "cybersecurity analyst",
    "AFRINIC": "african network information centre",
}

EXPANSIONS = {}
LITERAL = set()
for _p in TABLE_PATHS:
    if os.path.exists(_p):
        _t = json.load(open(_p))
        LITERAL = set(_t.get("literal", []))
        ALLOW |= LITERAL
        # Some acronyms are not derivable from their letters at all: C2 is a numeronym for command
        # and control, and the X in XSS stands in for "cross". Comparing against the expansion the
        # table already states is simpler and more honest than inventing a rule for each pattern.
        EXPANSIONS = {k: v.lower() for k, v in _t.get("expand", {}).items()}
        TABLE_USED = _p
        break
else:
    TABLE_USED = None
EXPANSIONS.update({k: v.lower() for k, v in BOOK_EXPANSIONS.items() if k not in LITERAL})


# ---------------------------------------------------------------------------------- text handling

FENCE = re.compile(r"^\s{0,3}(`{3,}|~{3,})")
INLINE_CODE = re.compile(r"(`+)(?:(?!\1).)*?\1", re.S)
HTML_COMMENT = re.compile(r"<!--.*?-->", re.S)
HTML_TAG = re.compile(r"</?[A-Za-z][^>]*>")
URL = re.compile(r"(?:https?|ftp)://\S+")
LINK_TARGET = re.compile(r"\]\([^)]*\)")
MATH_BLOCK = re.compile(r"\$\$.*?\$\$", re.S)
MATH_INLINE = re.compile(r"\$[^$\n]{1,200}\$")
MYST_ROLE = re.compile(r"\{[a-z-]+\}`[^`]*`")
# Identifiers that are names, not acronyms. Removing them is cheaper and safer than teaching the
# matcher about every numbering scheme in the corpus.
IDENTIFIER = re.compile(
    r"\b(?:CVE-\d{4}-\d+"
    r"|CWE-\d+"
    r"|T\d{4}(?:\.\d{3})?"          # MITRE ATT&CK technique
    r"|TA\d{4}"                     # MITRE tactic
    r"|M\d{4}"                      # MITRE mitigation
    r"|S\d{4}"                      # MITRE software
    r"|G\d{4}"                      # MITRE group
    r"|A\d{2}:\d{4}"                # OWASP category with year
    r"|API\d{1,2}:\d{4}"
    r"|MS\d{2}-\d{3}"               # Microsoft bulletin
    r"|RFC\s?\d+"
    r"|ISO/?IEC\s?\d+"
    r"|SP\s?800-\d+[A-Za-z0-9-]*"
    r")\b")
# A CVSS vector is one indivisible string. `AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H` reads as eight
# unexpanded acronyms and is in fact the exact text an exercise asks students to interpret.
CVSS_VECTOR = re.compile(r"(?:CVSS:[0-9.]+/)?(?:[A-Z]{1,2}:[A-Z]/){2,}[A-Z]{1,2}:[A-Z]")
# Windows registry paths, environment variables, and Windows API names in prose.
REGISTRY = re.compile(r"\bHKEY_[A-Z_]+(?:\\[^\s]*)?")
WINPATH = re.compile(r"\b[A-Za-z]:\\[^\s]*")
POSIXPATH = re.compile(r"(?<![\w.])/(?:etc|usr|var|proc|sys|opt|bin|sbin|dev|tmp|home)/[^\s,;)]*")


def strip_fences(text):
    """Drop fenced code blocks, keeping line structure so nothing else shifts.

    MyST `:::` directives are prose containers (note, warning, admonition) and are kept; only
    backtick and tilde fences are code.
    """
    out, fence = [], None
    for line in text.split("\n"):
        m = FENCE.match(line)
        if fence is None:
            if m:
                fence = m.group(1)[0] * 3
                out.append(" " * len(line))
                continue
            out.append(line)
        else:
            if m and m.group(1)[0] * 3 == fence:
                fence = None
            out.append(" " * len(line))
    return "\n".join(out)


def blank(m):
    return " " * (m.end() - m.start())


def prose(text):
    """The text with every non-prose region blanked out, character offsets preserved."""
    text = strip_fences(text)
    for pat in (HTML_COMMENT, MATH_BLOCK, MATH_INLINE, MYST_ROLE, INLINE_CODE, URL, LINK_TARGET,
                CVSS_VECTOR, IDENTIFIER, REGISTRY, WINPATH, POSIXPATH, HTML_TAG):
        text = pat.sub(blank, text)
    return text


def cell_texts(path):
    """(cell index, prose text) for every markdown cell of a notebook, or one entry for a .md."""
    if path.endswith(".ipynb"):
        nb = json.load(open(path))
        return [(i, prose("".join(c["source"])))
                for i, c in enumerate(nb["cells"]) if c["cell_type"] == "markdown"]
    return [(0, prose(open(path, encoding="utf-8").read()))]


# ------------------------------------------------------------------------------------- expansion

# Accented letters are part of a word: without them "Reseaux IP Europeens" tokenizes as R, seaux,
# IP, Europ, ens and RIPE never matches its own expansion.
TOKEN = re.compile(r"[A-Za-zÀ-ÖØ-öø-ÿ0-9'/-]+")


def tokenize(text):
    return TOKEN.findall(text)


def initials(tokens, skip=True):
    """Initial letters of a run of words, splitting on hyphen and slash.

    `skip` drops joining words, which is what makes "Authenticated Encryption with Associated Data"
    give AEAD. But a whole family of acronyms takes its letters FROM those words: separation of
    duties is SoD, software as a service is SaaS. So callers try it both ways.
    """
    out = []
    for w in tokens:
        if skip and w.lower() in SKIP_WORDS:
            continue
        for part in re.split(r"[-/]", w):
            if part:
                out.append(part[0].upper())
    return "".join(out)


def loose_match(words, acr):
    """True if `words` reads as an expansion of `acr` that is not a strict initialism.

    ECB is electronic codebook, where the C and the B are both inside the second word, and CTR is
    simply counter. So a weaker test: the acronym's letters appear in order across the phrase,
    anchored at both ends. Both anchors matter; without them almost any short phrase beginning with
    the right letter matches something.
    """
    if not words or not acr:
        return False
    acr = acr.upper()
    if words[0][0].upper() != acr[0]:
        return False
    letters = "".join(words).upper()
    tail_start = len(letters) - len(words[-1])
    pos = -1
    for k, ch in enumerate(acr):
        pos = letters.find(ch, pos + 1)
        if pos < 0:
            return False
        if k == len(acr) - 1 and pos < tail_start:
            return False
    return True


def norm(s):
    """Lower case, accents dropped, hyphens and slashes to spaces, whitespace collapsed.

    So that "cross site scripting", "cross-site scripting" and "Cross-Site Scripting" are one
    phrase. The table stores one spelling; the book uses several. Accents are dropped because RIPE
    stands for Reseaux IP Europeens, which the book spells properly and a plain-ASCII table does not.
    """
    s = unicodedata.normalize("NFKD", s.lower())
    s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[-/,]", " ", s)).strip()


def matches(run, acr, loose=True):
    up = acr.upper()
    # An acronym is not its own expansion. Without this, the loose rule reported the learning
    # objective "(ECB, CBC, CFB, OFB, CTR, GCM) ... why ECB is insecure" as expanding ECB, because
    # the letters of ECB do appear in order inside the token ECB. Four of the six modes on that line
    # passed the check for that reason alone, and the line expands none of them.
    for w in run:
        for part in re.split(r"[-/]", w):
            if part.upper() == up:
                return False
    if initials(run) == up or initials(run, skip=False) == up:
        return True
    # The loose rule (letters in order, anchored at both ends) is the weakest of the three, so it is
    # only allowed on a run of ordinary words sitting right against the acronym. Unanchored, it read
    # "of operation ECB" as an expansion of OFB.
    if loose and not any(w.isupper() or is_mixed_acronym(w) for w in run) and loose_match(run, acr):
        return True
    known = EXPANSIONS.get(acr) or EXPANSIONS.get(singular(acr))
    if known:
        return norm(" ".join(run)) == norm(known)
    return False


def expanded_at(tokens, i, acr):
    """True if the occurrence at token index `i` carries its expansion on either side.

    The deck version only considered runs touching the acronym, because a slide bullet puts the two
    next to each other. Book prose does not: it writes "the DIE triad, Distributed, Immutable,
    Ephemeral" and "the NICE Framework (the NIST National Initiative for Cybersecurity Education
    Workforce Framework)", where an apposition sits between the letters and the words. So every
    contiguous run inside the window is tried, on both sides.

    A run that matches by chance costs nothing: it means the acronym is treated as already expanded
    and left alone. The expensive error is the opposite one, editing text that did not need it, and
    a looser matcher cannot cause that.
    """
    span = len(acr) + 6
    before, after = tokens[max(0, i - span):i], tokens[i + 1:i + 1 + span]
    for start in range(len(before)):
        for end in range(start + 1, len(before) + 1):
            gap = len(before) - end          # words between the run and the acronym
            if gap <= 3 and matches(before[start:end], acr, loose=(gap == 0)):
                return True
    for start in range(len(after)):
        for end in range(start + 1, len(after) + 1):
            if start <= 3 and matches(after[start:end], acr, loose=(start == 0)):
                return True
    return False


def occurrences(tokens, acr):
    """Indices where the acronym appears, plural or singular, alone or inside a compound.

    A plural has to count, or the first use is missed: chapter 1 writes "Constrained Data Items
    (CDIs)" and then uses CDI on its own later, and a scan that only looked for CDI reported the
    later, unexpanded use as the first one and asked for an expansion the chapter already gives.

    But a fragment of a hyphenated proper name is not a use of that acronym. Chapter 17 names the
    NIST signature standard FN-DSA, and FN is in the table as "false negative", so the scan asked
    the chapter to expand an acronym it never uses. The rule below: if EVERY appearance is as a
    hyphen-joined part of a compound whose neighbor is itself acronym-shaped, the compound is the
    term and the fragment is not. One standalone appearance anywhere puts every occurrence back in
    scope, so this cannot hide a real first use.

    Hyphens only, never slashes. A slash pairs two terms that each stand alone: IDS/IPS is a use of
    both IDS and IPS, and treating it as one name dropped IDS out of the glossary's defined set and
    broke two appendices. A hyphen inside an all-caps compound builds a single name instead.
    """
    found, standalone = [], False
    for i, t in enumerate(tokens):
        pieces = re.split(r"[-/]", t)
        parts = [singular(debase(p)) for p in pieces]
        if singular(debase(t)) == acr:
            found.append(i)
            standalone = True
        elif acr in parts:
            found.append(i)
            hyphen_only = "/" not in t
            neighbors = [p for p, whole in zip(pieces, parts) if whole != acr]
            if not (hyphen_only and any(is_acronym_shaped(p) for p in neighbors)):
                standalone = True
    if found and not standalone:
        return
    for i in found:
        yield i


def expanded_anywhere(tokens, acr):
    return any(expanded_at(tokens, i, acr) for i in occurrences(tokens, acr))


# ------------------------------------------------------------------------------------------ scan

def chapter_files():
    out = []
    for d in sorted(os.listdir(CHAPTERS)):
        full = os.path.join(CHAPTERS, d)
        if not os.path.isdir(full):
            continue
        for f in sorted(os.listdir(full)):
            if f.endswith((".ipynb", ".md")):
                out.append((d, os.path.join(full, f)))
    return out


def glossary_terms():
    """Acronyms Appendix B defines, and acronyms it merely mentions."""
    if not os.path.exists(GLOSSARY):
        return set(), set()
    text = " ".join(t for _, t in cell_texts(GLOSSARY))
    toks = tokenize(text)
    seen = {singular(a) for a in acronyms_in(text)}
    defined = {a for a in seen if expanded_anywhere(toks, a)}
    return defined, seen


def ordinary_words(files):
    """Words the book uses in lower case as ordinary English rather than as acronyms.

    CHECK, TERM, CLASS and SELECT are English; XSS and SIEM are not. Deriving the distinction from
    the book's own vocabulary beats maintaining a stoplist. An acronym-shaped token never votes
    itself into the ordinary vocabulary.

    The first version of this test was "the lower-case spelling appears at least three times", an
    absolute count over whatever set of files the run happened to see. That is not a property of the
    word, it is a property of the run, and it made the scanner's answer depend on how much prose the
    book contained. The same commit measured 0 failures on one run and 20 on another, because a
    truncated file set crossed different thresholds. The identical bug was found and fixed on the
    deck-side copy of this scanner, where scanning one course reported findings that scanning the
    whole corpus did not.

    Two changes, both of which make the answer independent of the size of the scanned set.

    A word is ordinary only if the book uses it in lower case MORE often than in acronym shape. That
    is a ratio, so it holds at nine chapters and at thirty-three: `of`, `from` and `state` outnumber
    OF, FROM and STATE by orders of magnitude, while a lower-case `ntp` inside a config example
    loses to NTP in the prose. Three occurrences are still required, so one stray spelling settles
    nothing on its own.

    And a term the table classifies is never ordinary. acronyms.json is the authoritative judgment
    and a vocabulary heuristic must not overrule it.
    """
    english, shapes = collections.Counter(), collections.Counter()
    for _, path in files:
        for _, text in cell_texts(path):
            for w in tokenize(text):
                if w.isupper() or is_mixed_acronym(w):
                    shapes[w.lower()] += 1
                else:
                    english[w.lower()] += 1
    classified = {k.lower() for k in EXPANSIONS}
    return {w for w, n in english.items()
            if n >= 3 and w not in classified and n > shapes.get(w, 0)}


def scan_chapter(path, ordinary, defined, mentioned, min_uses=1, chapter=""):
    """Findings for one file, as (acronym, uses, first cell, status)."""
    cells = cell_texts(path)
    blob = tokenize(" ".join(t for _, t in cells))
    uses, first_cell = collections.Counter(), {}
    for idx, text in cells:
        for a in acronyms_in(text):
            a = singular(a)
            if a in ALLOW or len(a) < 2 or a.lower() in ordinary:
                continue
            if (chapter, a) in CHAPTER_LITERAL:
                continue
            uses[a] += 1
            first_cell.setdefault(a, idx)
    out = []
    for a, n in uses.items():
        if n < min_uses:
            continue
        hits = list(occurrences(blob, a))
        if not hits:
            continue
        if expanded_at(blob, hits[0], a):
            continue                                    # expanded at first use: passes
        if a in defined:
            continue                                    # glossary defines it: passes
        status = ("LATE" if expanded_anywhere(blob, a) else
                  "GLOSSARY-MENTION" if a in mentioned else "MISSING")
        out.append((a, n, first_cell[a], status))
    return sorted(out, key=lambda r: (r[3] != "MISSING", -r[1], r[0]))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--chapter", help="substring of the chapter directory name")
    ap.add_argument("--min", type=int, default=1, help="only report acronyms used at least N times")
    ap.add_argument("--json", help="write findings to this path")
    ap.add_argument("--unknown", action="store_true",
                    help="list reported tokens that are in neither table, for adjudication")
    a = ap.parse_args()

    files = chapter_files()
    if TABLE_USED:
        print(f"table: {TABLE_USED}  ({len(EXPANSIONS)} expandable, {len(LITERAL)} literal)")
    else:
        print("WARNING: acronyms.json not found; literal list unavailable, refusing to run")
        return 2

    ordinary = ordinary_words(files)
    defined, mentioned = glossary_terms()
    print(f"{len(files)} files, {len(ordinary)} ordinary words, "
          f"{len(defined)} acronyms defined in Appendix B\n")

    if a.chapter:
        files = [(d, p) for d, p in files if a.chapter.lower() in d.lower()]

    report, grand, unknown = {}, 0, collections.Counter()
    for d, path in files:
        if d == "appendix_b" or d in GENERATED:
            continue
        bad = scan_chapter(path, ordinary, defined, mentioned, a.min, d)
        if not bad:
            continue
        grand += len(bad)
        report[d] = [{"acronym": x[0], "uses": x[1], "first_cell": x[2], "status": x[3],
                      "expansion": EXPANSIONS.get(x[0], "")} for x in bad]
        print(f"  {d}  ({len(bad)})")
        for acr, n, cell, status in bad:
            exp = EXPANSIONS.get(acr, "")
            tag = "" if acr in EXPANSIONS else "  [unclassified]"
            if acr not in EXPANSIONS and acr not in LITERAL:
                unknown[acr] += n
            print(f"      {acr:10s} {n:3d}x  cell {cell:3d}  {status:16s} {exp}{tag}")
        print()

    print(f"{grand} acronym-and-chapter pairs fail the rule")
    if a.unknown and unknown:
        print(f"\n{len(unknown)} tokens in neither table, most used first:")
        for t, n in unknown.most_common():
            print(f"      {t:10s} {n}x")
    if a.json:
        json.dump({"total": grand, "chapters": report}, open(a.json, "w"), indent=1)
        print(f"\nwrote {a.json}")
    return 1 if grand else 0


if __name__ == "__main__":
    sys.exit(main())
