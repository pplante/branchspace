---
id: TASK-011
title: Implement `branchspace shell-integration` Command
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-01-31 21:22'
updated_date: '2026-02-01 22:11'
labels:
  - cli
  - shell
milestone: 'Phase 3: Shell Integration'
dependencies:
  - TASK-004
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement shell integration installation command.

**Functionality:**
- Detect which shells are installed (bash, zsh)
- Generate shell function that captures `branchspace cd` output and performs the actual `cd`
- Use questionary to prompt user for which shell configs to update
- Append function to .bashrc and/or .zshrc
- Make appending idempotent (don't duplicate if already present)

**Shell Function Pattern:**
```bash
branchspace() {
  if [[ "$1" == "cd" ]]; then
    local target=$(command branchspace cd "${@:2}")
    if [[ -n "$target" ]]; then
      cd "$target"
    fi
  else
    command branchspace "$@"
  fi
}
```

**Usage:** `branchspace shell-integration`

**Dependencies:** Main CLI Scaffold, questionary
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Detects installed shells (bash, zsh)
- [x] #2 Generates shell function that wraps branchspace cd
- [x] #3 Prompts user to select which shell configs to update
- [x] #4 Appends function to .bashrc/.zshrc safely (idempotent)
- [x] #5 Shows instructions for manual installation if user declines
- [x] #6 Unit tests for shell function generation
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add shell integration helper to generate the wrapper function and detect available rc files (bash/zsh).
2. Implement idempotent append logic that checks for an existing marker before writing.
3. Wire `branchspace shell-integration` to prompt via questionary, update selected shells, or print manual instructions.
4. Add unit tests for function generation and idempotent detection.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added shell integration helpers for detecting rc files, generating wrapper function, and idempotent appends.
- Wired `branchspace shell-integration` with questionary selection and manual instructions fallback.
- Added unit tests for function markers and idempotent append behavior.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented shell integration support for the CLI.

Changes:
- Added helpers to detect shell rc files, generate the wrapper function, and append integration idempotently.
- Wired `branchspace shell-integration` to prompt via questionary, update selected rc files, or print manual instructions.
- Added unit tests for integration snippet generation and idempotent append behavior.

Tests:
- pytest
<!-- SECTION:FINAL_SUMMARY:END -->
