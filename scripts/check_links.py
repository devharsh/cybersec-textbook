#!/usr/bin/env python3
"""External link checker for the cybersecurity textbook.

Extracts every external http(s) URL from the chapters, the appendices,
intro.md and references.bib, then checks each one and writes a
machine-readable JSON report.

Design notes
------------
Many publishers and standards bodies reject a bare HEAD from a script with
403 or 405, so every URL is retried with a GET carrying a normal browser
User-Agent before it is called dead. Rate limiting (429) and timeouts are
treated as "retry later", not as breakage: after the retries are exhausted
they are reported as UNVERIFIABLE so a human can judge them.

Classification
--------------
OK            final status 2xx, no redirect
REDIRECT      final status 2xx reached through one or more redirects
BROKEN        404, 410, or a DNS / TLS / connection failure that persisted
UNVERIFIABLE  403, 401, 429, timeouts, and 5xx that persisted

Usage
-----
    python3 scripts/check_links.py                    # check everything
    python3 scripts/check_links.py --out report.json  # custom report path
    python3 scripts/check_links.py --extract-only     # just list the URLs
    python3 scripts/check_links.py --workers 16
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone

try:
    import requests
    from requests.adapters import HTTPAdapter
except ImportError:  # pragma: no cover
    sys.exit("check_links.py needs the 'requests' package: pip install requests")

import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Directories that hold generated output rather than source.
SKIP_DIRS = {".git", ".build", "_build", "__pycache__", ".ipynb_checkpoints", "node_modules"}

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
)

HEADERS = {
    "User-Agent": BROWSER_UA,
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}

# A bare URL ends at whitespace or at one of these structural characters.
URL_RE = re.compile(r"""https?://[^\s<>"'`\\|]+""")

# Trailing characters that are almost always punctuation rather than URL.
TRAILING_JUNK = ".,;:!?'\""

# Hosts that are examples in the prose rather than links a reader should follow.
# A single-label host (no dot at all, such as "evil" or "host") is always a
# placeholder, and the teaching domains below are deliberately fictional: the
# phishing look-alike in Chapter 4 and PortSwigger's standard example host.
EXAMPLE_HOST_RE = re.compile(
    r"^(?:"
    r"[^.]+"                             # single-label hosts: evil, host, server
    r"|(?:\d{1,3}\.){3}\d{1,3}"          # bare IP addresses
    r"|localhost"
    r"|.*\.local"
    r"|.*\.onion"
    r"|.*\.example"
    r"|example\.(?:com|org|net|edu)"
    r"|.*\.example\.(?:com|org|net|edu)"
    r"|insecure-website\.com"            # PortSwigger's teaching domain
    r"|paypa1-support\.com"              # deliberate look-alike in Chapter 4
    r"|(?:target|victim|evil|attacker|malicious|bank|company|corp|acme|yourdomain|yoursite|mysite|test|internal|intranet|vulnerable)"
    r"(?:-[a-z]+)?\.(?:com|org|net|local|io|co)"
    r"|.*\.(?:target|victim|evil|attacker|acme)\.(?:com|org|net)"
    r")$",
    re.IGNORECASE,
)


def host_of(url: str) -> str:
    m = re.match(r"https?://([^/:?#]+)", url)
    return m.group(1).lower() if m else ""


def is_example_url(url: str) -> bool:
    """True for placeholder hosts that exist only to illustrate syntax."""
    return bool(EXAMPLE_HOST_RE.match(host_of(url)))


def clean_url(raw: str) -> str:
    """Trim trailing punctuation and unbalanced brackets off a captured URL."""
    url = raw.strip()
    # Markdown / LaTeX wrappers.
    url = url.rstrip(")]}>,;")
    changed = True
    while changed:
        changed = False
        while url and url[-1] in TRAILING_JUNK:
            url = url[:-1]
            changed = True
        # Drop one unbalanced closing bracket at a time.
        for opener, closer in (("(", ")"), ("[", "]"), ("{", "}")):
            while url.endswith(closer) and url.count(closer) > url.count(opener):
                url = url[:-1]
                changed = True
    # Strip a trailing backslash left by LaTeX escaping.
    url = url.rstrip("\\")
    return url


def iter_source_files(root: str):
    """Yield every source file whose links we care about."""
    targets = []
    intro = os.path.join(root, "intro.md")
    if os.path.isfile(intro):
        targets.append(intro)
    bib = os.path.join(root, "references.bib")
    if os.path.isfile(bib):
        targets.append(bib)
    chapters = os.path.join(root, "chapters")
    for dirpath, dirnames, filenames in os.walk(chapters):
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in sorted(filenames):
            if name.endswith((".ipynb", ".md")):
                targets.append(os.path.join(dirpath, name))
    return targets


def extract_from_notebook(path: str):
    """Yield (url, cell_index, cell_type) from a notebook's non-code cells.

    Code cells are still scanned but flagged, because a dead link inside a
    code cell is worth reporting even though the text must not be edited.
    """
    with open(path, encoding="utf-8") as fh:
        nb = json.load(fh)
    for idx, cell in enumerate(nb.get("cells", [])):
        source = cell.get("source", [])
        if isinstance(source, list):
            text = "".join(source)
        else:
            text = source or ""
        ctype = cell.get("cell_type", "unknown")
        for match in URL_RE.finditer(text):
            yield clean_url(match.group(0)), idx, ctype


def extract_from_text(path: str):
    """Yield (url, line_number, context) from a plain-text file.

    Fenced code blocks are marked so an editor knows not to touch them.
    """
    in_fence = False
    with open(path, encoding="utf-8", errors="replace") as fh:
        for lineno, line in enumerate(fh, start=1):
            stripped = line.lstrip()
            if stripped.startswith("```") or stripped.startswith("~~~"):
                in_fence = not in_fence
                continue
            ctype = "code" if in_fence else "markdown"
            for match in URL_RE.finditer(line):
                yield clean_url(match.group(0)), lineno, ctype


def collect_urls(root: str):
    """Build {url: [occurrences]} across the whole book."""
    index: dict[str, list[dict]] = {}
    for path in iter_source_files(root):
        rel = os.path.relpath(path, root)
        try:
            if path.endswith(".ipynb"):
                found = extract_from_notebook(path)
            else:
                found = extract_from_text(path)
            for url, loc, ctype in found:
                if not url or len(url) < 11:
                    continue
                index.setdefault(url, []).append(
                    {"file": rel, "location": loc, "context": ctype}
                )
        except Exception as exc:  # pragma: no cover
            print(f"  ! could not read {rel}: {exc}", file=sys.stderr)
    return index


def make_session() -> requests.Session:
    session = requests.Session()
    session.headers.update(HEADERS)
    adapter = HTTPAdapter(pool_connections=32, pool_maxsize=32, max_retries=0)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session


def check_one(url: str, timeout: float, attempts: int = 3) -> dict:
    """Check a single URL, HEAD first then GET, with retries on soft failures."""
    result = {
        "url": url,
        "status": None,
        "final_url": None,
        "classification": "UNVERIFIABLE",
        "method": None,
        "note": "",
    }

    if is_example_url(url):
        result["classification"] = "EXAMPLE"
        result["note"] = "placeholder host used to illustrate syntax, not a real link"
        return result

    session = make_session()
    last_error = ""

    for attempt in range(attempts):
        if attempt:
            time.sleep(min(2 ** attempt, 8))
        for method in ("HEAD", "GET"):
            try:
                kwargs = dict(
                    timeout=timeout,
                    allow_redirects=True,
                    verify=True,
                )
                if method == "GET":
                    kwargs["stream"] = True
                resp = session.request(method, url, **kwargs)
                code = resp.status_code
                final = resp.url
                if method == "GET":
                    try:
                        next(resp.iter_content(2048), None)
                    except Exception:
                        pass
                    resp.close()

                result["status"] = code
                result["final_url"] = final
                result["method"] = method

                if 200 <= code < 300:
                    same = final.rstrip("/") == url.rstrip("/")
                    result["classification"] = "OK" if same else "REDIRECT"
                    session.close()
                    return result
                if code in (404, 410):
                    # Confirm a HEAD 404 with a GET before declaring it dead.
                    if method == "HEAD":
                        continue
                    result["classification"] = "BROKEN"
                    result["note"] = f"HTTP {code}"
                    session.close()
                    return result
                if code in (401, 403, 405, 406, 429, 999):
                    if method == "HEAD":
                        continue  # retry as GET
                    last_error = f"HTTP {code}"
                    result["note"] = (
                        "server refuses automated requests" if code in (401, 403, 999)
                        else "rate limited" if code == 429
                        else f"HTTP {code}"
                    )
                    break  # try again on the next attempt
                if code >= 500:
                    if method == "HEAD":
                        continue
                    last_error = f"HTTP {code}"
                    result["note"] = f"server error {code}"
                    break
                # Any other 4xx: treat the GET result as authoritative.
                if method == "GET":
                    last_error = f"HTTP {code}"
                    result["note"] = f"HTTP {code}"
                    break
            except requests.exceptions.SSLError as exc:
                last_error = f"TLS error: {exc.__class__.__name__}"
                result["note"] = last_error
            except requests.exceptions.TooManyRedirects:
                last_error = "redirect loop"
                result["note"] = last_error
                result["classification"] = "BROKEN"
                session.close()
                return result
            except requests.exceptions.ConnectTimeout:
                last_error = "connect timeout"
                result["note"] = last_error
            except requests.exceptions.ReadTimeout:
                last_error = "read timeout"
                result["note"] = last_error
            except requests.exceptions.ConnectionError as exc:
                text = str(exc)
                if "Name or service not known" in text or "nodename nor servname" in text \
                        or "getaddrinfo failed" in text or "Failed to resolve" in text:
                    last_error = "DNS does not resolve"
                    result["note"] = last_error
                    result["classification"] = "BROKEN"
                    session.close()
                    return result
                last_error = "connection error"
                result["note"] = last_error
            except Exception as exc:  # pragma: no cover
                last_error = f"{exc.__class__.__name__}"
                result["note"] = last_error

    session.close()
    if not result["note"]:
        result["note"] = last_error or "no response"
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--root", default=REPO_ROOT, help="repository root")
    parser.add_argument("--out", default=None, help="path for the JSON report")
    parser.add_argument("--workers", type=int, default=12, help="parallel checks")
    parser.add_argument("--timeout", type=float, default=25.0, help="per-request timeout")
    parser.add_argument("--attempts", type=int, default=3, help="retries on soft failures")
    parser.add_argument("--extract-only", action="store_true",
                        help="list the extracted URLs and exit without checking")
    parser.add_argument("--filter", default=None,
                        help="only check URLs containing this substring")
    args = parser.parse_args()

    root = os.path.abspath(args.root)
    out_path = args.out or os.path.join(root, "scripts", "link_report.json")

    print(f"Scanning {root} ...", file=sys.stderr)
    index = collect_urls(root)
    urls = sorted(index)
    if args.filter:
        urls = [u for u in urls if args.filter in u]
    print(f"Found {len(urls)} distinct URLs in "
          f"{sum(len(v) for v in index.values())} places", file=sys.stderr)

    if args.extract_only:
        for url in urls:
            print(url)
        return 0

    results: dict[str, dict] = {}
    done = 0
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        futures = {pool.submit(check_one, u, args.timeout, args.attempts): u for u in urls}
        for fut in as_completed(futures):
            url = futures[fut]
            try:
                res = fut.result()
            except Exception as exc:  # pragma: no cover
                res = {"url": url, "status": None, "final_url": None,
                       "classification": "UNVERIFIABLE", "method": None,
                       "note": f"checker error: {exc}"}
            res["occurrences"] = index.get(url, [])
            results[url] = res
            done += 1
            if done % 25 == 0:
                print(f"  {done}/{len(urls)} checked", file=sys.stderr, flush=True)

    buckets: dict[str, list] = {}
    for url in urls:
        buckets.setdefault(results[url]["classification"], []).append(results[url])

    report = {
        "generated": datetime.now(timezone.utc).isoformat(),
        "root": root,
        "total_urls": len(urls),
        "total_occurrences": sum(len(index.get(u, [])) for u in urls),
        "summary": {k: len(v) for k, v in sorted(buckets.items())},
        "results": [results[u] for u in urls],
    }
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(report, fh, indent=2, ensure_ascii=False)
        fh.write("\n")

    print("\n=== Summary ===")
    for key in ("OK", "REDIRECT", "EXAMPLE", "UNVERIFIABLE", "BROKEN"):
        if key in buckets:
            print(f"{key:14s} {len(buckets[key])}")
    print(f"\nReport written to {out_path}")

    for key in ("BROKEN", "UNVERIFIABLE"):
        if buckets.get(key):
            print(f"\n--- {key} ---")
            for res in sorted(buckets[key], key=lambda r: r["url"]):
                files = ", ".join(sorted({o["file"] for o in res["occurrences"]}))
                print(f"{res['url']}\n    {res['note']} (status={res['status']}) [{files}]")

    return 1 if buckets.get("BROKEN") else 0


if __name__ == "__main__":
    sys.exit(main())
