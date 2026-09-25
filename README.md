# SahilSharma9024.github.io

Personal portfolio — projects, experience and how to get in touch.

Plain HTML, CSS and JavaScript with a small Python build step. No framework,
no npm, no dependencies.

## Working on it

```bash
python build.py            # writes dist/
cd dist && python -m http.server 8000
```

Then open <http://localhost:8000>.

## Where things live

| Path | What it is |
| --- | --- |
| `src/partials/` | Shared chrome (nav, footer, modal) and the page sections |
| `src/data/projects.py` | Every project — add one here, not in the HTML |
| `src/covers.py` | The SVG cover art generated per project |
| `build.py` | Stitches it all into `dist/` |
| `styles.css`, `script.js` | Copied through untouched |

Adding a project means one entry in `src/data/projects.py`, one scene in
`src/covers.py`, and a rebuild. The card, the grid, the deck on the home page,
the detail page and the sitemap all follow from that.

## Deploying

Pushing to `main` triggers `.github/workflows/pages.yml`, which builds and
publishes. Repository Settings → Pages → Source must be set to
**GitHub Actions**.
