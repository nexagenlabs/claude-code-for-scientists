# Gate inventory

Every gate in this repository, what it checks, and how to run it as a
hook that actually blocks.

## Why a wrapper exists

A gate run from the shell exits 1 when it fails. That is the Unix
convention and it is correct.

A Claude Code hook that exits 1 does not block. The agent treats it as a
non-blocking error and the action proceeds. Only exit 2 blocks.

`tools/as_hook.py` runs a gate, passes its output through, and turns a
non-zero exit into exit 2. One script then serves both purposes without
either being wrong. The gates below are unmodified: their exit codes are
correct for the command line, and the wrapper is the mechanism that
makes them block. This is Chapter 20.

## Running a gate as a hook

```
python tools/as_hook.py python <gate>
```

The wrapper reads the hook payload from standard input and discards it,
because these gates inspect files rather than the payload.

Every gate below is listed with two commands. The first runs it the way
its build README runs it, which exits 0 on pass and 1 on failure. The
second runs the same script through the wrapper, which exits 0 on pass
and 2 on failure. Nothing about the gate changes between them.

**The working directory matters.** Every gate below reads its inputs
from the current directory. A hook must run with the build directory as
its working directory, not the repository root. Paths in the table are
relative to the repository root, and the commands assume you have
changed into the build directory first.

Field names and event names for wiring a hook are version-dependent.
Check `TOOLING.md` before copying anything into a settings file.

---

## The gates

### `builds/04-first-session/tests/gate_plate.py`

Chapter 4. Seven checks on a cleaned plate: that all 32 wells are
accounted for as either kept or excluded, that no well appears twice,
that every sample identifier was recognised, that every excluded row
carries a reason, that absorbances fall between 0 and 4, that no
unplanned treatment appeared, and that there is one time point.

```
cd builds/04-first-session
python tests/gate_plate.py
python ../../tools/as_hook.py python tests/gate_plate.py
```

### `builds/07-verification-gates/gates.py`

Chapter 7. Four families of gate over the plate pipeline.

- Conservation: nothing appears or disappears without being counted.
- Range: every value is physically possible for the instrument.
- Invariant: DMSO normalises to 100 by construction, checked against
  what the pipeline wrote rather than recomputed.
- Provenance: the data matches what the sample sheet said was on the
  plate.

It takes the four file paths as optional arguments, so it can be run
against a faulted copy.

```
cd builds/07-verification-gates
python gates.py
python ../../tools/as_hook.py python gates.py
```

### `builds/12-publication-figures/tests/gate_figure.py`

Chapter 12. Checks a figure against the journal's stated requirements:
at least 300 dpi, 89 mm single column width within half a millimetre,
and a submittable colour mode.

```
cd builds/12-publication-figures
python tests/gate_figure.py
python ../../tools/as_hook.py python tests/gate_figure.py
```

### `builds/13-sequence-and-omics/read_accounting.py`

Chapter 13. Reads in must equal reads accounted for, per sample, at
every step. Flags any sample whose assigned fraction falls below the
threshold.

Exits 1 on the shipped fixture, where one sample has 35.5 per cent of
its reads assigned.

```
cd builds/13-sequence-and-omics
python read_accounting.py
python ../../tools/as_hook.py python read_accounting.py
```

### `builds/16-lab-data-management/manifest.py --check`

Chapter 16. Verifies a raw data directory against its checksum
manifest. It notices a file that changed, a file that went missing and
a file that was added.

The same script builds the manifest when run without `--check`, so it
is a gate only in its checking mode.

```
cd builds/16-lab-data-management
python manifest.py --check
python ../../tools/as_hook.py python manifest.py --check
```

### `builds/17-manuscript-assembly/check_numbers.py`

Chapter 17. Compares every number in the manuscript prose against the
results file. The manuscript is the claim and the results file is the
evidence.

Exits 1 on the shipped fixture, which carries three mismatches.

```
cd builds/17-manuscript-assembly
python check_numbers.py
python ../../tools/as_hook.py python check_numbers.py
```

### `builds/17-manuscript-assembly/citations.py`

Chapter 17. Resolves every DOI in the bibliography. Needs network
access, though the cached responses in `crossref_cache.json` let it run
offline.

Exits 1 on the shipped fixture, where one DOI does not resolve.

```
cd builds/17-manuscript-assembly
python citations.py
python ../../tools/as_hook.py python citations.py
```

### `builds/18-deposition/tests/deposit_check.py`

Chapter 18. Checks whether a prepared deposit would be usable by a
stranger: that a README exists and says something, that the manifest
matches the files present, that a data dictionary covers the columns,
and that nothing is present which must never be in a public deposit.

```
cd builds/18-deposition
python tests/deposit_check.py
python ../../tools/as_hook.py python tests/deposit_check.py
```

### `builds/19-grant-and-thesis-drafting/claim_check.py`

Chapter 19. Two checks on a draft: that every claim resolves to
evidence, and that the language is hedged to match the strength of that
evidence.

Exits 1 on the shipped draft, which carries three problems on purpose.

```
cd builds/19-grant-and-thesis-drafting
python claim_check.py
python ../../tools/as_hook.py python claim_check.py
```

### `builds/21-error-hunt/gate_log.py`

Chapter 21. Five checks on the defect log the chapter reports counts
from: that every row is complete, that every chapter number is one that
exists, that no defect class appears outside the seven the chapter
describes, that the class counts sum to the number of rows, and that no
defect is recorded as having been caught by rereading.

The last is the chapter's headline claim, checked against the file it is
drawn from. Exits 0 on the shipped log.

```
cd builds/21-error-hunt
python gate_log.py
python ../../tools/as_hook.py python gate_log.py
```

### `builds/02-what-an-agent-does/gated.py`

Chapter 2. One assertion in front of an analysis: that both runs report
IC50 in the same unit. It is a demonstration rather than a reusable
gate, and it is listed here because it fails the way a gate fails.

Exits 1 on the shipped fixture, where the two files disagree on units.

```
cd builds/02-what-an-agent-does
python gated.py
python ../../tools/as_hook.py python gated.py
```

### `check_setup.py`

Chapter 3. The environment gate. Checks that the interpreter and the
packages the repository needs are present and importable. Run it from
the repository root before anything else.

```
python check_setup.py
python tools/as_hook.py python check_setup.py
```

### `templates/verify_plate.py`

Chapter attribution unresolved. Four gates over a cleaned plate: that
the plate arrived complete, that every well is kept or deliberately
dropped, that the blanks were removed rather than hidden, and that the
absorbances are physically possible.

**It does not run as shipped.** It reads `data/plate_raw.csv` and
`data/plate_2026_03_11_clean.csv`, and neither exists in this
repository. It is a shape to copy, not a gate to wire up. No hook
command is given for that reason.

TODO(human): confirm which chapter this file belongs to, then either
give it the data it needs or state in the file that it is illustrative.

---

## Verified

On 2026-09-18 the wrapper was checked against a real gate on
deliberately broken input. One well in a copy of
`builds/04-first-session/plate_clean.csv` had its `od595` set to
9.9999, which is outside the instrument range.

| Invocation | Exit code |
|---|---|
| `python tests/gate_plate.py` | 1 |
| `python tools/as_hook.py python tests/gate_plate.py` | 2 |

Both printed the same failure, `AssertionError: OD outside instrument
range`. The wrapper changes the exit code and nothing else.

Repeated on 2026-09-19, on the same gate and the same broken well, and
extended to the passing case and to the Chapter 21 gate.

| Gate | Input | Direct | Through the wrapper |
|---|---|---|---|
| `builds/04-first-session/tests/gate_plate.py` | as shipped | 0 | 0 |
| `builds/04-first-session/tests/gate_plate.py` | one well at 9.9999 | 1 | 2 |
| `builds/21-error-hunt/gate_log.py` | as shipped | 0 | 0 |
| `builds/21-error-hunt/gate_log.py` | one row added saying a defect was caught by rereading | 1 | 2 |

The Chapter 21 case is the useful one to repeat, because the row that
breaks it is the chapter's headline claim written into the file the
chapter draws its counts from.
