"""Shell integration utilities for branchspace."""

from dataclasses import dataclass
from pathlib import Path

from branchspace.console import get_console
from branchspace.console import info


MARKER_START = "# >>> branchspace shell integration >>>"
MARKER_END = "# <<< branchspace shell integration <<<"


@dataclass(frozen=True)
class ShellIntegration:
    """Shell integration definition."""

    name: str
    rc_path: Path


def detect_shell_rc_files(home: Path | None = None) -> list[ShellIntegration]:
    """Detect available shell rc files for bash, zsh, and fish."""
    base = home or Path.home()
    candidates = [
        ShellIntegration("bash", base / ".bashrc"),
        ShellIntegration("zsh", base / ".zshrc"),
        ShellIntegration("fish", base / ".config/fish/config.fish"),
    ]
    return [candidate for candidate in candidates if candidate.rc_path.exists()]


def build_bash_integration() -> str:
    """Return the bash shell integration snippet with completion."""
    lines = [
        MARKER_START,
        "branchspace() {",
        '  if [[ "$1" == "cd" ]]; then',
        '    local target=$(command branchspace cd "${@:2}")',
        '    if [[ -n "$target" ]]; then',
        '      cd "$target"',
        "    fi",
        "  else",
        '    command branchspace "$@"',
        "  fi",
        "}",
        'eval "$(_BRANCHSPACE_COMPLETE=bash_source branchspace)"',
        MARKER_END,
    ]
    return "\n".join(lines)


def build_zsh_integration() -> str:
    """Return the zsh shell integration snippet with completion."""
    lines = [
        MARKER_START,
        "branchspace() {",
        '  if [[ "$1" == "cd" ]]; then',
        '    local target=$(command branchspace cd "${@:2}")',
        '    if [[ -n "$target" ]]; then',
        '      cd "$target"',
        "    fi",
        "  else",
        '    command branchspace "$@"',
        "  fi",
        "}",
        'eval "$(_BRANCHSPACE_COMPLETE=zsh_source branchspace)"',
        MARKER_END,
    ]
    return "\n".join(lines)


def build_fish_integration() -> str:
    """Return the fish shell integration snippet with completion."""
    lines = [
        MARKER_START,
        "function branchspace",
        '    if test (count $argv) -gt 0 && test $argv[1] = "cd"',
        "        set target (command branchspace cd $argv[2..])",
        '        if test -n "$target"',
        "            cd $target",
        "        end",
        "    else",
        "        command branchspace $argv",
        "    end",
        "end",
        "_BRANCHSPACE_COMPLETE=fish_source branchspace | source",
        MARKER_END,
    ]
    return "\n".join(lines)


def build_shell_function(shell: str = "bash") -> str:
    """Return the shell integration function snippet for the given shell.

    Args:
        shell: Shell name ("bash", "zsh", or "fish"). Defaults to "bash".

    Returns:
        Shell integration snippet for the specified shell
    """
    if shell == "bash":
        return build_bash_integration()
    elif shell == "zsh":
        return build_zsh_integration()
    elif shell == "fish":
        return build_fish_integration()
    else:
        # Fallback to bash-style for unknown shells
        return build_bash_integration()


def has_integration(content: str) -> bool:
    """Return True if integration markers are present."""
    return MARKER_START in content and MARKER_END in content


def append_integration(rc_path: Path, snippet: str) -> bool:
    """Append the integration snippet if not already present.

    Returns True if appended, False if already present.
    """
    existing = rc_path.read_text(encoding="utf-8") if rc_path.exists() else ""
    if has_integration(existing):
        return False
    content = existing.rstrip() + "\n\n" + snippet + "\n"
    rc_path.write_text(content, encoding="utf-8")
    return True


def render_manual_instructions() -> None:
    """Render manual installation instructions for all shells."""
    info("Add the following snippet to your shell rc file:")
    console = get_console()

    info("\nFor bash (.bashrc):")
    console.print(build_bash_integration())

    info("\nFor zsh (.zshrc):")
    console.print(build_zsh_integration())

    info("\nFor fish (~/.config/fish/config.fish):")
    console.print(build_fish_integration())
