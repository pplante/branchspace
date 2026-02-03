"""Tests for shell integration helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from branchspace.shell_integration import MARKER_END
from branchspace.shell_integration import MARKER_START
from branchspace.shell_integration import append_integration
from branchspace.shell_integration import build_bash_integration
from branchspace.shell_integration import build_fish_integration
from branchspace.shell_integration import build_shell_function
from branchspace.shell_integration import build_zsh_integration
from branchspace.shell_integration import has_integration


if TYPE_CHECKING:
    from pathlib import Path


def test_build_shell_function_contains_markers():
    snippet = build_shell_function()

    assert MARKER_START in snippet
    assert MARKER_END in snippet
    assert "branchspace()" in snippet


def test_build_bash_integration_contains_completion():
    snippet = build_bash_integration()

    assert MARKER_START in snippet
    assert MARKER_END in snippet
    assert "branchspace()" in snippet
    assert 'eval "$(_BRANCHSPACE_COMPLETE=bash_source branchspace)"' in snippet


def test_build_zsh_integration_contains_completion():
    snippet = build_zsh_integration()

    assert MARKER_START in snippet
    assert MARKER_END in snippet
    assert "branchspace()" in snippet
    assert 'eval "$(_BRANCHSPACE_COMPLETE=zsh_source branchspace)"' in snippet


def test_build_fish_integration_contains_completion():
    snippet = build_fish_integration()

    assert MARKER_START in snippet
    assert MARKER_END in snippet
    assert "function branchspace" in snippet
    assert "_BRANCHSPACE_COMPLETE=fish_source branchspace | source" in snippet


def test_build_shell_function_dispatches_to_bash():
    bash_snippet = build_shell_function("bash")
    expected = build_bash_integration()

    assert bash_snippet == expected


def test_build_shell_function_dispatches_to_zsh():
    zsh_snippet = build_shell_function("zsh")
    expected = build_zsh_integration()

    assert zsh_snippet == expected


def test_build_shell_function_dispatches_to_fish():
    fish_snippet = build_shell_function("fish")
    expected = build_fish_integration()

    assert fish_snippet == expected


def test_build_shell_function_defaults_to_bash():
    default_snippet = build_shell_function()
    bash_snippet = build_bash_integration()

    assert default_snippet == bash_snippet


def test_build_shell_function_unknown_shell_falls_back_to_bash():
    unknown_snippet = build_shell_function("unknown")
    bash_snippet = build_bash_integration()

    assert unknown_snippet == bash_snippet


def test_append_integration_is_idempotent(tmp_path: Path):
    rc_file = tmp_path / ".bashrc"
    rc_file.write_text("export PATH=$PATH", encoding="utf-8")
    snippet = build_shell_function()

    appended = append_integration(rc_file, snippet)
    appended_again = append_integration(rc_file, snippet)

    assert appended is True
    assert appended_again is False
    assert has_integration(rc_file.read_text(encoding="utf-8"))
