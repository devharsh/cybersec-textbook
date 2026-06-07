#!/usr/bin/env python3
"""Publish a new version of an existing Zenodo record with an updated PDF.

Used by the GitHub Action in .github/workflows/zenodo-deposit.yml on each release.
It creates a new version of the concept record, replaces the file with the current
PDF, sets the version/date, and publishes. The concept DOI always resolves to the
newest version.

Required environment variables:
  ZENODO_TOKEN          Zenodo personal access token (scopes: deposit:write, deposit:actions)
  ZENODO_CONCEPT_RECID  Numeric concept record id (the "Cite all versions" record)
Optional:
  PDF                   Path to the PDF (default: Cybersecurity_Theory_Practice_Ethics.pdf)
  VERSION               Version string, e.g. 1.1.1 (leading 'v' is stripped)
"""
import os, sys, datetime, requests

BASE = "https://zenodo.org/api"
TOKEN = os.environ["ZENODO_TOKEN"]
CONCEPT = os.environ["ZENODO_CONCEPT_RECID"]
PDF = os.environ.get("PDF", "Cybersecurity_Theory_Practice_Ethics.pdf")
VERSION = (os.environ.get("VERSION") or "").lstrip("vV").strip()
P = {"access_token": TOKEN}

def jcheck(r):
    if not r.ok:
        sys.exit(f"Zenodo API error {r.status_code} on {r.url}\n{r.text[:800]}")
    return r

# 1. find the most recent deposition for this concept (must be owned by the token)
deps = jcheck(requests.get(f"{BASE}/deposit/depositions",
              params={**P, "q": f"conceptrecid:{CONCEPT}", "sort": "mostrecent", "size": 1})).json()
if not deps:
    sys.exit(f"No depositions found for conceptrecid {CONCEPT}. Check the id and token ownership.")
latest_id = deps[0]["id"]
print("Latest deposition id:", latest_id)

# 2. create a new version draft
nv = jcheck(requests.post(f"{BASE}/deposit/depositions/{latest_id}/actions/newversion", params=P)).json()
draft = jcheck(requests.get(nv["links"]["latest_draft"], params=P)).json()
draft_id = draft["id"]
bucket = draft["links"]["bucket"]
print("New draft id:", draft_id)

# 3. remove carried-over files
for f in draft.get("files", []):
    jcheck(requests.delete(f"{BASE}/deposit/depositions/{draft_id}/files/{f['id']}", params=P))

# 4. upload the new PDF
with open(PDF, "rb") as fp:
    jcheck(requests.put(f"{bucket}/{os.path.basename(PDF)}", data=fp, params=P))
print("Uploaded:", os.path.basename(PDF))

# 5. update version + publication date
md = draft["metadata"]
if VERSION:
    md["version"] = VERSION
md["publication_date"] = datetime.date.today().isoformat()
jcheck(requests.put(f"{BASE}/deposit/depositions/{draft_id}", params=P, json={"metadata": md}))

# 6. publish
pub = jcheck(requests.post(f"{BASE}/deposit/depositions/{draft_id}/actions/publish", params=P)).json()
print("Published new version. DOI:", pub.get("doi"))
