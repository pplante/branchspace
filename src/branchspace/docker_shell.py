"""Docker shell command builder for branchspace."""

import re
import subprocess

from dataclasses import dataclass
from pathlib import Path

from branchspace.config import BranchspaceConfig
from branchspace.config import ContainerBuildConfig
from branchspace.config import ContainerImageConfig
from branchspace.git_utils import get_current_branch


class DockerShellError(RuntimeError):
    """Raised when docker shell execution fails."""


@dataclass(frozen=True)
class DockerCommandPlan:
    """Represents docker commands to run for shell."""

    commands: list[list[str]]
    container_name: str


def _sanitize_branch_name(branch: str) -> str:
    return re.sub(r"[^A-Za-z0-9_.-]+", "-", branch).strip("-")


def build_container_name(branch: str) -> str:
    sanitized = _sanitize_branch_name(branch)
    return f"branchspace-{sanitized}" if sanitized else "branchspace"


def _build_run_command(
    image: str,
    container_name: str,
    worktree_path: Path,
    shell: str,
    command: str | None,
) -> list[str]:
    base = [
        "docker",
        "run",
        "--rm",
        "-it",
        "--name",
        container_name,
        "-v",
        f"{worktree_path}:/workspace",
        "-w",
        "/workspace",
        image,
    ]
    if command:
        base += [shell, "-lc", command]
    else:
        base += [shell]
    return base


def build_docker_commands(
    config: BranchspaceConfig,
    branch: str,
    worktree_path: Path,
    command: str | None = None,
) -> DockerCommandPlan:
    container_name = build_container_name(branch)
    commands: list[list[str]] = []

    if isinstance(config.container_config, ContainerImageConfig):
        image = config.container_config.image
        commands.append(["docker", "pull", image])
        commands.append(
            _build_run_command(image, container_name, worktree_path, config.shell, command)
        )
        return DockerCommandPlan(commands=commands, container_name=container_name)

    if isinstance(config.container_config, ContainerBuildConfig):
        image = container_name
        context_path = Path(config.container_config.context)
        dockerfile_path = Path(config.container_config.dockerfile)
        if not context_path.is_absolute():
            context_path = worktree_path / context_path
        if not dockerfile_path.is_absolute():
            dockerfile_path = worktree_path / dockerfile_path
        commands.append(
            [
                "docker",
                "build",
                "-t",
                image,
                "-f",
                str(dockerfile_path),
                str(context_path),
            ]
        )
        commands.append(
            _build_run_command(image, container_name, worktree_path, config.shell, command)
        )
        return DockerCommandPlan(commands=commands, container_name=container_name)

    raise DockerShellError("Unsupported container configuration.")


def run_docker_shell(
    config: BranchspaceConfig,
    worktree_path: Path | None = None,
    *,
    command: str | None = None,
) -> DockerCommandPlan:
    if worktree_path is None:
        worktree_path = Path.cwd().resolve()
    branch = get_current_branch(worktree_path)
    if branch is None:
        raise DockerShellError("Cannot determine current branch.")

    plan = build_docker_commands(config, branch, worktree_path, command=command)
    for cmd in plan.commands:
        subprocess.run(cmd, check=True)
    return plan
