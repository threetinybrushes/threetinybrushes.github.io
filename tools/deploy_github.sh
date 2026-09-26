#!/usr/bin/env bash
# Run after `gh auth login` (as airdrew32). Creates the public repo, pushes main, enables Pages from main /.
set -euo pipefail
cd "$(dirname "$0")/.."
gh auth status
gh repo create airdrew32/threetinybrushes-site --public --source=. --remote=origin --push \
  --description "Static marketing site for Three Tiny Brushes. Checkout stays on Square."
gh api -X POST repos/airdrew32/threetinybrushes-site/pages -f 'source[branch]=main' -f 'source[path]=/' \
  || gh api repos/airdrew32/threetinybrushes-site/pages
echo "Preview (after the first Pages build, ~1 min): https://airdrew32.github.io/threetinybrushes-site/"
