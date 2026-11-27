import os
"""Cryptographic erase: destroy the key, not the data.
One drawing, two label sets: the cybersecurity book (ch17) and the Bedrock book (bk)."""
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fig import *
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out", "") + ""

LABELS = {
    "ch17_crypto_erase": {
        "title": "Cryptographic erase: destroy the key, not the data",
        "steps": [("lock", "Encrypt from", "the first write", "a self-encrypting drive", "encrypts every block"),
                  ("key", "Find every", "key copy", "media key, wrapping key,", "backups, escrow"),
                  ("chip", "Zeroize", "the keys", "NVMe Sanitize crypto", "erase, or Format SES=2"),
                  ("certificate", "Verify and", "certify", "ciphertext stays, now", "unreadable; record it")],
        "fails": [("Plaintext written before", "encryption was turned on"),
                  ("A key copy survives", "in a backup or escrow"),
                  ("Firmware that does not", "really encrypt or zeroize")]},
    "bk_crypto_erase": {
        "title": "Crypto-shredding Bedrock data with a customer managed key",
        "steps": [("lock", "Encrypt from", "creation", "custom model, knowledge", "base, agent, S3 data"),
                  ("key", "Find every", "copy", "other keys, replicas,", "logs, exports"),
                  ("trash", "Schedule key", "deletion", "AWS KMS waits 7 to 30", "days, then deletes"),
                  ("certificate", "Verify and", "record", "resources fail to decrypt;", "keep the CloudTrail log")],
        "fails": [("Resource created with an", "AWS owned key you cannot delete"),
                  ("A copy encrypted under", "a different key survives"),
                  ("Data keys a service", "already holds in memory")]},
}

def draw(name):
    L = LABELS[name]
    p = Fig(1180, 446, L["title"],
            "Four numbered steps from left to right: encrypt the data from the first write, find every copy of the key, "
            "destroy the keys, and verify and record the result, leaving ciphertext that can no longer be read. "
            "A fifth panel below lists three ways the erase fails: plaintext written before encryption, a surviving key "
            "copy, and an implementation that does not really encrypt or destroy the key.")
    W, G, X0 = 266, 25, 18
    for i, (ic, a, b, s1, s2) in enumerate(L["steps"]):
        x = X0 + i * (W + G); n = i + 1
        p.rect(x, 52, W, 222, "#eef5fc" if n < 4 else "#edf7ee", BLUE if n < 4 else GREEN, 2, rx=14, step=n)
        p.icon(ic, x + W / 2, 106, 58, step=n)
        p.text(x + W / 2, 162, a, 15, INK, "bold", step=n)
        p.text(x + W / 2, 181, b, 15, INK, "bold", step=n)
        p.text(x + W / 2, 214, s1, 12.5, MUTED, step=n)
        p.text(x + W / 2, 232, s2, 12.5, MUTED, step=n)
        p.badge(n, x + W - 20, 72, step=n, color=BLUE if n < 4 else GREEN)
        if i < 3:
            p.arrow([(x + W + 3, 163), (x + W + G - 3, 163)], color=INK, step=n + 1, width=2.2)
    # 5: how it fails
    p.zone(18, 296, 1144, 132, "How cryptographic erase fails", color=RED, fill="#fdeeee", step=5)
    p.badge(5, 1142, 316, step=5, color=RED)
    for i, (a, b) in enumerate(L["fails"]):
        x = 60 + i * 380
        p.icon("cross", x + 10, 372, 34, step=5)
        p.text(x + 38, 366, a, 14, INK, "bold", anchor="start", step=5)
        p.text(x + 38, 386, b, 14, INK, "bold", anchor="start", step=5)
    p.save(OUT + name)

if __name__ == "__main__":
    for nm in LABELS: draw(nm)
    print("ok")
