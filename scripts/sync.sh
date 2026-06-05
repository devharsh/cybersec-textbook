#!/usr/bin/env bash
# One-step git sync for the cybersec-textbook.
# Usage:
#   bash scripts/sync.sh "your commit message"
#   bash scripts/sync.sh            # uses a timestamped default message
# Run this from your Mac (the sandbox cannot remove .git/index.lock).
set -e
cd "$(dirname "$0")/.."

MSG="${1:-Update book content ($(date '+%Y-%m-%d %H:%M:%S'))}"

# Clear any stale lock left by an interrupted git process.
[ -f .git/index.lock ] && rm -f .git/index.lock || true

# Never commit macOS junk, even if it was staged earlier.
git rm -r --cached --quiet --ignore-unmatch '.DS_Store' '**/.DS_Store' 2>/dev/null || true

git add -A
if git diff --cached --quiet; then
  echo "No staged changes to commit."
else
  git commit -m "$MSG"
fi
git pull --rebase origin main
git push origin main
echo "Done: committed, pulled, and pushed to origin/main."
