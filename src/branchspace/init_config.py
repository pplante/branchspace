"""Initialization helpers for branchspace configuration."""

from __future__ import annotations

import json

from dataclasses import dataclass
from pathlib import Path

import questionary

from branchspace.config import BranchspaceConfig
from branchspace.config import ContainerBuildConfig
from branchspace.config import ContainerImageConfig
from branchspace.config import CONFIG_FILENAME
from branchspace.config import get_git_root


DOCKERFILE_CANDIDATES = ("Dockerfile", "Dockerfile.dev", "Dockerfile.local")


@dataclass(frozen=True)
class ProjectDetection:
    """Project detection results."""

    dockerfiles: list[Path]
    has_node: bool
    has_python: bool


def detect_project(root: Path) -> ProjectDetection:
    dockerfiles: list[Path] = []
    for name in DOCKERFILE_CANDIDATES:
        candidate = root / name
        if candidate.exists():
            dockerfiles.append(candidate)

    has_node = (root / "package.json").exists()
    has_python = (root / "pyproject.toml").exists() or (root / "setup.py").exists()
    return ProjectDetection(dockerfiles=dockerfiles, has_node=has_node, has_python=has_python)


def choose_container_config(
    detection: ProjectDetection,
) -> ContainerImageConfig | ContainerBuildConfig:
    if detection.dockerfiles:
        choices = [file.name for file in detection.dockerfiles]
        choices.append("Skip Dockerfile")
        selection = questionary.select(
            "Found Dockerfile(s). Use one for build config?",
            choices=choices,
        ).unsafe_ask()
        if selection and selection != "Skip Dockerfile":
            return ContainerBuildConfig(context=".", dockerfile=selection)

    if detection.has_node:
        image = questionary.select(
            "Select Node.js base image:",
            choices=["node:20", "node:22", "node:24"],
        ).unsafe_ask()
        if image:
            return ContainerImageConfig(image=image)
    if detection.has_python:
        image = questionary.select(
            "Select Python base image:",
            choices=["python:3.11", "python:3.12", "python:3.13"],
        ).unsafe_ask()
        if image:
            return ContainerImageConfig(image=image)

    image = questionary.text("Enter Docker base image:", default="ubuntu:24.04").unsafe_ask()
    if not image:
        image = "ubuntu:24.04"
    return ContainerImageConfig(image=image)


def build_default_config(
    container_config: ContainerImageConfig | ContainerBuildConfig,
) -> BranchspaceConfig:
    return BranchspaceConfig(containerConfig=container_config)


def write_config(root: Path, config: BranchspaceConfig) -> Path:
    path = root / CONFIG_FILENAME
    data = config.model_dump(by_alias=True)
    path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    return path


def init_config() -> Path:
    root = get_git_root()
    if root is None:
        raise RuntimeError("Not inside a git repository.")
    detection = detect_project(root)
    container_config = choose_container_config(detection)
    config = build_default_config(container_config)
    return write_config(root, config)
