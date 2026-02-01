"""Template variable substitution utilities."""

from __future__ import annotations

import re

from collections.abc import Mapping
from typing import overload


class TemplateVariableError(ValueError):
    """Raised when a required template variable is missing."""


_VARIABLE_PATTERN = re.compile(r"\$(BASE_PATH|WORKTREE_PATH|BRANCH_NAME|SOURCE_BRANCH)")


def normalize_template_variables(variables: Mapping[str, str]) -> dict[str, str]:
    """Normalize template variable keys to bare names.

    Accepts keys with or without the leading '$'.
    """
    normalized: dict[str, str] = {}
    for key, value in variables.items():
        name = key[1:] if key.startswith("$") else key
        normalized[name] = value
    return normalized


def _substitute_string(template: str, variables: Mapping[str, str], strict: bool) -> str:
    def replace(match: re.Match[str]) -> str:
        name = match.group(1)
        if name not in variables:
            if strict:
                raise TemplateVariableError(f"Missing template variable: {name}")
            return match.group(0)
        return variables[name]

    return _VARIABLE_PATTERN.sub(replace, template)


@overload
def substitute_template(
    value: str,
    variables: Mapping[str, str],
    *,
    strict: bool = True,
) -> str: ...


@overload
def substitute_template(
    value: list[str],
    variables: Mapping[str, str],
    *,
    strict: bool = True,
) -> list[str]: ...


def substitute_template(
    value: str | list[str],
    variables: Mapping[str, str],
    *,
    strict: bool = True,
) -> str | list[str]:
    """Substitute template variables in a string or list of strings."""
    normalized = normalize_template_variables(variables)

    if isinstance(value, str):
        return _substitute_string(value, normalized, strict)

    if not isinstance(value, list):
        raise TypeError("Template value must be a string or list of strings")

    substituted: list[str] = []
    for item in value:
        if not isinstance(item, str):
            raise TypeError("Template list items must be strings")
        substituted.append(_substitute_string(item, normalized, strict))

    return substituted
