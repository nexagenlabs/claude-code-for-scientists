#!/usr/bin/env python3
"""check_setup.py, the Chapter 3 gate for Claude Code for Scientists.

Run this before Chapter 4. It checks the things the rest of the book
assumes and says plainly which ones are missing. It changes nothing.

    python3 check_setup.py      macOS, Linux
    python check_setup.py       Windows
"""
import os
import platform
import shutil
import subprocess
import sys
from pathlib import Path

PASS, FAIL, WARN = "PASS", "FAIL", "WARN"
IS_WINDOWS = platform.system() == "Windows"
results = []


def record(name, status, detail):
    results.append((name, status, detail))


def run(cmd):
    """Return (ok, first line of output). Never raises.

    On Windows the installed command is often a .CMD or .BAT shim, which
    the operating system will not execute directly from a process call.
    Those need a shell, so use one when the resolved path is a shim.
    """
    try:
        shim = str(cmd[0]).lower().endswith((".cmd", ".bat"))
        needs_shell = IS_WINDOWS and shim
        if needs_shell:
            quoted = " ".join(f'"{c}"' if " " in str(c) else str(c)
                              for c in cmd)
            out = subprocess.run(quoted, capture_output=True,
                                 text=True, timeout=30, shell=True)
        else:
            out = subprocess.run(cmd, capture_output=True,
                                 text=True, timeout=30)
        text = (out.stdout or out.stderr).strip().splitlines()
        return out.returncode == 0, (text[0] if text else "")
    except (OSError, subprocess.SubprocessError):
        return False, "could not run"


# 1. Python version. The book's code assumes 3.9 or newer.
v = sys.version_info
record("Python 3.9+", PASS if v >= (3, 9) else FAIL,
       f"found {v.major}.{v.minor}.{v.micro} "
       f"via '{Path(sys.executable).name}'")

# 2. The three libraries every analysis chapter uses.
for pkg in ("pandas", "numpy", "matplotlib"):
    try:
        mod = __import__(pkg)
        record(pkg, PASS,
               getattr(mod, "__version__", "version unknown"))
    except ImportError:
        record(pkg, FAIL, "not installed, see Chapter 3")

# 3. Claude Code itself.
claude = shutil.which("claude")
if claude:
    ok, line = run([claude, "--version"])
    if ok:
        record("Claude Code", PASS, line)
    else:
        record("Claude Code", WARN,
               f"found at {claude} but it would not report a version")
    record("Claude Code path", PASS, claude)
else:
    record("Claude Code", FAIL, "not on PATH, see Chapter 3")

# 4. Git, because Chapter 8 depends on it and reproducibility does too.
git = shutil.which("git")
if git:
    _, line = run([git, "--version"])
    record("git", PASS, line)
else:
    record("git", FAIL, "not installed")

# 5. Are we standing somewhere sensible? Running the agent in your home
#    directory gives it read access to everything you own.
cwd = Path.cwd().resolve()
home = Path.home().resolve()
if cwd == home:
    record("Working directory", FAIL,
           "this is your home directory, "
           "start in a project folder instead")
else:
    record("Working directory", PASS, str(cwd))

# 6. Can we actually write here?
probe = cwd / ".setup_write_probe"
try:
    probe.write_text("ok")
    probe.unlink()
    record("Write access", PASS, "this folder is writable")
except OSError as exc:
    record("Write access", FAIL, f"cannot write here: {exc.strerror}")

# 7. Is this folder under version control? A warning, not a failure.
inside_repo = False
if git:
    inside_repo, _ = run([git, "rev-parse", "--is-inside-work-tree"])
record("Version control", PASS if inside_repo else WARN,
       "this folder is a git repository" if inside_repo
       else "not a repository yet, Chapter 8 sets one up")

# ------------------------------------------------------- report
width = max(len(n) for n, _, _ in results)
print()
for name, status, detail in results:
    print(f"  [{status}] {name.ljust(width)}  {detail}")

failures = [n for n, s, _ in results if s == FAIL]
warnings = [n for n, s, _ in results if s == WARN]
print()
if failures:
    print(f"{len(failures)} check(s) failed: {', '.join(failures)}")
    print("Chapter 4 will not work until these pass. "
          "Chapter 3 covers each one.")
    sys.exit(1)
if warnings:
    print(f"All required checks passed, with "
          f"{len(warnings)} warning(s). You can start Chapter 4.")
else:
    print("All checks passed. Start Chapter 4.")
sys.exit(0)
