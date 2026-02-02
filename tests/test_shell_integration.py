"""Tests for shell integration helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from branchspace.shell_integration import MARKER_END
from branchspace.shell_integration import MARKER_START
from branchspace.shell_integration import append_integration
from branchspace.shell_integration import build_shell_function
from branchspace.shell_integration import has_integration


if TYPE_CHECKING:
    from pathlib import Path


def test_build_shell_function_contains_markers():
    snippet = build_shell_function()

    assert MARKER_START in snippet
    assert MARKER_END in snippet
    assert "branchspace()" in snippet


def test_append_integration_is_idempotent(tmp_path: Path):
    rc_file = tmp_path / ".bashrc"
    rc_file.write_text("export PATH=$PATH", encoding="utf-8")
    snippet = build_shell_function()

    appended = append_integration(rc_file, snippet)
    appended_again = append_integration(rc_file, snippet)

    assert appended is True
    assert appended_again is False
    assert has_integration(rc_file.read_text(encoding="utf-8"))
