#!/usr/bin/env python3
"""Run a gate as a hook.

A gate run from the shell exits 1 on failure, which is the Unix
convention. A hook that exits 1 does not block: Claude Code treats it as
a non-blocking error and the action proceeds. Only exit 2 blocks.

This wrapper runs the gate and translates the failure code, so one
script can serve both purposes without either being wrong.

    usage: as_hook.py python3 gates.py
"""
import subprocess, sys

if len(sys.argv) < 2:
    sys.exit("usage: as_hook.py <command> [args...]")

sys.stdin.read()                      # the hook payload; the gate ignores it
run = subprocess.run(sys.argv[1:], capture_output=True, text=True)
sys.stdout.write(run.stdout)
if run.returncode != 0:
    sys.stderr.write(run.stderr or run.stdout)
    sys.exit(2)                       # the only code that blocks
sys.exit(0)
