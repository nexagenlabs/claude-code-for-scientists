# Claude Code for Scientists

Companion code for **Claude Code for Scientists: Turn Your Data, Papers and
Lab Workflows into Reproducible Pipelines with AI Coding Agents** by
Suryaprakash Tripathy.

Each folder under `builds/` corresponds to one build in the book. Clone once
and you have everything.

```
git clone https://github.com/nexagenlabs/claude-code-for-scientists.git
cd claude-code-for-scientists
python -m venv .venv
```

Then activate it. The command differs by platform, and using the wrong one
leaves you installing into whatever Python happens to be on your PATH.

```
source .venv/bin/activate      # macOS and Linux
.venv\Scripts\activate          # Windows
```

```
pip install -r requirements.txt
python check_setup.py
```

`check_setup.py` is the gate from Chapter 3. Run it before anything else. It
changes nothing and tells you what is missing.

On Windows use `python` rather than `python3`. On many installations
`python3` resolves to a Microsoft Store stub and fails with a message that
looks like a broken install and is not one.

<!-- BUILDS TABLE -->

## Gates

Every build ships the gate that checks its output. A gate exits 0 when it
passes and 1 when it fails, which is the convention at a command line.

A hook only blocks a tool call on exit 2, so wire a gate in through
`tools/as_hook.py` rather than directly. Chapter 20 explains why, and
`docs/gates.md` lists every gate with the command to run it either way.

## Hooks and skills

`hooks/` holds the pre-tool hook from Chapter 20 that refuses any write into
`data/raw`. `skills/` holds the research skills, added one at a time as each
is validated against its chapter rather than all at once.

## Chapters and builds

`CHAPTERS.md` lists every chapter with its number and title. The companion
site reads it for the title of each chapter page. The README table above and
the appendix take a build's chapter number from its directory name, which is
why every build folder is named for its chapter.

## Tooling

Version numbers, command names and configuration shapes change faster than
books do. `TOOLING.md` records what each chapter was verified against, with
the date. Where this repository and the printed book disagree, the file is
right.

## Errata

Found an error in the book or the code? Open an issue, or email
biotech.suryaprakash@gmail.com if you would rather not use GitHub. Confirmed
corrections are listed at science.nexagenlabs.com/errata.

## Licence

Code and skills are MIT licensed. Book text, figures and tables are not.
