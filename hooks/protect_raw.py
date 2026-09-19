#!/usr/bin/env python3
"""PreToolUse hook: refuse any write into data/raw.

Chapter 5 put "data/raw is read only" in CLAUDE.md, which shapes what the
agent tries. This makes it something the agent cannot do.
"""
import json, sys

event = json.load(sys.stdin)
tool = event.get("tool_name", "")
args = event.get("tool_input", {})

target = args.get("file_path", "") or args.get("command", "")
writing = tool in ("Write", "Edit", "NotebookEdit") or (
    tool == "Bash" and any(op in target for op in (">", ">>", "mv ", "rm ", "sed -i"))
)

if writing and "data/raw" in target:
    print(json.dumps({"hookSpecificOutput": {
        "hookEventName": "PreToolUse",
        "permissionDecision": "deny",
        "permissionDecisionReason":
            "data/raw is read only. Note the problem in the log and "
            "correct it downstream, or ask me to change the raw file "
            "deliberately."}}))
    sys.exit(0)

sys.exit(0)
