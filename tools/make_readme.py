#!/usr/bin/env python3
"""Build README.md from README.template.md plus the filesystem.

The builds table is generated rather than typed, so the README cannot
drift from what is actually in the repository. Run it after adding or
renaming a build, and commit the result.

    python tools/make_readme.py
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE = os.path.join(ROOT, "README.template.md")
OUT = os.path.join(ROOT, "README.md")
BUILDS = os.path.join(ROOT, "builds")
MARKER = "<!-- BUILDS TABLE -->"


def first_sentence(readme_path):
    """The first real sentence of a build's README, as its description."""
    if not os.path.exists(readme_path):
        return ""
    for line in open(readme_path, encoding="utf-8", errors="ignore"):
        line = line.strip()
        if not line or line.startswith(("#", "|", "-", "```", ">")):
            continue
        return line.split(". ")[0].rstrip(".") + "."
    return ""


def chapter_of(slug):
    """Builds are named NN-slug, where NN is the chapter number."""
    m = re.match(r"(\d+)[-_]", slug)
    return m.group(1).lstrip("0") or "0" if m else ""


def main():
    if not os.path.isdir(BUILDS):
        sys.exit("no builds/ directory")
    rows = []
    for slug in sorted(os.listdir(BUILDS)):
        d = os.path.join(BUILDS, slug)
        if not os.path.isdir(d):
            continue
        name = slug.split("-", 1)[-1].replace("-", " ").title()
        rows.append((chapter_of(slug), slug, name,
                     first_sentence(os.path.join(d, "README.md"))))
    if not rows:
        sys.exit("builds/ is empty")

    table = ["## The builds", "",
             f"{len(rows)} builds, one folder each. Every one stands alone: open "
             "its folder, read its README, run it, then run its gate.", "",
             "| Chapter | Build | What it does |",
             "|---------|-------|--------------|"]
    for ch, slug, name, desc in rows:
        table.append(f"| {ch} | [`{slug}`](builds/{slug}) | {desc} |")
    table += ["", "Chapters not listed here ship no build. The book says so "
              "where that is the case."]

    text = open(TEMPLATE, encoding="utf-8").read()
    if MARKER not in text:
        sys.exit(f"{TEMPLATE} has no {MARKER} line")
    text = text.replace(MARKER, "\n".join(table))
    open(OUT, "w", encoding="utf-8").write(text)
    print(f"README.md written from {len(rows)} build(s)")


if __name__ == "__main__":
    main()
