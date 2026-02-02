"""Tests for agent instruction generation."""

from __future__ import annotations

from pathlib import Path

import pytest

from branchspace.agents import generate_instructions
from branchspace.agents import write_instructions


def test_generate_instructions_includes_sections():
    instructions = generate_instructions(["Claude Code", "Codex CLI"])

    assert "# Branchspace - AI Agent Instructions" in instructions
    assert "## Project Overview" in instructions
    assert "## Command Reference" in instructions
    assert "## Integration Tips" in instructions
    assert "Intended for: Claude Code, Codex CLI" in instructions


def test_write_instructions_overwrite(tmp_path: Path):
    target = tmp_path / "AGENTS.md"
    target.write_text("old", encoding="utf-8")

    write_instructions(target, "new", "overwrite")

    assert target.read_text(encoding="utf-8") == "new"


def test_write_instructions_append(tmp_path: Path):
    target = tmp_path / "AGENTS.md"
    target.write_text("old", encoding="utf-8")

    write_instructions(target, "new", "append")

    assert target.read_text(encoding="utf-8") == "old\n\nnew"


def test_write_instructions_append_empty(tmp_path: Path):
    target = tmp_path / "AGENTS.md"

    write_instructions(target, "new", "append")

    assert target.read_text(encoding="utf-8") == "new"


def test_write_instructions_skip(tmp_path: Path):
    target = tmp_path / "AGENTS.md"
    target.write_text("old", encoding="utf-8")

    write_instructions(target, "new", "skip")

    assert target.read_text(encoding="utf-8") == "old"


def test_write_instructions_invalid_mode(tmp_path: Path):
    target = tmp_path / "AGENTS.md"

    with pytest.raises(ValueError, match="Unknown write mode"):
        write_instructions(target, "new", "bad")
