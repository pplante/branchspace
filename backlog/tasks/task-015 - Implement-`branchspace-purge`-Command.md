---
id: TASK-015
title: Implement `branchspace purge` Command
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-01-31 21:23'
updated_date: '2026-02-02 01:42'
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

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add docker purge helper to build lists of containers/images/volumes by branch naming pattern.
2. Implement dry-run preview output and optional --force flag to skip confirmation.
3. Wire `branchspace purge` to use the helper and questionary confirmation prompt.
4. Add unit tests for resource discovery and purge command generation.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added Docker purge helper to discover containers/images/volumes and render previews.
- Wired `branchspace purge` with --dry-run and --force options plus confirmation prompts.
- Added unit tests for resource discovery and CLI wiring.

- Added Docker purge helper to discover containers/images/volumes and render previews.

- Wired `branchspace purge` with --dry-run and --force options plus confirmation prompts.

- Added unit tests for resource discovery and CLI wiring.
<!-- SECTION:NOTES:END -->
