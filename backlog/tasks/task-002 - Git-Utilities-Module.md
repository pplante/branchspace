---
id: TASK-002
title: Git Utilities Module
status: In Progress
assignee:
  - claude
created_date: '2026-01-31 21:19'
updated_date: '2026-01-31 21:55'
labels:
  - infrastructure
  - git
milestone: 'Phase 1: Core Infrastructure'
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement core git operations needed by branchspace:

- Repository detection (find .git directory)
- Worktree operations: create, list, remove
- Branch operations: create, delete, check if checked out elsewhere
- Protected branch detection (main, master, develop, staging, production)
- Uncommitted changes detection
- Unpushed commits detection

All operations should wrap git CLI commands with proper error handling.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Can detect if current directory is in a git repo
- [ ] #2 Can list existing worktrees with metadata
- [ ] #3 Can create worktree with new branch
- [ ] #4 Can remove worktree safely
- [ ] #5 Protected branch list configurable or hard-coded per README
- [ ] #6 Detects uncommitted changes and unpushed commits
- [ ] #7 Unit tests for git utilities
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan

### Issues to Fix

1. **Test infrastructure**: Replace broken `TemporaryDirectory().__enter__()` pattern with proper context managers
2. **`list_worktrees()`**: Strip `refs/heads/` prefix from branch names
3. **`create_worktree()`**: Add `-b` flag support for creating new branches
4. **`list_branches()`**: Properly detect if branch is checked out in another worktree
5. **Adjust test expectations**: Fix incorrect assertions

### Execution Order
1. Fix `git_utils.py` implementation bugs first
2. Fix test infrastructure and assertions in `test_git_utils.py`
3. Run tests to verify all pass
<!-- SECTION:PLAN:END -->
