---
id: TASK-001
title: Configuration System with Pydantic Models
status: To Do
assignee: []
created_date: '2026-01-31 21:19'
labels:
  - infrastructure
  - config
milestone: 'Phase 1: Core Infrastructure'
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement the configuration system for branchspace.json parsing and validation using Pydantic.

The config file supports:
- `worktreeCopyPatterns`: string[] - Files to copy to new worktrees
- `worktreeCopyIgnores`: string[] - Files to exclude from copying
- `worktreePathTemplate`: string - Template for worktree directory
- `postCreateCmd`: string[] - Commands to run after creation
- `terminalCommand`: string - Command to open editor
- `purgeOnRemove`: boolean - Delete branch + Docker on remove
- `containerConfig`: object - Container configuration (image or build)
- `shell`: string - Shell for interactive sessions

Config discovery should search from current directory up to repo root.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Pydantic models for all config options match README spec
- [ ] #2 Default values match README defaults
- [ ] #3 Config file discovery from cwd to repo root
- [ ] #4 Graceful handling of missing/invalid config files
- [ ] #5 Unit tests for config parsing and validation
<!-- AC:END -->
