---
id: TASK-013
title: Container Config Parser
status: In Progress
assignee:
  - '@opencode'
created_date: '2026-01-31 21:22'
updated_date: '2026-02-02 01:11'
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
