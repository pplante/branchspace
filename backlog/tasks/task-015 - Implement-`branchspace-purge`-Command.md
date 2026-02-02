---
id: TASK-015
title: Implement `branchspace purge` Command
status: Done
assignee:
  - '@opencode'
created_date: '2026-01-31 21:23'
updated_date: '2026-02-02 02:39'
labels:
  - cli
  - docker
milestone: 'Phase 4: Docker Features'
dependencies:
  - TASK-002
priority: medium
ordinal: 4000
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
- [x] #1 Removes containers matching branch naming pattern
- [x] #2 Removes images built for branch (if build config)
- [x] #3 Removes volumes if any created
- [x] #4 Shows what will be removed before confirmation
- [x] #5 Dry-run option to preview changes
- [x] #6 Unit tests for purge logic
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
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented the `branchspace purge` command for cleaning Docker resources.

Changes:
- Added purge helper to discover containers, images, and volumes by branch-based naming and render previews.
- Wired CLI with --dry-run and --force options plus confirmation prompts.
- Added unit tests for resource discovery and CLI wiring.

Tests:
- pytest
<!-- SECTION:FINAL_SUMMARY:END -->
