---
description: "Explain Skeptic Validator plugin and usage"
---

# Skeptic Validator Help

Please explain the following to the user:

## What is Skeptic Validator?

Skeptic Validator is a rigorous validation agent that demands concrete evidence before accepting that code changes are correct. It's designed to catch the gap between "I think it works" and "I can prove it works."

**Core philosophy:** Trust nothing. Verify everything. Show your evidence.

## When to Use It

**After bug fixes:**
```
/validate src/auth/login.ts
```
Ensures the fix actually resolves the issue without regressions.

**After implementing features:**
```
/validate "the new caching layer"
```
Verifies the feature works as intended with concrete proof.

**After performance optimizations:**
```
/validate
```
Demands benchmark evidence, not just "it feels faster."

**After security patches:**
```
/validate security-fix
```
Confirms vulnerabilities are actually closed.

## What It Does

1. **Identifies changes** - Uses git diff/status to find what changed
2. **Runs tests** - Executes relevant test suites and captures output
3. **Demands proof** - Requires actual logs, not just claims
4. **Reports findings** - Provides evidence-based validation report

## Example Output

```
## Validation Report

### Changes Validated
- Fixed null pointer in `processUser()` (src/handlers/user.ts:45)

### Evidence Gathered
- Test suite: 47 passed, 0 failed
- Specific test `should handle null user` now passes
- Related tests for user processing: all green

### Issues Found
- None

### Confidence: HIGH
The fix is verified with passing tests and no regressions detected.
```

## Key Principles

- **"Tests pass" is not enough** - Show the actual test output
- **"It works" is not enough** - Demonstrate it working
- **"I fixed it" is not enough** - Prove the fix is correct
- **Assumptions are not evidence** - Verify or acknowledge uncertainty

## Available Commands

- `/validate [target]` - Run validation on changes (or specific file/description)
- `/skeptic-validator:help` - Show this help message
