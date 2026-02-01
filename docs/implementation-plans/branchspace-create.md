## Stage 1: Foundations
**Goal**: Build core create logic and supporting helpers.
**Success Criteria**: Branchspace create can determine target paths, copy required files, and run post-create hooks for a single branch.
**Tests**: Unit tests for template substitution usage, copy include/exclude behavior, and post-create command execution.
**Status**: Not Started

## Stage 2: CLI Integration
**Goal**: Wire create command into Click CLI with progress output.
**Success Criteria**: `branchspace create <branch>` triggers worktree creation with Rich spinners and CLI output.
**Tests**: CLI integration test for create command entrypoint.
**Status**: Not Started

## Stage 3: Multi-branch support and terminal launch
**Goal**: Support multiple branches in one invocation and optional terminalCommand.
**Success Criteria**: Multiple worktrees created per invocation, terminalCommand executed when configured.
**Tests**: Unit tests covering multi-branch and terminal command behavior.
**Status**: Not Started
