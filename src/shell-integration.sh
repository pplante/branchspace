#!/usr/bin/env sh
# branchspace shell integration
#
# Add this to your ~/.bashrc or ~/.zshrc:
#   source /path/to/shell-integration.sh
#
# This wrapper enables the 'branchspace cd' command to change directories
# in your current shell session and provides shell completion.

# Mark that shell integration is loaded
export _BRANCHSPACE_SHELL_INTEGRATION=1

branchspace() {
  if [[ "$1" == "cd" ]]; then
    local target=$(command branchspace cd --print-path "$2")
    if [[ -n "$target" ]]; then
      cd "$target" || return 1
    fi
  else
    command branchspace "$@"
  fi
}

# Shell completion setup
if [[ -n "$BASH_VERSION" ]]; then
  # Bash completion
  eval "$(_BRANCHSPACE_COMPLETE=bash_source branchspace)"
elif [[ -n "$ZSH_VERSION" ]]; then
  # Zsh completion
  eval "$(_BRANCHSPACE_COMPLETE=zsh_source branchspace)"
fi
