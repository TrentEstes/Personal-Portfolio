# Trent Estes — Portfolio

Brand and packaging design portfolio. Static site, hosted with GitHub Pages.

## Structure

- `index.html` — the whole site (built file; don't edit by hand)
- `images-web/` — web-sized images
- `fonts/` — self-hosted fonts (Bricolage Grotesque, IBM Plex Sans, IBM Plex Mono)
- `src/page.html` — layout, styles and scripts
- `src/content.py` — project text, image order and poster list
- `src/build.py` — combines the two into `index.html`

## Editing

1. Change text or images in `src/content.py` (or layout in `src/page.html`).
2. From the repo root, run `python3 src/build.py`.
3. Commit and push. GitHub Pages republishes in a minute or two.

Contact details (email, phone, LinkedIn, résumé link) are in the `SITE` block near the top of the script in `src/page.html`.
