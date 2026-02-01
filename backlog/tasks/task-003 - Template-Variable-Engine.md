---
id: TASK-003
title: Template Variable Engine
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-01-31 21:19'
updated_date: '2026-02-01 18:59'
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

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Locate config parsing/templating usage for worktreePathTemplate, postCreateCmd, terminalCommand to align substitution points.
2. Implement a template substitution helper that replaces $BASE_PATH, $WORKTREE_PATH, $BRANCH_NAME, $SOURCE_BRANCH for both strings and list entries, with defined behavior for unknown variables.
3. Add tests covering single string and list substitutions, missing variable handling, and mixed literals.
4. Wire helper into command flows that consume these templates, ensuring existing behavior preserved.
<!-- SECTION:PLAN:END -->
