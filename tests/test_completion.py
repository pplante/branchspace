"""Tests for shell completion helpers."""

from __future__ import annotations

from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

from branchspace.completion import WorktreeBranchComplete
from branchspace.git_utils import GitWorktree


def test_worktree_branch_complete_returns_matching_branches():
    """Test that WorktreeBranchComplete returns worktree branches."""
    mock_worktrees = [
        GitWorktree(
            path=Path("/repo/worktrees/feature-1"),
            branch="feature-1",
            committed=True,
            detached=False,
        ),
        GitWorktree(
            path=Path("/repo/worktrees/feature-2"),
            branch="feature-2",
            committed=True,
            detached=False,
        ),
        GitWorktree(
            path=Path("/repo/worktrees/main"),
            branch="main",
            committed=True,
            detached=False,
        ),
    ]

    with patch("branchspace.completion.list_worktrees", return_value=mock_worktrees):
        completer = WorktreeBranchComplete()
        ctx = MagicMock()
        param = MagicMock()

        # Test empty prefix - should return all branches
        items = completer(ctx, param, "")
        assert len(items) == 3
        assert {item.value for item in items} == {"feature-1", "feature-2", "main"}


def test_worktree_branch_complete_filters_by_prefix():
    """Test that WorktreeBranchComplete filters branches by prefix."""
    mock_worktrees = [
        GitWorktree(
            path=Path("/repo/worktrees/feature-1"),
            branch="feature-1",
            committed=True,
            detached=False,
        ),
        GitWorktree(
            path=Path("/repo/worktrees/feature-2"),
            branch="feature-2",
            committed=True,
            detached=False,
        ),
        GitWorktree(
            path=Path("/repo/worktrees/main"),
            branch="main",
            committed=True,
            detached=False,
        ),
    ]

    with patch("branchspace.completion.list_worktrees", return_value=mock_worktrees):
        completer = WorktreeBranchComplete()
        ctx = MagicMock()
        param = MagicMock()

        # Test filtering by prefix
        items = completer(ctx, param, "feature")
        assert len(items) == 2
        assert {item.value for item in items} == {"feature-1", "feature-2"}


def test_worktree_branch_complete_excludes_detached():
    """Test that WorktreeBranchComplete excludes detached worktrees."""
    mock_worktrees = [
        GitWorktree(
            path=Path("/repo/worktrees/feature-1"),
            branch="feature-1",
            committed=True,
            detached=False,
        ),
        GitWorktree(
            path=Path("/repo/worktrees/detached"),
            branch="HEAD",
            committed=True,
            detached=True,
        ),
    ]

    with patch("branchspace.completion.list_worktrees", return_value=mock_worktrees):
        completer = WorktreeBranchComplete()
        ctx = MagicMock()
        param = MagicMock()

        # Detached worktree should not be included
        items = completer(ctx, param, "")
        assert len(items) == 1
        assert items[0].value == "feature-1"


def test_worktree_branch_complete_handles_errors_gracefully():
    """Test that WorktreeBranchComplete handles errors gracefully."""
    with patch("branchspace.completion.list_worktrees", side_effect=Exception("Git error")):
        completer = WorktreeBranchComplete()
        ctx = MagicMock()
        param = MagicMock()

        # Should return empty list on error
        items = completer(ctx, param, "")
        assert items == []
