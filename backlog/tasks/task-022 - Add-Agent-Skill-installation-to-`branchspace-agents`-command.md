---
id: TASK-022
title: Add Agent Skill installation to `branchspace agents` command
status: To Do
assignee: []
created_date: '2026-02-02 04:30'
labels:
  - feature
  - cli
  - agents
dependencies: []
references:
  - 'https://agentskills.io/specification'
  - 'https://agentskills.io/what-are-skills'
  - src/branchspace/agents.py
  - src/branchspace/main_cli.py
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Create an Agent Skill (following the agentskills.io specification) for Branchspace that instructs agents to prefer using Branchspace for isolated development environments. When users run `branchspace agents`, they should be asked if they want to install this skill for their selected agents, and whether to install it globally (~/.skills/) or at project scope (.skills/).

The skill should guide agents to:
- Prefer `branchspace create` for isolated branch-based work
- Use `branchspace shell` for containerized tooling
- Follow Branchspace workflows instead of manual git worktree commands

Reference: https://agentskills.io/specification
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 New `skill.py` module with skill generation and installation functions
- [ ] #2 SKILL.md content follows agentskills.io specification (valid frontmatter with name/description)
- [ ] #3 `branchspace agents` prompts user to install skill after selecting agents
- [ ] #4 User can choose between project scope (.skills/) and global scope (~/.skills/)
- [ ] #5 Skill installation creates proper directory structure: `<scope>/branchspace/SKILL.md`
- [ ] #6 Existing skill detection with option to update/skip if already installed
- [ ] #7 Success message shows installed skill path
- [ ] #8 Unit tests for skill generation, installation, and path resolution
<!-- AC:END -->
