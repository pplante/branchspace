---
id: TASK-016
title: Implement `branchspace init` Command
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-01-31 21:23'
updated_date: '2026-02-02 01:58'
labels:
  - cli
  - config
milestone: 'Phase 4: Docker Features'
dependencies:
  - TASK-001
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement automatic project detection and configuration generation.

**Functionality:**
- Scan project for:
  - Dockerfile, Dockerfile.dev, Dockerfile.local
  - package.json (Node.js)
  - pyproject.toml, setup.py (Python)
- If Dockerfile found: offer to use it for containerConfig
- If no Dockerfile: offer image selection based on detected project type
- Use questionary for interactive prompts
- Generate branchspace.json with sensible defaults

**Usage:** `branchspace init`

**Dependencies:** Configuration System, questionary
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Detects Dockerfile, Dockerfile.dev, or similar files
- [ ] #2 Offers to use detected Dockerfile for build config
- [ ] #3 Falls back to prompting for base image selection
- [ ] #4 Generates complete branchspace.json with sensible defaults
- [ ] #5 Detects project type (Node.js, Python) for smart defaults
- [ ] #6 Unit tests for detection logic
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Add project detection helper to scan for Dockerfiles and language indicators (package.json, pyproject.toml, setup.py).
2. Implement init logic to choose build config if Dockerfile found, otherwise prompt for base image based on project type.
3. Generate branchspace.json with defaults + chosen containerConfig and write to repo root.
4. Wire `branchspace init` to prompts and add unit tests for detection logic.
<!-- SECTION:PLAN:END -->
