# Rafael de Morais Pinto | Portfolio and Resume

Personal portfolio and PDF resume built with Python and Jinja2 and published on GitHub Pages.

[View portfolio](https://rrafaelpinto.github.io/) · [Resume (PDF)](https://rrafaelpinto.github.io/resume.pdf)

## Local preview

Use Python 3.12, the version used by the deployment workflow.

```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python build.py
python -m http.server -d dist 8000
```

Open [localhost:8000](http://localhost:8000). The build generates the site and PDF in `dist/`.

For an HTML-only preview, run `python build.py --no-pdf`. The site builds without loading WeasyPrint, and the resume link requires a full build.

PDF generation requires Pango. On Ubuntu, install `libpango-1.0-0` and `libpangoft2-1.0-0`. On macOS, run `brew install pango`.

## Content and layout

The website and PDF use the profile data in [`data/resume.yaml`](data/resume.yaml). The website layout lives in [`templates/index.html.j2`](templates/index.html.j2) and [`static/style.css`](static/style.css). The PDF has its own [template](templates/resume.html.j2), which includes a short project description.

## Deployment

Set the GitHub Pages source to **GitHub Actions** under **Settings → Pages**. The [deploy workflow](.github/workflows/deploy.yml) builds and publishes the site on pushes to `main` and supports manual runs.
