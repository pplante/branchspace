"""Tests for worktree removal logic."""

from __future__ import annotations

from pathlib import Path

import pytest

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


def test_remove_worktree_blocks_checked_out_elsewhere(tmp_path: Path, monkeypatch):
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
    monkeypatch.setattr("branchspace.worktree_remove.Path.cwd", lambda: repo_root)

    with pytest.raises(WorktreeRemoveError):
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
    monkeypatch.setattr("branchspace.worktree_remove.Path.cwd", lambda: worktree_path)

    result = remove_worktree_for_branch(
        "feature", BranchspaceConfig(), repo_root=repo_root, confirm=True
    )

    assert result.removed is False
