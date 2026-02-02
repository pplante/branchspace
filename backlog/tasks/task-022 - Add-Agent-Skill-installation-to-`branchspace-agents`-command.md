---
id: TASK-022
title: Add Agent Skill installation to `branchspace agents` command
status: Done
assignee:
  - '@claude'
created_date: '2026-02-02 04:30'
updated_date: '2026-02-02 04:45'
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
- [x] #1 New `skill.py` module with skill generation and installation functions
- [x] #2 SKILL.md content follows agentskills.io specification (valid frontmatter with name/description)
- [x] #3 `branchspace agents` prompts user to install skill after selecting agents
- [x] #4 User can choose between project scope (.skills/) and global scope (~/.skills/)
- [x] #5 Skill installation creates proper directory structure: `<scope>/branchspace/SKILL.md`
- [x] #6 Existing skill detection with option to update/skip if already installed
- [x] #7 Success message shows installed skill path
- [x] #8 Unit tests for skill generation, installation, and path resolution
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
1. Create `src/branchspace/skill.py` with skill generation and installation logic
2. Update `src/branchspace/main_cli.py` to add skill installation prompts to agents command
3. Create `tests/test_skill.py` with unit tests
4. Run tests to verify functionality
5. Manual verification of the CLI flow
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
Implemented in feature/agent-skill worktree

All 18 skill tests pass

Full test suite passes (139 tests)

Linting and mypy pass
<!-- SECTION:NOTES:END -->

## Final Summary

<!-- SECTION:FINAL_SUMMARY:BEGIN -->
## Summary

Added Agent Skill installation support to the `branchspace agents` command, following the agentskills.io specification.

## Changes

### New Files
- **`src/branchspace/skill.py`**: New module containing:
  - `generate_skill_content()` - Generates SKILL.md with valid frontmatter and comprehensive instructions
  - `get_skill_install_path(scope)` - Returns path for global (~/.skills/) or project (.skills/) scope
  - `install_skill(scope)` - Creates the skill directory and writes SKILL.md
  - `is_skill_installed(scope)` - Checks if skill already exists at given scope

- **`tests/test_skill.py`**: 18 unit tests covering:
  - Skill content generation and format validation
  - Path resolution for both scopes
  - Installation and overwrite behavior

### Modified Files
- **`src/branchspace/main_cli.py`**: Updated `agents` command to:
  - Prompt user to install the Branchspace Agent Skill after selecting agents
  - Let user choose between project scope or global scope
  - Detect existing skills and offer Update/Skip options
  - Display success message with installed path

## Skill Content

The installed SKILL.md includes:
- Valid YAML frontmatter with `name: branchspace` and description
- Guidance on when to use Branchspace (new features, clean environments, containerized dev)
- Key commands reference table
- Step-by-step workflow example
- Best practices for agent behavior

## Tests

All 139 tests pass (138 passed, 1 skipped). Linting and type checking pass.
<!-- SECTION:FINAL_SUMMARY:END -->
