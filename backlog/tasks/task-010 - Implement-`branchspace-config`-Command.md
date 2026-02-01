---
id: TASK-010
title: Implement `branchspace config` Command
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-01-31 21:22'
updated_date: '2026-02-01 21:07'
labels:
  - cli
  - config
milestone: 'Phase 2: Worktree Commands'
dependencies:
  - TASK-001
  - TASK-005
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement command to display current configuration.

**Functionality:**
- Load configuration from branchspace.json
- Display all config values in a readable format
- Show both explicit values and defaults
- Indicate config file location (or "using defaults" if none)

**Usage:** `branchspace config`

**Dependencies:** Configuration System, Rich Console Utilities
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Displays all configuration values
- [ ] #2 Shows defaults for missing values
- [ ] #3 Indicates config file path or 'using defaults'
- [ ] #4 Formats output nicely with Rich
- [ ] #5 Unit tests for config display
<!-- AC:END -->
