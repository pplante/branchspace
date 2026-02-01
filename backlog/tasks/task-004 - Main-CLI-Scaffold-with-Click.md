---
id: TASK-004
title: Main CLI Scaffold with Click
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-01-31 21:19'
updated_date: '2026-02-01 19:17'
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

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Locate current CLI entry points and existing package layout; confirm how __main__.py calls the CLI.
2. Implement a Click group in a new main_cli module with version option pulling from branchspace.__init__.__version__.
3. Register placeholder subcommands (create, rm, cd, ls, shell, purge, init, config, shell-integration) with clear help text.
4. Add tests to validate --help shows commands and --version output, and that the entrypoint works via invoking the CLI module.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added Click-based CLI group with version option and placeholder subcommands.
- Added CLI tests for help output, version flag, module entrypoint, and placeholder commands.
<!-- SECTION:NOTES:END -->
