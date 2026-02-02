"""Rich console utilities for branchspace output."""

from collections.abc import Iterator
from contextlib import contextmanager
from dataclasses import dataclass

from rich.console import Console
from rich.status import Status
from rich.table import Table


@dataclass(frozen=True)
class ConsoleTheme:
    success: str = "green"
    warning: str = "yellow"
    error: str = "red"
    info: str = "cyan"
    muted: str = "dim"


_THEME = ConsoleTheme()
_CONSOLE = Console()


def get_console() -> Console:
    """Return the shared console instance."""
    return _CONSOLE


def success(message: str) -> None:
    """Print a success message."""
    _CONSOLE.print(f"[bold {_THEME.success}]+[/] {message}")


def warning(message: str) -> None:
    """Print a warning message."""
    _CONSOLE.print(f"[bold {_THEME.warning}]![/] {message}")


def error(message: str) -> None:
    """Print an error message."""
    _CONSOLE.print(f"[bold {_THEME.error}]x[/] {message}")


def info(message: str) -> None:
    """Print an informational message."""
    _CONSOLE.print(f"[{_THEME.info}]{message}[/]")


def build_worktree_table() -> Table:
    """Create a worktree listing table."""
    table = Table(title="Worktrees", show_lines=False)
    table.add_column("Path", style=_THEME.info)
    table.add_column("Branch", style="bold")
    table.add_column("Status", style=_THEME.muted)
    return table


@contextmanager
def spinner(message: str) -> Iterator[Status]:
    """Display a spinner for long-running operations."""
    status = _CONSOLE.status(f"[{_THEME.info}]{message}[/]", spinner="dots")
    status.start()
    try:
        yield status
    finally:
        status.stop()
