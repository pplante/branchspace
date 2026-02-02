---
id: TASK-015
title: Implement `branchspace purge` Command
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-01-31 21:23'
updated_date: '2026-02-02 01:40'
labels:
  - cli
  - docker
milestone: 'Phase 4: Docker Features'
dependencies:
  - TASK-002
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement Docker cleanup command for current branch.

**Functionality:**
- Identify Docker resources associated with current branch:
  - Containers (running or stopped)
  - Images (if built from Dockerfile)
  - Volumes (if any created)
- Show preview of what will be removed
- Prompt for confirmation (or support --force flag)
- Remove all identified resources

**Usage:** `branchspace purge`

**Dependencies:** Git Utilities (for branch detection)
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Removes containers matching branch naming pattern
- [ ] #2 Removes images built for branch (if build config)
- [ ] #3 Removes volumes if any created
- [ ] #4 Shows what will be removed before confirmation
- [ ] #5 Dry-run option to preview changes
- [ ] #6 Unit tests for purge logic
<!-- AC:END -->
