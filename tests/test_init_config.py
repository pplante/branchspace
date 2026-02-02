"""Tests for init config helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from branchspace.init_config import detect_project


if TYPE_CHECKING:
    from pathlib import Path


def test_detect_project_finders(tmp_path: Path):
    (tmp_path / "Dockerfile").write_text("FROM python:3.12", encoding="utf-8")
    (tmp_path / "package.json").write_text("{}", encoding="utf-8")
    (tmp_path / "pyproject.toml").write_text("[project]", encoding="utf-8")

    detection = detect_project(tmp_path)

    assert detection.dockerfiles
    assert detection.has_node is True
    assert detection.has_python is True
