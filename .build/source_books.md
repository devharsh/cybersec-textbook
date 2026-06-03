# Source-Book Coverage Mapping

## 1. Nakov, "Practical Cryptography for Developers" (cryptobook.nakov.com)
Topics (verified from preface "What Does this Book Cover"):
- Hash functions: SHA-2, SHA-3, BLAKE2, RIPEMD160, collisions  -> Ch02
- MAC codes: HMAC, CMAC, UMAC, MAC-based RNG  -> Ch02
- KDF: PBKDF2, Scrypt, Bcrypt, Argon2, crypt()  -> Ch02
- Password hashing/encryption  -> Ch02, Ch19 (policy)
- Secure random / entropy / CSPRNG  -> Ch02 (links to attached (Pseudo)Randomness.ipynb)
- Key exchange: DHKE, ECDH  -> Ch02
- Symmetric ciphers: block vs stream, CBC/CTR/GCM, AES (Rijndael), Salsa20/ChaCha20  -> Ch02 (links to attached Modes_of_operations.ipynb)
- Authenticated encryption: AES-256-GCM, ChaCha20-Poly1305, AES-CTR-HMAC  -> Ch02
- Asymmetric: RSA, ECC (points, named curves secp256k1/P-256/P-521/Curve25519/Curve448)  -> Ch02 (links to attached RSA_Cryptosystem.ipynb)
- Integrated encryption: ECIES hybrid  -> Ch02
- Digital signatures: RSA, ECDSA, EdDSA  -> Ch02 (links to attached Integrity.ipynb)
- Quantum-safe crypto: SPHINCS+, NewHope, what is quantum-broken  -> Ch02 + Ch17
- Certificates, TLS, OTP, OAuth  -> Ch02, Ch03 (TLS), Ch05/Ch11 (IAM)

## 2. Boneh & Shoup, "A Graduate Course in Applied Cryptography" (crypto.stanford.edu)
Part I Secret-key cryptography:
- Intro / historical ciphers; Shannon ciphers & perfect secrecy (one-time pad)  -> Ch02 (links to attached Cryptanalyze_this!.ipynb)
- Stream ciphers, PRGs, semantic security  -> Ch02
- Block ciphers (PRPs/PRFs), AES/DES internals, modes  -> Ch02
- Message integrity: MACs, CBC-MAC, PMAC, NMAC  -> Ch02
- Collision-resistant hashing, Merkle-Damgard, Merkle trees  -> Ch02, Ch17 (blockchain)
- Authenticated encryption (AEAD)  -> Ch02
Part II Public-key cryptography:
- Number theory, key exchange (DH), trapdoor permutations (RSA)  -> Ch02
- Public-key encryption (CCA security), ElGamal, hybrid  -> Ch02
- Digital signatures, hash-based signatures  -> Ch02
- Identification protocols, zero-knowledge proofs  -> Ch02 + Ch17
- Elliptic curves, pairings  -> Ch02
Part III Protocols:
- Authenticated key exchange, TLS  -> Ch02, Ch03
- Secure multi-party computation, oblivious transfer  -> Ch02 + Ch17 (oblivious computation)

## 3. Darshan penetration-testing checklist (OSCP/HTB style notes)
- Information gathering / enumeration methodology  -> Ch06, Ch07
- Service/port enumeration (FTP21, SSH22, SMTP25, DNS53, HTTP80/443, SMB139/445, SNMP161, RDP3389, etc.)  -> Ch07, Ch08 (links to Appendix B ports)
- Vulnerability scanning  -> Ch08
- Web application testing (dirbusting, LFI/RFI, SQLi, XSS, file upload, command injection)  -> Ch10
- Exploitation / public exploits / Metasploit  -> Ch09
- Buffer overflow (stack)  -> Ch09
- Windows & Linux privilege escalation  -> Ch09
- Active Directory attacks (Kerberoasting, pass-the-hash, BloodHound)  -> Ch09
- Pivoting / tunneling / port forwarding  -> Ch09
- Password attacks / cracking (Hydra, John, Hashcat)  -> Ch08, Ch09
- Post-exploitation, persistence, covering tracks  -> Ch09
- Reporting  -> Ch06

# Attached lab notebooks (user uploads) -> reuse as chapter code cells
- (Pseudo)Randomness.ipynb            -> Ch02 (CSPRNG section)
- Cryptanalyze_this!.ipynb            -> Ch02 (classical cipher cryptanalysis)
- Integrity.ipynb                     -> Ch02 (hashing/MAC/signatures)
- Modes_of_operations.ipynb           -> Ch02 (block cipher modes)
- RSA_Cryptosystem.ipynb              -> Ch02 (RSA)
- CTF platforms.rtf / CTF tools.rtf   -> Ch16 (CTF)

# Advanced topics requested (placement)
- Homomorphic encryption (PHE/SHE/FHE)        -> Ch02 (intro) + Ch17 (depth)
- Post-quantum cryptography (lattice/ML-KEM/ML-DSA/SPHINCS+)  -> Ch02 + Ch17
- Functional encryption                        -> Ch02 + Ch17
- Steganography (LSB, stego vs crypto)         -> Ch02 + Ch13 (forensics) + Ch16 (CTF)
- AI/LLM security (prompt injection, model theft, data poisoning, OWASP LLM Top 10)  -> Ch17
- Hardware security (HSM, TPM, secure boot, side channels)  -> Ch11 + Ch17
- CPU protection rings (ring 0-3, kernel/user mode)  -> Ch09 + Ch01 (architecture)
- Trusted Execution Environments (Intel SGX, ARM TrustZone, AMD SEV)  -> Ch17 + Ch09
- Sandboxes (containers, seccomp, browser sandboxes, VM isolation)  -> Ch09 + Ch11 + Ch15 (malware analysis)
- Return-Oriented Programming (ROP, gadgets, DEP/ASLR bypass)  -> Ch09
- Oblivious computation (ORAM, oblivious transfer, MPC, PIR)  -> Ch02 + Ch17
