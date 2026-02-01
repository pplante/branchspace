"""Tests for the main branchspace CLI."""

from __future__ import annotations

import subprocess

from pathlib import Path

import pytest

from click.testing import CliRunner

from branchspace import __version__
from branchspace.main_cli import main


class TestMainCli:
    """Tests for main CLI entrypoint."""

    def test_help_lists_commands(self):
        runner = CliRunner()
        result = runner.invoke(main, ["--help"])

        assert result.exit_code == 0
        assert "create" in result.output
        assert "rm" in result.output
        assert "cd" in result.output
        assert "ls" in result.output
        assert "shell" in result.output
        assert "purge" in result.output
        assert "init" in result.output
        assert "config" in result.output
        assert "shell-integration" in result.output

    def test_version_flag(self):
        runner = CliRunner()
        result = runner.invoke(main, ["--version"])

        assert result.exit_code == 0
        assert __version__ in result.output

    def test_module_entrypoint_runs(self):
        result = subprocess.run(
            ["python", "-m", "branchspace", "--version"],
            capture_output=True,
            text=True,
            check=False,
        )

        assert result.returncode == 0
        assert __version__ in result.stdout

    @pytest.mark.parametrize(
        "command",
        [
            "create",
            "rm",
            "cd",
            "ls",
            "shell",
            "purge",
            "init",
            "config",
            "shell-integration",
        ],
    )
    def test_placeholder_commands(self, command: str):
        runner = CliRunner()
        result = runner.invoke(main, [command])

        assert result.exit_code == 0
        assert "Not implemented yet." in result.output
