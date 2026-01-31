---
id: TASK-001
title: Configuration System with Pydantic Models
status: In Progress
assignee:
  - claude
created_date: '2026-01-31 21:19'
updated_date: '2026-01-31 21:28'
labels:
  - infrastructure
  - config
milestone: 'Phase 1: Core Infrastructure'
dependencies: []
priority: high
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Implement the configuration system for branchspace.json parsing and validation using Pydantic.

The config file supports:
- `worktreeCopyPatterns`: string[] - Files to copy to new worktrees
- `worktreeCopyIgnores`: string[] - Files to exclude from copying
- `worktreePathTemplate`: string - Template for worktree directory
- `postCreateCmd`: string[] - Commands to run after creation
- `terminalCommand`: string - Command to open editor
- `purgeOnRemove`: boolean - Delete branch + Docker on remove
- `containerConfig`: object - Container configuration (image or build)
- `shell`: string - Shell for interactive sessions

Config discovery should search from current directory up to repo root.
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [x] #1 Pydantic models for all config options match README spec
- [x] #2 Default values match README defaults
- [x] #3 Config file discovery from cwd to repo root
- [x] #4 Graceful handling of missing/invalid config files
- [x] #5 Unit tests for config parsing and validation
<!-- AC:END -->

## Implementation Plan

<!-- SECTION:PLAN:BEGIN -->
## Implementation Plan

### 1. Create Pydantic Models (`src/branchspace/config.py`)

**Container Config Models:**
- `ContainerImageConfig` - image-based setup with `image: str`
- `ContainerBuildConfig` - Dockerfile-based with `context: str`, `dockerfile: str`
- Use discriminated union for `containerConfig` field

**Main Config Model (`BranchspaceConfig`):**
- All fields with camelCase aliases for JSON compatibility
- Default values matching README spec:
  - `worktreeCopyPatterns`: `[".env*", ".vscode/**"]`
  - `worktreeCopyIgnores`: `["**/node_modules/**", "**/dist/**"]`
  - `worktreePathTemplate`: `"$BASE_PATH.worktree"`
  - `postCreateCmd`: `[]`
  - `terminalCommand`: `""`
  - `purgeOnRemove`: `False`
  - `containerConfig`: `{"image": "ubuntu:24.04"}`
  - `shell`: `"bash"`

### 2. Implement Config Discovery
- `find_config_file(start_path: Path | None = None) -> Path | None`
- Search from start_path (or cwd) upward to git repo root
- Return first `branchspace.json` found, or None

### 3. Implement Config Loading
- `load_config(path: Path | None = None) -> BranchspaceConfig`
- Uses discovery if no path provided
- Returns defaults if no config file found
- Raises clear ValidationError for invalid configs

### 4. Create Unit Tests (`tests/test_config.py`)
- Test model validation and defaults
- Test config discovery logic
- Test error handling for missing/invalid configs

### Key Files
- `src/branchspace/config.py` (new)
- `tests/__init__.py` (new)
- `tests/test_config.py` (new)
<!-- SECTION:PLAN:END -->

## Implementation Notes

<!-- SECTION:NOTES:BEGIN -->
## Verification Results

- All 33 tests pass: `uv run pytest tests/test_config.py -v`
- Linting clean: `uv run ruff check src/branchspace/config.py tests/test_config.py`
- Code coverage: 95%

## Files Created

- `src/branchspace/config.py` - Pydantic models and config loading
- `tests/__init__.py` - Test package init
- `tests/test_config.py` - Comprehensive unit tests
<!-- SECTION:NOTES:END -->
