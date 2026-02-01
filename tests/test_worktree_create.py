"""Tests for worktree creation logic."""

from __future__ import annotations

from pathlib import Path

from branchspace.config import BranchspaceConfig
from branchspace.config import TemplateContext
from branchspace.worktree_create import CreateWorktreeError
from branchspace.worktree_create import copy_worktree_files
from branchspace.worktree_create import create_worktree_for_branch


def test_create_worktree_resolves_template_path(tmp_path: Path, monkeypatch):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    config = BranchspaceConfig(worktreePathTemplate=".worktrees/$BRANCH_NAME")

    monkeypatch.setattr(
        "branchspace.worktree_create.get_current_branch",
        lambda _path=None: "main",
    )
    monkeypatch.setattr(
        "branchspace.worktree_create.git_create_worktree",
        lambda path, branch, repository_path=None, create_branch=True: None,
    )
    monkeypatch.setattr(
        "branchspace.worktree_create.copy_worktree_files",
        lambda *args, **kwargs: None,
    )

    created = create_worktree_for_branch(
        "feature", config, repo_root=repo_root, open_terminal=False
    )

    assert created.path == repo_root / ".worktrees/feature"


def test_copy_worktree_files_applies_ignores(tmp_path: Path):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".env").write_text("secret")
    (repo_root / "notes.txt").write_text("hi")
    (repo_root / "node_modules").mkdir()
    (repo_root / "node_modules" / "skip.txt").write_text("skip")

    worktree_path = tmp_path / "worktree"
    worktree_path.mkdir()

    copy_worktree_files(
        repo_root,
        worktree_path,
        patterns=[".env*", "**/*"],
        ignore_patterns=["**/node_modules/**"],
    )

    assert (worktree_path / ".env").is_file()
    assert (worktree_path / "notes.txt").is_file()
    assert not (worktree_path / "node_modules" / "skip.txt").exists()


def test_create_worktree_requires_current_branch(tmp_path: Path, monkeypatch):
    repo_root = tmp_path / "repo"
    repo_root.mkdir()

    config = BranchspaceConfig()

    monkeypatch.setattr(
        "branchspace.worktree_create.get_current_branch",
        lambda _path=None: None,
    )

    monkeypatch.setattr(
        "branchspace.worktree_create.git_create_worktree",
        lambda path, branch, repository_path=None, create_branch=True: None,
    )
    monkeypatch.setattr(
        "branchspace.worktree_create.copy_worktree_files",
        lambda *args, **kwargs: None,
    )

    try:
        create_worktree_for_branch("feature", config, repo_root=repo_root, open_terminal=False)
    except CreateWorktreeError as exc:
        assert "current branch" in str(exc)
    else:
        raise AssertionError("Expected CreateWorktreeError")


def test_template_context_mapping_used():
    context = TemplateContext(
        base_path="repo",
        worktree_path="/tmp/repo/worktrees/feature",
        branch_name="feature",
        source_branch="main",
    )

    mapping = context.as_mapping()

    assert mapping["BASE_PATH"] == "repo"
