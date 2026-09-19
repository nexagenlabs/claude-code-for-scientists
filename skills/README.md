# Skills

Skills are added to this directory one chapter at a time, as each one is
validated against the chapter it belongs to. A skill that has not been
run against a known input on a real chapter does not belong here, even
if it looks correct.

This is the same rule the book applies to everything else. A skill you
cannot verify is a skill you have to trust, and the argument of the book
is against trusting.

## What a skill directory contains

Each skill is one directory, laid out like this.

```
skills/
  rnaseq-qc/
    SKILL.md        what it does and when it applies
    scripts/        the code it runs
    testdata/       small, real, and including something broken
    tests/          the gate that proves the skill still works
```

The test data must be small enough to live in the repository and real
enough to be worth running. The `testdata/` directory contains something
broken on purpose, so the reader can watch the gate catch it.

## The six flagship skills

These six must exist, and pass their own gates, before the book goes
live. None of them has been written yet. Each needs to be
written against its validated chapter, which is a judgement that was not
delegated to the autonomous build that assembled this repository.

- TODO(human): write the RNA-seq QC skill, validated against Chapter 13
- TODO(human): write the docking prep skill, validated against Chapter 14
- TODO(human): write the statistical report skill with assumption
  checks, validated against Chapter 10
- TODO(human): write the LaTeX manuscript assembly skill, validated
  against Chapter 17
- TODO(human): write the citation verification skill, validated against
  Chapter 17
- TODO(human): write the figure DPI compliance skill, validated against
  Chapter 12

The chapter attributions above are read from the titles in
`CHAPTERS.md`. Confirm each one against the manuscript before
writing the skill, because the chapter that demonstrates a technique is
not always the chapter that should own the skill.

## Why this directory is nearly empty

The repository was assembled by an autonomous run whose brief put skill
authoring out of scope. Inventing skills for chapters that had not been
validated would put untested instructions in a repository people are
meant to trust. An empty directory is recoverable. A plausible wrong
skill is not.
