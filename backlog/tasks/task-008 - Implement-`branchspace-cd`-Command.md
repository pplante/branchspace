---
id: TASK-008
title: Implement `branchspace cd` Command
status: To Do
assignee: []
created_date: '2026-01-31 21:22'
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
- [ ] #1 Outputs worktree path for given branch name
- [ ] #2 Outputs git root when no branch specified
- [ ] #3 Returns error if branch/worktree not found
- [ ] #4 Works with shell integration to perform actual cd
- [ ] #5 Unit tests for path resolution
<!-- AC:END -->
