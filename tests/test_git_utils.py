"""Tests for git utilities module."""

from __future__ import annotations

import subprocess

from pathlib import Path

import pytest

from branchspace.git_utils import BranchInfo
from branchspace.git_utils import GitStatus
from branchspace.git_utils import GitWorktree
from branchspace.git_utils import create_worktree
from branchspace.git_utils import get_current_branch
from branchspace.git_utils import get_git_status
from branchspace.git_utils import get_protected_branches
from branchspace.git_utils import has_uncommitted_changes
from branchspace.git_utils import has_unpushed_commits
from branchspace.git_utils import is_git_repository
from branchspace.git_utils import list_branches
from branchspace.git_utils import list_worktrees
from branchspace.git_utils import remove_worktree


def _init_git_repo(path: Path, with_commit: bool = False) -> None:
    """Initialize a git repository with optional initial commit."""
    subprocess.run(["git", "init"], cwd=path, capture_output=True, check=True)
    subprocess.run(
        ["git", "config", "user.email", "test@example.com"],
        cwd=path,
        capture_output=True,
        check=True,
    )
    subprocess.run(
        ["git", "config", "user.name", "Test User"],
        cwd=path,
        capture_output=True,
        check=True,
    )
    if with_commit:
        (path / "README.md").write_text("# Test Repo")
        subprocess.run(["git", "add", "README.md"], cwd=path, capture_output=True, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Initial commit"],
            cwd=path,
            capture_output=True,
            check=True,
        )


class TestIsGitRepository:
    """Tests for is_git_repository function."""

    def test_returns_true_in_repo(self):
        """Test returns True when in a git repository."""
        result = is_git_repository()
        assert result is True

    def test_returns_false_outside_repo(self, tmp_path: Path):
        """Test returns False when not in a git repository."""
        result = is_git_repository(tmp_path)
        assert result is False

    def test_checks_specific_path(self, tmp_path: Path):
        """Test checks the specified path."""
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True, check=True)

        subdir = tmp_path / "subdir"
        subdir.mkdir()

        assert is_git_repository(tmp_path) is True
        assert is_git_repository(subdir) is True


class TestGetCurrentBranch:
    """Tests for get_current_branch function."""

    def test_returns_branch_name(self):
        """Test returns current branch name."""
        branch = get_current_branch()
        assert branch is not None
        assert branch != "HEAD"

    def test_returns_none_on_detached(self, tmp_path: Path):
        """Test returns None when in detached HEAD state."""
        _init_git_repo(tmp_path, with_commit=True)
        # Create a second commit so we can detach to a previous one
        (tmp_path / "file2.txt").write_text("content")
        subprocess.run(["git", "add", "file2.txt"], cwd=tmp_path, capture_output=True, check=True)
        subprocess.run(
            ["git", "commit", "-m", "Second commit"],
            cwd=tmp_path,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "checkout", "--detach", "HEAD~1"],
            cwd=tmp_path,
            capture_output=True,
            check=True,
        )

        branch = get_current_branch(tmp_path)
        assert branch is None

    def test_returns_none_in_non_repo(self, tmp_path: Path):
        """Test returns None when not in a git repository."""
        branch = get_current_branch(tmp_path)
        assert branch is None


class TestListWorktrees:
    """Tests for list_worktrees function."""

    def test_lists_existing_worktrees(self, tmp_path: Path):
        """Test lists existing worktrees."""
        _init_git_repo(tmp_path, with_commit=True)

        worktree_path = tmp_path / "worktree1"
        create_worktree(worktree_path, "feature-1", tmp_path)

        worktrees = list_worktrees(tmp_path)

        # Should have main worktree + feature-1 worktree
        assert len(worktrees) >= 2
        assert any(w.branch == "feature-1" for w in worktrees)

    def test_returns_main_worktree_only_when_no_additional_worktrees(self, tmp_path: Path):
        """Test returns only the main worktree when no additional worktrees exist."""
        _init_git_repo(tmp_path, with_commit=True)

        worktrees = list_worktrees(tmp_path)

        # The main worktree is always included
        assert len(worktrees) == 1
        assert worktrees[0].branch == "main"


class TestCreateWorktree:
    """Tests for create_worktree function."""

    def test_creates_worktree_with_branch(self, tmp_path: Path):
        """Test creates worktree with new branch."""
        _init_git_repo(tmp_path, with_commit=True)

        worktree_path = tmp_path / "worktree1"
        worktree = create_worktree(worktree_path, "feature-1", tmp_path)

        assert worktree.path == worktree_path
        assert worktree.branch == "feature-1"
        assert worktree.committed is True
        assert worktree.detached is False

        assert worktree_path.exists()

    def test_fails_if_worktree_exists(self, tmp_path: Path):
        """Test raises error if worktree already exists."""
        _init_git_repo(tmp_path, with_commit=True)

        worktree_path = tmp_path / "worktree1"
        create_worktree(worktree_path, "feature-1", tmp_path)

        with pytest.raises(subprocess.CalledProcessError):
            create_worktree(worktree_path, "feature-2", tmp_path)

    def test_creates_worktree_with_existing_branch(self, tmp_path: Path):
        """Test creates worktree with an existing branch."""
        _init_git_repo(tmp_path, with_commit=True)

        # Create a branch first
        subprocess.run(
            ["git", "branch", "existing-branch"],
            cwd=tmp_path,
            capture_output=True,
            check=True,
        )

        worktree_path = tmp_path / "worktree1"
        worktree = create_worktree(worktree_path, "existing-branch", tmp_path, create_branch=False)

        assert worktree.path == worktree_path
        assert worktree.branch == "existing-branch"
        assert worktree_path.exists()


class TestRemoveWorktree:
    """Tests for remove_worktree function."""

    def test_removes_worktree(self, tmp_path: Path):
        """Test removes worktree successfully."""
        _init_git_repo(tmp_path, with_commit=True)

        worktree_path = tmp_path / "worktree1"
        create_worktree(worktree_path, "feature-1", tmp_path)

        remove_worktree(worktree_path, repository_path=tmp_path)

        assert not worktree_path.exists()

    def test_force_removes_worktree_with_uncommitted_changes(self, tmp_path: Path):
        """Test force removes worktree with uncommitted changes."""
        _init_git_repo(tmp_path, with_commit=True)

        worktree_path = tmp_path / "worktree1"
        create_worktree(worktree_path, "feature-1", tmp_path)
        (worktree_path / "new_file.txt").write_text("content")

        remove_worktree(worktree_path, force=True, repository_path=tmp_path)

        assert not worktree_path.exists()


class TestGetProtectedBranches:
    """Tests for get_protected_branches function."""

    def test_returns_default_when_no_config(self, tmp_path: Path):
        """Test returns default protected branches when no config exists."""
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True, check=True)

        protected = get_protected_branches(tmp_path)

        assert set(protected) == {"main", "master", "develop", "staging", "production"}

    def test_reads_from_config(self, tmp_path: Path):
        """Test reads protected branches from git config."""
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True, check=True)
        subprocess.run(
            ["git", "config", "branch.protected1.protect", "true"],
            cwd=tmp_path,
            capture_output=True,
            check=True,
        )
        subprocess.run(
            ["git", "config", "branch.protected2.protect", "true"],
            cwd=tmp_path,
            capture_output=True,
            check=True,
        )

        protected = get_protected_branches(tmp_path)

        assert "protected1" in protected
        assert "protected2" in protected


class TestHasUncommittedChanges:
    """Tests for has_uncommitted_changes function."""

    def test_returns_false_when_clean(self, tmp_path: Path):
        """Test returns False when working directory is clean."""
        _init_git_repo(tmp_path, with_commit=True)

        assert has_uncommitted_changes(tmp_path) is False

    def test_returns_true_with_staged_changes(self, tmp_path: Path):
        """Test returns True when there are staged but uncommitted changes."""
        _init_git_repo(tmp_path, with_commit=True)
        (tmp_path / "new_file.txt").write_text("content")
        subprocess.run(
            ["git", "add", "new_file.txt"], cwd=tmp_path, capture_output=True, check=True
        )

        assert has_uncommitted_changes(tmp_path) is True

    def test_returns_true_with_modified_tracked_file(self, tmp_path: Path):
        """Test returns True when a tracked file is modified."""
        _init_git_repo(tmp_path, with_commit=True)
        # Modify the existing README.md
        (tmp_path / "README.md").write_text("Modified content")

        assert has_uncommitted_changes(tmp_path) is True

    def test_returns_false_for_untracked(self, tmp_path: Path):
        """Test returns False for untracked files (with --untracked-files=no)."""
        _init_git_repo(tmp_path, with_commit=True)
        (tmp_path / "untracked.txt").write_text("content")

        assert has_uncommitted_changes(tmp_path) is False


class TestHasUnpushedCommits:
    """Tests for has_unpushed_commits function."""

    def test_returns_false_when_no_remote(self, tmp_path: Path):
        """Test returns False when there are no remotes (nothing to compare against)."""
        _init_git_repo(tmp_path, with_commit=True)

        # Without a remote, there's nothing to be "unpushed" to
        assert has_unpushed_commits(tmp_path) is False

    def test_returns_false_when_no_commits(self, tmp_path: Path):
        """Test returns False when repo has no commits yet."""
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True, check=True)

        # No commits means no unpushed commits
        assert has_unpushed_commits(tmp_path) is False


class TestListBranches:
    """Tests for list_branches function."""

    def test_lists_all_branches(self, tmp_path: Path):
        """Test lists all branches."""
        _init_git_repo(tmp_path, with_commit=True)
        subprocess.run(
            ["git", "branch", "feature-branch"],
            cwd=tmp_path,
            capture_output=True,
            check=True,
        )

        branches = list_branches(tmp_path)

        assert len(branches) >= 2
        branch_names = [b.name for b in branches]
        assert "main" in branch_names
        assert "feature-branch" in branch_names

    def test_marks_current_branch(self, tmp_path: Path):
        """Test marks the current branch."""
        _init_git_repo(tmp_path, with_commit=True)

        branches = list_branches(tmp_path)

        current_branches = [b for b in branches if b.is_current]
        assert len(current_branches) == 1
        assert current_branches[0].name == "main"

    def test_detects_protected_branches(self, tmp_path: Path):
        """Test detects which branches are protected."""
        _init_git_repo(tmp_path, with_commit=True)

        branches = list_branches(tmp_path)

        # main is in the default protected branches list
        main_branch = next(b for b in branches if b.name == "main")
        assert main_branch.is_protected is True

    def test_detects_branches_checked_out_elsewhere(self, tmp_path: Path):
        """Test detects branches checked out in other worktrees."""
        _init_git_repo(tmp_path, with_commit=True)

        worktree_path = tmp_path / "worktree1"
        create_worktree(worktree_path, "feature-1", tmp_path)

        branches = list_branches(tmp_path)

        # feature-1 is checked out in worktree1, so from main's perspective it's elsewhere
        feature_branch = next((b for b in branches if b.name == "feature-1"), None)
        assert feature_branch is not None
        assert feature_branch.is_checked_out_elsewhere is True

    def test_current_branch_not_marked_as_checked_out_elsewhere(self, tmp_path: Path):
        """Test that the current branch is not marked as checked out elsewhere."""
        _init_git_repo(tmp_path, with_commit=True)

        branches = list_branches(tmp_path)

        main_branch = next(b for b in branches if b.name == "main")
        assert main_branch.is_current is True
        assert main_branch.is_checked_out_elsewhere is False


class TestGetGitStatus:
    """Tests for get_git_status function."""

    def test_returns_full_status_in_repo(self, tmp_path: Path):
        """Test returns comprehensive status in repository."""
        _init_git_repo(tmp_path, with_commit=True)

        status = get_git_status(tmp_path)

        assert status.is_git_repo is True
        assert status.current_branch == "main"
        # Has main worktree
        assert len(status.worktrees) == 1
        assert set(status.protected_branches) == {
            "main",
            "master",
            "develop",
            "staging",
            "production",
        }

    def test_detects_uncommitted_changes(self, tmp_path: Path):
        """Test detects uncommitted changes in status."""
        _init_git_repo(tmp_path, with_commit=True)
        (tmp_path / "README.md").write_text("Modified content")

        status = get_git_status(tmp_path)

        assert status.uncommitted_changes is True

    def test_detects_unpushed_commits(self, tmp_path: Path):
        """Test unpushed commits detection returns False without a remote."""
        _init_git_repo(tmp_path, with_commit=True)

        status = get_git_status(tmp_path)

        # Without a remote, unpushed_commits is False (nothing to push to)
        assert status.unpushed_commits is False

    def test_detects_worktrees(self, tmp_path: Path):
        """Test detects worktrees in status."""
        _init_git_repo(tmp_path, with_commit=True)

        worktree_path = tmp_path / "worktree1"
        create_worktree(worktree_path, "feature-1", tmp_path)

        status = get_git_status(tmp_path)

        assert len(status.worktrees) >= 2
        assert any(w.branch == "feature-1" for w in status.worktrees)


class TestDataClasses:
    """Tests for data classes."""

    def test_git_worktree_creation(self):
        """Test GitWorktree data class creation."""
        worktree = GitWorktree(
            path=Path("/some/path"),
            branch="feature-1",
            committed=True,
            detached=False,
        )

        assert worktree.path == Path("/some/path")
        assert worktree.branch == "feature-1"
        assert worktree.committed is True
        assert worktree.detached is False

    def test_git_status_creation(self):
        """Test GitStatus data class creation."""
        status = GitStatus(
            is_git_repo=True,
            uncommitted_changes=False,
            unpushed_commits=True,
            current_branch="main",
            worktrees=[],
            protected_branches=["main", "master"],
        )

        assert status.is_git_repo is True
        assert status.uncommitted_changes is False
        assert status.unpushed_commits is True
        assert status.current_branch == "main"
        assert len(status.protected_branches) == 2

    def test_branch_info_creation(self):
        """Test BranchInfo data class creation."""
        branch = BranchInfo(
            name="feature-1",
            is_current=True,
            is_protected=False,
            is_checked_out_elsewhere=False,
            has_unpushed_commits=False,
        )

        assert branch.name == "feature-1"
        assert branch.is_current is True
        assert branch.is_protected is False
        assert branch.is_checked_out_elsewhere is False
        assert branch.has_unpushed_commits is False
