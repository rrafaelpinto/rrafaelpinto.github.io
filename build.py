"""Build the static site and the PDF resume from data/resume.yaml into dist/."""

import argparse
import datetime as dt
import shutil
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, StrictUndefined

ROOT = Path(__file__).parent
DIST = ROOT / "dist"


def load_data() -> dict:
    data = yaml.safe_load((ROOT / "data" / "resume.yaml").read_text(encoding="utf-8"))
    data["build_date"] = dt.date.today().strftime("%b %Y")
    return data


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

    print(f"Built {DIST}")


if __name__ == "__main__":
    main()
