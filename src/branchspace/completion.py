"""Shell completion helpers for branchspace CLI."""

from __future__ import annotations

from typing import TYPE_CHECKING

from click.shell_completion import CompletionItem

from branchspace.git_utils import list_worktrees


if TYPE_CHECKING:
    from click.core import Context
    from click.core import Parameter


class WorktreeBranchComplete:
    """Complete with existing worktree branch names."""

    def __call__(self, ctx: Context, param: Parameter, incomplete: str) -> list[CompletionItem]:
        """Return completion items for worktree branches.

        Args:
            ctx: Click context
            param: Parameter being completed
            incomplete: Partial value typed by user

        Returns:
            List of CompletionItem objects for matching branches
        """
        try:
            worktrees = list_worktrees()
            return [
                CompletionItem(wt.branch)
                for wt in worktrees
                if wt.branch.startswith(incomplete) and not wt.detached
            ]
        except Exception:
            return []
