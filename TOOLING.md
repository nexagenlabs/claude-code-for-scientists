# TOOLING.md

Verified facts about the tool surface, with the date each was checked.

The rule this file exists to enforce: **no version number, file path or
command flag appears in the printed text unless it also appears here.**
If it is not in this file, it cannot go stale in print, because it is
not in print.

Entries marked `TODO(human)` could not be verified on the machine that
assembled this repository. They are headings with nothing under them on
purpose. An empty entry costs a reader a minute. A wrong one costs more
than that, and is the failure this file exists to prevent.

**Last verified: 2026-09-18**

---

## 1. Claude Code

| Fact | Value | How it was checked |
|---|---|---|
| Version | `2.1.276 (Claude Code)` | `claude --version` on 2026-09-18 |
| Installed via | npm, global | `%APPDATA%\npm\claude.ps1` |

Every chapter that names a command should say "current form in
TOOLING.md" rather than promising the printed form is still correct.

TODO(human): start the changelog at the bottom of this file from this
version, and add an entry whenever one of these values moves.

---

## 2. The interpreter

Verified on 2026-09-18.

| Fact | Value |
|---|---|
| Working command | `python` |
| `python3` | Not available. Resolves to the Microsoft Store alias stub and exits with "Python was not found". |
| Version | Python 3.14.0 |
| Location | `C:\Python314\python.exe` |

`TASK.md` and much of the book are written with `python3`, which is
correct on macOS and Linux and wrong on this machine. Commands in this
repository use `python`. Substitute whichever runs on yours.

Other interpreters present, none of which carried the scientific stack:

| Version | Location |
|---|---|
| 3.12.10 | `%LOCALAPPDATA%\Programs\Python\Python312\python.exe` |
| 3.10 | `%LOCALAPPDATA%\Programs\Python\Python310\python.exe` |

---

## 3. Packages the builds were verified against

None of these were installed on this machine. A virtual environment was
created from Python 3.12.10 and they were installed into it, for the
reasons in `NOTES_FOR_HUMAN.md`. Every build output in this repository
was produced by that environment.

Verified on 2026-09-18 by importing each one and reading `__version__`.

| Package | Version |
|---|---|
| Python | 3.12.10 |
| numpy | 2.5.3 |
| pandas | 3.0.6 |
| scipy | 1.18.1 |
| matplotlib | 3.11.2 |
| openpyxl | 3.1.5 |
| pillow | 12.3.0 |
| pyyaml | 6.0.3 |

Exact pins for the whole environment are in `requirements.lock.txt`.

Note that pandas 3 and numpy 2 are both major versions ahead of what
much published analysis code was written against. If a build behaves
differently for you, compare your versions against this table first.

---

## 4. Operating system

Verified on 2026-09-18.

| Fact | Value |
|---|---|
| Edition | Microsoft Windows 11 Home Single Language |
| Version | 10.0.26200 |
| Build | 26200 |
| Architecture | 64-bit |
| Shell used | PowerShell 5.1.26100.9444, and Git Bash |

One Windows behaviour is recorded in `hooks/README.md` and worth
repeating here: PowerShell puts a byte order mark at the front of
anything it pipes to a native program, which makes `json.load` refuse
the input. It affects testing a hook by hand. It does not affect an
installed hook.

---

## 5. Hook event names

| Fact | Value | How it was checked |
|---|---|---|
| The event `protect_raw.py` is written for | `PreToolUse` | The script emits this name in its own output, and the string is present in the installed `claude.exe`. |

TODO(human): verify the full set of hook event names against current
documentation. Only the one name above could be verified here, and one
name is not the list the chapters need.

---

## 6. Settings file location and shape

| Fact | Value | How it was checked |
|---|---|---|
| Project settings path | `.claude/settings.json` | Present in this repository and read by the run. |
| Permissions block | A `permissions` object holding `allow` and `deny` arrays of `Tool(pattern)` strings | Read from the supplied `.claude/settings.json`. |

TODO(human): verify the shape of the hooks block against current
documentation. The key that holds it, the way a matcher is expressed
and the field names inside it could not be verified on this machine,
so `.claude/settings.example.json` carries a `TODO(human)` rather than a
guess. Fill that in, then record the shape here.

TODO(human): record the user-level settings file location as distinct
from the project-level one. Only the project-level path was observed.

---

## 7. Skills directory layout

TODO(human): verify against current docs. The layout this repository
intends to use is one directory per skill holding `SKILL.md`,
`scripts/`, `testdata/` and `tests/`. That is the book's plan for the
directory, not a verified statement about what Claude Code reads, and
the two need to agree before either goes into print.

---

## 8. MCP configuration shape

TODO(human): verify against current docs. The repository layout calls
for an `mcp/` directory holding server configurations for PubMed,
CrossRef and PDB. No such configuration file was supplied with the
chapter code, and nothing about the format could be verified on this
machine.

---

## Changelog

| Date | What changed |
|---|---|
| 2026-09-18 | File created by the autonomous build. Sections 1 to 4 verified on this machine. Sections 5 to 8 are headings awaiting a documentation pass. |
