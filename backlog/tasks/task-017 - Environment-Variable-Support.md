---
id: TASK-017
title: Environment Variable Support
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-01-31 21:23'
updated_date: '2026-02-02 02:35'
labels:
  - config
milestone: 'Phase 5: Polish & Cross-Platform'
dependencies:
  - TASK-001
priority: low
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add support for environment variable overrides.

**Functionality:**
- `BRANCHSPACE_BASE` - Override default worktree base location
- Default value: `$HOME/worktrees`
- Environment variables should take precedence over config file values

**Usage:**
```bash
export BRANCHSPACE_BASE="$HOME/my-worktrees"
branchspace create feature-auth  # Creates in $HOME/my-worktrees/...
```

**Dependencies:** Configuration System
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 BRANCHSPACE_BASE overrides default worktree location
- [ ] #2 Default is $HOME/worktrees
- [ ] #3 Environment variable documented in --help
- [ ] #4 Unit tests for env var handling
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add env var handling to config loading and/or worktree path resolution, defaulting to $HOME/worktrees.
2. Ensure env override takes precedence over config for worktree base.
3. Update CLI help/docs to mention BRANCHSPACE_BASE.
4. Add unit tests for env override and default base.
<!-- SECTION:PLAN:END -->
