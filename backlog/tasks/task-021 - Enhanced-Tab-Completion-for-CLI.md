---
id: TASK-021
title: Enhanced Tab Completion for CLI
status: To Do
assignee: []
created_date: '2026-02-02 04:19'
labels:
  - cli
  - shell
  - enhancement
dependencies:
  - TASK-012
priority: medium
---

## Description

<!-- SECTION:DESCRIPTION:BEGIN -->
Add dynamic branch/worktree completion and auto-install completion scripts via shell-integration command.

**Goals:**
1. **Dynamic worktree completion** for `rm` and `cd` commands - complete with existing worktree branch names
2. **Auto-install shell completions** in the `shell-integration` command for bash, zsh, and fish

**Background:**
- Click already provides basic completion for commands and flags via `_BRANCHSPACE_COMPLETE` env var
- The `shell-integration` command currently only installs the `branchspace` shell function for `cd` support
- Users must manually add completion eval lines to their shell rc files

**Scope:**
- `create` command will NOT have dynamic completion (users typically type new branch names)
- Fish shell support will be added to `shell-integration` (currently only bash/zsh)

---

## Implementation Plan

### Part 1: Dynamic Branch/Worktree Completion

#### 1.1 Create `src/branchspace/completion.py`

```python
"""Shell completion helpers for branchspace CLI."""
from click.shell_completion import CompletionItem
from branchspace.git_utils import list_worktrees

class WorktreeBranchComplete:
    """Complete with existing worktree branch names."""
    
    def __call__(self, ctx, param, incomplete):
        try:
            worktrees = list_worktrees()
            return [
                CompletionItem(wt.branch)
                for wt in worktrees
                if wt.branch.startswith(incomplete) and not wt.detached
            ]
        except Exception:
            return []
```

#### 1.2 Modify `src/branchspace/main_cli.py`

- Import `WorktreeBranchComplete` from completion module
- Add `shell_complete=WorktreeBranchComplete()` to `rm` argument
- Add `shell_complete=WorktreeBranchComplete()` to `cd` argument

#### 1.3 Create `tests/test_completion.py`

- Test that `WorktreeBranchComplete` returns worktree branches
- Test filtering by incomplete prefix
- Test graceful handling when not in git repo

---

### Part 2: Auto-Install Completions in Shell Integration

#### 2.1 Update `src/branchspace/shell_integration.py`

**Add Fish detection to `detect_shell_rc_files()`:**
```python
candidates = [
    ShellIntegration("bash", base / ".bashrc"),
    ShellIntegration("zsh", base / ".zshrc"),
    ShellIntegration("fish", base / ".config/fish/config.fish"),
]
```

**Create shell-specific integration builders:**

`build_bash_integration()`:
```bash
# >>> branchspace shell integration >>>
branchspace() {
  if [[ "$1" == "cd" ]]; then
    local target=$(command branchspace cd "${@:2}")
    if [[ -n "$target" ]]; then
      cd "$target"
    fi
  else
    command branchspace "$@"
  fi
}
eval "$(_BRANCHSPACE_COMPLETE=bash_source branchspace)"
# <<< branchspace shell integration <<<
```

`build_zsh_integration()`:
```bash
# >>> branchspace shell integration >>>
branchspace() {
  if [[ "$1" == "cd" ]]; then
    local target=$(command branchspace cd "${@:2}")
    if [[ -n "$target" ]]; then
      cd "$target"
    fi
  else
    command branchspace "$@"
  fi
}
eval "$(_BRANCHSPACE_COMPLETE=zsh_source branchspace)"
# <<< branchspace shell integration <<<
```

`build_fish_integration()`:
```fish
# >>> branchspace shell integration >>>
function branchspace
    if test (count $argv) -gt 0 && test $argv[1] = "cd"
        set target (command branchspace cd $argv[2..])
        if test -n "$target"
            cd $target
        end
    else
        command branchspace $argv
    end
end
_BRANCHSPACE_COMPLETE=fish_source branchspace | source
# <<< branchspace shell integration <<<
```

**Update `build_shell_function()` signature:**
- Accept shell name parameter: `build_shell_function(shell: str) -> str`
- Dispatch to appropriate builder based on shell type

#### 2.2 Update `main_cli.py` shell_integration command

- Pass shell type when calling `build_shell_function(candidate.name)`

#### 2.3 Update tests

- Add fish shell tests to `tests/test_shell_integration.py`
- Test completion snippets are included in output

---

## Files Summary

| File | Action |
|------|--------|
| `src/branchspace/completion.py` | Create |
| `src/branchspace/main_cli.py` | Modify |
| `src/branchspace/shell_integration.py` | Modify |
| `tests/test_completion.py` | Create |
| `tests/test_shell_integration.py` | Modify |
<!-- SECTION:DESCRIPTION:END -->

## Acceptance Criteria
<!-- AC:BEGIN -->
- [ ] #1 Dynamic completion for `rm` command shows existing worktree branches
- [ ] #2 Dynamic completion for `cd` command shows existing worktree branches
- [ ] #3 shell-integration installs bash completion eval in .bashrc
- [ ] #4 shell-integration installs zsh completion eval in .zshrc
- [ ] #5 shell-integration detects and supports fish shell (~/.config/fish/config.fish)
- [ ] #6 shell-integration installs fish completion script
- [ ] #7 All existing tests continue to pass
- [ ] #8 New tests cover completion functionality
<!-- AC:END -->
