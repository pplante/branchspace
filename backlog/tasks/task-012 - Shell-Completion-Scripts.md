---
id: TASK-012
title: Shell Completion Scripts
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-01-31 21:22'
updated_date: '2026-02-02 00:51'
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
- [ ] #1 Generates bash completion script
- [ ] #2 Generates zsh completion script
- [ ] #3 Generates fish completion script
- [ ] #4 Completions include all commands and arguments
- [ ] #5 Instructions in README match implementation
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Ensure Click completion support is enabled (env var hooks) without additional flags.
2. Verify README instructions align with Click completion env vars for bash/zsh/fish.
3. Add a lightweight test or script check to ensure completion generation works for each shell.
<!-- SECTION:PLAN:END -->
