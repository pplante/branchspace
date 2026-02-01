---
id: TASK-006
title: Implement `branchspace create` Command
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-01-31 21:22'
updated_date: '2026-02-01 19:50'
labels:
  - cli
  - worktree
milestone: 'Phase 2: Worktree Commands'
dependencies:
  - TASK-001
  - TASK-002
  - TASK-003
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement the main worktree creation command with full feature support.

**Functionality:**
- Accept one or more branch names as arguments
- Create git worktree for each branch
- Apply `worktreePathTemplate` for destination path
- Copy files matching `worktreeCopyPatterns` (excluding `worktreeCopyIgnores`)
- Execute `postCreateCmd` commands in the new worktree
- Optionally run `terminalCommand` to open editor

**Usage:** `branchspace create <branch>...`

**Dependencies:** Configuration System, Git Utilities, Template Engine
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Creates worktree at path from worktreePathTemplate
- [ ] #2 Copies files matching worktreeCopyPatterns
- [ ] #3 Excludes files matching worktreeCopyIgnores
- [ ] #4 Runs postCreateCmd in new worktree directory
- [ ] #5 Runs terminalCommand if configured
- [ ] #6 Supports creating multiple worktrees in one command
- [ ] #7 Shows progress with Rich spinners
- [ ] #8 Unit tests for create logic
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Review existing config, git utilities, and template substitution to define create inputs and outputs.
2. Implement core create logic module: resolve worktree path template, create worktree, copy included files excluding ignores, run postCreateCmd, and optionally terminalCommand; support multiple branches.
3. Integrate Rich console helpers/spinner for progress output and surface errors consistently.
4. Wire the logic into the Click create command and add unit tests for create logic and CLI entrypoint.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added worktree creation module with template resolution, file copy, post-create hooks, and terminal command support.
- Wired create command to config loading, worktree creation, and Rich spinner output.
- Added unit tests for template path resolution, copy ignore behavior, and CLI argument handling.

- Added worktree creation module with template resolution, file copy, post-create hooks, and terminal command support.

- Wired create command to config loading, worktree creation, and Rich spinner output.

- Added unit tests for template path resolution, copy ignore behavior, and CLI argument handling.
<!-- SECTION:NOTES:END -->
