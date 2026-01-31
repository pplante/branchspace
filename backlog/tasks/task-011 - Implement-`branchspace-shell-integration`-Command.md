---
id: TASK-011
title: Implement `branchspace shell-integration` Command
status: To Do
assignee: []
created_date: '2026-01-31 21:22'
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
- [ ] #1 Detects installed shells (bash, zsh)
- [ ] #2 Generates shell function that wraps branchspace cd
- [ ] #3 Prompts user to select which shell configs to update
- [ ] #4 Appends function to .bashrc/.zshrc safely (idempotent)
- [ ] #5 Shows instructions for manual installation if user declines
- [ ] #6 Unit tests for shell function generation
<!-- AC:END -->
