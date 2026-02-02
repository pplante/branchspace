---
id: TASK-013
title: Container Config Parser
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-01-31 21:22'
updated_date: '2026-02-02 01:12'
labels:
  - docker
  - config
milestone: 'Phase 4: Docker Features'
dependencies:
  - TASK-001
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Extend the configuration system to properly parse and validate containerConfig.

**Config Variants:**
1. **Image Config**: `{"image": "python:3.14"}`
2. **Build Config**: `{"context": ".", "dockerfile": "Dockerfile.dev"}`

**Validation:**
- Image config requires `image` field
- Build config requires `context` field, `dockerfile` is optional (defaults to "Dockerfile")

**Dependencies:** Configuration System
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Parses image config format: {"image": "python:3.14"}
- [ ] #2 Parses build config format: {"context": ".", "dockerfile": "Dockerfile.dev"}
- [ ] #3 Validates config and provides helpful error messages
- [ ] #4 Unit tests for all config variants
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Review existing container config models and validation in config.py to see current behavior.
2. Adjust discriminator/validation to enforce image vs build requirements with clear errors.
3. Add unit tests covering valid image/build configs and invalid configs (missing required fields).
4. Update README/config docs if any usage needs clarification.
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
- Updated container build config to require context and added default dockerfile behavior.
- Expanded config parsing tests for build container defaults and validation errors.

- Updated container build config to require context and added default dockerfile behavior.

- Expanded config parsing tests for build container defaults and validation errors.
<!-- SECTION:NOTES:END -->
