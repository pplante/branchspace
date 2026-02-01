---
id: TASK-003
title: Template Variable Engine
status: Done
assignee:
  - '@opencode'
created_date: '2026-01-31 21:19'
updated_date: '2026-02-01 19:04'
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
- [x] #1 All 4 template variables work correctly
- [x] #2 Variables substitute in strings and lists of strings
- [x] #3 Missing variables handled gracefully (or error)
- [x] #4 Unit tests for template substitution
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Locate config parsing/templating usage for worktreePathTemplate, postCreateCmd, terminalCommand to align substitution points.
2. Implement a template substitution helper that replaces $BASE_PATH, $WORKTREE_PATH, $BRANCH_NAME, $SOURCE_BRANCH for both strings and list entries, with defined behavior for unknown variables.
3. Add tests covering single string and list substitutions, missing variable handling, and mixed literals.
4. Wire helper into command flows that consume these templates, ensuring existing behavior preserved.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added template substitution helper with strict missing-variable behavior and variable normalization.
- Added template context mapping for BASE_PATH/WORKTREE_PATH/BRANCH_NAME/SOURCE_BRANCH.
- Added tests for string/list substitutions and missing variables.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented template-variable substitution utilities for branchspace config usage.

Changes:
- Added `substitute_template` with strict missing-variable handling plus variable normalization for $BASE_PATH/$WORKTREE_PATH/$BRANCH_NAME/$SOURCE_BRANCH.
- Introduced `TemplateContext` to provide consistent mapping for config-driven templates.
- Added unit tests covering string and list substitution paths and missing variable behavior.

Tests:
- pytest
<!-- SECTION:FINAL_SUMMARY:END -->
