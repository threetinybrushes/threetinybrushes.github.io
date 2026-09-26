# threetinybrushes-site

Static marketing site for **Three Tiny Brushes** (personalized kids' paint name kits). No build step, no framework.
Checkout stays on Square: every "Shop" button links to https://threetinybrushes.square.site.

- `index.html`: the single page. `404.html`: self-contained not-found page.
- `css/styles.css`: all styles (tokens from the design spec).
- `img/`: responsive images (400/600/800/1600 px, WebP + JPEG), logos, `og.jpg` (1200x630).
- `robots.txt`, `sitemap.xml`, favicons in the root. All asset paths are relative, so the site works at
  `https://<user>.github.io/threetinybrushes-site/` and later at `https://threetinybrushes.com/`.
- `tools/`: `make_images.py` (regenerates `img/`), `build_html.py` (regenerates `index.html`, including prices and JSON-LD), `shots.py` (screenshots).

Prices in `tools/build_html.py` mirror the live Square site (checked Sep 25, 2026). Update them there and rerun if Square changes.

No CNAME yet. Add one only when the domain is ready to move.
