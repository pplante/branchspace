---
id: TASK-014
title: Implement `branchspace shell` Command
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-01-31 21:22'
updated_date: '2026-02-02 01:39'
labels:
  - cli
  - docker
milestone: 'Phase 4: Docker Features'
dependencies:
  - TASK-013
  - TASK-002
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement Docker shell command for branch-specific containers.

**Functionality:**
- Determine container configuration (image vs build)
- For image config: Pull image if needed, run ephemeral container
- For build config: Build image from Dockerfile, run ephemeral container
- Mount current worktree at /workspace
- Name container based on branch for isolation
- Open interactive shell using configured `shell` (default: bash)
- Support running a single command: `branchspace shell "npm install"`

**Usage:**
- `branchspace shell` → interactive shell
- `branchspace shell "npm test"` → run command and exit

**Dependencies:** Container Config Parser, Git Utilities
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Opens interactive shell in container with branch-specific name
- [x] #2 Mounts current directory at /workspace
- [x] #3 Uses configured shell (bash default)
- [x] #4 Supports running single command instead of interactive shell
- [x] #5 Builds image from Dockerfile if build config specified
- [x] #6 Pulls image if image config specified
- [x] #7 Unit tests for Docker command generation
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add a docker command builder that inspects containerConfig, current branch, and shell settings to build docker run/build/pull commands.
2. Implement logic for image vs build configs (pull or build) and build container name from branch.
3. Wire `branchspace shell` to execute commands and handle optional single command argument.
4. Add unit tests covering command generation for image and build configs.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Added docker shell command builder for image/build configs and branch-based container naming.
- Wired `branchspace shell` to run docker pull/build + run with optional command argument.
- Added unit tests for docker command generation and CLI wiring.
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
Implemented the `branchspace shell` Docker runner.

Changes:
- Added docker command builder supporting image pulls and Dockerfile builds with branch-based container naming.
- Wired the CLI `shell` command to run docker commands and optional one-off command execution.
- Added unit tests for docker command generation and CLI wiring.

Tests:
- pytest
<!-- SECTION:FINAL_SUMMARY:END -->
