# Hooks

Hooks are what turn a rule you wrote down into a rule the agent cannot
break. Chapter 5 put "data/raw is read only" in `CLAUDE.md`, which
shapes what the agent tries. A hook makes it something the agent cannot
do. This directory holds the Chapter 20 hook.

## `protect_raw.py`

A PreToolUse hook that refuses any write into `data/raw`.

It reads a JSON payload on standard input and looks at two things: the
tool being used, and the path or command it is being used on. It treats
the action as a write when the tool is `Write`, `Edit` or `NotebookEdit`,
or when the tool is `Bash` and the command contains a redirect, `mv`,
`rm` or `sed -i`. If that write touches `data/raw`, it prints a deny
decision and the action does not happen.

It always exits 0. The deny is carried in what it prints, not in the
exit code. This is the opposite of how a gate works, and the difference
is worth holding onto: a gate reports through its exit code, a
PreToolUse hook reports through its output.

The message it returns tells the agent what to do instead, which matters
more than the refusal:

> data/raw is read only. Note the problem in the log and correct it
> downstream, or ask me to change the raw file deliberately.

### Verified

Tested on 2026-09-18 against Claude Code 2.1.276 with three payloads.
`TASK.md` refers to three payloads in the script's docstring; there are
none there, so these were constructed to match what it describes.

| Payload | Tool | Path or command | Result |
|---|---|---|---|
| 1 | `Edit` | `data/raw/plate_P1.csv` | denied |
| 2 | `Bash` | `echo 1.234 > data/raw/plate_P1.csv` | denied |
| 3 | `Edit` | `data/clean/plate_clean.csv` | allowed |

Both writes into `data/raw` were denied, each returning
`permissionDecision: deny` under `hookSpecificOutput`, with
`hookEventName: PreToolUse`. The write into `data/clean` produced no
output, which is how this hook says yes.

You can repeat it. In bash, including Git Bash on Windows:

```
echo '{"tool_name":"Edit","tool_input":{"file_path":"data/raw/x.csv"}}' | python hooks/protect_raw.py
```

The single quotes are needed. Without them the shell eats the braces
and the hook receives nothing it can parse.

### Testing it from PowerShell does not work the obvious way

Piping a string into the hook from PowerShell can fail like this:

```
json.decoder.JSONDecodeError: Unexpected UTF-8 BOM (decode using utf-8-sig)
```

PowerShell can put a byte order mark at the front of what it sends
through a pipe to a native program, and `json.load` will not accept
one. Verified on 2026-09-18 and re-tested on 2026-09-19, Windows 11,
PowerShell 5.1.

It needs `$OutputEncoding` to be a UTF-8 encoding that carries a
preamble, which `[System.Text.Encoding]::UTF8` is, and Python to be
reading stdin as UTF-8. With the default `$OutputEncoding` on a stock
PowerShell 5.1 the pipe works. `NOTES_FOR_HUMAN.md` has the four cases
that were tried.

Three things work. In the order you are most likely to have them:

Git Bash, with the payload in single quotes, as shown above.

A mark-free `$OutputEncoding`, set before you pipe:

```
$OutputEncoding = New-Object System.Text.UTF8Encoding $false
```

Or write the payload without a mark and redirect it through `cmd`:

```
[System.IO.File]::WriteAllText("p.json", '{"tool_name":"Edit","tool_input":{"file_path":"data/raw/x.csv"}}', (New-Object System.Text.UTF8Encoding $false))
cmd /c "python hooks\protect_raw.py < p.json"
```

This affects testing the hook by hand and nothing else. Claude Code
sends the payload to the hook itself and does not go through a
PowerShell pipe, so a hook that fails this way at the prompt still
works when it is installed. Use Git Bash if you have it.

### What it does not do

It matches on the literal string `data/raw` appearing in the path or
command. An absolute path that reaches the same directory by another
route will not match, and neither will a relative path that climbs out
of the project and back in. It is a guard against the ordinary mistake,
not against a determined effort to get around it.

It also cannot see inside a script. A `Bash` call that runs a Python
file which writes to `data/raw` shows the hook only the name of the
script.

## Installing them

Copy `.claude/settings.example.json` to `.claude/settings.json` and fill
in the hooks wiring.

**The wiring is not filled in for you, and that is deliberate.** The
structure of a hooks block, and the names of the fields inside it, are
version-dependent. They could not be verified on the machine that
assembled this repository, so the example file carries a `TODO(human)`
rather than a guess that would look right and fail quietly.

What the example file does carry, because all three were verified:

- the event name, `PreToolUse`
- the command for the raw-data hook, `python hooks/protect_raw.py`
- the command for the gate wrapper,
  `python tools/as_hook.py python <the gate script>`

`docs/gates.md` gives the wrapper command for every gate in the
repository, and explains why a gate needs the wrapper at all. The short
version: a gate exits 1 when it fails, a hook only blocks on 2, and
`tools/as_hook.py` translates.

Check `TOOLING.md` before you wire anything up.

## A note on scope

This directory holds one hook. The repository also carries `agents/`
for the Chapter 20 sub-agent definitions and `mcp/` for the PubMed,
CrossRef and PDB server configurations. Neither has content yet.

TODO(human): write the Chapter 20 sub-agent definitions into `agents/`.
TODO(human): write the MCP server configurations into `mcp/`. The
configuration shape is version-dependent and belongs in TOOLING.md
first.
