#!/usr/bin/env python3
"""Safe text substitution helper for the textbook.

Edits only markdown/raw notebook cells and non-fenced regions of .md files.
Never touches code cells or fenced code blocks. Validates that every notebook
still parses as JSON after the write, and preserves the source-as-list-of-lines
structure by substituting inside each list element rather than rejoining.
"""

from __future__ import annotations

import json
import os
import re
import sys

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _resplit(text: str, had_trailing_newline: bool):
    """Split text back into notebook source form: one line per element, each
    ending in a newline except (optionally) the last."""
    parts = text.splitlines(keepends=True)
    if not parts:
        return []
    if had_trailing_newline and not parts[-1].endswith("\n"):
        parts[-1] += "\n"
    return parts


def apply_notebook_multiline(path: str, edits, cells=None, dry=False):
    """Like apply_notebook but the pattern may span newlines inside one cell."""
    with open(path, encoding="utf-8") as fh:
        original = fh.read()
    nb = json.loads(original)
    trailing_newline = original.endswith("\n")
    hits = []
    for idx, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") == "code":
            continue
        if cells is not None and idx not in cells:
            continue
        src = cell.get("source")
        if not isinstance(src, list):
            continue
        text = "".join(src)
        ends_nl = text.endswith("\n")
        new_text = text
        for old, new in edits:
            if old in new_text:
                hits.append((idx, old[:60], new_text.count(old)))
                new_text = new_text.replace(old, new)
        if new_text != text:
            cell["source"] = _resplit(new_text, ends_nl)
    if hits and not dry:
        out = json.dumps(nb, indent=1, ensure_ascii=False)
        if trailing_newline:
            out += "\n"
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(out)
        with open(path, encoding="utf-8") as fh:
            check = json.load(fh)
        assert "nbformat" in check and isinstance(check.get("cells"), list)
    return hits


def apply_notebook(path: str, edits, cells=None, dry=False):
    """edits: list of (old, new). cells: optional set of cell indices to limit to."""
    with open(path, encoding="utf-8") as fh:
        original = fh.read()
    nb = json.loads(original)
    trailing_newline = original.endswith("\n")
    hits = []
    for idx, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") == "code":
            continue
        if cells is not None and idx not in cells:
            continue
        src = cell.get("source")
        if not isinstance(src, list):
            continue
        for j, line in enumerate(src):
            for old, new in edits:
                if old in line:
                    n = line.count(old)
                    src[j] = src[j].replace(old, new)
                    hits.append((idx, j, old, n))
    if hits and not dry:
        out = json.dumps(nb, indent=1, ensure_ascii=False)
        if trailing_newline:
            out += "\n"
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(out)
        # Re-validate: the file must still parse and keep its structure.
        with open(path, encoding="utf-8") as fh:
            check = json.load(fh)
        assert "nbformat" in check and isinstance(check.get("cells"), list)
    return hits


def apply_markdown(path: str, edits, dry=False):
    """Substitute in a .md file, skipping fenced code blocks."""
    with open(path, encoding="utf-8") as fh:
        lines = fh.readlines()
    in_fence = False
    hits = []
    for i, line in enumerate(lines):
        s = line.lstrip()
        if s.startswith("```") or s.startswith("~~~"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for old, new in edits:
            if old in line:
                hits.append((i + 1, old, line.count(old)))
                lines[i] = lines[i].replace(old, new)
    if hits and not dry:
        with open(path, "w", encoding="utf-8") as fh:
            fh.writelines(lines)
    return hits


def apply_plain(path: str, edits, dry=False):
    """Substitute in a plain text file such as references.bib."""
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    hits = []
    for old, new in edits:
        n = text.count(old)
        if n:
            hits.append((old, n))
            text = text.replace(old, new)
    if hits and not dry:
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    return hits


def edit(relpath: str, edits, cells=None, dry=False, multiline=False):
    path = os.path.join(REPO, relpath)
    if relpath.endswith(".ipynb"):
        if multiline:
            hits = apply_notebook_multiline(path, edits, cells=cells, dry=dry)
        else:
            hits = apply_notebook(path, edits, cells=cells, dry=dry)
    elif relpath.endswith(".md"):
        hits = apply_markdown(path, edits, dry=dry)
    else:
        hits = apply_plain(path, edits, dry=dry)
    label = "WOULD EDIT" if dry else "EDITED"
    if hits:
        print(f"{label} {relpath}: {len(hits)} substitution site(s)")
        for h in hits:
            print(f"    {h}")
    else:
        print(f"NO MATCH  {relpath}: {[e[0][:70] for e in edits]}")
    return hits


def validate_all():
    """Confirm every notebook in the repo still parses and keeps nbformat."""
    import glob
    bad = []
    for p in sorted(glob.glob(os.path.join(REPO, "chapters", "*", "*.ipynb"))):
        try:
            with open(p, encoding="utf-8") as fh:
                nb = json.load(fh)
            assert "nbformat" in nb, "missing nbformat"
            assert isinstance(nb.get("cells"), list), "cells not a list"
            for c in nb["cells"]:
                assert "cell_type" in c and "source" in c, "malformed cell"
                assert isinstance(c["source"], list), "source not a list"
        except Exception as exc:
            bad.append((os.path.relpath(p, REPO), str(exc)))
    if bad:
        for p, e in bad:
            print(f"INVALID {p}: {e}")
        return False
    print("All notebooks parse and keep nbformat, cells and list-form source.")
    return True


if __name__ == "__main__":
    validate_all()
