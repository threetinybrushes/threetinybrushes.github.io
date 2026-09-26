#!/usr/bin/env bash
# Run after `gh auth login` as Rachel's GitHub account (threetinybrushes).
# Creates the public user-site repo, pushes main, enables Pages. Live at https://threetinybrushes.github.io/
set -euo pipefail
cd "$(dirname "$0")/.."
OWNER=${OWNER:-threetinybrushes}
REPO="$OWNER.github.io"
gh repo create "$OWNER/$REPO" --public --source=. --remote=origin --push \
  || { git remote add origin "https://github.com/$OWNER/$REPO.git" 2>/dev/null || true; git push -u origin main; }
gh api -X POST "repos/$OWNER/$REPO/pages" -f 'source[branch]=main' -f 'source[path]=/' \
  || gh api "repos/$OWNER/$REPO/pages"
echo "Live (after first Pages build, ~1 min): https://$OWNER.github.io/"
