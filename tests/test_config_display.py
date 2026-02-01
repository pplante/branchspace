"""Tests for config display helpers."""

from __future__ import annotations

from branchspace.config import BranchspaceConfig
from branchspace.config import ContainerBuildConfig
from branchspace.config_display import build_config_table


def test_build_config_table_includes_keys():
    config = BranchspaceConfig()
    table = build_config_table(config)

    headers = [column.header for column in table.columns]
    assert headers == ["Key", "Value"]
    assert table.title == "Branchspace Configuration"


def test_build_config_table_with_build_config():
    config = BranchspaceConfig(container_config=ContainerBuildConfig())
    table = build_config_table(config)

    assert table.title == "Branchspace Configuration"
