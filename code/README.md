# Companion Code

Small, self-contained programs that accompany the textbook. They are teaching
examples meant to be read, compiled, and modified inside a disposable lab
environment, never run against systems you do not own or have explicit written
authorization to test.

## Layout

- `crypto/` Classical and modern cryptography examples in Java, C, and C++:
  Caesar and Vigenere ciphers, AES in ECB and CTR modes, ElGamal, HMAC, hashing,
  digital signatures, CRC and Hamming codes, and secure versus insecure random
  number generation. Supports Chapter 2.
- `notebooks/` Jupyter notebooks for cryptography labs: pseudo-randomness,
  classical cryptanalysis, integrity checks, block-cipher modes of operation,
  and the RSA cryptosystem. Supports Chapter 2.
- `networking/` Socket programming and TLS: date and web client/server pairs in
  Java, a C++ client/server pair, and a self-signed HTTPS server in Python.
  Supports Chapter 3.
- `exploitation/` Deliberately vulnerable C programs that isolate one
  memory-corruption failure mode each (stack overflow, unbounded recursion, heap
  exhaustion, an overflow that changes an authorization flag), plus a
  compilation-stages demonstration (`hello.c` with its preprocessed and assembly
  output). Supports Chapter 9. Build only in an isolated virtual machine.

## Safety and licensing

The `exploitation/` programs are intentionally unsafe and are provided solely for
authorized, isolated study of how memory-corruption bugs arise. Compile them with
mitigations disabled only inside a throwaway virtual machine. All code here is
provided for educational use under the book's CC BY 4.0 license; where an example
depends on a third-party library (for example the Crypto++ examples), that
library's own license applies to the library.
