---
id: TASK-007
title: Implement `branchspace ls` Command
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-01-31 21:22'
updated_date: '2026-02-01 20:53'
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

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Extend git utilities or add list helper to gather worktrees and dirty status plus current worktree identification.
2. Implement list logic that builds a Rich table using console helpers, including current-worktree highlighting.
3. Wire `branchspace ls` command to use the list logic and handle empty/solo worktree cases.
4. Add unit tests for table rows and status formatting (clean/dirty/current).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added worktree list logic with current/dirty status detection and Rich table rendering.
- Wired `branchspace ls` to show a formatted table or a no-worktrees message.
- Added unit tests for list status detection and CLI output behavior.

- Added worktree list logic with current/dirty status detection and Rich table rendering.

- Wired `branchspace ls` to show a formatted table or a no-worktrees message.

- Added unit tests for list status detection and CLI output behavior.
<!-- SECTION:NOTES:END -->
