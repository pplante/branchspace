"""Git utilities for branchspace operations."""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Optional


class ProtectedBranchLevel(Enum):
    """Protection level for branches."""

    NONE = "none"
    REQUIRE_PULL_REQUEST = "pr"
    REQUIRE_BRANCH_PROTECTION = "protection"


@dataclass
class GitStatus:
    """Represents git repository status."""

    is_git_repo: bool
    uncommitted_changes: bool
    unpushed_commits: bool
    current_branch: Optional[str] = None
    worktrees: list[GitWorktree] = field(default_factory=list)
    protected_branches: list[str] = field(default_factory=list)


@dataclass
class GitWorktree:
    """Represents a git worktree."""

    path: Path
    branch: str
    committed: bool
    detached: bool


@dataclass
class BranchInfo:
    """Represents branch information."""

    name: str
    is_current: bool
    is_protected: bool
    is_checked_out_elsewhere: bool
    has_unpushed_commits: bool


def _run_git_command(
    command: list[str], cwd: Optional[Path] = None, capture_output: bool = True
) -> subprocess.CompletedProcess:
    """Run a git command with proper error handling.

    Args:
        command: Git command to run as list of strings
        cwd: Working directory to run command in
        capture_output: Whether to capture stdout/stderr

    Returns:
        Completed process result

    Raises:
        CalledProcessError: If git command fails
    """
    try:
        result = subprocess.run(
            ["git"] + command,
            cwd=cwd,
            capture_output=capture_output,
            text=True,
            check=True,
        )
        return result
    except subprocess.CalledProcessError as e:
        if e.stderr:
            raise
        raise


def is_git_repository(path: Optional[Path] = None) -> bool:
    """Check if a directory is a git repository.

    Args:
        path: Directory to check. Defaults to current directory.

    Returns:
        True if the directory is a git repository, False otherwise.
    """
    try:
        _run_git_command(["rev-parse", "--is-inside-work-tree"], cwd=path)
        return True
    except subprocess.CalledProcessError:
        return False


def get_current_branch(path: Optional[Path] = None) -> Optional[str]:
    """Get the current branch name for the repository.

    Args:
        path: Directory to check. Defaults to current directory.

    Returns:
        Current branch name, or None if not on a branch.
    """
    try:
        result = _run_git_command(["rev-parse", "--abbrev-ref", "HEAD"], cwd=path)
        branch = result.stdout.strip()
        return branch if branch != "HEAD" else None
    except subprocess.CalledProcessError:
        return None


def list_worktrees(path: Optional[Path] = None) -> list[GitWorktree]:
    """List all worktrees in the repository.

    Args:
        path: Repository path. Defaults to current directory.

    Returns:
        List of GitWorktree objects representing each worktree.

    Raises:
        CalledProcessError: If git command fails.
    """
    result = _run_git_command(["worktree", "list", "--porcelain"], cwd=path)

    worktrees = []
    current_path = None
    current_branch = None
    current_committed = None

    for line in result.stdout.strip().split("\n"):
        if not line:
            if current_path and current_branch:
                is_detached = current_branch == "HEAD"
                worktrees.append(
                    GitWorktree(
                        path=current_path,
                        branch=current_branch,
                        committed=current_committed is not None,
                        detached=is_detached,
                    )
                )
            current_path = None
            current_branch = None
            current_committed = None
            continue

        parts = line.split(None, 1)
        prefix = parts[0]
        value = parts[1] if len(parts) > 1 else ""

        if prefix == "worktree":
            current_path = Path(value)
        elif prefix == "branch":
            # Strip refs/heads/ prefix if present
            current_branch = value.removeprefix("refs/heads/")
        elif prefix == "HEAD detached":
            current_branch = "HEAD"
            current_committed = False

    # Add the last worktree if present
    if current_path and current_branch:
        worktrees.append(
            GitWorktree(
                path=current_path,
                branch=current_branch,
                committed=current_committed is not None,
                detached=current_branch == "HEAD",
            )
        )

    return worktrees


def create_worktree(
    path: Path,
    branch: str,
    repository_path: Optional[Path] = None,
    create_branch: bool = True,
) -> GitWorktree:
    """Create a new worktree with a new or existing branch.

    Args:
        path: Path where the worktree should be created
        branch: Name of the branch to create or existing branch to check out
        repository_path: Path to the repository. Defaults to current directory.
        create_branch: If True, create a new branch. If False, use existing branch.

    Returns:
        GitWorktree object representing the newly created worktree.

    Raises:
        CalledProcessError: If worktree creation fails.
    """
    if create_branch:
        _run_git_command(
            ["worktree", "add", "-b", branch, str(path)],
            cwd=repository_path,
        )
    else:
        _run_git_command(
            ["worktree", "add", str(path), branch],
            cwd=repository_path,
        )

    return GitWorktree(
        path=path,
        branch=branch,
        committed=True,
        detached=False,
    )


def remove_worktree(
    worktree_path: Path,
    force: bool = False,
    repository_path: Optional[Path] = None,
) -> None:
    """Remove a worktree safely.

    Args:
        worktree_path: Path to the worktree to remove
        force: Force removal even if it has uncommitted changes.
        repository_path: Path to the main repository. Defaults to current directory.

    Raises:
        CalledProcessError: If worktree removal fails.
    """
    if force:
        _run_git_command(["worktree", "remove", "--force", str(worktree_path)], cwd=repository_path)
    else:
        _run_git_command(["worktree", "remove", str(worktree_path)], cwd=repository_path)


def get_protected_branches(
    repository_path: Optional[Path] = None,
) -> list[str]:
    """Get the list of protected branch names.

    Args:
        repository_path: Repository path. Defaults to current directory.

    Returns:
        List of protected branch names.
    """
    default_protected = ["main", "master", "develop", "staging", "production"]
    try:
        config = _run_git_command(
            ["config", "--get-regexp", r"branch\.(.*)\.protect"],
            cwd=repository_path,
            capture_output=True,
        )
        lines = config.stdout.strip().split("\n")
        protected = set()

        for line in lines:
            parts = line.split()
            if len(parts) >= 2:
                full_key = parts[0]
                branch_name = full_key.replace("branch.", "").split(".")[0]
                protected.add(branch_name)

        return sorted(protected) if protected else default_protected
    except subprocess.CalledProcessError:
        return default_protected


def has_uncommitted_changes(path: Optional[Path] = None) -> bool:
    """Check if there are uncommitted changes in the repository.

    Args:
        path: Repository path. Defaults to current directory.

    Returns:
        True if there are uncommitted changes, False otherwise.
    """
    try:
        result = _run_git_command(
            ["status", "--porcelain", "--untracked-files=no"],
            cwd=path,
            capture_output=True,
        )
        return bool(result.stdout.strip())
    except subprocess.CalledProcessError:
        return False


def has_unpushed_commits(path: Optional[Path] = None) -> bool:
    """Check if there are commits that haven't been pushed to the remote.

    Args:
        path: Repository path. Defaults to current directory.

    Returns:
        True if there are unpushed commits, False otherwise.
    """
    try:
        result = _run_git_command(
            ["rev-list", "--not", "--remotes", "HEAD"],
            cwd=path,
            capture_output=True,
        )
        return bool(result.stdout.strip())
    except subprocess.CalledProcessError:
        return False


def list_branches(path: Optional[Path] = None) -> list[BranchInfo]:
    """List all branches in the repository.

    Args:
        path: Repository path. Defaults to current directory.

    Returns:
        List of BranchInfo objects representing each branch.

    Raises:
        CalledProcessError: If git command fails.
    """
    protected_branches = get_protected_branches(path)

    # Get branches checked out in worktrees
    worktrees = list_worktrees(path)
    branches_in_worktrees = {w.branch for w in worktrees if not w.detached}

    result = _run_git_command(["branch", "-a", "--format=%(refname:short)|%(HEAD)"], cwd=path)
    branches = []

    for line in result.stdout.strip().split("\n"):
        if not line:
            continue

        parts = line.split("|")
        if len(parts) < 2:
            continue

        branch_name = parts[0].strip()
        is_head = parts[1].strip() == "*"

        # Branch is checked out elsewhere if it's in a worktree but not current
        is_checked_out_elsewhere = branch_name in branches_in_worktrees and not is_head

        branches.append(
            BranchInfo(
                name=branch_name,
                is_current=is_head,
                is_protected=branch_name in protected_branches,
                is_checked_out_elsewhere=is_checked_out_elsewhere,
                has_unpushed_commits=False,
            )
        )

    return branches


def get_git_status(path: Optional[Path] = None) -> GitStatus:
    """Get comprehensive git status information.

    Args:
        path: Repository path. Defaults to current directory.

    Returns:
        GitStatus object with all relevant status information.
    """
    is_repo = is_git_repository(path)
    current_branch = get_current_branch(path) if is_repo else None
    uncommitted = has_uncommitted_changes(path) if is_repo else False
    unpushed = has_unpushed_commits(path) if is_repo else False
    protected_branches = get_protected_branches(path) if is_repo else []
    worktrees = list_worktrees(path) if is_repo else []

    return GitStatus(
        is_git_repo=is_repo,
        uncommitted_changes=uncommitted,
        unpushed_commits=unpushed,
        current_branch=current_branch,
        worktrees=worktrees,
        protected_branches=protected_branches,
    )
