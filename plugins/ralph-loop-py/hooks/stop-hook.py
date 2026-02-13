#!/usr/bin/env python3
"""
Ralph Loop Stop Hook
Prevents session exit when a ralph-loop is active.
Feeds Claude's output back as input to continue the loop.
"""

import json
import os
import re
import sys
from pathlib import Path


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content."""
    lines = content.split('\n')
    if not lines or lines[0].strip() != '---':
        return {}, content

    frontmatter_end = -1
    for i, line in enumerate(lines[1:], 1):
        if line.strip() == '---':
            frontmatter_end = i
            break

    if frontmatter_end == -1:
        return {}, content

    # Parse simple YAML (key: value pairs)
    frontmatter = {}
    for line in lines[1:frontmatter_end]:
        if ':' in line:
            key, _, value = line.partition(':')
            key = key.strip()
            value = value.strip()
            # Remove surrounding quotes
            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1]
            elif value.startswith("'") and value.endswith("'"):
                value = value[1:-1]
            frontmatter[key] = value

    # Get content after frontmatter
    prompt_text = '\n'.join(lines[frontmatter_end + 1:]).strip()

    return frontmatter, prompt_text


def extract_promise_text(output: str) -> str:
    """Extract text from <promise> tags."""
    match = re.search(r'<promise>(.*?)</promise>', output, re.DOTALL)
    if match:
        # Normalize whitespace
        return ' '.join(match.group(1).split())
    return ""


def main():
    # Read hook input from stdin
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        hook_input = {}

    # Check if ralph-loop is active
    state_file = Path(".claude/ralph-loop.local.md")

    if not state_file.exists():
        # No active loop - allow exit
        sys.exit(0)

    try:
        content = state_file.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Warning: Failed to read state file: {e}", file=sys.stderr)
        sys.exit(0)

    frontmatter, prompt_text = parse_frontmatter(content)

    # Session-scoping: only trap the session that created this loop
    stored_session_id = frontmatter.get('session_id', '')
    if stored_session_id:
        # Derive current session ID from transcript path
        transcript_path = hook_input.get('transcript_path', '')
        current_session_id = Path(transcript_path).stem if transcript_path else ''
        if current_session_id and current_session_id != stored_session_id:
            # Different session — not ours, allow exit
            sys.exit(0)

    # Extract values
    iteration_str = frontmatter.get('iteration', '')
    max_iterations_str = frontmatter.get('max_iterations', '0')
    completion_promise = frontmatter.get('completion_promise', 'null')

    # Validate numeric fields
    try:
        iteration = int(iteration_str)
    except (ValueError, TypeError):
        print("Warning: Ralph loop: State file corrupted", file=sys.stderr)
        print(f"   File: {state_file}", file=sys.stderr)
        print(f"   Problem: 'iteration' field is not a valid number (got: '{iteration_str}')", file=sys.stderr)
        print("", file=sys.stderr)
        print("   This usually means the state file was manually edited or corrupted.", file=sys.stderr)
        print("   Ralph loop is stopping. Run /ralph-loop again to start fresh.", file=sys.stderr)
        state_file.unlink(missing_ok=True)
        sys.exit(0)

    try:
        max_iterations = int(max_iterations_str)
    except (ValueError, TypeError):
        print("Warning: Ralph loop: State file corrupted", file=sys.stderr)
        print(f"   File: {state_file}", file=sys.stderr)
        print(f"   Problem: 'max_iterations' field is not a valid number (got: '{max_iterations_str}')", file=sys.stderr)
        print("", file=sys.stderr)
        print("   This usually means the state file was manually edited or corrupted.", file=sys.stderr)
        print("   Ralph loop is stopping. Run /ralph-loop again to start fresh.", file=sys.stderr)
        state_file.unlink(missing_ok=True)
        sys.exit(0)

    # Check if max iterations reached
    if max_iterations > 0 and iteration >= max_iterations:
        print(f"Ralph loop: Max iterations ({max_iterations}) reached.")
        state_file.unlink(missing_ok=True)
        sys.exit(0)

    # Get transcript path from hook input
    transcript_path = hook_input.get('transcript_path', '')

    if not transcript_path or not Path(transcript_path).exists():
        print("Warning: Ralph loop: Transcript file not found", file=sys.stderr)
        print(f"   Expected: {transcript_path}", file=sys.stderr)
        print("   This is unusual and may indicate a Claude Code internal issue.", file=sys.stderr)
        print("   Ralph loop is stopping.", file=sys.stderr)
        state_file.unlink(missing_ok=True)
        sys.exit(0)

    # Read transcript and find last assistant message
    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Warning: Failed to read transcript: {e}", file=sys.stderr)
        state_file.unlink(missing_ok=True)
        sys.exit(0)

    # Find last assistant message (JSONL format)
    last_assistant_line = None
    for line in reversed(lines):
        if '"role":"assistant"' in line or '"role": "assistant"' in line:
            last_assistant_line = line
            break

    if not last_assistant_line:
        print("Warning: Ralph loop: No assistant messages found in transcript", file=sys.stderr)
        print(f"   Transcript: {transcript_path}", file=sys.stderr)
        print("   This is unusual and may indicate a transcript format issue", file=sys.stderr)
        print("   Ralph loop is stopping.", file=sys.stderr)
        state_file.unlink(missing_ok=True)
        sys.exit(0)

    # Parse the assistant message
    try:
        msg_data = json.loads(last_assistant_line)
        content_items = msg_data.get('message', {}).get('content', [])
        text_parts = [item.get('text', '') for item in content_items if item.get('type') == 'text']
        last_output = '\n'.join(text_parts)
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print("Warning: Ralph loop: Failed to parse assistant message JSON", file=sys.stderr)
        print(f"   Error: {e}", file=sys.stderr)
        print("   This may indicate a transcript format issue", file=sys.stderr)
        print("   Ralph loop is stopping.", file=sys.stderr)
        state_file.unlink(missing_ok=True)
        sys.exit(0)

    if not last_output:
        print("Warning: Ralph loop: Assistant message contained no text content", file=sys.stderr)
        print("   Ralph loop is stopping.", file=sys.stderr)
        state_file.unlink(missing_ok=True)
        sys.exit(0)

    # Check for completion promise
    if completion_promise and completion_promise != 'null':
        promise_text = extract_promise_text(last_output)
        if promise_text and promise_text == completion_promise:
            print(f"Ralph loop: Detected <promise>{completion_promise}</promise>")
            state_file.unlink(missing_ok=True)
            sys.exit(0)

    # Not complete - continue loop
    next_iteration = iteration + 1

    if not prompt_text:
        print("Warning: Ralph loop: State file corrupted or incomplete", file=sys.stderr)
        print(f"   File: {state_file}", file=sys.stderr)
        print("   Problem: No prompt text found", file=sys.stderr)
        print("", file=sys.stderr)
        print("   This usually means:", file=sys.stderr)
        print("     - State file was manually edited", file=sys.stderr)
        print("     - File was corrupted during writing", file=sys.stderr)
        print("", file=sys.stderr)
        print("   Ralph loop is stopping. Run /ralph-loop again to start fresh.", file=sys.stderr)
        state_file.unlink(missing_ok=True)
        sys.exit(0)

    # Update iteration in state file
    updated_content = re.sub(
        r'^iteration: \d+',
        f'iteration: {next_iteration}',
        content,
        flags=re.MULTILINE
    )
    state_file.write_text(updated_content, encoding='utf-8')

    # Build system message
    if completion_promise and completion_promise != 'null':
        system_msg = f"Ralph iteration {next_iteration} | To stop: output <promise>{completion_promise}</promise> (ONLY when statement is TRUE - do not lie to exit!)"
    else:
        system_msg = f"Ralph iteration {next_iteration} | No completion promise set - loop runs infinitely"

    # Output JSON to block the stop and feed prompt back
    result = {
        "decision": "block",
        "reason": prompt_text,
        "systemMessage": system_msg
    }
    print(json.dumps(result))

    sys.exit(0)


if __name__ == "__main__":
    main()
