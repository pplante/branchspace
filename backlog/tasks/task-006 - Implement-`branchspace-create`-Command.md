---
id: TASK-006
title: Implement `branchspace create` Command
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
