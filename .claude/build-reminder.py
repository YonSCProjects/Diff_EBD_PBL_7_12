#!/usr/bin/env python3
"""PostToolUse hook: when a source file is edited, print a reminder to rebuild the matching build_output artifact.

Input: Claude Code PostToolUse JSON on stdin.
Output: hookSpecificOutput JSON with an additionalContext reminder, or nothing (exit 0).
Non-blocking: always exit 0.
"""
import sys, json

# Force UTF-8 stdout so em-dashes, non-ASCII chars, etc. render correctly on Windows
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

def main():
    try:
        d = json.load(sys.stdin)
    except Exception:
        return

    f = (d.get("tool_input", {}) or {}).get("file_path", "") or ""
    if not f:
        return

    # Normalize Windows backslashes to forward slashes
    g = f.replace("\\", "/")

    # Skip excluded dirs
    for ex in ["/.claude/", "/.git/", "/memory/", "/node_modules/", "/build_output/"]:
        if ex in g:
            return

    # Require project root in path
    marker = "Diferential pbl for BE/"
    idx = g.find(marker)
    if idx < 0:
        return
    rel = g[idx + len(marker):]

    msg = None

    if rel == "Arduino_PBL_Program.md":
        msg = (
            "Arduino_PBL_Program.md was edited — rebuild the master document:\n"
            "  npx --yes md-to-pdf --config-file md-to-pdf.config.js Arduino_PBL_Program.md\n"
            "  npx --yes md-to-pdf --config-file md-to-pdf.config.js --as-html Arduino_PBL_Program.md\n"
            "  mv Arduino_PBL_Program.pdf Arduino_PBL_Program.html build_output/"
        )
    elif rel == "Arduino_PBL_Program_Overview.md":
        msg = (
            "Arduino_PBL_Program_Overview.md was edited — rebuild the EN overview (PDF + cards appendix):\n"
            "  node build_overview_with_cards.js en"
        )
    elif rel == "Arduino_PBL_Program_Overview_he.md":
        msg = (
            "Arduino_PBL_Program_Overview_he.md was edited — rebuild the HE overview (PDF + cards appendix):\n"
            "  node build_overview_with_cards.js he"
        )
    elif rel == "Arduino_Principles.md":
        msg = (
            "Arduino_Principles.md was edited. This file is source-of-truth but NOT directly built.\n"
            "If this is a semantic change (new/renamed/removed principle, changed evidence, added/removed design rule), "
            "also propagate the change to:\n"
            "  - Arduino_PBL_Program.md §4 (master doc, full depth)\n"
            "  - Arduino_PBL_Program_Overview.md (EN overview, compact form)\n"
            "  - Arduino_PBL_Program_Overview_he.md (HE overview, compact form)\n"
            "Then rebuild each (master via md-to-pdf, overviews via build_overview_with_cards.js)."
        )
    elif rel == "Arduino_Projects/Project_1_Light_Signals/Arduino_Project_1.md":
        msg = (
            "Arduino_Project_1.md was edited — rebuild the Project 1 PDF:\n"
            '  npx --yes md-to-pdf --config-file md-to-pdf.config.js "Arduino_Projects/Project_1_Light_Signals/Arduino_Project_1.md"\n'
            "  mv Arduino_Projects/Project_1_Light_Signals/Arduino_Project_1.pdf build_output/"
        )
    elif (rel.startswith("Arduino_Projects/Project_1_Light_Signals/reference_cards/")
          or rel.startswith("Arduino_Projects/Project_1_Light_Signals/task_cards/")) and rel.endswith(".html"):
        msg = (
            "EN navigation or reference card edited — rebuild the EN overview "
            "(cards are embedded into its appendix via puppeteer):\n"
            "  node build_overview_with_cards.js en"
        )
    elif (rel.startswith("Arduino_Projects/Project_1_Light_Signals/reference_cards_he/")
          or rel.startswith("Arduino_Projects/Project_1_Light_Signals/task_cards_he/")) and rel.endswith(".html"):
        msg = (
            "HE navigation or reference card edited — rebuild the HE overview "
            "(cards are embedded into its appendix via puppeteer):\n"
            "  node build_overview_with_cards.js he"
        )
    # style.css / card.js: inlined into overview HTML by build_overview_with_cards.js
    elif rel in ("Arduino_Projects/Project_1_Light_Signals/task_cards/style.css",
                 "Arduino_Projects/Project_1_Light_Signals/task_cards/card.js"):
        msg = (
            "Shared card stylesheet or script edited — rebuild BOTH overviews "
            "(style.css/card.js are inlined into overview HTML):\n"
            "  node build_overview_with_cards.js en\n"
            "  node build_overview_with_cards.js he"
        )

    if msg is None:
        return

    out = {
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": (
                "BUILD-OUTPUT REMINDER — " + msg
                + "\n\nYon works from build_output/ files. Do not declare the task done until build_output/ reflects the change."
            ),
        }
    }
    print(json.dumps(out, ensure_ascii=False))

if __name__ == "__main__":
    main()
