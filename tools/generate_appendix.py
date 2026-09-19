#!/usr/bin/env python3
"""Build docs/appendix_b.md from the repository itself.

Nothing here is typed by hand. The build table, the gate table and the
skills table are all read off the filesystem, so the printed appendix
cannot drift away from what the repository actually contains.

    python tools/generate_appendix.py

Exits 0 when the appendix is written, 1 when the repository is not
shaped the way this script expects.
"""
import ast
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "docs", "appendix_b.md")

# Repository tooling is not a gate, whatever its exit code looks like.
NOT_GATES = {os.path.join("tools", "as_hook.py"),
             os.path.join("tools", "generate_appendix.py"),
             os.path.join("tools", "make_readme.py")}

SKIP_DIRS = (".git", "source", "__pycache__", ".venv", ".build",
             "venv", "env", "node_modules")


def read(path):
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            return f.read()
    except OSError:
        return ""


def cell(text, limit=160):
    """Flatten text so it survives a markdown table cell.

    Quoted docstrings sometimes carry a dash this repository does not
    use in its own prose, so it is normalised to a comma here.
    """
    text = re.sub(r"\s+", " ", (text or "").strip())
    text = re.sub(r"\s*[—–]\s*", ", ", text)
    text = text.replace("|", "\\|")
    if len(text) > limit:
        cut = text[:limit].rsplit(" ", 1)[0]
        text = cut + "..."
    return text


def first_sentence(text):
    text = re.sub(r"\s+", " ", (text or "").strip())
    m = re.match(r"(.+?[.!?])(\s|$)", text)
    return m.group(1) if m else text


def section(md, heading):
    """Return the body of a '## heading' section of a markdown file."""
    pat = r"^##\s+" + re.escape(heading) + r"\s*$"
    m = re.search(pat, md, re.M)
    if not m:
        return ""
    rest = md[m.end():]
    nxt = re.search(r"^##\s+", rest, re.M)
    return rest[:nxt.start()] if nxt else rest


def code_block(md):
    m = re.search(r"```\n(.*?)```", md, re.S)
    return m.group(1).strip() if m else ""


def chapter_of(relpath):
    """Chapter number from a path like builds/07-slug/gates.py."""
    parts = relpath.replace("\\", "/").split("/")
    if len(parts) > 1 and parts[0] == "builds":
        m = re.match(r"(\d+)-", parts[1])
        if m:
            return int(m.group(1))
    return None


def is_gate(path):
    """A gate asserts, or exits with something that is not plain 0.

    This is read from the code rather than from a list, so a gate
    added later appears in the appendix without anyone editing it.
    """
    try:
        tree = ast.parse(read(path))
    except SyntaxError:
        return False
    # An assertion inside try/except is a demonstration, not a gate:
    # it is caught, so it never reaches the exit code.
    caught = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Try):
            for stmt in node.body:
                for inner in ast.walk(stmt):
                    if isinstance(inner, ast.Assert):
                        caught.add(id(inner))
    for node in ast.walk(tree):
        if isinstance(node, ast.Assert) and id(node) not in caught:
            return True
        if isinstance(node, ast.Call):
            func = node.func
            name = getattr(func, "attr", getattr(func, "id", ""))
            if name != "exit":
                continue
            if not node.args:
                continue
            arg = node.args[0]
            zero = (isinstance(arg, ast.Constant) and arg.value == 0)
            if not zero:
                return True
    return False


def docstring_of(path):
    """The docstring, or the leading comment, or an honest blank."""
    text = read(path)
    try:
        doc = ast.get_docstring(ast.parse(text)) or ""
    except SyntaxError:
        doc = ""
    if doc.strip():
        return doc
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("#!"):
            continue
        if line.startswith("#"):
            return line.lstrip("#").strip()
        if line:
            break
    return ""


def collect_builds():
    base = os.path.join(ROOT, "builds")
    rows = []
    if not os.path.isdir(base):
        return rows
    for name in sorted(os.listdir(base)):
        d = os.path.join(base, name)
        if not os.path.isdir(d):
            continue
        md = read(os.path.join(d, "README.md"))
        what = first_sentence(section(md, "What this build does"))
        run = code_block(section(md, "How to run it"))
        cmds = [l.strip() for l in run.splitlines() if l.strip()]
        m = re.match(r"(\d+)-", name)
        rows.append({
            "chapter": int(m.group(1)) if m else None,
            "dir": "builds/" + name,
            "what": what,
            "run": cmds,
        })
    return rows


def collect_gates():
    rows = []
    for base, dirs, files in os.walk(ROOT):
        dirs[:] = [x for x in dirs if x not in SKIP_DIRS]
        for f in sorted(files):
            if not f.endswith(".py"):
                continue
            full = os.path.join(base, f)
            rel = os.path.relpath(full, ROOT)
            if rel in NOT_GATES:
                continue
            if not is_gate(full):
                continue
            rows.append({
                "path": rel.replace("\\", "/"),
                "checks": first_sentence(docstring_of(full)),
                "chapter": chapter_of(rel),
            })
    rows.sort(key=lambda r: (r["chapter"] is None, r["chapter"] or 0,
                             r["path"]))
    return rows


def skill_description(d):
    """Read a skill's description from its SKILL.md."""
    md = read(os.path.join(d, "SKILL.md"))
    if not md:
        return ""
    m = re.search(r"^description:\s*(.+)$", md, re.M)
    if m:
        return m.group(1).strip().strip("'\"")
    body = re.sub(r"^---.*?---", "", md, count=1, flags=re.S)
    for line in body.splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            return line
    return ""


def collect_skills():
    base = os.path.join(ROOT, "skills")
    rows = []
    if not os.path.isdir(base):
        return rows
    for name in sorted(os.listdir(base)):
        d = os.path.join(base, name)
        if not os.path.isdir(d):
            continue
        rows.append({
            "name": name,
            "dir": "skills/" + name,
            "description": skill_description(d),
            "has_skill_md": os.path.exists(os.path.join(d, "SKILL.md")),
            "has_tests": os.path.isdir(os.path.join(d, "tests")),
        })
    return rows


def render(builds, gates, skills):
    L = []
    L.append("# Appendix B: what is in the companion repository")
    L.append("")
    L.append("This appendix is generated by "
             "`tools/generate_appendix.py`, which reads")
    L.append("the repository and writes this file. It is not typed by "
             "hand, so it")
    L.append("cannot drift away from what the repository "
             "contains. If a build is")
    L.append("listed here, it is on disk. If it is on disk, it is "
             "listed here.")
    L.append("")
    L.append("Regenerate it with:")
    L.append("")
    L.append("```")
    L.append("python tools/generate_appendix.py")
    L.append("```")
    L.append("")

    L.append("## Builds")
    L.append("")
    if builds:
        L.append("%d builds, one per chapter that has runnable code."
                 % len(builds))
        L.append("")
        L.append("| Ch | Directory | What it does | How to run it |")
        L.append("|---|---|---|---|")
        for b in builds:
            ch = str(b["chapter"]) if b["chapter"] is not None else "?"
            run = "<br>".join("`%s`" % c for c in b["run"]) or "?"
            L.append("| %s | `%s` | %s | %s |"
                     % (ch, b["dir"], cell(b["what"]), run))
    else:
        L.append("No builds found.")
    L.append("")

    L.append("## Gates")
    L.append("")
    L.append("A gate checks a claim and exits non-zero when the claim "
             "fails. These")
    L.append("are found by reading the code: a script counts as a gate "
             "when it")
    L.append("asserts, or exits with something other than plain zero.")
    L.append("")
    L.append("`docs/gates.md` gives the command to run each one as a "
             "hook, and")
    L.append("explains why a hook needs `tools/as_hook.py` to block.")
    L.append("")
    if gates:
        L.append("| Ch | Path | What it checks |")
        L.append("|---|---|---|")
        for g in gates:
            ch = str(g["chapter"]) if g["chapter"] is not None else "?"
            says = cell(g["checks"]) or "no description in the file"
            L.append("| %s | `%s` | %s |" % (ch, g["path"], says))
        unattributed = [g for g in gates if g["chapter"] is None]
        if unattributed:
            L.append("")
            L.append("%d gate(s) are marked `?` because they sit "
                     "outside `builds/` and" % len(unattributed))
            L.append("carry no chapter number in their path.")
    else:
        L.append("No gates found.")
    L.append("")

    L.append("## Skills")
    L.append("")
    if skills:
        L.append("| Skill | Directory | Description "
                 "| SKILL.md | tests |")
        L.append("|---|---|---|---|---|")
        for s in skills:
            L.append("| %s | `%s` | %s | %s | %s |"
                     % (s["name"], s["dir"],
                        cell(s["description"])
                        or "no description found",
                        "yes" if s["has_skill_md"] else "no",
                        "yes" if s["has_tests"] else "no"))
    else:
        L.append("No skill directories found.")
        L.append("")
        L.append("`skills/README.md` lists the six flagship skills as "
                 "`TODO(human)`")
        L.append("entries. They are written per chapter as each one is "
                 "validated, and")
        L.append("none has been written yet. This table fills "
                 "itself in as they land.")
    L.append("")

    L.append("## Counts")
    L.append("")
    L.append("| Thing | Number |")
    L.append("|---|---|")
    L.append("| Builds | %d |" % len(builds))
    L.append("| Gates | %d |" % len(gates))
    L.append("| Skills | %d |" % len(skills))
    L.append("")
    return "\n".join(L) + "\n"


def main():
    if not os.path.isdir(os.path.join(ROOT, "builds")):
        sys.stderr.write("no builds/ directory at %s\n" % ROOT)
        return 1
    builds = collect_builds()
    gates = collect_gates()
    skills = collect_skills()
    if not builds:
        sys.stderr.write("builds/ is empty, refusing to write\n")
        return 1
    missing = [b["dir"] for b in builds if not b["what"]]
    if missing:
        sys.stderr.write("no description found for: %s\n"
                         % ", ".join(missing))
        return 1
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(render(builds, gates, skills))
    print("wrote %s" % os.path.relpath(OUT, ROOT).replace("\\", "/"))
    print("  %d builds, %d gates, %d skills"
          % (len(builds), len(gates), len(skills)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
