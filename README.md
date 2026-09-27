# threetinybrushes-site

Static marketing site for **Three Tiny Brushes** (paint-your-own kits for kids: personalized name kits, sibling kits, and room for seasonal kits and party packs). No build step, no framework.
Checkout stays on Square: every "Shop" button links to https://threetinybrushes.square.site.

- `index.html`: the single page. `404.html`: self-contained not-found page.
- `css/styles.css`: all styles (tokens from the design spec).
- `img/`: responsive images (400/600/800/1600 px, WebP + JPEG), logos, `og.jpg` (1200x630).
- `robots.txt`, `sitemap.xml`, favicons in the root. All asset paths are relative, so the site works at
  `https://<user>.github.io/threetinybrushes-site/` and later at `https://threetinybrushes.com/`.
- `js/monitoring.js`: Sentry (errors) + Microsoft Clarity config, loaded deferred by `index.html` and `404.html`. With `SENTRY_DSN` and `CLARITY_ID` empty it does nothing and makes no network requests. When a DSN is set, `tools/deploy_github.sh` stamps `RELEASE` with the git short sha (a small "Stamp Sentry release" commit). Hand-written, unminified JS, so no source maps are needed. Setup steps: MONITORING.md (kept outside the repo).
- `tools/`: `make_images.py` (regenerates `img/`), `build_html.py` (regenerates `index.html`, including prices and JSON-LD), `shots.py` (screenshots).

Prices in `tools/build_html.py` mirror the live Square site (checked Sep 25, 2026). Update them there and rerun if Square changes.

No CNAME yet. Add one only when the domain is ready to move.

Dino photo: `img/dino-mite-{400,600,800,1600}.{jpg,webp}` (8 files). Referenced in `index.html` by the Dino-Mite shop card
and the pickup section photo, and in JSON-LD as `img/dino-mite-1600.jpg`. To swap: replace those files (same names/sizes,
or rerun `tools/make_images.py` from a new source photo), then rerun `tools/build_html.py`.
