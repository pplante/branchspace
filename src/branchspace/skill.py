"""Agent Skill generation and installation for branchspace."""

from __future__ import annotations

from pathlib import Path

from branchspace.agents import get_project_root


SKILL_NAME = "branchspace"

SKILL_DESCRIPTION = (
    "Use Branchspace to work on code in isolated git worktree and Docker "
    "environments. Prefer branchspace commands for branch-based development workflows."
)

SKILL_BODY = """\
# Branchspace - Isolated Development Environments

Use Branchspace when you need to work on code in isolation without affecting the main working directory.

## When to Use Branchspace

- **Starting work on a new feature or bug fix**: Use `branchspace create <branch>` to create an isolated worktree
- **Need a clean environment**: Each worktree has its own working directory
- **Containerized development**: Use `branchspace shell` to work inside a Docker container with the code mounted

## Key Commands

| Task | Command |
|------|---------|
| Create isolated worktree | `branchspace create <branch>` |
| List worktrees | `branchspace ls` |
| Navigate to worktree | `branchspace cd <branch>` |
| Run in container | `branchspace shell [command]` |
| Remove worktree | `branchspace rm <branch>` |

## Workflow

1. **Create a worktree** for your feature branch:
   ```bash
   branchspace create feature/my-feature
   ```

2. **Navigate** to the worktree:
   ```bash
   branchspace cd feature/my-feature
   ```

3. **Work in isolation** - changes don't affect the main directory

4. **Use containerized shell** if the project requires specific tooling:
   ```bash
   branchspace shell
   ```

## Best Practices

- Prefer `branchspace create` over manual `git worktree add` for consistent setup
- Use `branchspace shell` when the project has a `branchspace.json` with container configuration
- Check `branchspace ls` to see active worktrees before creating new ones
- Clean up with `branchspace rm` when done to avoid orphaned worktrees
"""


def generate_skill_content() -> str:
    """Generate the full SKILL.md content with frontmatter and body."""
    frontmatter = f"""\
---
name: {SKILL_NAME}
description: {SKILL_DESCRIPTION}
---
"""
    return frontmatter + "\n" + SKILL_BODY


def get_global_skills_dir() -> Path:
    """Return the global skills directory (~/.skills/)."""
    return Path.home() / ".skills"


def get_project_skills_dir() -> Path:
    """Return the project-scoped skills directory (.skills/)."""
    return get_project_root() / ".skills"


def get_skill_install_path(scope: str) -> Path:
    """Return the full path to the skill directory for the given scope.

    Args:
        scope: Either "global" or "project"

    Returns:
        Path to the skill directory (e.g., ~/.skills/branchspace/ or .skills/branchspace/)
    """
    if scope == "global":
        base = get_global_skills_dir()
    elif scope == "project":
        base = get_project_skills_dir()
    else:
        raise ValueError(f"Unknown scope: {scope}. Must be 'global' or 'project'.")

    return base / SKILL_NAME


def get_skill_md_path(scope: str) -> Path:
    """Return the full path to the SKILL.md file for the given scope."""
    return get_skill_install_path(scope) / "SKILL.md"


def is_skill_installed(scope: str) -> bool:
    """Check if the skill is already installed at the given scope."""
    return get_skill_md_path(scope).exists()


def install_skill(scope: str) -> Path:
    """Install the branchspace skill at the given scope.

    Args:
        scope: Either "global" or "project"

    Returns:
        Path to the installed SKILL.md file
    """
    skill_dir = get_skill_install_path(scope)
    skill_dir.mkdir(parents=True, exist_ok=True)

    skill_md_path = skill_dir / "SKILL.md"
    content = generate_skill_content()
    skill_md_path.write_text(content, encoding="utf-8")

    return skill_md_path


def format_skill_path(path: Path, scope: str) -> str:
    """Format a skill path for user-friendly display.

    For project scope, returns a relative path like '.skills/branchspace/SKILL.md'.
    For global scope, returns a home-relative path like '~/.skills/branchspace/SKILL.md'.

    Args:
        path: The absolute path to format
        scope: Either "global" or "project"

    Returns:
        A user-friendly string representation of the path
    """
    if scope == "project":
        try:
            return str(path.relative_to(get_project_root()))
        except ValueError:
            return str(path)
    elif scope == "global":
        try:
            return "~/" + str(path.relative_to(Path.home()))
        except ValueError:
            return str(path)
    return str(path)
