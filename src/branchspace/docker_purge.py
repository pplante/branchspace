"""Docker purge helper for branchspace."""

from __future__ import annotations

import subprocess

from dataclasses import dataclass
from pathlib import Path

import questionary

from branchspace.console import info
from branchspace.docker_shell import build_container_name
from branchspace.git_utils import get_current_branch


class DockerPurgeError(RuntimeError):
    """Raised when purge operations fail."""


@dataclass(frozen=True)
class DockerResources:
    """Docker resources to remove."""

    containers: list[str]
    images: list[str]
    volumes: list[str]

    def is_empty(self) -> bool:
        return not (self.containers or self.images or self.volumes)


def _list_docker_ids(args: list[str]) -> list[str]:
    result = subprocess.run(args, capture_output=True, text=True, check=True)
    return [line.strip() for line in result.stdout.splitlines() if line.strip()]


def discover_resources(container_name: str) -> DockerResources:
    containers = _list_docker_ids(
        ["docker", "ps", "-a", "--filter", f"name=^{container_name}$", "-q"]
    )
    images = _list_docker_ids(["docker", "images", "--filter", f"reference={container_name}", "-q"])
    volumes = _list_docker_ids(
        ["docker", "volume", "ls", "--filter", f"name=^{container_name}$", "-q"]
    )
    return DockerResources(containers=containers, images=images, volumes=volumes)


def render_preview(resources: DockerResources) -> None:
    if resources.containers:
        info(f"Containers: {', '.join(resources.containers)}")
    if resources.images:
        info(f"Images: {', '.join(resources.images)}")
    if resources.volumes:
        info(f"Volumes: {', '.join(resources.volumes)}")


def purge_resources(resources: DockerResources) -> None:
    if resources.containers:
        subprocess.run(["docker", "rm", "-f", *resources.containers], check=False)
    if resources.images:
        subprocess.run(["docker", "rmi", "-f", *resources.images], check=False)
    if resources.volumes:
        subprocess.run(["docker", "volume", "rm", *resources.volumes], check=False)


def confirm_purge() -> bool:
    return bool(questionary.confirm("Remove these Docker resources?").unsafe_ask())


def run_docker_purge(
    *,
    worktree_path: Path | None = None,
    dry_run: bool = False,
    force: bool = False,
) -> DockerResources:
    if worktree_path is None:
        worktree_path = Path.cwd().resolve()
    branch = get_current_branch(worktree_path)
    if branch is None:
        raise DockerPurgeError("Cannot determine current branch.")

    container_name = build_container_name(branch)
    resources = discover_resources(container_name)
    render_preview(resources)

    if resources.is_empty():
        return resources

    if dry_run:
        return resources

    if not force and not confirm_purge():
        return resources

    purge_resources(resources)
    return resources
