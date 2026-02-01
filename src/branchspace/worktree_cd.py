"""Worktree path resolution for `branchspace cd`."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from branchspace.config import get_git_root
from branchspace.git_utils import list_worktrees


class WorktreeLookupError(RuntimeError):
    """Raised when a worktree path cannot be resolved."""


@dataclass(frozen=True)
class WorktreePath:
    """Resolved worktree path for a branch."""

    branch: Optional[str]
    path: Path


def resolve_worktree_path(branch: str | None, repo_root: Path | None = None) -> WorktreePath:
    """Resolve a worktree path for a branch or git root when branch is None."""
    root = get_git_root(repo_root)
    if root is None:
        raise WorktreeLookupError("Not inside a git repository.")

    if branch is None:
        return WorktreePath(branch=None, path=root)

    for worktree in list_worktrees(root):
        if worktree.branch == branch:
            return WorktreePath(branch=branch, path=worktree.path)

    raise WorktreeLookupError(f"No worktree found for branch '{branch}'.")
