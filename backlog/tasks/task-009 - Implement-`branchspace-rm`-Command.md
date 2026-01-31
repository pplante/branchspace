---
id: TASK-009
title: Implement `branchspace rm` Command
status: To Do
assignee: []
created_date: '2026-01-31 21:22'
labels:
  - cli
  - worktree
milestone: 'Phase 2: Worktree Commands'
dependencies:
  - TASK-001
  - TASK-002
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement worktree removal with comprehensive safety checks.

**Functionality:**
- Accept one or more branch names to remove
- Safety checks before removal:
  - Protected branch check (main, master, develop, staging, production)
  - Uncommitted changes warning with confirmation
  - Unpushed commits warning with confirmation
  - Branch checked out elsewhere check
- If `purgeOnRemove` is true, also delete the branch and run Docker purge
- Remove the worktree directory

**Usage:** `branchspace rm <branch>...`

**Dependencies:** Configuration System, Git Utilities
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Removes worktree directory
- [ ] #2 Blocks removal of protected branches with error message
- [ ] #3 Prompts for confirmation if uncommitted changes
- [ ] #4 Prompts for confirmation if unpushed commits
- [ ] #5 Errors if branch is checked out elsewhere
- [ ] #6 Respects purgeOnRemove config to delete branch
- [ ] #7 Supports removing multiple worktrees
- [ ] #8 Unit tests for rm logic and safety checks
<!-- AC:END -->
