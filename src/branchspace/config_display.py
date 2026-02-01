"""Helpers to display branchspace configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from rich.table import Table

from branchspace.config import BranchspaceConfig
from branchspace.config import ContainerBuildConfig
from branchspace.config import ContainerImageConfig
from branchspace.config import find_config_file
from branchspace.config import load_config
from branchspace.console import get_console
from branchspace.console import info


@dataclass(frozen=True)
class ConfigView:
    """Represents configuration values for display."""

    config: BranchspaceConfig
    config_path: Path | None


def load_config_view() -> ConfigView:
    """Load configuration and return a display view."""
    config_path = find_config_file()
    return ConfigView(config=load_config(config_path), config_path=config_path)


def _iter_config_rows(config: BranchspaceConfig) -> Iterable[tuple[str, str]]:
    yield "worktreeCopyPatterns", ", ".join(config.worktree_copy_patterns)
    yield "worktreeCopyIgnores", ", ".join(config.worktree_copy_ignores)
    yield "worktreePathTemplate", config.worktree_path_template
    yield "postCreateCmd", ", ".join(config.post_create_cmd) or "(none)"
    yield "terminalCommand", config.terminal_command or "(none)"
    yield "purgeOnRemove", "true" if config.purge_on_remove else "false"
    if isinstance(config.container_config, ContainerImageConfig):
        yield "containerConfig.image", config.container_config.image
    elif isinstance(config.container_config, ContainerBuildConfig):
        yield "containerConfig.context", config.container_config.context
        yield "containerConfig.dockerfile", config.container_config.dockerfile
    yield "shell", config.shell


def build_config_table(config: BranchspaceConfig) -> Table:
    """Build a Rich table representing configuration values."""
    table = Table(title="Branchspace Configuration")
    table.add_column("Key", style="cyan")
    table.add_column("Value", style="bold")
    for key, value in _iter_config_rows(config):
        table.add_row(key, value)
    return table


def render_config(view: ConfigView) -> None:
    """Render the configuration to the console."""
    if view.config_path is None:
        info("Using defaults (no branchspace.json found).")
    else:
        info(f"Config file: {view.config_path}")
    table = build_config_table(view.config)
    get_console().print(table)
