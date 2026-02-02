---
id: TASK-014
title: Implement `branchspace shell` Command
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-01-31 21:22'
updated_date: '2026-02-02 01:31'
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
- [ ] #1 Opens interactive shell in container with branch-specific name
- [ ] #2 Mounts current directory at /workspace
- [ ] #3 Uses configured shell (bash default)
- [ ] #4 Supports running single command instead of interactive shell
- [ ] #5 Builds image from Dockerfile if build config specified
- [ ] #6 Pulls image if image config specified
- [ ] #7 Unit tests for Docker command generation
<!-- AC:END -->
