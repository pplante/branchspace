"""Configuration system for branchspace using Pydantic models."""

import json
import os
import subprocess

from pathlib import Path
from typing import Annotated

from pydantic import BaseModel
from pydantic import ConfigDict
from pydantic import Field
from pydantic import ValidationError


# Config filename
CONFIG_FILENAME = "branchspace.json"


class ContainerImageConfig(BaseModel):
    """Container configuration using a Docker image."""

    model_config = ConfigDict(populate_by_name=True)

    image: str = Field(description="Docker image to use")


class ContainerBuildConfig(BaseModel):
    """Container configuration using a Dockerfile build."""

    model_config = ConfigDict(populate_by_name=True)

    context: str = Field(description="Build context path")
    dockerfile: str = Field(default="Dockerfile", description="Dockerfile path")


# Union type for container config - can be image-based or build-based
ContainerConfig = Annotated[
    ContainerImageConfig | ContainerBuildConfig,
    Field(discriminator=None),
]


def _default_container_config() -> ContainerImageConfig:
    """Return the default container configuration."""
    return ContainerImageConfig(image="ubuntu:24.04")


class BranchspaceConfig(BaseModel):
    """Main configuration model for branchspace.json."""

    model_config = ConfigDict(
        populate_by_name=True,
        extra="ignore",  # Ignore unknown fields for forward compatibility
    )

    # File patterns to copy to new worktrees
    worktree_copy_patterns: list[str] = Field(
        default_factory=lambda: [".env*", ".vscode/**"],
        alias="worktreeCopyPatterns",
        description="Glob patterns for files to copy to new worktrees",
    )

    # File patterns to exclude from copying
    worktree_copy_ignores: list[str] = Field(
        default_factory=lambda: ["**/node_modules/**", "**/dist/**"],
        alias="worktreeCopyIgnores",
        description="Glob patterns for files to exclude from copying",
    )

    # Template for worktree directory path
    worktree_path_template: str = Field(
        default_factory=lambda: f"{os.path.expanduser('~')}/.branchspace/worktrees/$BRANCH_NAME",
        alias="worktreePathTemplate",
        description="Template for worktree directory path",
    )

    # Commands to run after worktree creation
    post_create_cmd: list[str] = Field(
        default_factory=list,
        alias="postCreateCmd",
        description="Commands to run after creating a worktree",
    )

    # Command to open editor/terminal
    terminal_command: str = Field(
        default="",
        alias="terminalCommand",
        description="Command to open editor in worktree",
    )

    # Whether to delete branch and Docker resources on remove
    purge_on_remove: bool = Field(
        default=False,
        alias="purgeOnRemove",
        description="Delete branch and Docker resources when removing worktree",
    )

    # Container configuration (image or build)
    container_config: ContainerImageConfig | ContainerBuildConfig = Field(
        default_factory=_default_container_config,
        alias="containerConfig",
        description="Docker container configuration",
    )

    # Shell for interactive sessions
    shell: str = Field(
        default="bash",
        description="Shell to use for interactive sessions",
    )


def get_git_root(start_path: Path | None = None) -> Path | None:
    """Find the git repository root from start_path or cwd.

    Args:
        start_path: Starting directory for search. Defaults to cwd.

    Returns:
        Path to git root, or None if not in a git repository.
    """
    if start_path is None:
        start_path = Path.cwd()

    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=start_path,
            capture_output=True,
            text=True,
            check=True,
        )
        return Path(result.stdout.strip())
    except (subprocess.CalledProcessError, FileNotFoundError):
        return None


def find_config_file(start_path: Path | None = None) -> Path | None:
    """Search for branchspace.json from start_path up to git root.

    Args:
        start_path: Starting directory for search. Defaults to cwd.

    Returns:
        Path to config file if found, None otherwise.
    """
    if start_path is None:
        start_path = Path.cwd()

    start_path = start_path.resolve()

    # Get git root to know where to stop searching
    git_root = get_git_root(start_path)

    # If not in a git repo, only check start_path
    if git_root is None:
        config_path = start_path / CONFIG_FILENAME
        return config_path if config_path.is_file() else None

    git_root = git_root.resolve()

    # Search from start_path up to git root
    current = start_path
    while True:
        config_path = current / CONFIG_FILENAME
        if config_path.is_file():
            return config_path

        # Stop if we've reached git root
        if current == git_root:
            break

        # Move up one directory
        parent = current.parent
        if parent == current:
            # Reached filesystem root
            break
        current = parent

    return None


class ConfigError(Exception):
    """Error loading or parsing configuration."""

    def __init__(self, message: str, path: Path | None = None):
        self.path = path
        super().__init__(message)


def load_config(path: Path | None = None) -> BranchspaceConfig:
    """Load configuration from file or return defaults.

    Args:
        path: Explicit path to config file. If None, uses discovery.

    Returns:
        BranchspaceConfig instance with loaded or default values.

    Raises:
        ConfigError: If the config file exists but is invalid.
    """
    # If no path provided, try to discover one
    if path is None:
        path = find_config_file()

    env_base = os.environ.get("BRANCHSPACE_BASE")

    def apply_env_overrides(config: BranchspaceConfig) -> BranchspaceConfig:
        if env_base:
            config.worktree_path_template = f"{env_base}/$BRANCH_NAME"
        return config

    # No config file found - return defaults
    if path is None:
        return apply_env_overrides(BranchspaceConfig())

    # Config file specified but doesn't exist
    if not path.is_file():
        return apply_env_overrides(BranchspaceConfig())

    # Load and parse the config file
    try:
        content = path.read_text(encoding="utf-8")
        data = json.loads(content)
    except json.JSONDecodeError as e:
        raise ConfigError(f"Invalid JSON in config file: {e}", path=path) from e
    except OSError as e:
        raise ConfigError(f"Error reading config file: {e}", path=path) from e

    # Validate with Pydantic
    try:
        return apply_env_overrides(BranchspaceConfig.model_validate(data))
    except ValidationError as e:
        # Format a user-friendly error message
        errors = []
        for error in e.errors():
            loc = ".".join(str(x) for x in error["loc"])
            msg = error["msg"]
            errors.append(f"  - {loc}: {msg}")
        error_details = "\n".join(errors)
        raise ConfigError(
            f"Invalid configuration in {path}:\n{error_details}",
            path=path,
        ) from e


class TemplateContext(BaseModel):
    """Template variables for expanding config strings."""

    base_path: str
    worktree_path: str
    branch_name: str
    source_branch: str

    def as_mapping(self) -> dict[str, str]:
        return {
            "BASE_PATH": self.base_path,
            "WORKTREE_PATH": self.worktree_path,
            "BRANCH_NAME": self.branch_name,
            "SOURCE_BRANCH": self.source_branch,
        }
