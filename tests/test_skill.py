"""Tests for Agent Skill generation and installation."""

from __future__ import annotations

from typing import TYPE_CHECKING
from unittest.mock import patch

import pytest


if TYPE_CHECKING:
    from pathlib import Path

from branchspace.skill import SKILL_DESCRIPTION
from branchspace.skill import SKILL_NAME
from branchspace.skill import generate_skill_content
from branchspace.skill import get_global_skills_dir
from branchspace.skill import get_project_skills_dir
from branchspace.skill import get_skill_install_path
from branchspace.skill import get_skill_md_path
from branchspace.skill import install_skill
from branchspace.skill import is_skill_installed


class TestGenerateSkillContent:
    """Tests for generate_skill_content function."""

    def test_includes_valid_frontmatter(self) -> None:
        content = generate_skill_content()

        assert content.startswith("---\n")
        assert f"name: {SKILL_NAME}" in content
        assert f"description: {SKILL_DESCRIPTION}" in content
        assert "\n---\n" in content

    def test_includes_skill_body(self) -> None:
        content = generate_skill_content()

        assert "# Branchspace - Isolated Development Environments" in content
        assert "## When to Use Branchspace" in content
        assert "## Key Commands" in content
        assert "## Workflow" in content
        assert "## Best Practices" in content

    def test_includes_command_reference(self) -> None:
        content = generate_skill_content()

        assert "branchspace create" in content
        assert "branchspace ls" in content
        assert "branchspace cd" in content
        assert "branchspace shell" in content
        assert "branchspace rm" in content


class TestGetSkillPaths:
    """Tests for skill path resolution functions."""

    def test_get_global_skills_dir(self) -> None:
        result = get_global_skills_dir()

        assert result.name == ".skills"
        assert str(result).startswith(str(result.home()))

    def test_get_project_skills_dir(self, tmp_path: Path) -> None:
        with patch("branchspace.skill.get_project_root", return_value=tmp_path):
            result = get_project_skills_dir()

        assert result == tmp_path / ".skills"

    def test_get_skill_install_path_global(self) -> None:
        result = get_skill_install_path("global")

        assert result.name == SKILL_NAME
        assert result.parent.name == ".skills"

    def test_get_skill_install_path_project(self, tmp_path: Path) -> None:
        with patch("branchspace.skill.get_project_root", return_value=tmp_path):
            result = get_skill_install_path("project")

        assert result == tmp_path / ".skills" / SKILL_NAME

    def test_get_skill_install_path_invalid_scope(self) -> None:
        with pytest.raises(ValueError, match="Unknown scope"):
            get_skill_install_path("invalid")

    def test_get_skill_md_path_global(self) -> None:
        result = get_skill_md_path("global")

        assert result.name == "SKILL.md"
        assert result.parent.name == SKILL_NAME

    def test_get_skill_md_path_project(self, tmp_path: Path) -> None:
        with patch("branchspace.skill.get_project_root", return_value=tmp_path):
            result = get_skill_md_path("project")

        assert result == tmp_path / ".skills" / SKILL_NAME / "SKILL.md"


class TestIsSkillInstalled:
    """Tests for is_skill_installed function."""

    def test_returns_false_when_not_installed(self, tmp_path: Path) -> None:
        with patch("branchspace.skill.get_project_root", return_value=tmp_path):
            result = is_skill_installed("project")

        assert result is False

    def test_returns_true_when_installed(self, tmp_path: Path) -> None:
        skill_dir = tmp_path / ".skills" / SKILL_NAME
        skill_dir.mkdir(parents=True)
        (skill_dir / "SKILL.md").write_text("test", encoding="utf-8")

        with patch("branchspace.skill.get_project_root", return_value=tmp_path):
            result = is_skill_installed("project")

        assert result is True


class TestInstallSkill:
    """Tests for install_skill function."""

    def test_creates_skill_directory(self, tmp_path: Path) -> None:
        with patch("branchspace.skill.get_project_root", return_value=tmp_path):
            install_skill("project")

        skill_dir = tmp_path / ".skills" / SKILL_NAME
        assert skill_dir.exists()
        assert skill_dir.is_dir()

    def test_writes_skill_md_file(self, tmp_path: Path) -> None:
        with patch("branchspace.skill.get_project_root", return_value=tmp_path):
            result = install_skill("project")

        assert result.exists()
        assert result.name == "SKILL.md"

    def test_skill_md_contains_valid_content(self, tmp_path: Path) -> None:
        with patch("branchspace.skill.get_project_root", return_value=tmp_path):
            result = install_skill("project")

        content = result.read_text(encoding="utf-8")
        assert content.startswith("---\n")
        assert f"name: {SKILL_NAME}" in content
        assert "# Branchspace" in content

    def test_returns_skill_md_path(self, tmp_path: Path) -> None:
        with patch("branchspace.skill.get_project_root", return_value=tmp_path):
            result = install_skill("project")

        expected = tmp_path / ".skills" / SKILL_NAME / "SKILL.md"
        assert result == expected

    def test_overwrites_existing_skill(self, tmp_path: Path) -> None:
        skill_dir = tmp_path / ".skills" / SKILL_NAME
        skill_dir.mkdir(parents=True)
        skill_md = skill_dir / "SKILL.md"
        skill_md.write_text("old content", encoding="utf-8")

        with patch("branchspace.skill.get_project_root", return_value=tmp_path):
            install_skill("project")

        content = skill_md.read_text(encoding="utf-8")
        assert "old content" not in content
        assert f"name: {SKILL_NAME}" in content

    def test_install_global_scope(self, tmp_path: Path) -> None:
        with patch("branchspace.skill.get_global_skills_dir", return_value=tmp_path):
            result = install_skill("global")

        expected = tmp_path / SKILL_NAME / "SKILL.md"
        assert result == expected
        assert result.exists()
