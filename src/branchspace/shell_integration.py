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
    """Detect available shell rc files for bash and zsh."""
    base = home or Path.home()
    candidates = [
        ShellIntegration("bash", base / ".bashrc"),
        ShellIntegration("zsh", base / ".zshrc"),
    ]
    return [candidate for candidate in candidates if candidate.rc_path.exists()]


def build_shell_function() -> str:
    """Return the shell integration function snippet."""
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
        MARKER_END,
    ]
    return "\n".join(lines)


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
    """Render manual installation instructions."""
    info("Add the following snippet to your shell rc file:")
    console = get_console()
    console.print(build_shell_function())
