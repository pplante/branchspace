---
id: TASK-020
title: Add agents command for AI instruction output
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-02-02 03:16'
updated_date: '2026-02-02 03:52'
labels:
  - cli
  - docs
  - agents
dependencies: []
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Provide a new `branchspace agents` command that lets users select supported AI coding agents and outputs unified instructions to console and/or files in the project root.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Users can run `branchspace agents` and select one or more agents from a menu.
- [x] #2 Command offers output target selection (console, files, or both).
- [x] #3 Generated instructions include project overview, command reference, and integration tips.
- [x] #4 When writing files, instructions are saved in the project root with appropriate filenames for selected agents.
- [x] #5 Command handles existing target files safely (prompt to append, overwrite, or skip).
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Review existing CLI patterns and questionary usage for menus and confirmations.
2. Implement agents command logic and instruction generator (new module + main_cli wiring).
3. Add file output handling for existing files (append/overwrite/skip prompt) and de-duplicate shared filenames.
4. Add tests for instruction content and file write behavior.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented agents instruction generator and CLI wiring.

Added tests for instructions and updated CLI help coverage.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Added an `agents` command that guides users through selecting supported AI agents and output targets, then generates unified branchspace instructions.

Changes:
- Added `src/branchspace/agents.py` to define supported agents, resolve project root, generate instruction content, and handle append/overwrite/skip file writes.
- Wired `branchspace agents` into `src/branchspace/main_cli.py` with questionary prompts, console output, and per-file handling for shared filenames.
- Added tests in `tests/test_agents.py` and updated CLI help coverage in `tests/test_main_cli.py`.

Tests:
- pytest
<!-- SECTION:FINAL_SUMMARY:END -->
