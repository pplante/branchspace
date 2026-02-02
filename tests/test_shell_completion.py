"""Tests for shell completion generation."""

from __future__ import annotations

from click.testing import CliRunner

from branchspace.main_cli import main


def test_bash_completion_source():
    runner = CliRunner()
    env = {"_BRANCHSPACE_COMPLETE": "bash_source"}
    result = runner.invoke(main, env=env)

    assert result.exit_code == 0
    assert "_branchspace_completion" in result.output


def test_zsh_completion_source():
    runner = CliRunner()
    env = {"_BRANCHSPACE_COMPLETE": "zsh_source"}
    result = runner.invoke(main, env=env)

    assert result.exit_code == 0
    assert "compdef" in result.output


def test_fish_completion_source():
    runner = CliRunner()
    env = {"_BRANCHSPACE_COMPLETE": "fish_source"}
    result = runner.invoke(main, env=env)

    assert result.exit_code == 0
    assert "complete --no-files --command" in result.output
