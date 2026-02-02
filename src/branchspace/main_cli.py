"""Main CLI entrypoint for branchspace."""

import subprocess

import click
import questionary

from branchspace import __version__
from branchspace.agents import SUPPORTED_AGENTS
from branchspace.agents import format_agent_label
from branchspace.agents import generate_instructions
from branchspace.agents import get_project_root
from branchspace.agents import write_instructions
from branchspace.config import ConfigError
from branchspace.config import load_config
from branchspace.config_display import load_config_view
from branchspace.config_display import render_config
from branchspace.console import error
from branchspace.console import info
from branchspace.console import spinner
from branchspace.console import success
from branchspace.docker_purge import DockerPurgeError
from branchspace.docker_purge import run_docker_purge
from branchspace.docker_shell import DockerShellError
from branchspace.docker_shell import run_docker_shell
from branchspace.init_config import init_config
from branchspace.shell_integration import append_integration
from branchspace.shell_integration import build_shell_function
from branchspace.shell_integration import detect_shell_rc_files
from branchspace.shell_integration import render_manual_instructions
from branchspace.skill import install_skill
from branchspace.skill import is_skill_installed
from branchspace.worktree_cd import WorktreeLookupError
from branchspace.worktree_cd import resolve_worktree_path
from branchspace.worktree_create import CreateWorktreeError
from branchspace.worktree_create import create_worktrees
from branchspace.worktree_list import build_worktree_list_table
from branchspace.worktree_list import list_worktree_statuses
from branchspace.worktree_remove import WorktreeRemoveError
from branchspace.worktree_remove import remove_worktrees


@click.group(
    "branchspace",
    help="Manage git worktrees and environments. Env: BRANCHSPACE_BASE overrides worktree base.",
)
@click.version_option(__version__, "--version", prog_name="branchspace")
def main() -> None:
    """Branchspace CLI."""


@main.command(help="Create a new worktree.")
@click.argument("branch", nargs=-1, required=True)
def create(branch: tuple[str, ...]) -> None:
    """Create a new worktree."""
    try:
        config = load_config()
    except ConfigError as exc:
        error(str(exc))
        raise SystemExit(1) from exc

    try:
        with spinner("Creating worktrees"):
            results = create_worktrees(list(branch), config)
    except CreateWorktreeError as exc:
        error(str(exc))
        raise SystemExit(1) from exc
    except OSError as exc:
        error(str(exc))
        raise SystemExit(1) from exc
    except subprocess.CalledProcessError as exc:
        error(exc.stderr.strip() if exc.stderr else str(exc))
        raise SystemExit(1) from exc

    for created in results:
        success(f"Created {created.branch} at {created.path}")
    info("Worktrees ready.")


@main.command(help="Remove a worktree.")
@click.argument("branch", nargs=-1, required=True)
def rm(branch: tuple[str, ...]) -> None:
    """Remove a worktree."""
    try:
        config = load_config()
    except ConfigError as exc:
        error(str(exc))
        raise SystemExit(1) from exc

    try:
        results = remove_worktrees(list(branch), config)
    except WorktreeRemoveError as exc:
        error(str(exc))
        raise SystemExit(1) from exc
    except subprocess.CalledProcessError as exc:
        error(exc.stderr.strip() if exc.stderr else str(exc))
        raise SystemExit(1) from exc

    for result in results:
        if result.removed:
            success(f"Removed {result.branch} at {result.path}")
        else:
            info(f"Skipped {result.branch} at {result.path}")


@main.command(help="Change to a worktree.")
@click.argument("branch", required=False)
def cd(branch: str | None) -> None:
    """Change to a worktree."""
    try:
        resolved = resolve_worktree_path(branch)
    except WorktreeLookupError as exc:
        error(str(exc))
        raise SystemExit(1) from exc

    click.echo(str(resolved.path))


@main.command(help="List worktrees.")
def ls() -> None:
    """List worktrees."""
    try:
        statuses = list_worktree_statuses()
    except subprocess.CalledProcessError as exc:
        error(exc.stderr.strip() if exc.stderr else str(exc))
        raise SystemExit(1) from exc

    if not statuses:
        info("No worktrees found.")
        return

    table = build_worktree_list_table(statuses)
    from branchspace.console import get_console

    get_console().print(table)


@main.command(help="Open an interactive shell.")
@click.argument("command", required=False)
def shell(command: str | None) -> None:
    """Open an interactive shell."""
    try:
        config = load_config()
    except ConfigError as exc:
        error(str(exc))
        raise SystemExit(1) from exc

    try:
        with spinner("Starting container shell"):
            run_docker_shell(config, command=command)
    except DockerShellError as exc:
        error(str(exc))
        raise SystemExit(1) from exc
    except subprocess.CalledProcessError as exc:
        error(exc.stderr.strip() if exc.stderr else str(exc))
        raise SystemExit(1) from exc


@main.command(help="Purge a worktree and related resources.")
@click.option("--force", is_flag=True, help="Skip confirmation prompts.")
@click.option("--dry-run", is_flag=True, help="Preview resources without removing.")
def purge(force: bool, dry_run: bool) -> None:
    """Purge a worktree and related resources."""
    try:
        with spinner("Discovering Docker resources"):
            resources = run_docker_purge(dry_run=dry_run, force=force)
    except DockerPurgeError as exc:
        error(str(exc))
        raise SystemExit(1) from exc
    except subprocess.CalledProcessError as exc:
        error(exc.stderr.strip() if exc.stderr else str(exc))
        raise SystemExit(1) from exc

    if resources.is_empty():
        info("No Docker resources found.")
        return

    if dry_run:
        info("Dry run only. No resources removed.")


@main.command(help="Initialize configuration for this repository.")
def init() -> None:
    """Initialize branchspace configuration."""
    try:
        config_path = init_config()
    except RuntimeError as exc:
        error(str(exc))
        raise SystemExit(1) from exc

    success(f"Created {config_path}")


@main.command(name="config", help="Show or edit configuration.")
def config_cmd() -> None:
    """Show or edit configuration."""
    try:
        view = load_config_view()
    except ConfigError as exc:
        error(str(exc))
        raise SystemExit(1) from exc

    render_config(view)


@main.command(name="shell-integration", help="Install shell integration.")
def shell_integration() -> None:
    """Install shell integration."""
    candidates = detect_shell_rc_files()
    if not candidates:
        info("No supported shell rc files detected.")
        render_manual_instructions()
        return

    choices = [f"{candidate.name}: {candidate.rc_path}" for candidate in candidates]
    selection = questionary.checkbox(
        "Select shell rc files to update:",
        choices=choices,
    ).unsafe_ask()

    if not selection:
        render_manual_instructions()
        return

    snippet = build_shell_function()
    updated = False
    for candidate in candidates:
        label = f"{candidate.name}: {candidate.rc_path}"
        if label not in selection:
            continue
        if append_integration(candidate.rc_path, snippet):
            success(f"Updated {candidate.rc_path}")
            updated = True
        else:
            info(f"Integration already present in {candidate.rc_path}")

    if not updated:
        render_manual_instructions()


@main.command(help="Generate AI agent instructions for this repository.")
def agents() -> None:
    """Generate AI agent instructions for this repository."""
    choices = [format_agent_label(agent) for agent in SUPPORTED_AGENTS]
    selection = questionary.checkbox(
        "Select agents to generate instructions for:",
        choices=choices,
    ).unsafe_ask()

    if not selection:
        info("No agents selected.")
        return

    # Ask about skill installation
    should_install_skill = questionary.confirm(
        "Install the Branchspace Agent Skill for these agents?",
        default=True,
    ).unsafe_ask()

    if should_install_skill:
        scope_choices = [
            "Project scope (.skills/ - committed with repo)",
            "Global scope (~/.skills/ - available everywhere)",
        ]
        scope_selection = questionary.select(
            "Where should the skill be installed?",
            choices=scope_choices,
        ).unsafe_ask()

        if scope_selection is not None:
            scope_key = "project" if "Project" in scope_selection else "global"

            # Check if already installed
            if is_skill_installed(scope_key):
                update_mode = questionary.select(
                    f"Skill already exists at {scope_key} scope. What would you like to do?",
                    choices=["Update", "Skip"],
                ).unsafe_ask()

                if update_mode == "Skip":
                    info("Skipped skill installation.")
                else:
                    skill_path = install_skill(scope_key)
                    success(f"Updated skill at {skill_path}")
            else:
                skill_path = install_skill(scope_key)
                success(f"Installed skill at {skill_path}")

    output_target = questionary.select(
        "Output instructions to:",
        choices=[
            "Console only",
            "Write to file(s)",
            "Both",
        ],
    ).unsafe_ask()

    if output_target is None:
        info("No output target selected.")
        return

    selected_agents = [
        agent for agent in SUPPORTED_AGENTS if format_agent_label(agent) in selection
    ]
    audience = [agent.name for agent in selected_agents]
    instructions = generate_instructions(audience)

    if output_target in {"Console only", "Both"}:
        click.echo(instructions)

    if output_target in {"Write to file(s)", "Both"}:
        project_root = get_project_root()
        filename_to_agents: dict[str, list[str]] = {}
        for agent in selected_agents:
            filename_to_agents.setdefault(agent.filename, []).append(agent.name)

        for filename, agent_names in filename_to_agents.items():
            target_path = project_root / filename
            file_exists = target_path.exists()
            if file_exists:
                mode = questionary.select(
                    f"{filename} exists. Choose how to update it:",
                    choices=[
                        "Append",
                        "Overwrite",
                        "Skip",
                    ],
                ).unsafe_ask()

                if mode is None:
                    info(f"Skipped {filename}.")
                    continue

                mode_key = mode.lower()
            else:
                mode_key = "overwrite"

            file_instructions = generate_instructions(agent_names)
            write_instructions(target_path, file_instructions, mode_key)
            if mode_key == "skip":
                info(f"Skipped {target_path}")
            else:
                success(f"Wrote {target_path}")
