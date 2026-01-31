---
id: TASK-004
title: Main CLI Scaffold with Click
status: To Do
assignee: []
created_date: '2026-01-31 21:19'
labels:
  - infrastructure
  - cli
milestone: 'Phase 1: Core Infrastructure'
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create the main CLI structure using Click:

- `branchspace` main group with help text
- `--version` flag showing version from __init__.py
- Placeholder commands for: create, rm, cd, ls, shell, purge, init, config, shell-integration
- Proper command grouping and help organization

Dependencies: click (already in pyproject.toml)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 branchspace --help shows all commands
- [ ] #2 branchspace --version shows current version
- [ ] #3 All command placeholders registered
- [ ] #4 CLI entrypoint works via `branchspace` command
<!-- AC:END -->
