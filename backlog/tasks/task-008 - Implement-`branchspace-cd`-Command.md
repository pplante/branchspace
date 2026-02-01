---
id: TASK-008
title: Implement `branchspace cd` Command
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-01-31 21:22'
updated_date: '2026-02-01 20:58'
labels:
  - cli
  - worktree
milestone: 'Phase 2: Worktree Commands'
dependencies:
  - TASK-002
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement the directory change helper command.

**Functionality:**
- Given a branch name, output the path to that worktree
- If no branch specified, output the git root path
- The shell integration function captures this output and performs the actual `cd`

**Usage:** 
- `branchspace cd feature-auth` → outputs `/path/to/worktree`
- `branchspace cd` → outputs `/path/to/git-root`

**Note:** This command outputs the path; actual directory change happens in shell integration.

**Dependencies:** Git Utilities
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Outputs worktree path for given branch name
- [x] #2 Outputs git root when no branch specified
- [x] #3 Returns error if branch/worktree not found
- [x] #4 Works with shell integration to perform actual cd
- [x] #5 Unit tests for path resolution
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add a worktree lookup helper using git utilities to resolve worktree path by branch name (and git root for default).
2. Implement `branchspace cd` command to output the resolved path or an error message with non-zero exit.
3. Add unit tests for branch lookup, git root fallback, and error cases (missing branch).
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added worktree path resolver for `branchspace cd` including git root fallback and missing-branch errors.
- Wired `branchspace cd` to print resolved path for shell integration.
- Added unit tests for root resolution and branch lookup behavior.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented the `branchspace cd` path resolver and CLI command.

Changes:
- Added `resolve_worktree_path` helper to return the git root or a branch worktree path with clear errors when missing.
- Wired `branchspace cd` to output the resolved path for shell integration.
- Added unit tests for root resolution, branch lookup, and missing-branch errors.

Tests:
- pytest
<!-- SECTION:FINAL_SUMMARY:END -->
