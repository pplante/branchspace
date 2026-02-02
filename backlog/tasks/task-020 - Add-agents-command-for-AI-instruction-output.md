---
id: TASK-020
title: Add agents command for AI instruction output
status: To Do
assignee: []
created_date: '2026-02-02 03:16'
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
- [ ] #1 Users can run `branchspace agents` and select one or more agents from a menu.
- [ ] #2 Command offers output target selection (console, files, or both).
- [ ] #3 Generated instructions include project overview, command reference, and integration tips.
- [ ] #4 When writing files, instructions are saved in the project root with appropriate filenames for selected agents.
- [ ] #5 Command handles existing target files safely (prompt to append, overwrite, or skip).
<!-- AC:END -->
