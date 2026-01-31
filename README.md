# branchspace

A Python CLI tool for managing git worktrees and branch-specific Docker environments.

## Features

- 🚀 Create and manage git worktrees with one command
- 🐳 Branch-specific isolated Docker environments
- 📋 Automatic file copying (env files, configs, etc.)
- ⚙️ Configurable post-creation commands
- 🎯 Template-based worktree paths
- 🔒 Protected branch safety checks
- 🗑️ Optional cleanup (worktree + branch + Docker)
- 🌐 Cross-platform (Linux, macOS, Windows WSL)

## Quick Start

```bash
# Install
pip install branchspace

# Set up shell integration (for cd command)
branchspace shell-integration

# Create a worktree
branchspace create feature-auth

# List worktrees
branchspace ls

# Navigate to worktree
branchspace cd feature-auth

# Remove worktree
branchspace rm feature-auth
```

## Installation

### Via uv

```bash
uv tool install branchspace
```

### From source

```bash
git clone https://github.com/yourusername/branchspace.git
cd branchspace
uv tool install .
```

### Shell Integration (Required for `cd` command)

To enable the `branchspace cd` command to change directories in your shell, run:

```bash
branchspace shell-integration
```

This will prompt you to select which shell configs to update (Bash, Zsh, or both).

## Commands

### Worktree Management

```bash
branchspace create <branch>...   # Create worktree(s) with new branch(es)
branchspace rm <branch>...       # Remove worktree(s) and optionally delete branch
branchspace cd [branch]          # Navigate to worktree (or git root if no branch)
branchspace ls                   # List all worktrees
```

### Docker Environment

```bash
branchspace shell [cmd]          # Open shell in Docker container (or run command)
branchspace purge                # Clean up Docker for current branch
branchspace init                 # Auto-detect and configure container setup
```

### Configuration

```bash
branchspace config               # Show current configuration
branchspace shell-integration    # Install shell integration to .bashrc/.zshrc
```

## Configuration

Create `branchspace.json` in your repository root:

```json
{
  "worktreeCopyPatterns": [
    ".env*",
    ".vscode/**"
  ],
  "worktreeCopyIgnores": [
    "**/node_modules/**",
    "**/dist/**"
  ],
  "worktreePathTemplate": ".worktrees/$BRANCH_NAME",
  "postCreateCmd": [
    "npm install"
  ],
  "terminalCommand": "code .",
  "purgeOnRemove": false,
  "containerConfig": {
    "image": "ubuntu:24.04"
  },
  "shell": "bash"
}
```

### Configuration Options

| Option                 | Type       | Default                       | Description                      |
|------------------------|------------|-------------------------------|----------------------------------|
| `worktreeCopyPatterns` | `string[]` | `[".env*", ".vscode/**"]`     | Files to copy to new worktrees   |
| `worktreeCopyIgnores`  | `string[]` | `["**/node_modules/**", ...]` | Files to exclude from copying    |
| `worktreePathTemplate` | `string`   | `"$BASE_PATH.worktree"`       | Template for worktree directory  |
| `postCreateCmd`        | `string[]` | `[]`                          | Commands to run after creation   |
| `terminalCommand`      | `string`   | `""`                          | Command to open editor           |
| `purgeOnRemove`        | `boolean`  | `false`                       | Delete branch + Docker on remove |
| `containerConfig`       | `object`   | `{"image": "ubuntu:24.04"}`    | Container configuration (see below) |
| `shell`                | `string`   | `"bash"`                      | Shell for interactive sessions   |

### Template Variables

Use in `worktreePathTemplate`, `postCreateCmd`, and `terminalCommand`:

- `$BASE_PATH` - Repository name (e.g., `myproject`)
- `$WORKTREE_PATH` - Full path to worktree
- `$BRANCH_NAME` - New branch name (e.g., `feature-auth`)
- `$SOURCE_BRANCH` - Current branch (e.g., `main`)

### Container Configuration

The `containerConfig` field supports three different container setup types:

#### 1. Image Config - Use a specific Docker image

```json
{
  "containerConfig": {
    "image": "python:3.14"
  }
}
```

Perfect for quick development environments with a specific base image. The current directory is mounted at `/workspace`.

#### 2. Build Config - Build from Dockerfile

```json
{
  "containerConfig": {
    "context": ".",
    "dockerfile": "Dockerfile.dev"
  }
}
```

Ideal when you need custom dependencies or system packages. Builds an image from your Dockerfile, then runs the ephemeral container with the current directory mounted at `/workspace`.

### Intelligent Container Detection

The `branchspace init` command automatically detects the best container configuration for your project:

1. **Dockerfile Projects**: If a `Dockerfile`, `Dockerfile.dev`, or similar is found, it offers to build from it
2. **Image-based Projects**: Falls back to selecting a base image with smart defaults

```bash
branchspace init
```

This creates an optimal `branchspace.json` configuration for your project setup.

## Examples

### Node.js Project

```json
{
  "worktreeCopyPatterns": [
    ".env*",
    "package.json"
  ],
  "worktreePathTemplate": ".worktrees/$BRANCH_NAME",
  "postCreateCmd": [
    "npm install"
  ],
  "terminalCommand": "code .",
  "containerConfig": {
    "image": "node:24"
  }
}
```

### Python Project

```json
{
  "worktreeCopyPatterns": [
    ".env*",
    "pyproject.toml"
  ],
  "worktreeCopyIgnores": [
    "**/__pycache__/**",
    "**/venv/**"
  ],
  "worktreePathTemplate": "$BASE_PATH-$BRANCH_NAME",
  "postCreateCmd": [
    "uv sync"
  ],
  "terminalCommand": "cursor .",
  "containerConfig": {
    "image": "python:3.14"
  }
}
```

### Project with Custom Dockerfile

```json
{
  "worktreeCopyPatterns": [
    ".env*",
    "pyproject.toml"
  ],
  "worktreePathTemplate": ".worktrees/$BRANCH_NAME",
  "postCreateCmd": [
    "uv sync"
  ],
  "containerConfig": {
    "context": ".",
    "dockerfile": "Dockerfile.dev"
  }
}
```

### Project with Container Configuration

```json
{
  "worktreeCopyPatterns": [
    ".env*",
    "pyproject.toml"
  ],
  "worktreePathTemplate": ".worktrees/$BRANCH_NAME",
  "postCreateCmd": [
    "uv sync"
  ],
  "containerConfig": "image:python:3.11"
}
```

## Safety Features

- **Protected branches**: Cannot delete `main`, `master`, `develop`, `staging`, `production`
- **Uncommitted changes**: Prompts before removing worktree
- **Unpushed commits**: Warns before deleting branch
- **Branch in use**: Cannot delete if checked out elsewhere

## Environment Variables

```bash
# Override default worktree location
export BRANCHSPACE_BASE="$HOME/my-worktrees"
```

Default: `$HOME/worktrees`

## Shell Completion

### Bash

```bash
eval "$(_BRANCHSPACE_COMPLETE=bash_source branchspace)" >> ~/.bashrc
```

### Zsh

```bash
eval "$(_BRANCHSPACE_COMPLETE=zsh_source branchspace)" >> ~/.zshrc
```

### Fish

```bash
_BRANCHSPACE_COMPLETE=fish_source branchspace > ~/.config/fish/completions/branchspace.fish
```

## Development

### Setup

```bash
git clone https://github.com/pplante/branchspace.git
cd branchspace
uv tool install . -e"
```

### Running tests

```bash
pytest
pytest --cov=branchspace
```

### Code formatting

```bash
ruff check src/
```

## Requirements

- Python 3.13+
- Git with worktree support
- Docker (optional, for Docker features)
- curl (required in containers for tool installation)

## License

MIT

## Credits

Inspired by [branchlet](https://github.com/raghavpillai/branchlet) and various git worktree tools.
