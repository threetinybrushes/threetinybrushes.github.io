#!/usr/bin/env bash
# Run after `gh auth login` as Rachel's GitHub account (threetinybrushes).
# Creates the public user-site repo, pushes main, enables Pages. Live at https://threetinybrushes.github.io/
set -euo pipefail
cd "$(dirname "$0")/.."
OWNER=${OWNER:-threetinybrushes}
REPO="$OWNER.github.io"
# Sentry release: when js/monitoring.js has a DSN, stamp RELEASE with the short sha of the code being deployed
# (a small follow-up commit, same author as the last commit). With an empty DSN nothing is stamped or committed.
MON=js/monitoring.js
if [ -f "$MON" ] && grep -qE "^var SENTRY_DSN = '[^']+'" "$MON" \
   && ! git log -1 --format=%s | grep -q '^Stamp Sentry release'; then
  SHA=$(git rev-parse --short HEAD)
  sed -i -E "s/^var RELEASE = '[^']*'/var RELEASE = '$SHA'/" "$MON"
  if ! git diff --quiet -- "$MON"; then
    git -c user.name="$(git log -1 --format=%an)" -c user.email="$(git log -1 --format=%ae)" commit -q -m "Stamp Sentry release $SHA" -- "$MON"
    echo "Stamped Sentry release $SHA"
  fi
fi
gh repo create "$OWNER/$REPO" --public --source=. --remote=origin --push \
  || { git remote add origin "https://github.com/$OWNER/$REPO.git" 2>/dev/null || true; git push -u origin main; }
gh api -X POST "repos/$OWNER/$REPO/pages" -f 'source[branch]=main' -f 'source[path]=/' \
  || gh api "repos/$OWNER/$REPO/pages"
echo "Live (after first Pages build, ~1 min): https://$OWNER.github.io/"
