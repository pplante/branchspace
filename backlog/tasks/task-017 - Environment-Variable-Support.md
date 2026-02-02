---
id: TASK-017
title: Environment Variable Support
status: Done
assignee:
  - '@opencode'
created_date: '2026-01-31 21:23'
updated_date: '2026-02-02 02:39'
labels:
  - config
milestone: 'Phase 5: Polish & Cross-Platform'
dependencies:
  - TASK-001
priority: low
ordinal: 2000
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
- [x] #1 BRANCHSPACE_BASE overrides default worktree location
- [x] #2 Default is $HOME/worktrees
- [x] #3 Environment variable documented in --help
- [x] #4 Unit tests for env var handling
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add env var handling to config loading and/or worktree path resolution, defaulting to $HOME/worktrees.
2. Ensure env override takes precedence over config for worktree base.
3. Update CLI help/docs to mention BRANCHSPACE_BASE.
4. Add unit tests for env override and default base.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added BRANCHSPACE_BASE override in config load and updated default worktree path template.
- Documented env var in CLI help and added unit tests for env handling.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added BRANCHSPACE_BASE support for worktree location overrides.

Changes:
- Updated default worktree path template to $HOME/worktrees and applied env var overrides during config load.
- Added env var mention to CLI help text.
- Added unit tests for BRANCHSPACE_BASE handling.

Tests:
- pytest
<!-- SECTION:FINAL_SUMMARY:END -->
