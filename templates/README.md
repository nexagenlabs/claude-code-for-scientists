# Templates

Starting points you copy into your own project and edit. Nothing here
runs as part of a build.

## `CLAUDE.md.example`

Chapter 5's research project context file, as the chapter builds it. It
describes one real project: a temozolomide and nanaomycin A combination
study in U87MG cells.

Copy it to `CLAUDE.md` at the root of your own project and replace the
content with your own. The parts worth keeping are the shape and the
specificity. It states which directory is read only, what the instrument
writes when a well saturates, and what a real well identifier looks
like. Those are the facts an agent cannot infer and will otherwise
guess.

Do not copy the project description itself. It describes somebody else's
experiment.

## `verify_plate.py`

A worked example of a verification gate, carried over from the book's
chapter code. It checks four things about a cleaned plate: that the
plate arrived complete, that every well is either kept or deliberately
dropped, that the blanks were removed rather than hidden, and that the
absorbances are physically possible.

**It does not run as shipped.** It reads `data/plate_raw.csv` and
`data/plate_2026_03_11_clean.csv`, and neither file exists anywhere in
this repository. It is here as a shape to copy, not a script to
execute. `builds/07-verification-gates/gates.py` is the runnable
treatment of the same idea.

TODO(human): confirm which chapter this file belongs to. It was
supplied at the top level of the chapter code rather than inside a
chapter folder, so the autonomous build could not attribute it.
Chapter 1 and Chapter 7 are both plausible from its content.

## `gate_template.py`

TODO(human): write the Chapter 7 verification gate skeleton. The
repository layout calls for `templates/gate_template.py`, but no such
file was supplied with the chapter code, and writing one from scratch
would mean inventing the chapter's structure. The four gate families in
`builds/07-verification-gates/gates.py` are the material it should be
derived from.
