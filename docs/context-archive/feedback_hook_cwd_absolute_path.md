---
name: Hooks need absolute paths, not relative
description: PostToolUse hooks run in whatever CWD the last Bash `cd` left — not guaranteed to be the project root. Use $CLAUDE_PROJECT_DIR (or an absolute path) in hook commands, never relative paths
type: feedback
originSessionId: e680ace2-857b-49f5-9ebd-56985d6eee86
---
**The bug.** A PostToolUse hook configured with `"command": "python .claude/build-reminder.py"` will fail intermittently because hooks don't always run from the project root. Specifically: if an earlier Bash tool call did `cd some/subdir && ...`, the session CWD persists (per Bash tool semantics: "The working directory persists between commands"). A subsequent Write/Edit that triggers the hook runs the hook with that cwd, and `.claude/build-reminder.py` resolves relative to the wrong directory.

**The symptom.** `PostToolUse:Write hook blocking error from command: "python .claude/build-reminder.py": [python...]: can't open file 'C:\...\some_other_dir\.claude\build-reminder.py': [Errno 2] No such file or directory`.

**The fix.** Use `$CLAUDE_PROJECT_DIR` env var in hook commands:

```json
{
  "type": "command",
  "command": "python \"${CLAUDE_PROJECT_DIR:-.}/.claude/build-reminder.py\"",
  "timeout": 10
}
```

The fallback `:-.` makes it still work when the env var isn't set (older Claude Code versions, other runners), falling back to cwd — which is wrong in the pathological case but identical to the original buggy behavior, so no regression.

**How to apply.** Any hook command that references project files should use absolute paths via `$CLAUDE_PROJECT_DIR` rather than relative paths. The same applies to any hook that reads other project config — if the hook references `.claude/settings.json` or a script in `scripts/`, absolute path it.

**Also:** before declaring "done" after adding a hook, the skill now specifies a "pipe-test + fire-test" workflow. That covers the path resolution at setup, but does NOT cover the cwd-drift case (because a fresh session has the project root as cwd). The drift only shows up after `cd` calls in the session accumulate. Absolute paths prevent it entirely.
