"""Worktree creation logic for branchspace."""

import glob
import subprocess

from collections.abc import Iterable
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path

from branchspace.config import BranchspaceConfig
from branchspace.config import TemplateContext
from branchspace.config import get_git_root
from branchspace.git_utils import create_worktree as git_create_worktree
from branchspace.git_utils import get_current_branch
from branchspace.template import TemplateVariableError
from branchspace.template import substitute_template


class CreateWorktreeError(RuntimeError):
    """Raised when worktree creation fails."""


@dataclass(frozen=True)
class CreatedWorktree:
    """Represents a created worktree result."""

    branch: str
    path: Path


def _ensure_git_root(repo_root: Path | None) -> Path:
    if repo_root is None:
        repo_root = get_git_root()
    if repo_root is None:
        raise CreateWorktreeError("Not inside a git repository.")
    return repo_root


def _resolve_worktree_path(
    template: str,
    base_path: str,
    branch_name: str,
    source_branch: str,
    project_name: str,
    repo_root: Path,
) -> Path:
    if "$WORKTREE_PATH" in template:
        raise CreateWorktreeError("worktreePathTemplate cannot reference $WORKTREE_PATH.")

    context = TemplateContext(
        base_path=base_path,
        worktree_path="",
        branch_name=branch_name,
        source_branch=source_branch,
        project_name=project_name,
    )
    resolved = substitute_template(template, context.as_mapping())
    path = Path(resolved)
    if not path.is_absolute():
        path = repo_root / path
    return path


def _is_ignored(relative_path: Path, ignore_patterns: Sequence[str]) -> bool:
    path = relative_path.as_posix()
    for pattern in ignore_patterns:
        matcher = Path(path)
        if matcher.match(pattern):
            return True
        if pattern.startswith("**/") and matcher.match(pattern[3:]):
            return True
    return False


def _iter_copy_sources(
    repo_root: Path,
    patterns: Sequence[str],
    ignore_patterns: Sequence[str],
) -> Iterable[tuple[Path, Path]]:
    seen: set[Path] = set()
    for pattern in patterns:
        matches = glob.glob(pattern, root_dir=repo_root, recursive=True)
        for match in matches:
            relative = Path(match)
            if relative in seen:
                continue
            seen.add(relative)
            if _is_ignored(relative, ignore_patterns):
                continue
            source = repo_root / relative
            if source.is_dir():
                continue
            yield source, relative


def copy_worktree_files(
    repo_root: Path,
    worktree_path: Path,
    patterns: Sequence[str],
    ignore_patterns: Sequence[str],
) -> None:
    """Copy configured files from repo root to the worktree."""
    for source, relative in _iter_copy_sources(repo_root, patterns, ignore_patterns):
        destination = worktree_path / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_bytes(source.read_bytes())


def run_post_create_commands(commands: Sequence[str], worktree_path: Path) -> None:
    """Run post-create commands inside the worktree."""
    for command in commands:
        subprocess.run(command, cwd=worktree_path, shell=True, check=True)


def run_terminal_command(command: str, worktree_path: Path) -> None:
    """Run terminal command to open editor or shell."""
    subprocess.Popen(command, cwd=worktree_path, shell=True)


def create_worktree_for_branch(
    branch: str,
    config: BranchspaceConfig,
    repo_root: Path | None = None,
    *,
    open_terminal: bool = True,
) -> CreatedWorktree:
    repo_root = _ensure_git_root(repo_root)
    base_path = repo_root.name
    source_branch = get_current_branch(repo_root)
    if source_branch is None:
        raise CreateWorktreeError("Cannot determine current branch.")

    try:
        worktree_path = _resolve_worktree_path(
            config.worktree_path_template,
            base_path,
            branch,
            source_branch,
            config.project_name or base_path,
            repo_root,
        )
    except TemplateVariableError as exc:
        raise CreateWorktreeError(str(exc)) from exc

    git_create_worktree(worktree_path, branch, repository_path=repo_root)

    context = TemplateContext(
        base_path=base_path,
        worktree_path=str(worktree_path),
        branch_name=branch,
        source_branch=source_branch,
        project_name=config.project_name or base_path,
    )
    variables = context.as_mapping()

    copy_worktree_files(
        repo_root,
        worktree_path,
        config.worktree_copy_patterns,
        config.worktree_copy_ignores,
    )

    if config.post_create_cmd:
        commands = substitute_template(config.post_create_cmd, variables)
        run_post_create_commands(commands, worktree_path)

    if open_terminal and config.terminal_command:
        terminal_command = substitute_template(config.terminal_command, variables)
        run_terminal_command(terminal_command, worktree_path)

    return CreatedWorktree(branch=branch, path=worktree_path)


def create_worktrees(
    branches: Sequence[str],
    config: BranchspaceConfig,
    repo_root: Path | None = None,
    *,
    open_terminal: bool = True,
) -> list[CreatedWorktree]:
    return [
        create_worktree_for_branch(
            branch,
            config,
            repo_root=repo_root,
            open_terminal=open_terminal,
        )
        for branch in branches
    ]
