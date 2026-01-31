# CLAUDE.md

This file provides guidance to Claude Code when working with code in this repository.

## Project Overview

branchspace is a Python CLI tool that provides a unified interface for managing git worktrees and branch-specific Docker environments.

## Key Architecture

### Python Package Structure

```
src/branchspace/
├── __init__.py          # Package version
├── __main__.py          # Module entry point
├── cli.py               # Click-based CLI commands
├── config.py            # Pydantic config models and loading
├── git.py               # Git operations (worktrees, branches)
├── docker.py            # Docker integration
└── templates.py         # Variable expansion and file copying
```

### Core Components

**Configuration System** (`config.py`):

- Pydantic models for `branchspace.json` validation
- Auto-discovery from git root
- Type-safe config with defaults

**CLI Interface** (`cli.py`):

- Click for command parsing and routing
- Rich for beautiful terminal output
- Questionary for interactive prompts

**Git Operations** (`git.py`):

- Worktree creation, removal, listing
- Branch safety checks (protected, uncommitted, unpushed)
- Parsing `git worktree list --porcelain`

**Docker Integration** (`docker.py`):

- Branch-specific project naming: `<base>_<branch>`
- Service detection and selection
- Build, exec, and cleanup operations

**Template Engine** (`templates.py`):

- Variable expansion: `$BASE_PATH`, `$BRANCH_NAME`, `$WORKTREE_PATH`, `$SOURCE_BRANCH`
- Glob-based file copying with include/exclude patterns

### Configuration Schema

The `branchspace.json` file in repository root:

```python
class BranchspaceConfig(BaseModel):
    worktree_copy_patterns: list[str]        # Files to copy to new worktrees
    worktree_copy_ignores: list[str]         # Files to exclude from copying
    worktree_path_template: str              # Template for worktree paths
    post_create_cmd: list[str]               # Commands to run after creation
    terminal_command: str                     # Command to open editor
    purge_on_remove: bool                     # Delete branch + Docker on rm
    shell: str                             # Shell for interactive sessions
    container_config: str | object           # Container configuration (supports shorthand)
```

### Container Configuration Shorthand

The `container_config` field supports both full objects and shorthand strings:

**Shorthand formats:**

- `"image:<name>"` → Use a pre-built Docker image
- `"build"` → Build from current directory (default Dockerfile)
- `"build:<context>"` → Build from custom context directory

**Examples:**

```json
{
  "container_config": "image:python:3.11"
}
```

```json
{
  "container_config": "build:./docker"
}
```

**Full configuration (equivalent to shorthand):**

```json
{
  "container_config": {
    "image": "python:3.11"
  }
}
```

### Container Types

**ContainerImageConfig**:

- Use a specific Docker image
- Mounts current directory as `/workspace`
- Good for simple environments

**BuildContainerConfig**:

- Build from Dockerfile in specified context
- Mounts current directory as `/workspace`
- Good for custom development environments

### Command Flow

**create**:

1. Validate branch doesn't exist
2. Calculate worktree path from template
3. Create worktree with `git worktree add`
4. Copy files based on patterns
5. Run post-create commands
6. Open terminal/editor

**rm**:

1. Find worktree by name (branch or directory)
2. Check for uncommitted changes (prompt)
3. Remove worktree with `git worktree remove`
4. If `purgeOnRemove`: delete branch + purge Docker

**run/shell**:

1. Get project name (`<base>_<branch>`)
2. Build and start containers
3. Select service (config or prompt)
4. Execute command in container

### Safety Features

- **Protected branches**: main, master, develop, staging, production
- **Uncommitted changes**: Prompt before removal
- **Unpushed commits**: Warn and confirm before deletion
- **Branch in use**: Cannot delete if checked out elsewhere

## Development Commands

### Setup

```bash
pip install -e ".[dev]"
```

### Testing

```bash
pytest
pytest --cov=branchspace
```

### Code quality

```bash
black src/
ruff check src/
mypy src/
```

### Install locally

```bash
pip install -e .
branchspace --help
```

## Technical Constraints

### Python Version

Requires Python 3.9+ for:

- Type hints with `list[str]` (no `typing.List`)
- `pathlib` improvements
- Modern Pydantic

### Dependencies

**Required**:

- click - CLI framework
- rich - Terminal formatting
- pydantic - Config validation
- questionary - Interactive prompts

**Optional**:

- docker (system command)
- git (system command)

### Shell Integration

The `cd` command cannot change the parent shell's directory from Python. Solution:

```bash
branchspace() {
  if [[ "$1" == "cd" ]]; then
    local target=$(command branchspace cd --print-path "$2")
    [[ -n "$target" ]] && cd "$target"
  else
    command branchspace "$@"
  fi
}
```

This wrapper intercepts `cd` commands and uses `--print-path` flag.

### Docker Container Management

The Docker integration creates ephemeral containers for development environments:

- **ContainerImageConfig**: Uses pre-built images with workspace mounted
- **BuildContainerConfig**: Builds from Dockerfile then mounts workspace

Containers are automatically named and cleaned up after use.

## Important Patterns

### Error Handling

All modules raise specific exceptions:

- `GitError` - Git operation failures
- `DockerError` - Docker operation failures
- `ValueError` - Config validation failures

CLI catches these and displays rich formatted errors.

### Path Handling

Always use `pathlib.Path`:

```python
worktree_path = Path(template_str)
worktree_path.parent.mkdir(parents=True, exist_ok=True)
```

### Subprocess Execution

Git and Docker commands use `subprocess.run`:

```python
result = subprocess.run(
    ["git", "worktree", "list", "--porcelain"],
    capture_output=True,
    text=True,
    check=True,
    cwd=cwd,
)
```

### Rich Output

Use console helpers for consistent formatting:

```python
from branchspace.cli import error, success, warning, info

error("Branch already exists")
success("Worktree created")
warning("Uncommitted changes")
info("Branch is protected")
```

### Config Aliases

Pydantic handles JSON camelCase → Python snake_case:

```python
class BranchspaceConfig(BaseModel):
    worktree_copy_patterns: list[str] = Field(
        alias="worktreeCopyPatterns"
    )
```

## Common Tasks

### Adding a new config option

1. Add field to `BranchspaceConfig` in `config.py`
2. Add alias for JSON compatibility
3. Set default value
4. Use in relevant command in `cli.py`

### Adding a new command

1. Add function decorated with `@main.command()` in `cli.py`
2. Add Click arguments/options
3. Import needed functions from other modules
4. Handle errors with try/except
5. Use rich console for output

### Adding git functionality

1. Add function to `git.py`
2. Use `run_git()` helper
3. Raise `GitError` on failures
4. Return typed data (Path, str, list, dataclass)

## Testing Strategy

### Unit Tests

Test individual functions:

- Template expansion
- Config loading/validation
- Git parsing functions
- Path calculations

### Integration Tests

Test command flows:

- Create → verify worktree exists
- RM → verify cleanup
- Config → verify JSON handling

### Manual Testing

Create test repo with:

- `branchspace.json`
- `Dockerfile` (optional)
- Multiple branches

## Important Notes

- **No Zsh dependency**: Pure Python, cross-platform
- **Git is source of truth**: Parse `git worktree list`, don't maintain state
- **Docker is optional**: All worktree commands work without Docker
- **Config is optional**: Everything has sensible defaults
- **Template variables**: Always expand before using paths
- **Interactive prompts**: Use questionary for user input
- **Glob patterns**: Support `**` for recursive matching
- Dont use local imports unless it fixes a circular import issue.

<!-- BACKLOG.MD MCP GUIDELINES START -->

<CRITICAL_INSTRUCTION>

## BACKLOG WORKFLOW INSTRUCTIONS

This project uses Backlog.md MCP for all task and project management activities.

**CRITICAL GUIDANCE**

- If your client supports MCP resources, read `backlog://workflow/overview` to understand when and how to use Backlog for this project.
- If your client only supports tools or the above request fails, call `backlog.get_workflow_overview()` tool to load the tool-oriented overview (it lists the matching guide tools).

- **First time working here?** Read the overview resource IMMEDIATELY to learn the workflow
- **Already familiar?** You should have the overview cached ("## Backlog.md Overview (MCP)")
- **When to read it**: BEFORE creating tasks, or when you're unsure whether to track work

These guides cover:
- Decision framework for when to create tasks
- Search-first workflow to avoid duplicates
- Links to detailed guides for task creation, execution, and finalization
- MCP tools reference

You MUST read the overview resource to understand the complete workflow. The information is NOT summarized here.

</CRITICAL_INSTRUCTION>

<!-- BACKLOG.MD MCP GUIDELINES END -->
