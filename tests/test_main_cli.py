"""Tests for the main branchspace CLI."""

from __future__ import annotations

import subprocess

from pathlib import Path

import pytest

from click.testing import CliRunner

from branchspace import __version__
from branchspace.config import BranchspaceConfig
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
            "init",
        ],
    )
    def test_placeholder_commands(self, command: str):
        runner = CliRunner()
        result = runner.invoke(main, [command])

        assert result.exit_code == 0
        assert "Not implemented yet." in result.output

    def test_ls_outputs_table(self, monkeypatch):
        runner = CliRunner()

        monkeypatch.setattr(
            "branchspace.main_cli.list_worktree_statuses",
            lambda _path=None: [],
        )

        result = runner.invoke(main, ["ls"])

        assert result.exit_code == 0
        assert "No worktrees found" in result.output

    def test_create_requires_branch_argument(self):
        runner = CliRunner()
        result = runner.invoke(main, ["create"])

        assert result.exit_code != 0
        assert "Missing argument" in result.output

    def test_rm_requires_branch_argument(self):
        runner = CliRunner()
        result = runner.invoke(main, ["rm"])

        assert result.exit_code != 0
        assert "Missing argument" in result.output

    def test_cd_outputs_root(self, monkeypatch):
        runner = CliRunner()

        monkeypatch.setattr(
            "branchspace.main_cli.resolve_worktree_path",
            lambda branch=None: type("Resolved", (), {"path": "/repo"})(),
        )

        result = runner.invoke(main, ["cd"])

        assert result.exit_code == 0
        assert result.output.strip() == "/repo"

    def test_config_renders_defaults(self, monkeypatch):
        runner = CliRunner()

        monkeypatch.setattr(
            "branchspace.main_cli.load_config_view",
            lambda: type("View", (), {"config": BranchspaceConfig(), "config_path": None})(),
        )
        monkeypatch.setattr("branchspace.main_cli.render_config", lambda _view: None)

        result = runner.invoke(main, ["config"])

        assert result.exit_code == 0

    def test_shell_integration_no_rc_files(self, monkeypatch):
        runner = CliRunner()

        monkeypatch.setattr(
            "branchspace.main_cli.detect_shell_rc_files",
            lambda: [],
        )
        monkeypatch.setattr("branchspace.main_cli.render_manual_instructions", lambda: None)

        result = runner.invoke(main, ["shell-integration"])

        assert result.exit_code == 0

    def test_shell_invokes_docker(self, monkeypatch):
        runner = CliRunner()
        monkeypatch.setattr("branchspace.main_cli.load_config", lambda: BranchspaceConfig())
        monkeypatch.setattr("branchspace.main_cli.run_docker_shell", lambda *_args, **_kwargs: None)

        result = runner.invoke(main, ["shell", "npm test"])

        assert result.exit_code == 0

    def test_purge_dry_run(self, monkeypatch):
        runner = CliRunner()
        monkeypatch.setattr(
            "branchspace.main_cli.run_docker_purge",
            lambda **_kwargs: type("Resources", (), {"is_empty": lambda self: True})(),
        )

        result = runner.invoke(main, ["purge", "--dry-run"])

        assert result.exit_code == 0
