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

## The builds

18 builds, one folder each. Every one stands alone: open its folder, read its README, run it, then run its gate.

| Chapter | Build | What it does |
|---------|-------|--------------|
| 0 | [`00-reading-code`](builds/00-reading-code) | Prints one small table five ways, then lets an assertion fail. |
| 2 | [`02-what-an-agent-does`](builds/02-what-an-agent-does) | Two readings of the same two files, one gated by an assertion. |
| 4 | [`04-first-session`](builds/04-first-session) | Turns a messy plate-reader export into a tidy, versioned dataset. |
| 6 | [`06-prompting-like-a-reviewer`](builds/06-prompting-like-a-reviewer) | Normalises one plate to its controls two different ways. |
| 7 | [`07-verification-gates`](builds/07-verification-gates) | Four families of verification gate, and a fault injector to test them. |
| 8 | [`08-git-and-environments`](builds/08-git-and-environments) | Two things that make a result hard to reproduce. |
| 9 | [`09-literature-triage`](builds/09-literature-triage) | Screens a corpus at two strictnesses, then measures both screens. |
| 10 | [`10-statistics-assumption-checks`](builds/10-statistics-assumption-checks) | Four demonstrations of counting the wrong thing. |
| 11 | [`11-survival-and-dose-response`](builds/11-survival-and-dose-response) | Fits a four-parameter logistic, and a Kaplan-Meier by hand. |
| 12 | [`12-publication-figures`](builds/12-publication-figures) | Regenerates a figure from its data rather than editing it by hand. |
| 13 | [`13-sequence-and-omics`](builds/13-sequence-and-omics) | A count matrix with a known answer and two seeded design problems. |
| 14 | [`14-docking-prep`](builds/14-docking-prep) | Builds a receptor file with the defects real PDB entries carry. |
| 15 | [`15-image-and-plate-reader`](builds/15-image-and-plate-reader) | Three kinds of plate and image data, each with a known answer. |
| 16 | [`16-lab-data-management`](builds/16-lab-data-management) | Three mechanisms for knowing that data has not quietly changed. |
| 17 | [`17-manuscript-assembly`](builds/17-manuscript-assembly) | Checks a manuscript against its own evidence. |
| 18 | [`18-deposition`](builds/18-deposition) | What a deposit needs before a stranger can use it. |
| 19 | [`19-grant-and-thesis-drafting`](builds/19-grant-and-thesis-drafting) | Two checks on a draft: are claims evidenced, is the language hedged. |
| 21 | [`21-error-hunt`](builds/21-error-hunt) | Summarises the defect log, and gates it against the chapter's claims. |

Chapters not listed here ship no build. The book says so where that is the case.

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
