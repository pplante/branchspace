---
id: TASK-007
title: Implement `branchspace ls` Command
status: To Do
assignee: []
created_date: '2026-01-31 21:22'
labels:
  - cli
  - worktree
milestone: 'Phase 2: Worktree Commands'
dependencies:
  - TASK-002
  - TASK-005
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement the worktree listing command with formatted output.

**Functionality:**
- List all worktrees for the current repository
- Display in a Rich table with columns: Branch, Path, Status (clean/dirty)
- Show the main worktree and all additional worktrees
- Indicate current worktree if applicable

**Usage:** `branchspace ls`

**Dependencies:** Git Utilities, Rich Console Utilities
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Displays all worktrees in a formatted table
- [ ] #2 Shows branch name, path, and dirty/clean status
- [ ] #3 Highlights current worktree
- [ ] #4 Handles repos with no additional worktrees gracefully
- [ ] #5 Unit tests for list logic
<!-- AC:END -->
