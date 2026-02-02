"""AI agent instruction generation for branchspace."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from branchspace.config import find_config_file
from branchspace.config import get_git_root


@dataclass(frozen=True)
class AgentSpec:
    """Represents a supported AI coding agent."""

    name: str
    filename: str
    recommended: bool = False


SUPPORTED_AGENTS: list[AgentSpec] = [
    AgentSpec(name="Claude Code", filename="CLAUDE.md", recommended=True),
    AgentSpec(name="Codex CLI", filename="AGENTS.md"),
    AgentSpec(name="OpenCode", filename="AGENTS.md"),
    AgentSpec(name="Cursor", filename=".cursorrules"),
    AgentSpec(name="GitHub Copilot CLI", filename="AGENTS.md"),
    AgentSpec(name="Windsurf", filename=".windsurfrules"),
    AgentSpec(name="Gemini CLI", filename="AGENTS.md"),
]


def format_agent_label(agent: AgentSpec) -> str:
    """Return a display label for a prompt menu."""
    if agent.recommended:
        return f"{agent.name} (Recommended)"
    return agent.name


def get_project_root() -> Path:
    """Resolve the project root for instruction output."""
    config_path = find_config_file()
    if config_path is not None:
        return config_path.parent

    git_root = get_git_root()
    if git_root is not None:
        return git_root

    return Path.cwd()


def generate_instructions(audience: list[str]) -> str:
    """Generate unified AI agent instructions for branchspace."""
    audience_label = ", ".join(audience) if audience else "AI coding agents"

    return "\n".join(
        [
            "# Branchspace - AI Agent Instructions",
            "",
            f"Intended for: {audience_label}",
            "",
            "## Project Overview",
            "branchspace is a CLI tool that manages git worktrees and branch-specific Docker environments.",
            "It provides a unified interface for creating, listing, and removing worktrees, plus running",
            "containerized shells tied to a branch.",
            "",
            "## Command Reference",
            "- `branchspace create <branch>`: Create one or more new worktrees.",
            "- `branchspace rm <branch>`: Remove worktrees safely.",
            "- `branchspace ls`: List worktrees and their status.",
            "- `branchspace cd <branch>`: Print the worktree path for shell integration.",
            "- `branchspace shell [command]`: Open an interactive container shell.",
            "- `branchspace purge`: Clean up Docker resources for worktrees.",
            "- `branchspace init`: Initialize `branchspace.json` configuration.",
            "- `branchspace config`: View resolved configuration values.",
            "- `branchspace shell-integration`: Install shell helpers for `branchspace cd`.",
            "",
            "## Integration Tips",
            "- Use `branchspace create` instead of manual `git worktree add` to keep workflows consistent.",
            "- Pair `branchspace ls` with `branchspace cd` for quick navigation between branches.",
            "- Prefer `branchspace shell` when the repo relies on containerized tooling.",
            "- Run `branchspace config` to confirm configuration values before automation steps.",
            "- Honor protected branches and prompts; avoid force removals without confirmation.",
        ]
    )


def write_instructions(path: Path, content: str, mode: str) -> None:
    """Write instructions to a file using the selected mode."""
    if mode == "skip":
        return

    if mode == "overwrite":
        path.write_text(content, encoding="utf-8")
        return

    if mode == "append":
        existing = ""
        if path.exists():
            existing = path.read_text(encoding="utf-8")

        if existing:
            if not existing.endswith("\n"):
                existing += "\n"
            existing += "\n"
            path.write_text(existing + content, encoding="utf-8")
        else:
            path.write_text(content, encoding="utf-8")
        return

    raise ValueError(f"Unknown write mode: {mode}")
