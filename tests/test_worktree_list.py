"""Tests for worktree listing logic."""

from __future__ import annotations

from pathlib import Path

from branchspace.worktree_list import WorktreeStatus
from branchspace.worktree_list import build_worktree_list_table
from branchspace.worktree_list import list_worktree_statuses


def test_list_worktree_statuses_marks_current(tmp_path: Path, monkeypatch):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    current_path = repo_root / "main"
    other_path = repo_root / "feature"
    current_path.mkdir()
    other_path.mkdir()

    monkeypatch.chdir(current_path)

    monkeypatch.setattr(
        "branchspace.worktree_list.list_worktrees",
        lambda _path=None: [
            type("WT", (), {"branch": "main", "path": current_path})(),
            type("WT", (), {"branch": "feature", "path": other_path})(),
        ],
    )
    monkeypatch.setattr(
        "branchspace.worktree_list.has_uncommitted_changes_with_untracked",
        lambda _path=None: False,
    )

    statuses = list_worktree_statuses(repo_root)

    assert any(status.is_current for status in statuses)
    assert any(status.branch == "main" and status.is_current for status in statuses)


def test_build_worktree_list_table_marks_dirty():
    statuses = [
        WorktreeStatus(branch="main", path=Path("/repo"), is_current=True, is_dirty=False),
        WorktreeStatus(
            branch="feature", path=Path("/repo/feature"), is_current=False, is_dirty=True
        ),
    ]

    table = build_worktree_list_table(statuses)

    assert table.title == "Worktrees"
    assert [column.header for column in table.columns] == ["Path", "Branch", "Status"]
    assert table.row_count == 2
