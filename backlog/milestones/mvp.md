# MVP - Core Worktree and Docker Management

## Description
Implement the core functionality needed for a usable branchspace tool: worktree creation/removal, Docker environment management, and basic configuration.

## Goals
- Users can create and remove git worktrees with automatic file copying
- Users can run isolated Docker environments per branch
- Basic configuration via branchspace.json

## Success Criteria
- [ ] `branchspace create <branch>` creates a worktree with file copying
- [ ] `branchspace rm <branch>` removes worktrees with safety checks
- [ ] `branchspace ls` lists all worktrees
- [ ] `branchspace cd <branch>` outputs path for shell navigation
- [ ] `branchspace shell` opens Docker container for current branch
- [ ] `branchspace config` shows current configuration
- [ ] Configuration loading from branchspace.json works

## Status
In Progress
