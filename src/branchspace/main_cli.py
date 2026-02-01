"""Main CLI entrypoint for branchspace."""

from __future__ import annotations

import subprocess

import click

from branchspace import __version__
from branchspace.config import ConfigError
from branchspace.config import load_config
from branchspace.console import error
from branchspace.console import info
from branchspace.console import spinner
from branchspace.console import success
from branchspace.worktree_create import CreateWorktreeError
from branchspace.worktree_create import create_worktrees
from branchspace.worktree_cd import WorktreeLookupError
from branchspace.worktree_cd import resolve_worktree_path
from branchspace.worktree_remove import WorktreeRemoveError
from branchspace.worktree_remove import remove_worktrees
from branchspace.worktree_list import build_worktree_list_table
from branchspace.worktree_list import list_worktree_statuses


@click.group("branchspace", help="Manage git worktrees and environments.")
@click.version_option(__version__, "--version", prog_name="branchspace")
def main() -> None:
    """Branchspace CLI."""


@main.command(help="Create a new worktree.")
@click.argument("branch", nargs=-1, required=True)
def create(branch: tuple[str, ...]) -> None:
    """Create a new worktree."""
    try:
        config = load_config()
    except ConfigError as exc:
        error(str(exc))
        raise SystemExit(1) from exc

    try:
        with spinner("Creating worktrees"):
            results = create_worktrees(list(branch), config)
    except CreateWorktreeError as exc:
        error(str(exc))
        raise SystemExit(1) from exc
    except OSError as exc:
        error(str(exc))
        raise SystemExit(1) from exc
    except subprocess.CalledProcessError as exc:
        error(exc.stderr.strip() if exc.stderr else str(exc))
        raise SystemExit(1) from exc

    for created in results:
        success(f"Created {created.branch} at {created.path}")
    info("Worktrees ready.")


@main.command(help="Remove a worktree.")
@click.argument("branch", nargs=-1, required=True)
def rm(branch: tuple[str, ...]) -> None:
    """Remove a worktree."""
    try:
        config = load_config()
    except ConfigError as exc:
        error(str(exc))
        raise SystemExit(1) from exc

    try:
        results = remove_worktrees(list(branch), config)
    except WorktreeRemoveError as exc:
        error(str(exc))
        raise SystemExit(1) from exc
    except subprocess.CalledProcessError as exc:
        error(exc.stderr.strip() if exc.stderr else str(exc))
        raise SystemExit(1) from exc

    for result in results:
        if result.removed:
            success(f"Removed {result.branch} at {result.path}")
        else:
            info(f"Skipped {result.branch} at {result.path}")


@main.command(help="Change to a worktree.")
@click.argument("branch", required=False)
def cd(branch: str | None) -> None:
    """Change to a worktree."""
    try:
        resolved = resolve_worktree_path(branch)
    except WorktreeLookupError as exc:
        error(str(exc))
        raise SystemExit(1) from exc

    click.echo(str(resolved.path))


@main.command(help="List worktrees.")
def ls() -> None:
    """List worktrees."""
    try:
        statuses = list_worktree_statuses()
    except subprocess.CalledProcessError as exc:
        error(exc.stderr.strip() if exc.stderr else str(exc))
        raise SystemExit(1) from exc

    if not statuses:
        info("No worktrees found.")
        return

    table = build_worktree_list_table(statuses)
    from branchspace.console import get_console

    get_console().print(table)


@main.command(help="Open an interactive shell.")
def shell() -> None:
    """Open an interactive shell."""
    click.echo("Not implemented yet.")


@main.command(help="Purge a worktree and related resources.")
def purge() -> None:
    """Purge a worktree and related resources."""
    click.echo("Not implemented yet.")


@main.command(help="Initialize configuration for this repository.")
def init() -> None:
    """Initialize branchspace configuration."""
    click.echo("Not implemented yet.")


@main.command(name="config", help="Show or edit configuration.")
def config_cmd() -> None:
    """Show or edit configuration."""
    click.echo("Not implemented yet.")


@main.command(name="shell-integration", help="Install shell integration.")
def shell_integration() -> None:
    """Install shell integration."""
    click.echo("Not implemented yet.")
