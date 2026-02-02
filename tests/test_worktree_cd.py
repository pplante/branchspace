"""Tests for worktree cd resolution."""

from __future__ import annotations

from typing import TYPE_CHECKING

import pytest


if TYPE_CHECKING:
    from pathlib import Path

from branchspace.worktree_cd import WorktreeLookupError
from branchspace.worktree_cd import resolve_worktree_path


def test_resolve_worktree_path_returns_root(tmp_path: Path, monkeypatch):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    monkeypatch.setattr("branchspace.worktree_cd.get_git_root", lambda _path=None: repo_root)

    result = resolve_worktree_path(None)

    assert result.path == repo_root
    assert result.branch is None


def test_resolve_worktree_path_finds_branch(tmp_path: Path, monkeypatch):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    feature_path = repo_root / "feature"
    feature_path.mkdir()

    monkeypatch.setattr("branchspace.worktree_cd.get_git_root", lambda _path=None: repo_root)
    monkeypatch.setattr(
        "branchspace.worktree_cd.list_worktrees",
        lambda _path=None: [type("WT", (), {"branch": "feature", "path": feature_path})()],
    )

    result = resolve_worktree_path("feature")

    assert result.path == feature_path
    assert result.branch == "feature"


def test_resolve_worktree_path_missing_branch(tmp_path: Path, monkeypatch):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    monkeypatch.setattr("branchspace.worktree_cd.get_git_root", lambda _path=None: repo_root)
    monkeypatch.setattr("branchspace.worktree_cd.list_worktrees", lambda _path=None: [])

    with pytest.raises(WorktreeLookupError):
        resolve_worktree_path("missing")
