#!/usr/bin/env python3
"""Build the companion site for Claude Code for Scientists.

Reads the repository and writes a static site to site/dist/. The build
list comes from builds/ and the chapter titles from CHAPTERS.md, so the
site cannot describe a build that does not exist. It does not read
docs/gates.md; the gates page links to that file rather than restating it.
Run it after any change to builds/ or CHAPTERS.md and commit the output.

    python site/build_site.py

The output is self contained. No fonts, scripts or styles are fetched from
anywhere, so the site works offline and has nothing to leak.
"""
import html
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "site", "dist")
BUILDS = os.path.join(ROOT, "builds")
DOMAIN = "science.nexagenlabs.com"
REPO = "https://github.com/nexagenlabs/claude-code-for-scientists"
TITLE = "Claude Code for Scientists"

CSS = """
:root{--bg:#fbfbfa;--fg:#1a1d21;--dim:#5c6570;--rule:#dfe1e4;
      --accent:#1f4d78;--code:#f2f3f4}
@media(prefers-color-scheme:dark){
  :root{--bg:#0f1319;--fg:#e6e8ea;--dim:#97a1ac;--rule:#262c34;
        --accent:#7fb0e0;--code:#171c23}}
*{box-sizing:border-box}
body{background:var(--bg);color:var(--fg);margin:0;
     font:16px/1.65 Georgia,'Times New Roman',serif;
     -webkit-text-size-adjust:100%}
.wrap{max-width:46rem;margin:0 auto;padding:3rem 1.25rem 5rem}
h1{font-size:1.9rem;line-height:1.25;margin:0 0 .4rem}
h2{font-size:1.2rem;margin:2.6rem 0 .7rem;padding-top:1.1rem;
   border-top:1px solid var(--rule)}
h3{font-size:1rem;margin:1.6rem 0 .4rem}
p,li{margin:.7rem 0}
a{color:var(--accent)}
code,.mono{font:.88em/1.5 ui-monospace,'SFMono-Regular',Consolas,monospace;
     background:var(--code);padding:.1em .35em;border-radius:3px}
pre{background:var(--code);padding:.9rem 1rem;border-radius:4px;
    overflow-x:auto;font-size:.85rem;line-height:1.5}
pre code{background:none;padding:0}
table{border-collapse:collapse;width:100%;margin:1.1rem 0;font-size:.93rem;
      display:block;overflow-x:auto}
th,td{text-align:left;padding:.45rem .7rem;border-bottom:1px solid var(--rule);
      vertical-align:top}
th{font-weight:600;white-space:nowrap}
.lede{color:var(--dim);font-size:1.02rem}
.note{border-left:3px solid var(--rule);padding:.1rem 0 .1rem 1rem;
      color:var(--dim);font-size:.95rem}
footer{margin-top:3.5rem;padding-top:1.1rem;border-top:1px solid var(--rule);
       color:var(--dim);font-size:.88rem}
ul{padding-left:1.2rem}
"""


def esc(s):
    """Decode any entities already in the source, then escape once.

    CHAPTERS.md is extracted from the manuscript, and an extraction that
    forgets to unescape leaves things like &apos; in the text. Escaping
    that again puts the entity on the page verbatim.
    """
    return html.escape(html.unescape(s), quote=False)


def page(title, body, desc=""):
    d = f'<meta name="description" content="{html.escape(desc, quote=True)}">' if desc else ""
    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{esc(title)}</title>{d}
<style>{CSS}</style></head>
<body><div class="wrap">
{body}
<footer>
<a href="/">{esc(TITLE)}</a> &middot;
<a href="{REPO}">repository</a> &middot;
<a href="/errata">errata</a><br>
Code and skills are MIT licensed. Book text, figures and tables are not.
</footer>
</div></body></html>
"""


def read_chapters():
    """Chapter number to title, from CHAPTERS.md if present."""
    out = {}
    for name in ("CHAPTERS.md", os.path.join(".build", "source", "CHAPTERS.md"),
                 os.path.join("source", "CHAPTERS.md")):
        p = os.path.join(ROOT, name)
        if os.path.exists(p):
            for line in open(p, encoding="utf-8"):
                m = re.match(r"\|\s*(\d+)\s*\|[^|]*\|\s*([^|]+?)\s*\|", line)
                if m:
                    out[int(m.group(1))] = m.group(2).strip()
            break
    return out


def read_builds():
    """Build slug, chapter number and first-sentence description."""
    rows = []
    if not os.path.isdir(BUILDS):
        return rows
    for slug in sorted(os.listdir(BUILDS)):
        d = os.path.join(BUILDS, slug)
        if not os.path.isdir(d):
            continue
        m = re.match(r"(\d+)[-_]", slug)
        ch = int(m.group(1)) if m else None
        desc = ""
        rp = os.path.join(d, "README.md")
        if os.path.exists(rp):
            for line in open(rp, encoding="utf-8", errors="ignore"):
                line = line.strip()
                if not line or line.startswith(("#", "|", "-", "```", ">")):
                    continue
                desc = line.split(". ")[0].rstrip(".") + "."
                break
        rows.append({"slug": slug, "chapter": ch, "desc": desc})
    return rows


def index_page(chapters, builds):
    by_ch = {}
    for b in builds:
        by_ch.setdefault(b["chapter"], []).append(b)

    rows = []
    for ch in sorted(k for k in by_ch if k is not None):
        names = ", ".join(f'<code>{esc(b["slug"])}</code>' for b in by_ch[ch])
        rows.append(f"<tr><td>{ch}</td><td>{names}</td>"
                    f'<td><code>/ch{ch:02d}</code></td></tr>')
    table = ("<table><thead><tr><th>Chapter</th><th>Build</th>"
             "<th>Printed address</th></tr></thead><tbody>"
             + "".join(rows) + "</tbody></table>")

    items = []
    for ch in sorted(k for k in by_ch if k is not None):
        for b in by_ch[ch]:
            title = esc(chapters.get(ch, ""))
            items.append(
                f'<li><strong>{esc(b["slug"])}</strong>'
                + (f' &mdash; {title}' if title else "")
                + f'<br>{esc(b["desc"])} '
                + f'<code>{DOMAIN}/ch{ch:02d}</code></li>')
    listing = "<ul>" + "".join(items) + "</ul>"

    missing = sorted(set(chapters) - {b["chapter"] for b in builds})
    miss_txt = ""
    if missing:
        nums = ", ".join(str(m) for m in missing)
        miss_txt = (f"<p>Chapters {nums} ship no build, so there is no address "
                    f"for them. If you typed one, you are in the right place "
                    f"already.</p>")

    body = f"""<h1>{esc(TITLE)}</h1>
<p class="lede">Companion code for <em>Claude Code for Scientists: Turn Your
Data, Papers and Lab Workflows into Reproducible Pipelines with AI Coding
Agents</em>, by Suryaprakash Tripathy.</p>

<p>{len(builds)} builds, one folder each, in
<a href="{REPO}">one repository</a>. Clone it once and you have everything in
the book. Each build stands alone: open its folder, read its README, run it,
then run its gate.</p>

<p><strong>Start here.</strong> Chapter 3 sets up the clone, the environment
and the requirements, and ends with a script that tells you whether you are
ready: <a href="/setup"><code>{DOMAIN}/setup</code></a></p>

<h2>Which build belongs to which chapter</h2>
{table}
{miss_txt}

<h2>The builds</h2>
{listing}

<h2>Gates</h2>
<p>Every build ships the gate that checks its output. A gate exits 0 when it
passes and 1 when it fails, which is the convention at a command line. A hook
only blocks on exit 2, so a gate wired into one goes through
<code>tools/as_hook.py</code>. Chapter 20 explains why, and the
<a href="/gates">gates page</a> points at the list that gives the exact path
and both commands for every one.</p>

<h2>Tooling</h2>
<p>Version numbers, command names and configuration shapes change faster than
books do, so no chapter depends on one. <a href="{REPO}/blob/main/TOOLING.md">
TOOLING.md</a> records what each chapter was verified against, with the date.
Where the book and that file disagree, the file is right.</p>

<h2>References</h2>
<p>Appendix D as machine-readable data, with a DOI on every entry that has one
and the verification status of each: <a href="/references"><code>{DOMAIN}/references</code></a></p>

<h2>Errata</h2>
<p>Corrections to the printed book are listed on the
<a href="/errata">errata page</a>. If you have found an error in the book or
the code, please report it: the page says how.</p>
"""
    return page(TITLE, body,
                f"Companion code for Claude Code for Scientists. "
                f"{len(builds)} builds, one per chapter that ships code.")


def setup_page():
    body = f"""<h1>Setup</h1>
<p class="lede">Chapter 3. Getting from a machine with nothing installed to
one that can run every build in the book.</p>

<h2>Clone and install</h2>
<pre><code>git clone {REPO}.git
cd claude-code-for-scientists
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt</code></pre>

<h2>Check it worked</h2>
<pre><code>python check_setup.py</code></pre>
<p>It changes nothing. It reports on your Python version, the three libraries
the analysis chapters use, whether Claude Code is on your path and answering,
whether git is present, whether you are standing in a sensible directory and
whether you can write to it.</p>
<p>A failure stops the next chapter working. A warning does not.</p>

<h2>On Windows</h2>
<p class="note">Use <code>python</code> rather than <code>python3</code>.
On many Windows installations <code>python3</code> resolves to a Microsoft
Store stub and fails with a message that looks like a broken install and is
not one.</p>

<h2>If it cannot find Claude Code</h2>
<p>The commonest first-run failure is that the program installed correctly and
your shell cannot see it yet. Open a new terminal before anything else. If it
still cannot be found, the install directory is not on your PATH, and Chapter
3 covers adding it.</p>
"""
    return page(f"Setup &middot; {TITLE}", body,
                "Setting up the environment for Claude Code for Scientists.")


def errata_page():
    body = f"""<h1>Errata</h1>
<p class="lede">Confirmed corrections to the printed book.</p>

<p><strong>No corrections have been confirmed yet.</strong> This page will
list them as they are found, newest first, each with the page, what it says,
and what it should say.</p>

<h2>Reporting one</h2>
<p>Open an issue on <a href="{REPO}/issues">the repository</a>, or email
<a href="mailto:biotech.suryaprakash@gmail.com">biotech.suryaprakash@gmail.com</a>
if you would rather not use GitHub.</p>
<p>Please include the page number and what you expected instead. If it is a
number that disagrees with the code, say which build you ran and what it
printed, because that distinguishes an error in the book from an error in the
repository, and the two are fixed differently.</p>

<p class="note">Chapter 21 reports every defect found while the book was
being written, along with what caught each one. This page continues that
record past publication.</p>
"""
    return page(f"Errata &middot; {TITLE}", body,
                "Confirmed corrections to Claude Code for Scientists.")


def references_page():
    body = f"""<h1>References</h1>
<p class="lede">Appendix D as data, with the verification status of every
entry.</p>

<p class="note">This page goes live with the book. Until then, the reference
list lives in the manuscript and the checking script lives in the repository.</p>

<h2>How the list was checked</h2>
<p>Chapter 17 argues that a fabricated citation cannot be caught by reading,
because every part of it was generated to look right, and that resolving it
catches all of them in seconds. It would be poor form for this book's own
list to be unchecked.</p>
<p>Every entry was resolved against CrossRef before publication, and the
script that does it is in the repository so you can rerun it rather than take
my word for it. If a reference here fails to resolve, please report it as an
erratum.</p>
"""
    return page(f"References &middot; {TITLE}", body,
                "The reference list for Claude Code for Scientists, with "
                "resolution status.")


def gates_page(builds):
    rows = []
    for b in builds:
        ch = b["chapter"]
        rows.append(f"<tr><td>{ch if ch is not None else ''}</td>"
                    f'<td><code>{esc(b["slug"])}</code></td>'
                    f'<td><a href="{REPO}/tree/main/builds/{esc(b["slug"])}">'
                    f"builds/{esc(b['slug'])}</a></td></tr>")
    table = ("<table><thead><tr><th>Chapter</th><th>Build</th><th>Folder</th>"
             "</tr></thead><tbody>" + "".join(rows) + "</tbody></table>")
    body = f"""<h1>Gates</h1>
<p class="lede">Every build ships the gate that checks its output.</p>

<h2>Where they are and what they are called</h2>
<p>Gates are not uniform. Some sit at the root of their build and some in
its <code>tests/</code> folder, and the names vary because each is named
for what it checks rather than for being a gate. One takes an argument.</p>
<p><a href="{REPO}/blob/main/docs/gates.md">docs/gates.md</a> lists every one
with its exact path and both commands: run directly, and run as a hook. Use
it rather than guessing at a filename.</p>

<h2>The two ways to run one</h2>
<p>Run directly and a gate exits 0 when it passes and 1 when it fails, which
is the Unix convention and what you want at a command line.</p>
<pre><code>python tools/as_hook.py python &lt;the gate&gt;</code></pre>
<p>That is the other way. A hook only blocks a tool call on exit 2. Exit 1 is
treated as a non-blocking error and the action proceeds, so a gate wired in
directly reports its failure and stops nothing. The wrapper translates the
code, which lets one script be correct in both places. Chapter 20 covers
this, including the two ways a hook can end up silently absent.</p>

<h2>The builds</h2>
{table}

<p class="note">A gate you have never seen fail is not a gate. Break something
on purpose and confirm it fails, for the reason you expected.</p>
"""
    return page(f"Gates &middot; {TITLE}", body,
                "Every gate in Claude Code for Scientists, and how to run it.")


def main():
    chapters = read_chapters()
    builds = read_builds()
    if not builds:
        print("warning: builds/ is empty or missing; the site will be thin",
              file=sys.stderr)

    if os.path.isdir(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    written = {}
    written["index.html"] = index_page(chapters, builds)
    written["setup.html"] = setup_page()
    written["errata.html"] = errata_page()
    written["references.html"] = references_page()
    written["gates.html"] = gates_page(builds)

    # One redirect page per chapter that has a build, so a printed address
    # never lands on a 404. Chapters without a build go to the index.
    have = {b["chapter"] for b in builds if b["chapter"] is not None}
    for ch in sorted(have):
        slug = next(b["slug"] for b in builds if b["chapter"] == ch)
        target = f"{REPO}/tree/main/builds/{slug}"
        written[f"ch{ch:02d}.html"] = page(
            f"Chapter {ch} &middot; {TITLE}",
            f'<h1>Chapter {ch}</h1><p class="lede">'
            f'{esc(chapters.get(ch, ""))}</p>'
            f'<p>The build for this chapter is <code>{esc(slug)}</code>.</p>'
            f'<p><a href="{target}">Open it on GitHub</a>, or see '
            f'<a href="/">all builds</a>.</p>')

    for name, content in written.items():
        with open(os.path.join(DIST, name), "w", encoding="utf-8") as f:
            f.write(content)

    with open(os.path.join(DIST, "_redirects"), "w", encoding="utf-8") as f:
        for ch in sorted(have):
            f.write(f"/ch{ch:02d}   /ch{ch:02d}.html   200\n")
        for p in ("setup", "errata", "references", "gates"):
            f.write(f"/{p}   /{p}.html   200\n")
        f.write("/*   /index.html   404\n")

    print(f"site built: {len(written)} pages, {len(have)} chapter addresses")
    print(f"output: {os.path.relpath(DIST, ROOT)}")


if __name__ == "__main__":
    main()
