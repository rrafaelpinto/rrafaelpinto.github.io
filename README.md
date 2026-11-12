# Portfolio and resume

Personal site and PDF resume generated from a single source file, `data/resume.yaml`.

## Local build

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python build.py            # dist/index.html, dist/resume.pdf
python build.py --no-pdf   # skip WeasyPrint
python -m http.server -d dist 8000
```

WeasyPrint needs Pango on the system (`apt install libpango-1.0-0 libpangoft2-1.0-0`, or `brew install pango`).

## Deploy

1. Push to `main` on GitHub.
2. In the repo, go to Settings > Pages and set Source to "GitHub Actions".
3. Each push to `main` rebuilds and publishes the site.

For a custom domain, set it in Settings > Pages and add the DNS records GitHub shows. GitHub stores it on the Pages config, so no `CNAME` file is needed with Actions deploys.

## Updating

Edit only `data/resume.yaml`. Site and PDF stay in sync.
