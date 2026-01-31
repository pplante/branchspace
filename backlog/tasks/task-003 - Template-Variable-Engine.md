---
id: TASK-003
title: Template Variable Engine
status: To Do
assignee: []
created_date: '2026-01-31 21:19'
labels:
  - infrastructure
milestone: 'Phase 1: Core Infrastructure'
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement template variable substitution for configuration strings.

Supported variables:
- `$BASE_PATH` - Repository name (e.g., `myproject`)
- `$WORKTREE_PATH` - Full path to worktree
- `$BRANCH_NAME` - New branch name (e.g., `feature-auth`)
- `$SOURCE_BRANCH` - Current branch (e.g., `main`)

Used in: worktreePathTemplate, postCreateCmd, terminalCommand
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 All 4 template variables work correctly
- [ ] #2 Variables substitute in strings and lists of strings
- [ ] #3 Missing variables handled gracefully (or error)
- [ ] #4 Unit tests for template substitution
<!-- AC:END -->
