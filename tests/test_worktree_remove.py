"""Tests for worktree removal logic."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest


if TYPE_CHECKING:
    from pathlib import Path

from branchspace.config import BranchspaceConfig
from branchspace.worktree_remove import WorktreeRemoveError
from branchspace.worktree_remove import remove_worktree_for_branch


def test_remove_worktree_blocks_protected_branch(tmp_path: Path, monkeypatch):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    monkeypatch.setattr("branchspace.worktree_remove.get_git_root", lambda _path=None: repo_root)
    monkeypatch.setattr("branchspace.worktree_remove.get_protected_branches", lambda _path=None: [])

    with pytest.raises(WorktreeRemoveError):
        remove_worktree_for_branch("main", BranchspaceConfig(), repo_root=repo_root, confirm=False)


def test_remove_worktree_blocks_checked_out_in_multiple_worktrees(tmp_path: Path, monkeypatch):
    """Test that removal is blocked when branch is checked out in multiple worktrees."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    worktree_path1 = repo_root / "feature1"
    worktree_path1.mkdir()
    worktree_path2 = repo_root / "feature2"
    worktree_path2.mkdir()

    monkeypatch.setattr("branchspace.worktree_remove.get_git_root", lambda _path=None: repo_root)
    monkeypatch.setattr("branchspace.worktree_remove.get_protected_branches", lambda _path=None: [])
    monkeypatch.setattr(
        "branchspace.worktree_remove.list_worktrees",
        lambda _path=None: [
            type("WT", (), {"branch": "feature", "path": worktree_path1})(),
            type("WT", (), {"branch": "feature", "path": worktree_path2})(),
        ],
    )

    with pytest.raises(WorktreeRemoveError, match="checked out in multiple worktrees"):
        remove_worktree_for_branch(
            "feature", BranchspaceConfig(), repo_root=repo_root, confirm=False
        )


def test_remove_worktree_confirms_dirty(tmp_path: Path, monkeypatch):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    worktree_path = repo_root / "feature"
    worktree_path.mkdir()

    monkeypatch.setattr("branchspace.worktree_remove.get_git_root", lambda _path=None: repo_root)
    monkeypatch.setattr("branchspace.worktree_remove.get_protected_branches", lambda _path=None: [])
    monkeypatch.setattr(
        "branchspace.worktree_remove.list_worktrees",
        lambda _path=None: [type("WT", (), {"branch": "feature", "path": worktree_path})()],
    )
    monkeypatch.setattr(
        "branchspace.worktree_remove.has_uncommitted_changes_with_untracked",
        lambda _path=None: True,
    )
    monkeypatch.setattr("branchspace.worktree_remove._confirm", lambda _prompt: False)

    result = remove_worktree_for_branch(
        "feature", BranchspaceConfig(), repo_root=repo_root, confirm=True
    )

    assert result.removed is False
