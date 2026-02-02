---
id: TASK-012
title: Shell Completion Scripts
status: Done
assignee:
  - '@opencode'
created_date: '2026-01-31 21:22'
updated_date: '2026-02-02 02:39'
labels:
  - cli
  - shell
milestone: 'Phase 3: Shell Integration'
dependencies:
  - TASK-004
priority: high
ordinal: 7000
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add shell completion support using Click's built-in completion.

**Functionality:**
- Configure Click to generate completion scripts for bash, zsh, and fish
- Document installation in README (already done, just verify it works)

**Verification:**
```bash
# Bash
eval "$(_BRANCHSPACE_COMPLETE=bash_source branchspace)"

# Zsh
eval "$(_BRANCHSPACE_COMPLETE=zsh_source branchspace)"

# Fish
_BRANCHSPACE_COMPLETE=fish_source branchspace > ~/.config/fish/completions/branchspace.fish
```

**Dependencies:** Main CLI Scaffold
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Generates bash completion script
- [x] #2 Generates zsh completion script
- [x] #3 Generates fish completion script
- [x] #4 Completions include all commands and arguments
- [x] #5 Instructions in README match implementation
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Ensure Click completion support is enabled (env var hooks) without additional flags.
2. Verify README instructions align with Click completion env vars for bash/zsh/fish.
3. Add a lightweight test or script check to ensure completion generation works for each shell.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Verified Click completion output for bash, zsh, and fish via env var hooks after setting prog_name.
- Added tests to assert completion script generation for bash/zsh/fish.
- Adjusted module entrypoint to use prog name for completion scripts.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Verified Click shell completion support and added coverage.

Changes:
- Set module entrypoint to use the `branchspace` program name to align completion output.
- Added tests to assert bash/zsh/fish completion script generation via Click env hooks.
- Confirmed README completion instructions match the implementation.

Tests:
- pytest
<!-- SECTION:FINAL_SUMMARY:END -->
