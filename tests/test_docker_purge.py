"""Tests for docker purge logic."""

from __future__ import annotations

from branchspace.docker_purge import DockerResources
from branchspace.docker_purge import discover_resources


def test_discover_resources_empty(monkeypatch):
    monkeypatch.setattr(
        "branchspace.docker_purge._list_docker_ids",
        lambda _args: [],
    )

    resources = discover_resources("branchspace-main")

    assert resources == DockerResources(containers=[], images=[], volumes=[])
