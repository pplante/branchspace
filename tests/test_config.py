"""Tests for the branchspace configuration system."""

from __future__ import annotations

import json
import subprocess

from pathlib import Path
from unittest.mock import patch

import pytest

from branchspace.config import CONFIG_FILENAME
from branchspace.config import BranchspaceConfig
from branchspace.config import ConfigError
from branchspace.config import ContainerBuildConfig
from branchspace.config import ContainerImageConfig
from branchspace.config import TemplateContext
from branchspace.config import find_config_file
from branchspace.config import get_git_root
from branchspace.config import load_config


class TestContainerImageConfig:
    """Tests for ContainerImageConfig model."""

    def test_create_with_image(self):
        """Test creating config with image."""
        config = ContainerImageConfig(image="python:3.14")
        assert config.image == "python:3.14"

    def test_requires_image(self):
        """Test that image field is required."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            ContainerImageConfig.model_validate({})


class TestContainerBuildConfig:
    """Tests for ContainerBuildConfig model."""

    def test_requires_context(self):
        """Test that context field is required."""
        from pydantic import ValidationError

        with pytest.raises(ValidationError):
            ContainerBuildConfig.model_validate({})

    def test_create_with_custom_values(self):
        """Test creating config with custom values."""
        config = ContainerBuildConfig(context="docker", dockerfile="Dockerfile.dev")
        assert config.context == "docker"
        assert config.dockerfile == "Dockerfile.dev"


class TestBranchspaceConfigDefaults:
    """Tests for BranchspaceConfig default values."""

    def test_default_worktree_copy_patterns(self):
        """Test default worktreeCopyPatterns matches README."""
        config = BranchspaceConfig()
        assert config.worktree_copy_patterns == [".env*", ".vscode/**"]

    def test_default_worktree_copy_ignores(self):
        """Test default worktreeCopyIgnores matches README."""
        config = BranchspaceConfig()
        assert config.worktree_copy_ignores == ["**/node_modules/**", "**/dist/**"]

    def test_default_worktree_path_template(self):
        """Test default worktreePathTemplate matches README."""
        config = BranchspaceConfig()
        assert "$BRANCH_NAME" in config.worktree_path_template

    def test_default_post_create_cmd(self):
        """Test default postCreateCmd is empty list."""
        config = BranchspaceConfig()
        assert config.post_create_cmd == []

    def test_default_terminal_command(self):
        """Test default terminalCommand is empty string."""
        config = BranchspaceConfig()
        assert config.terminal_command == ""

    def test_default_purge_on_remove(self):
        """Test default purgeOnRemove is False."""
        config = BranchspaceConfig()
        assert config.purge_on_remove is False

    def test_default_container_config(self):
        """Test default containerConfig matches README."""
        config = BranchspaceConfig()
        assert isinstance(config.container_config, ContainerImageConfig)
        assert config.container_config.image == "ubuntu:24.04"

    def test_default_project_name(self):
        """Test default projectName is empty."""
        config = BranchspaceConfig()
        assert config.project_name == ""

    def test_default_shell(self):
        """Test default shell is bash."""
        config = BranchspaceConfig()
        assert config.shell == "bash"


class TestBranchspaceConfigParsing:
    """Tests for BranchspaceConfig JSON parsing."""

    def test_parse_camel_case_json(self):
        """Test parsing JSON with camelCase keys."""
        data = {
            "worktreeCopyPatterns": [".env"],
            "worktreeCopyIgnores": ["**/cache/**"],
            "worktreePathTemplate": ".worktrees/$BRANCH_NAME",
            "postCreateCmd": ["npm install"],
            "terminalCommand": "code .",
            "purgeOnRemove": True,
            "containerConfig": {"image": "node:24"},
            "shell": "zsh",
            "projectName": "branchspace",
        }
        config = BranchspaceConfig.model_validate(data)

        assert config.worktree_copy_patterns == [".env"]
        assert config.worktree_copy_ignores == ["**/cache/**"]
        assert config.worktree_path_template == ".worktrees/$BRANCH_NAME"
        assert config.post_create_cmd == ["npm install"]
        assert config.terminal_command == "code ."
        assert config.purge_on_remove is True
        assert isinstance(config.container_config, ContainerImageConfig)
        assert config.container_config.image == "node:24"
        assert config.shell == "zsh"
        assert config.project_name == "branchspace"

    def test_parse_snake_case_json(self):
        """Test parsing JSON with snake_case keys."""
        data = {
            "worktree_copy_patterns": [".env"],
            "shell": "fish",
        }
        config = BranchspaceConfig.model_validate(data)

        assert config.worktree_copy_patterns == [".env"]
        assert config.shell == "fish"

    def test_parse_build_container_config(self):
        """Test parsing containerConfig with build configuration."""
        data = {
            "containerConfig": {
                "context": ".",
                "dockerfile": "Dockerfile.dev",
            }
        }
        config = BranchspaceConfig.model_validate(data)

        assert isinstance(config.container_config, ContainerBuildConfig)
        assert config.container_config.context == "."
        assert config.container_config.dockerfile == "Dockerfile.dev"

    def test_parse_build_container_config_defaults_dockerfile(self):
        """Test parsing containerConfig with build configuration defaults."""
        data = {"containerConfig": {"context": "docker"}}
        config = BranchspaceConfig.model_validate(data)

        assert isinstance(config.container_config, ContainerBuildConfig)
        assert config.container_config.context == "docker"
        assert config.container_config.dockerfile == "Dockerfile"

    def test_ignores_unknown_fields(self):
        """Test that unknown fields are ignored."""
        data = {
            "unknownField": "value",
            "anotherUnknown": 123,
            "shell": "zsh",
        }
        config = BranchspaceConfig.model_validate(data)
        assert config.shell == "zsh"
        assert not hasattr(config, "unknownField")

    def test_partial_config_uses_defaults(self):
        """Test that missing fields use defaults."""
        data = {"shell": "fish"}
        config = BranchspaceConfig.model_validate(data)

        assert config.shell == "fish"
        assert config.worktree_copy_patterns == [".env*", ".vscode/**"]
        assert config.purge_on_remove is False


class TestBranchspaceConfigEnvOverrides:
    """Tests for env var overrides."""

    def test_env_base_override(self, monkeypatch, tmp_path: Path):
        monkeypatch.setenv("BRANCHSPACE_BASE", str(tmp_path))
        config = load_config(path=None)

        assert config.worktree_path_template == f"{tmp_path}/$BRANCH_NAME"


class TestGetGitRoot:
    """Tests for get_git_root function."""

    def test_returns_git_root_in_repo(self, tmp_path: Path):
        """Test finding git root in a repository."""
        # Create a git repo
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True, check=True)

        # Create a subdirectory
        subdir = tmp_path / "src" / "app"
        subdir.mkdir(parents=True)

        # Should find repo root from subdirectory
        root = get_git_root(subdir)
        assert root is not None
        assert root.resolve() == tmp_path.resolve()

    def test_returns_none_outside_repo(self, tmp_path: Path):
        """Test returns None when not in a git repository."""
        # tmp_path is not a git repo
        root = get_git_root(tmp_path)
        assert root is None

    def test_uses_cwd_when_no_path(self):
        """Test uses cwd when no start_path provided."""
        # This test runs from project root which is a git repo
        root = get_git_root()
        assert root is not None


class TestFindConfigFile:
    """Tests for find_config_file function."""

    def test_finds_config_in_current_dir(self, tmp_path: Path):
        """Test finding config file in current directory."""
        # Create git repo
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True, check=True)

        # Create config file
        config_path = tmp_path / CONFIG_FILENAME
        config_path.write_text('{"shell": "zsh"}')

        result = find_config_file(tmp_path)
        assert result is not None
        assert result == config_path

    def test_finds_config_in_parent_dir(self, tmp_path: Path):
        """Test finding config file in parent directory."""
        # Create git repo
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True, check=True)

        # Create config in repo root
        config_path = tmp_path / CONFIG_FILENAME
        config_path.write_text('{"shell": "zsh"}')

        # Create and search from subdirectory
        subdir = tmp_path / "src" / "app"
        subdir.mkdir(parents=True)

        result = find_config_file(subdir)
        assert result is not None
        assert result == config_path

    def test_returns_none_when_no_config(self, tmp_path: Path):
        """Test returns None when no config file exists."""
        # Create git repo without config
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True, check=True)

        result = find_config_file(tmp_path)
        assert result is None

    def test_stops_at_git_root(self, tmp_path: Path):
        """Test search stops at git root boundary."""
        # Create config in tmp_path (outside git repo)
        outer_config = tmp_path / CONFIG_FILENAME
        outer_config.write_text('{"shell": "outer"}')

        # Create git repo in subdirectory
        repo_path = tmp_path / "repo"
        repo_path.mkdir()
        subprocess.run(["git", "init"], cwd=repo_path, capture_output=True, check=True)

        # Should not find the outer config
        result = find_config_file(repo_path)
        assert result is None

    def test_handles_non_git_directory(self, tmp_path: Path):
        """Test behavior in non-git directory."""
        # Create config without git repo
        config_path = tmp_path / CONFIG_FILENAME
        config_path.write_text('{"shell": "zsh"}')

        result = find_config_file(tmp_path)
        assert result == config_path


class TestLoadConfig:
    """Tests for load_config function."""

    def test_returns_defaults_when_no_config(self, tmp_path: Path):
        """Test returns default config when no file found."""
        # Create git repo without config
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True, check=True)

        with patch("branchspace.config.find_config_file", return_value=None):
            config = load_config()

        assert config.shell == "bash"
        assert config.worktree_copy_patterns == [".env*", ".vscode/**"]

    def test_loads_config_from_file(self, tmp_path: Path):
        """Test loading config from file."""
        config_path = tmp_path / CONFIG_FILENAME
        config_path.write_text(
            json.dumps(
                {
                    "worktreeCopyPatterns": [".env"],
                    "shell": "fish",
                }
            )
        )

        config = load_config(config_path)

        assert config.shell == "fish"
        assert config.worktree_copy_patterns == [".env"]

    def test_raises_on_invalid_json(self, tmp_path: Path):
        """Test raises ConfigError on invalid JSON."""
        config_path = tmp_path / CONFIG_FILENAME
        config_path.write_text("{ invalid json }")

        with pytest.raises(ConfigError) as exc_info:
            load_config(config_path)

        assert "Invalid JSON" in str(exc_info.value)
        assert exc_info.value.path == config_path

    def test_raises_on_validation_error(self, tmp_path: Path):
        """Test raises ConfigError on validation error."""
        config_path = tmp_path / CONFIG_FILENAME
        config_path.write_text(
            json.dumps(
                {
                    "purgeOnRemove": "not a boolean",
                }
            )
        )

        with pytest.raises(ConfigError) as exc_info:
            load_config(config_path)

        assert "Invalid configuration" in str(exc_info.value)
        assert exc_info.value.path == config_path

    def test_returns_defaults_for_nonexistent_explicit_path(self, tmp_path: Path):
        """Test returns defaults when explicit path doesn't exist."""
        nonexistent = tmp_path / "nonexistent.json"

        config = load_config(nonexistent)

        assert config.shell == "bash"

    def test_uses_discovery_when_no_path_provided(self, tmp_path: Path):
        """Test uses find_config_file when no path provided."""
        # Create git repo with config
        subprocess.run(["git", "init"], cwd=tmp_path, capture_output=True, check=True)
        config_path = tmp_path / CONFIG_FILENAME
        config_path.write_text(json.dumps({"shell": "zsh"}))

        # Mock cwd to be in the temp repo
        with patch("branchspace.config.find_config_file", return_value=config_path):
            config = load_config()

        assert config.shell == "zsh"


class TestConfigError:
    """Tests for ConfigError exception."""

    def test_stores_path(self):
        """Test ConfigError stores the file path."""
        path = Path("/some/path/config.json")
        error = ConfigError("test message", path=path)

        assert error.path == path
        assert "test message" in str(error)

    def test_path_is_optional(self):
        """Test ConfigError works without path."""
        error = ConfigError("test message")

        assert error.path is None
        assert "test message" in str(error)


class TestTemplateContext:
    """Tests for template context mapping."""

    def test_as_mapping(self):
        """Test mapping exposes expected template keys."""
        context = TemplateContext(
            base_path="myproject",
            worktree_path="/repo/worktrees/feature-auth",
            branch_name="feature-auth",
            source_branch="main",
            project_name="branchspace",
        )

        mapping = context.as_mapping()

        assert mapping == {
            "BASE_PATH": "myproject",
            "WORKTREE_PATH": "/repo/worktrees/feature-auth",
            "BRANCH_NAME": "feature-auth",
            "SOURCE_BRANCH": "main",
            "PROJECT_NAME": "branchspace",
        }
