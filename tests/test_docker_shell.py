"""Tests for docker shell command building."""

from __future__ import annotations

from pathlib import Path

from branchspace.config import BranchspaceConfig
from branchspace.config import ContainerBuildConfig
from branchspace.config import ContainerImageConfig
from branchspace.docker_shell import build_docker_commands


def test_build_docker_commands_image_config():
    config = BranchspaceConfig(containerConfig=ContainerImageConfig(image="python:3.14"))
    plan = build_docker_commands(config, "feature", Path("/repo"), command="npm test")

    assert plan.commands[0] == ["docker", "pull", "python:3.14"]
    assert "docker" in plan.commands[1][0]
    assert "python:3.14" in plan.commands[1]


def test_build_docker_commands_build_config():
    config = BranchspaceConfig(containerConfig=ContainerBuildConfig(context="."))
    plan = build_docker_commands(config, "feature", Path("/repo"))

    assert plan.commands[0][0:3] == ["docker", "build", "-t"]
    assert plan.commands[1][0:2] == ["docker", "run"]
