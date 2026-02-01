## Stage 1: Removal core
**Goal**: Implement worktree removal logic with safety checks.
**Success Criteria**: Worktree removal validates protected branches, checked-out-elsewhere, and dirty/unpushed warnings.
**Tests**: Unit tests for protected-branch and checked-out-elsewhere checks.
**Status**: Not Started

## Stage 2: Confirmations and purge
**Goal**: Add confirmation prompts and purge-on-remove branch deletion.
**Success Criteria**: Prompts appear for dirty/unpushed; purge deletes branch when enabled.
**Tests**: Unit tests for confirm flows and branch deletion.
**Status**: Not Started

## Stage 3: CLI wiring
**Goal**: Wire `branchspace rm` to removal logic and report results.
**Success Criteria**: CLI removes one or many worktrees with proper exit codes and messages.
**Tests**: CLI integration tests for error and success paths.
**Status**: Not Started
