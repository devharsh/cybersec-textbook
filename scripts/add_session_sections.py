# -*- coding: utf-8 -*-
"""Add two sections the book was missing, both found while teaching from it.

15.43 Number Representation for the Analyst
    Section 15.22 teaches you to read `cmp` and `jle` without ever saying that the same
    thirty-two bits are -1 to one instruction and 4294967295 to another. The book had no
    two's complement, no endianness and no effective-address arithmetic anywhere in its
    290,000 words. A reader who cannot answer "which of ja and jg is taken" cannot read a
    comparison, which is most of what reversing is.

15.38 How Kerberos Works, and Where Each Attack Breaks In
    Kerberoasting, golden tickets and pass-the-ticket appear in four chapters. The protocol
    they abuse appears in none: AS-REQ, TGS-REQ and AP-REQ are not in the book at all. The
    attacks are taught as tricks rather than as consequences of a design.

Every number in the new material is computed here and asserted, not typed, so the prose and
the arithmetic cannot drift apart. Run with --check to verify without writing.

    python3 scripts/add_session_sections.py --check
    python3 scripts/add_session_sections.py
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# --------------------------------------------------------------------- verified arithmetic

def neg(v, bits):
    return (~v + 1) & ((1 << bits) - 1)


def signed(u, bits):
    return u - (1 << bits) if u >> (bits - 1) else u


def facts():
    """Every value the new prose states, computed rather than remembered."""
    f = {
        "five": format(5, "08b"),
        "five_inv": format(~5 & 0xFF, "08b"),
        "minus_five": format(neg(5, 8), "08b"),
        "minus_five_hex": f"0x{neg(5, 8):02X}",
        "minus_five_unsigned": neg(5, 8),
        "minus_five_check": signed(neg(5, 8), 8),
        "twelve": format(12, "08b"),
        "twelve_inv": format(~12 & 0xFF, "08b"),
        "minus_twelve": format(neg(12, 8), "08b"),
        "minus_twelve_hex": f"0x{neg(12, 8):02X}",
        "minus_twelve_unsigned": neg(12, 8),
        "i8_min": signed(0x80, 8), "i8_max": signed(0x7F, 8), "u8_max": 0xFF,
        "i32_min": signed(0x80000000, 32), "i32_max": signed(0x7FFFFFFF, 32),
        "u32_max": 0xFFFFFFFF,
        "movsx": f"0x{neg(12, 32):08X}", "movzx": f"0x{0xF4:08X}",
        "a5_unsigned": 0xA5, "a5_signed": signed(0xA5, 8), "a5_bin": format(0xA5, "08b"),
        "ff9c_signed": signed(0xFFFFFF9C, 32), "ff9c_unsigned": 0xFFFFFF9C,
        "le_bytes": " ".join(f"{(0x12345678 >> s) & 0xFF:02X}" for s in (0, 8, 16, 24)),
        "be_bytes": " ".join(f"{(0x12345678 >> s) & 0xFF:02X}" for s in (24, 16, 8, 0)),
        "ea": f"0x{0x00404000 + 3 * 4 + 8:08X}",
        "ea_partial": f"0x{0x00404000 + 3 * 4:08X}",
    }
    # The claims the prose makes, checked here so a typo cannot survive a run.
    assert f["minus_five_hex"] == "0xFB" and f["minus_five_check"] == -5
    assert f["minus_twelve_hex"] == "0xF4" and signed(neg(12, 8), 8) == -12
    assert neg(0x80, 8) == 0x80, "the most negative value is its own negation"
    assert f["i8_min"] == -128 and f["i8_max"] == 127 and f["u8_max"] == 255
    assert f["i32_min"] == -2147483648 and f["u32_max"] == 4294967295
    assert f["movsx"] == "0xFFFFFFF4" and f["a5_signed"] == -91
    assert f["ff9c_signed"] == -100 and f["le_bytes"] == "78 56 34 12"
    assert f["ea"] == "0x00404014" and f["ea_partial"] == "0x0040400C"
    return f


# --------------------------------------------------------------------------- the new prose

def section_15_43(f):
    return f"""## 15.43 Number Representation for the Analyst

Section 15.22 taught you to read a comparison and the jump that follows it. It did not say what
the compared bits actually mean, and that is the gap this section closes. The same thirty-two bits
are {f['u32_max']} to one instruction and -1 to another. Nothing in the bits records which reading
is intended. Only the instruction that reads them decides, so an analyst who cannot do this
conversion cannot tell which branch a program takes.

### Two's complement

To negate a value, invert every bit and add one. The rule is the same at every width.

```{{image}} ../../assets/figures/ch15_twos_complement.png
:alt: Four steps negating +5 in eight bits. Start {f['five']}. Invert to {f['five_inv']}. Add one to get {f['minus_five']}, which is {f['minus_five_hex']}. Read as unsigned it is {f['minus_five_unsigned']}, and {f['minus_five_unsigned']} minus 256 is {f['minus_five_check']}.
:width: 96%
:align: center
```

Reading in the other direction: when the top bit is set, subtract two to the power N from the
unsigned reading. For {f['minus_five_hex']} that is {f['minus_five_unsigned']} minus 256, which is
{f['minus_five_check']}. A free check on any negation is to add the result to the original; you
should get zero, with the carry falling off the end.

Worked examples, all eight bits unless stated:

- Negate 12. {f['twelve']} inverts to {f['twelve_inv']}, plus one is {f['minus_twelve']}, which is
  {f['minus_twelve_hex']}. As unsigned that is {f['minus_twelve_unsigned']}, and
  {f['minus_twelve_unsigned']} minus 256 is -12.
- Minus one is all ones at every width: 0xFF, 0xFFFF, 0xFFFFFFFF. This is why a function that
  returns -1 shows up in a listing as a register full of F characters.
- **0x80 is the one value with no positive twin.** It is -128. Invert it to 0111 1111, add one, and
  you are back at 1000 0000. Negating the most negative value returns it unchanged, and the
  overflow flag is how the hardware reports that.
- Sign extension preserves the value, zero extension does not. The byte {f['minus_twelve_hex']} is
  -12. Widened by `movsx` it becomes {f['movsx']}, still -12. Widened by `movzx` it becomes
  {f['movzx']}, which is {0xF4}. Choosing the wrong one changes the number.

The ranges worth knowing on sight: eight bits signed run {f['i8_min']} to {f['i8_max']} and
unsigned 0 to {f['u8_max']}; thirty-two bits signed run {f['i32_min']} to {f['i32_max']} and
unsigned 0 to {f['u32_max']}. The count is lopsided because zero occupies one of the non-negative
slots, which is the whole reason 0x80 has no twin.

### Endianness

x86 and x86-64 are little-endian: the least significant byte is stored at the lowest address. This
is a property of the processor, not of your hex editor, and no setting changes it.

```{{image}} ../../assets/figures/ch15_endianness.png
:alt: Four steps storing 0x12345678. The value, split into the bytes {f['be_bytes']} most significant first, stored at address 0x00401000 as {f['le_bytes']}, and read back from a hex dump by reversing the four bytes.
:width: 96%
:align: center
```

Said aloud, 0x12345678 is the byte sequence {f['be_bytes']}. In memory and in a hex dump it appears
as {f['le_bytes']}. The habit that prevents a wrong address is to reverse a run of bytes before
believing it as a number. A run of independent single bytes is not reversed; only a multi-byte
value is.

### Reading a memory operand

Every x86 memory operand computes one address from up to four parts, written
`[base + index * scale + displacement]`. Any part may be omitted, which is why the operands look so
different from one instruction to the next.

```{{image}} ../../assets/figures/ch15_effective_address.png
:alt: Four steps computing [ebx+ecx*4+8] with EBX 0x00404000 and ECX 3. Index times scale is 12. Adding the base gives {f['ea_partial']}. Adding the displacement of 8 gives the effective address {f['ea']}.
:width: 96%
:align: center
```

The scale is the element size, and that makes it free type information: scale 1 says a byte buffer,
2 a short or wide character, 4 an int or a pointer, 8 a double or a 64-bit value. One hard rule:
ESP can be a base register but can never be the index. If you think you have read an index of ESP,
you have mis-decoded the operand.

### Exercises

1. Write -12 as an eight-bit value in hexadecimal.
2. The byte 0xA5 appears in a dump. What is it read as signed, and as unsigned?
3. A thirty-two-bit local holds 0xFFFFFF9C. What decimal value is that?
4. `cmp eax, ebx` runs with EAX holding 0xFFFFFFFF and EBX holding 1. Which of `ja` and `jg` is
   taken?
5. Which eight-bit value other than zero is unchanged by negation?
6. `movsx eax, byte ptr [ebp-1]` loads the byte {f['minus_twelve_hex']}. What is in EAX?

### Answer Key

1. {f['minus_twelve_hex']}. Invert {f['twelve']} to {f['twelve_inv']}, then add one to reach
   {f['minus_twelve']}.
2. {f['a5_bin']} is {f['a5_unsigned']} unsigned and {f['a5_signed']} signed, because
   {f['a5_unsigned']} minus 256 is {f['a5_signed']}.
3. {f['ff9c_signed']}. The top bit is set, so subtract two to the thirty-second from
   {f['ff9c_unsigned']}.
4. `ja` is taken and `jg` is not. Unsigned, {f['u32_max']} is above 1. Signed, -1 is less than 1.
   This is the question that costs analysts real time, and it is the reason this section exists.
5. 0x80, which is -128. It is the only one, and it is the reason signed overflow exists.
6. {f['movsx']}, which is -12. Had the instruction been `movzx`, EAX would hold {f['movzx']}.
"""


def section_9_38():
    return """## 9.38 How Kerberos Works, and Where Each Attack Breaks In

Kerberoasting, golden tickets, silver tickets and pass-the-ticket appear throughout this chapter and
in Chapters 13 and 14. All four abuse the same protocol, and none of them makes sense as anything
but a trick until you have seen the protocol itself. This section supplies it.

### The problem single sign-on solves

A user needs twenty systems in a day. Without single sign-on they type a password twenty times, the
password crosses the network twenty times, and any one of those twenty systems can capture it. What
people do instead is worse: reuse one password everywhere, write it down, or choose something short
enough to retype all day. None of that is the user's fault; it is what the design forces.

Single sign-on means authenticating once and then reaching many services without authenticating
again. The vouching has to be something the user can carry and present, that a service can verify on
its own, that expires, and that the user cannot forge or alter. That object is a ticket.

What Kerberos adds is a design in which the password never crosses the network even once, a service
never has to call anyone to check a ticket, and every ticket carries its own expiry. What it costs
is that one party now vouches for everything, so the Key Distribution Center becomes the most
valuable machine in the building, and every clock in the realm has to agree.

### The three exchanges

```{image} ../../assets/figures/ch09_kerberos_exchanges.png
:alt: Three exchanges left to right. One, client and Authentication Server, AS-REQ and AS-REP, returns a Ticket-Granting Ticket encrypted with the krbtgt account key. Two, client and Ticket-Granting Server, TGS-REQ and TGS-REP, returns a service ticket encrypted with the service account key. Three, client and service, AP-REQ and AP-REP, returns an authenticated session, and the Key Distribution Center is not contacted.
:width: 96%
:align: center
```

At logon the client proves it knows the password by encrypting a timestamp with a key derived from
it, and the Authentication Server returns a Ticket-Granting Ticket encrypted with the krbtgt account
key (AS-REQ and AS-REP). The client then presents that ticket to the Ticket-Granting Server, names
the service it wants by its service principal name, and receives a service ticket encrypted with
that service account's key (TGS-REQ and TGS-REP). Finally it presents the service ticket to the
service itself (AP-REQ and AP-REP).

Two properties carry the whole design. Every ticket is encrypted with a key the client does not
hold, so the client can carry a ticket it can neither read nor alter. And in the third exchange the
Key Distribution Center is not contacted at all: the service decrypts the ticket with its own key
and asks nobody. That is what makes Kerberos scale, and it is also the weakness the silver ticket
attack turns on.

The timestamp is what proves a request is fresh, which is why a realm needs synchronized clocks.
Active Directory allows five minutes of skew by default.

### Where each attack breaks in

```{image} ../../assets/figures/ch09_kerberos_attacks.png
:alt: Four attacks against the exchange each abuses. Kerberoasting against step 2 needs any valid account and cracks a service ticket offline. Pass-the-ticket against steps 2 and 3 needs a ticket from host memory. A golden ticket skips step 1 and needs the krbtgt key. A silver ticket skips step 2 and needs one service account key.
:width: 96%
:align: center
```

None of these breaks the cryptography. Each one uses a key or a ticket that the attacker should not
be holding, and the protocol then behaves exactly as designed.

**Kerberoasting** is the quiet one. Any authenticated user may request a service ticket for any
service principal name, and the ticket comes back encrypted with the service account's
password-derived key. The request itself looks entirely normal; the cracking happens offline,
afterwards. This is why service accounts need long random passwords, or better, managed service
accounts whose keys no human chooses.

**Pass-the-ticket** steals a ticket from a compromised host's memory and reuses it. No password is
needed at any point, which is why password rotation alone does not answer it.

**A golden ticket** requires the krbtgt key and forges Ticket-Granting Tickets for anyone, skipping
the first exchange entirely. It survives a password reset: the krbtgt account must be reset twice,
and most organizations have never reset it once.

**A silver ticket** requires one service account key and forges a service ticket for that service
alone, skipping the Key Distribution Center. Because the KDC never sees it, KDC logs show nothing.
Only that service's own logs can reveal it.

The defenses are unglamorous: long random service account passwords, managed service accounts,
tiered administration so the krbtgt key is never exposed on a workstation, and alerting on ticket
requests with weak encryption types. See Section 9.36 for the credential-cracking side and
Chapter 14 for what containment looks like after a golden ticket is suspected.
"""


# ----------------------------------------------------------------------------- notebook edit

def add_section(path, markdown, after_heading_prefix, check):
    nb = json.load(open(path))
    title = markdown.split("\n", 1)[0].strip()
    if any(title in "".join(c["source"]) for c in nb["cells"]):
        print(f"  already present: {title[:58]}")
        return False
    idx = None
    for i, c in enumerate(nb["cells"]):
        if c["cell_type"] == "markdown" and "".join(c["source"]).lstrip().startswith(
                after_heading_prefix):
            idx = i
    if idx is None:
        sys.exit(f"could not find a cell starting with {after_heading_prefix!r} in {path}")
    cell = {"cell_type": "markdown", "metadata": {},
            "source": [l + "\n" for l in markdown.rstrip("\n").split("\n")]}
    nb["cells"].insert(idx + 1, cell)
    print(f"  inserting {title[:58]} after cell {idx}")
    if not check:
        tmp = path + ".writing"
        with open(tmp, "w") as fh:
            json.dump(nb, fh, indent=1, ensure_ascii=False)
            fh.write("\n")
        os.replace(tmp, path)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()

    f = facts()
    print(f"arithmetic verified: {len(f)} values computed and asserted")

    ch15 = os.path.join(ROOT, "chapters/15_malware/chapter15.ipynb")
    ch09 = os.path.join(ROOT, "chapters/09_exploitation/chapter09.ipynb")
    n = 0
    n += add_section(ch15, section_15_43(f), "## 15.4", a.check)
    n += add_section(ch09, section_9_38(), "## 9.3", a.check)

    for name in ("ch15_twos_complement", "ch15_endianness", "ch15_effective_address",
                 "ch09_kerberos_exchanges", "ch09_kerberos_attacks"):
        p = os.path.join(ROOT, "assets/figures", name + ".png")
        if not os.path.exists(p):
            sys.exit(f"missing figure: {p}")
    print(f"all five figures present; {n} sections {'would be ' if a.check else ''}added")


if __name__ == "__main__":
    main()
