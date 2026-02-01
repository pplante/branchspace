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
def rm() -> None:
    """Remove a worktree."""
    click.echo("Not implemented yet.")


@main.command(help="Change to a worktree.")
def cd() -> None:
    """Change to a worktree."""
    click.echo("Not implemented yet.")


@main.command(help="List worktrees.")
def ls() -> None:
    """List worktrees."""
    click.echo("Not implemented yet.")


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
