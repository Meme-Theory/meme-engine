#!/usr/bin/env python3
"""
Ralph Loop Setup Script
Creates state file for in-session Ralph loop.
"""

import sys
from datetime import datetime, timezone
from pathlib import Path

HELP_TEXT = """Ralph Loop - Interactive self-referential development loop

USAGE:
  /ralph-loop [PROMPT...] [OPTIONS]

ARGUMENTS:
  PROMPT...    Initial prompt to start the loop (can be multiple words without quotes)

OPTIONS:
  --max-iterations <n>           Maximum iterations before auto-stop (default: unlimited)
  --completion-promise '<text>'  Promise phrase (USE QUOTES for multi-word)
  -h, --help                     Show this help message

DESCRIPTION:
  Starts a Ralph Loop in your CURRENT session. The stop hook prevents
  exit and feeds your output back as input until completion or iteration limit.

  To signal completion, you must output: <promise>YOUR_PHRASE</promise>

  Use this for:
  - Interactive iteration where you want to see progress
  - Tasks requiring self-correction and refinement
  - Learning how Ralph works

EXAMPLES:
  /ralph-loop Build a todo API --completion-promise 'DONE' --max-iterations 20
  /ralph-loop --max-iterations 10 Fix the auth bug
  /ralph-loop Refactor cache layer  (runs forever)
  /ralph-loop --completion-promise 'TASK COMPLETE' Create a REST API

STOPPING:
  Only by reaching --max-iterations or detecting --completion-promise
  No manual stop - Ralph runs infinitely by default!

MONITORING:
  # View current iteration:
  grep '^iteration:' .claude/ralph-loop.local.md

  # View full state:
  head -10 .claude/ralph-loop.local.md
"""


def main():
    args = sys.argv[1:]

    prompt_parts = []
    max_iterations = 0
    completion_promise = "null"

    # Parse arguments
    i = 0
    while i < len(args):
        arg = args[i]

        if arg in ('-h', '--help'):
            print(HELP_TEXT)
            sys.exit(0)

        elif arg == '--max-iterations':
            if i + 1 >= len(args) or not args[i + 1]:
                print("Error: --max-iterations requires a number argument", file=sys.stderr)
                print("", file=sys.stderr)
                print("   Valid examples:", file=sys.stderr)
                print("     --max-iterations 10", file=sys.stderr)
                print("     --max-iterations 50", file=sys.stderr)
                print("     --max-iterations 0  (unlimited)", file=sys.stderr)
                print("", file=sys.stderr)
                print("   You provided: --max-iterations (with no number)", file=sys.stderr)
                sys.exit(1)

            try:
                max_iterations = int(args[i + 1])
                if max_iterations < 0:
                    raise ValueError("negative")
            except ValueError:
                print(f"Error: --max-iterations must be a positive integer or 0, got: {args[i + 1]}", file=sys.stderr)
                print("", file=sys.stderr)
                print("   Valid examples:", file=sys.stderr)
                print("     --max-iterations 10", file=sys.stderr)
                print("     --max-iterations 50", file=sys.stderr)
                print("     --max-iterations 0  (unlimited)", file=sys.stderr)
                print("", file=sys.stderr)
                print("   Invalid: decimals (10.5), negative numbers (-5), text", file=sys.stderr)
                sys.exit(1)
            i += 2

        elif arg == '--completion-promise':
            if i + 1 >= len(args) or not args[i + 1]:
                print("Error: --completion-promise requires a text argument", file=sys.stderr)
                print("", file=sys.stderr)
                print("   Valid examples:", file=sys.stderr)
                print("     --completion-promise 'DONE'", file=sys.stderr)
                print("     --completion-promise 'TASK COMPLETE'", file=sys.stderr)
                print("     --completion-promise 'All tests passing'", file=sys.stderr)
                print("", file=sys.stderr)
                print("   You provided: --completion-promise (with no text)", file=sys.stderr)
                print("", file=sys.stderr)
                print("   Note: Multi-word promises must be quoted!", file=sys.stderr)
                sys.exit(1)
            completion_promise = args[i + 1]
            i += 2

        else:
            # Non-option argument - collect as prompt part
            prompt_parts.append(arg)
            i += 1

    # Join prompt parts
    prompt = ' '.join(prompt_parts)

    # Validate prompt
    if not prompt:
        print("Error: No prompt provided", file=sys.stderr)
        print("", file=sys.stderr)
        print("   Ralph needs a task description to work on.", file=sys.stderr)
        print("", file=sys.stderr)
        print("   Examples:", file=sys.stderr)
        print("     /ralph-loop Build a REST API for todos", file=sys.stderr)
        print("     /ralph-loop Fix the auth bug --max-iterations 20", file=sys.stderr)
        print("     /ralph-loop --completion-promise 'DONE' Refactor code", file=sys.stderr)
        print("", file=sys.stderr)
        print("   For all options: /ralph-loop --help", file=sys.stderr)
        sys.exit(1)

    # Create .claude directory if needed
    claude_dir = Path(".claude")
    claude_dir.mkdir(exist_ok=True)

    # Format completion promise for YAML
    if completion_promise and completion_promise != "null":
        completion_promise_yaml = f'"{completion_promise}"'
    else:
        completion_promise_yaml = "null"

    # Create state file
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    state_content = f"""---
active: true
iteration: 1
max_iterations: {max_iterations}
completion_promise: {completion_promise_yaml}
started_at: "{now}"
---

{prompt}
"""

    state_file = claude_dir / "ralph-loop.local.md"
    state_file.write_text(state_content, encoding='utf-8')

    # Output setup message
    max_iter_display = str(max_iterations) if max_iterations > 0 else "unlimited"
    if completion_promise != "null":
        promise_display = f"{completion_promise} (ONLY output when TRUE - do not lie!)"
    else:
        promise_display = "none (runs forever)"

    print(f"""Ralph loop activated in this session!

Iteration: 1
Max iterations: {max_iter_display}
Completion promise: {promise_display}

The stop hook is now active. When you try to exit, the SAME PROMPT will be
fed back to you. You'll see your previous work in files, creating a
self-referential loop where you iteratively improve on the same task.

To monitor: head -10 .claude/ralph-loop.local.md

WARNING: This loop cannot be stopped manually! It will run infinitely
    unless you set --max-iterations or --completion-promise.

""")

    # Output the initial prompt
    if prompt:
        print("")
        print(prompt)

    # Display completion promise requirements if set
    if completion_promise != "null":
        print("")
        print("=" * 60)
        print("CRITICAL - Ralph Loop Completion Promise")
        print("=" * 60)
        print("")
        print("To complete this loop, output this EXACT text:")
        print(f"  <promise>{completion_promise}</promise>")
        print("")
        print("STRICT REQUIREMENTS (DO NOT VIOLATE):")
        print("  - Use <promise> XML tags EXACTLY as shown above")
        print("  - The statement MUST be completely and unequivocally TRUE")
        print("  - Do NOT output false statements to exit the loop")
        print("  - Do NOT lie even if you think you should exit")
        print("")
        print("IMPORTANT - Do not circumvent the loop:")
        print("  Even if you believe you're stuck, the task is impossible,")
        print("  or you've been running too long - you MUST NOT output a")
        print("  false promise statement. The loop is designed to continue")
        print("  until the promise is GENUINELY TRUE. Trust the process.")
        print("")
        print("  If the loop should stop, the promise statement will become")
        print("  true naturally. Do not force it by lying.")
        print("=" * 60)


if __name__ == "__main__":
    main()
