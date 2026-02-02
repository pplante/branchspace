"""Worktree listing logic for branchspace."""

from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path

from branchspace.console import build_worktree_table as build_rich_worktree_table
from branchspace.git_utils import GitWorktree
from branchspace.git_utils import has_uncommitted_changes_with_untracked
from branchspace.git_utils import list_worktrees


@dataclass(frozen=True)
class WorktreeStatus:
    """Represents the status of a worktree for display."""

    branch: str
    path: Path
    is_current: bool
    is_dirty: bool


def _resolve_current_worktree_path(worktrees: Iterable[GitWorktree]) -> Path | None:
    for worktree in worktrees:
        if worktree.branch != "HEAD" and worktree.path.resolve() == Path.cwd().resolve():
            return worktree.path.resolve()
    return None


def list_worktree_statuses(repository_path: Path | None = None) -> list[WorktreeStatus]:
    worktrees = list_worktrees(repository_path)
    current_path = _resolve_current_worktree_path(worktrees)
    statuses: list[WorktreeStatus] = []
    for worktree in worktrees:
        status = WorktreeStatus(
            branch=worktree.branch,
            path=worktree.path,
            is_current=current_path is not None and worktree.path.resolve() == current_path,
            is_dirty=has_uncommitted_changes_with_untracked(worktree.path),
        )
        statuses.append(status)
    return sorted(statuses, key=lambda item: item.path.as_posix())


def build_worktree_list_table(statuses: list[WorktreeStatus]):
    table = build_rich_worktree_table()
    for status in statuses:
        branch_label = status.branch
        if status.is_current:
            branch_label = f"* {branch_label}"
        cleanliness = "dirty" if status.is_dirty else "clean"
        table.add_row(str(status.path), branch_label, cleanliness)
    return table
