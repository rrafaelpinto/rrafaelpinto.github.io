"""Build the static site and the PDF resume from data/resume.yaml into dist/."""

import argparse
import datetime as dt
import json
import shutil
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).parent
DIST = ROOT / "dist"
SITE_URL = "https://rrafaelpinto.github.io/"


def load_data() -> dict:
    data = yaml.safe_load((ROOT / "data" / "resume.yaml").read_text(encoding="utf-8"))
    data["build_date"] = dt.date.today().strftime("%b %Y")
    data["site_url"] = SITE_URL
    basics = data["basics"]
    person = {
        "@context": "https://schema.org",
        "@type": "Person",
        "name": basics["name"],
        "jobTitle": basics["title"],
        "description": basics["tagline"],
        "url": SITE_URL,
        "email": f"mailto:{basics['email']}",
        "sameAs": [link["url"] for link in basics["links"]],
        "knowsAbout": [item for group in data["skills"] for item in group["items"]][:20],
        "alumniOf": sorted({e["institution"] for e in data["education"]}),
    }
    data["person_jsonld"] = json.dumps(person, ensure_ascii=False).replace("</", "<\\/")
    return data


def write_seo_files() -> None:
    today = dt.date.today().isoformat()
    (DIST / "robots.txt").write_text(f"User-agent: *\nAllow: /\nSitemap: {SITE_URL}sitemap.xml\n", encoding="utf-8")
    urls = "".join(
        f"  <url><loc>{SITE_URL}{path}</loc><lastmod>{today}</lastmod></url>\n"
        for path in ("", "resume.pdf")
    )
    (DIST / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        f"{urls}</urlset>\n",
        encoding="utf-8",
    )


def render(env: Environment, template: str, data: dict) -> str:
    return env.get_template(template).render(**data)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-pdf", action="store_true", help="Skip PDF generation.")
    args = parser.parse_args()

    env = Environment(
        loader=FileSystemLoader(ROOT / "templates"),
        undefined=StrictUndefined,
        autoescape=True,
    )
    data = load_data()

    if DIST.exists():
        shutil.rmtree(DIST)
    shutil.copytree(ROOT / "static", DIST)

    (DIST / "index.html").write_text(render(env, "index.html.j2", data), encoding="utf-8")
    resume_html = render(env, "resume.html.j2", data)
    (DIST / "resume.html").write_text(resume_html, encoding="utf-8")

    if not args.no_pdf:
        from weasyprint import HTML

        HTML(string=resume_html, base_url=str(ROOT)).write_pdf(DIST / "resume.pdf")

    write_seo_files()
    print(f"Built {DIST}")


if __name__ == "__main__":
    main()
