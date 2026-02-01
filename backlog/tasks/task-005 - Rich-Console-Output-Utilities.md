---
id: TASK-005
title: Rich Console Output Utilities
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-01-31 21:19'
updated_date: '2026-02-01 19:21'
labels:
  - infrastructure
  - cli
milestone: 'Phase 1: Core Infrastructure'
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create consistent output formatting using Rich library:

- Console singleton for consistent output
- Success/warning/error message styling
- Tables for worktree listing
- Spinners for long-running operations
- Confirmation prompts (can integrate with questionary)

Dependencies: rich (already in pyproject.toml)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Console helper functions for success/warning/error output
- [ ] #2 Table formatting for worktree list
- [ ] #3 Spinner context manager for async operations
- [ ] #4 Consistent color scheme throughout
<!-- AC:END -->
