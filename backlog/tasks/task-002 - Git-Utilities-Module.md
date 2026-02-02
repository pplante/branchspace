---
id: TASK-002
title: Git Utilities Module
status: Done
assignee:
  - claude
created_date: '2026-01-31 21:19'
updated_date: '2026-02-02 02:39'
labels:
  - infrastructure
  - git
milestone: 'Phase 1: Core Infrastructure'
dependencies: []
priority: high
ordinal: 17000
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
- [x] #1 Can detect if current directory is in a git repo
- [x] #2 Can list existing worktrees with metadata
- [x] #3 Can create worktree with new branch
- [x] #4 Can remove worktree safely
- [x] #5 Protected branch list configurable or hard-coded per README
- [x] #6 Detects uncommitted changes and unpushed commits
- [x] #7 Unit tests for git utilities
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

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## Summary

Fixed implementation bugs and test infrastructure issues in the Git Utilities Module. The module was already substantially implemented but had 18 failing tests out of 32.

## Changes

### Implementation Fixes (`src/branchspace/git_utils.py`)

1. **`list_worktrees()`**: Fixed branch name parsing to strip `refs/heads/` prefix - branches are now returned as `main` instead of `refs/heads/main`

2. **`create_worktree()`**: Added `create_branch` parameter (default `True`) to support:
   - Creating worktrees with new branches using `-b` flag
   - Creating worktrees with existing branches

3. **`list_branches()`**: Completely rewrote `is_checked_out_elsewhere` logic - now properly checks if a branch is checked out in another worktree by comparing against `list_worktrees()` results instead of incorrectly checking if the branch exists

4. **`remove_worktree()`**: Added `repository_path` parameter to allow running the command from the correct git repository context

### Test Fixes (`tests/test_git_utils.py`)

1. Replaced broken `TemporaryDirectory().__enter__()` pattern with pytest's `tmp_path` fixture
2. Added `_init_git_repo()` helper function that properly initializes git repos with user config and optional initial commit
3. Fixed test expectations:
   - `list_worktrees()` includes the main worktree
   - `has_unpushed_commits()` returns `False` without a remote (nothing to compare against)
4. Added new tests for edge cases

## Test Results

- **33 tests pass** (was 14 passing, 18 failing)
- **96% code coverage** on git_utils.py
- Full test suite: 66 tests passing
<!-- SECTION:FINAL_SUMMARY:END -->
