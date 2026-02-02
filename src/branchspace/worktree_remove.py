"""Worktree removal logic for branchspace."""

from collections.abc import Iterable
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

import questionary

from branchspace.config import BranchspaceConfig
from branchspace.config import get_git_root
from branchspace.git_utils import get_protected_branches
from branchspace.git_utils import has_uncommitted_changes_with_untracked
from branchspace.git_utils import has_unpushed_commits
from branchspace.git_utils import list_worktrees
from branchspace.git_utils import remove_worktree


PROTECTED_BRANCHES = {"main", "master", "develop", "staging", "production"}


class WorktreeRemoveError(RuntimeError):
    """Raised when worktree removal fails."""


@dataclass(frozen=True)
class RemovalResult:
    """Represents the result of a worktree removal."""

    branch: str
    path: Path
    removed: bool


def _ensure_git_root(repo_root: Path | None) -> Path:
    root = get_git_root(repo_root)
    if root is None:
        raise WorktreeRemoveError("Not inside a git repository.")
    return root


def _is_protected(branch: str, repo_root: Path) -> bool:
    protected = set(get_protected_branches(repo_root)) | PROTECTED_BRANCHES
    return branch in protected


def _branch_checked_out_elsewhere(branch: str, worktrees: Sequence, current_path: Path) -> bool:
    for worktree in worktrees:
        if worktree.branch == branch and worktree.path.resolve() != current_path:
            return True
    return False


def _confirm(prompt: str) -> bool:
    return bool(questionary.confirm(prompt).unsafe_ask())


def _find_worktree_path(branch: str, worktrees: Sequence) -> Path | None:
    for worktree in worktrees:
        if worktree.branch == branch:
            return worktree.path
    return None


def remove_worktree_for_branch(
    branch: str,
    config: BranchspaceConfig,
    repo_root: Path | None = None,
    *,
    confirm: bool = True,
) -> RemovalResult:
    root = _ensure_git_root(repo_root)
    if _is_protected(branch, root):
        raise WorktreeRemoveError(f"Branch '{branch}' is protected and cannot be removed.")

    worktrees = list_worktrees(root)
    current_path = Path.cwd().resolve()
    if _branch_checked_out_elsewhere(branch, worktrees, current_path):
        raise WorktreeRemoveError(f"Branch '{branch}' is checked out in another worktree.")

    worktree_path = _find_worktree_path(branch, worktrees)
    if worktree_path is None:
        raise WorktreeRemoveError(f"No worktree found for branch '{branch}'.")

    if (
        confirm
        and has_uncommitted_changes_with_untracked(worktree_path)
        and not _confirm(f"Worktree '{branch}' has uncommitted changes. Remove anyway?")
    ):
        return RemovalResult(branch=branch, path=worktree_path, removed=False)

    if (
        confirm
        and has_unpushed_commits(worktree_path)
        and not _confirm(f"Worktree '{branch}' has unpushed commits. Remove anyway?")
    ):
        return RemovalResult(branch=branch, path=worktree_path, removed=False)

    remove_worktree(worktree_path, repository_path=root)

    if config.purge_on_remove:
        import subprocess

        subprocess.run(["git", "branch", "-D", branch], cwd=root, check=False)

    return RemovalResult(branch=branch, path=worktree_path, removed=True)


def remove_worktrees(
    branches: Iterable[str],
    config: BranchspaceConfig,
    repo_root: Path | None = None,
    *,
    confirm: bool = True,
) -> list[RemovalResult]:
    results: list[RemovalResult] = []
    for branch in branches:
        results.append(
            remove_worktree_for_branch(
                branch,
                config,
                repo_root=repo_root,
                confirm=confirm,
            )
        )
    return results
