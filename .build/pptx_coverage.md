# PPTX Topic Coverage Map (COSC 489 + Cybersecurity 101)

Both decks share the same technical content (Cybersecurity 101 = subset; COSC 489 adds course/syllabus
slides). Every topic below is mapped to the chapter that covers it. [x]=already built, [plan]=must be
included when that chapter is built.

## Foundations / framing
- Cybersecurity definition (Wikipedia) -> Ch01 [x]
- CIA triad; Confidentiality/Integrity/Availability structure of the deck -> Ch01 [x]
- Risks, Threats, Governance Frameworks; Ethical hacking intro -> Ch01 [x], Ch06 [plan]
- Rules of Engagement (RoE) -> Ch06 [plan]

## Cryptography (all in Ch02 [x])
- Eavesdropping attack -> Ch02 (confidentiality) [x] + Ch03 (sniffing) [plan]
- Vigenere cipher + full cryptanalysis (n-grams, Kasiski distance, frequency analysis, keyword table,
  brute force) -> Ch02 2.2 [x]
- Symmetric key encryption (RC4, AES, DES, 3DES, QUAD); fast, key distribution problem, no
  authentication/non-repudiation -> Ch02 2.5 [x] (QUAD = stream cipher; add name)
- Public key encryption -> Ch02 2.10 [x]
- HTTPS = HTTP + TLS(SSL); SSL/TLS handshake -> Ch02 2.14 [x]
- Post-quantum cryptography (integer factorization, discrete log, EC discrete log) -> Ch02 2.15 [x]
- Integrity; cryptographic hash requirements; collision resistance -> Ch02 2.7 [x]
- MD5 collisions (Wang & Yu, 2004-2005) -> Ch02 2.7 [x] (specific mention added)
- How hashes are cracked: dictionary, brute force, lookup tables, reverse lookup, rainbow tables
  -> Ch02 2.9 [x]
- Cryptanalysis; bigger key size, SHA-384/512 -> Ch02 2.2/2.7/2.17 [x]

## Networking + availability -> Ch03 [plan: must include]
- TCP/IP, TCP three-way handshake (SYN, SYN-ACK, ACK), seq/ack example
- ifconfig / ipconfig; IP addressing
- DoS/DDoS attack concept; quantity vs quality
- DoS types: teardrop / IP fragmentation, DNS flood, UDP flood, HTTP flood, SYN flood, Ping/ICMP flood
- SYN flood mechanics (tying up half-open connections)
- SYN-flood mitigations: increasing backlog queue, recycling oldest half-open connection, micro blocks,
  SYN cookies, RST cookies, stack tweaking
- Eavesdropping / sniffing

## Tools -> Ch08 Scanning [plan] + Appendix A [x has nmap]
- nmap (host/port scan), hping3 (packet crafting / SYN flood), wireshark (capture/filter),
  LOIC (Low Orbit Ion Cannon)

## Detection/Defense -> Ch12 IDS/IPS [plan: must include]
- IDS vs IPS; NIDS (network IDS); HIDS
- Detection methods: signature-based detection
- Snort (open-source NIPS): install, snort.conf, local.rules, console mode

## Action items baked into upcoming chapter builds
- Ch03: TCP handshake + DoS taxonomy + SYN flood + all 6 SYN-flood mitigations + sniffing/eavesdropping.
- Ch08: nmap, hping3, wireshark as worked tool examples.
- Ch12: IDS vs IPS, NIDS/HIDS, signature detection, Snort with config commands.
- Ch06: ethical hacking intro, governance framing, Rules of Engagement.
