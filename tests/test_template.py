"""Tests for template substitution utilities."""

from __future__ import annotations

import pytest

from branchspace.template import TemplateVariableError
from branchspace.template import substitute_template


class TestSubstituteTemplate:
    """Tests for substitute_template."""

    def test_substitutes_all_variables(self):
        template = "$BASE_PATH/$BRANCH_NAME from $SOURCE_BRANCH at $WORKTREE_PATH"
        variables = {
            "BASE_PATH": "myproject",
            "BRANCH_NAME": "feature-auth",
            "SOURCE_BRANCH": "main",
            "WORKTREE_PATH": "/repo/worktrees/feature-auth",
        }

        result = substitute_template(template, variables)

        assert result == "myproject/feature-auth from main at /repo/worktrees/feature-auth"

    def test_substitutes_list_items(self):
        template = [
            "echo $BASE_PATH",
            "cd $WORKTREE_PATH",
            "git checkout $BRANCH_NAME",
        ]
        variables = {
            "$BASE_PATH": "myproject",
            "$WORKTREE_PATH": "/repo/worktrees/feature-auth",
            "$BRANCH_NAME": "feature-auth",
        }

        result = substitute_template(template, variables)

        assert result == [
            "echo myproject",
            "cd /repo/worktrees/feature-auth",
            "git checkout feature-auth",
        ]

    def test_missing_variable_raises_by_default(self):
        template = "use $BASE_PATH and $SOURCE_BRANCH"
        variables = {"BASE_PATH": "myproject"}

        with pytest.raises(TemplateVariableError):
            substitute_template(template, variables)

    def test_unknown_variable_raises(self):
        template = "use $UNKNOWN_VAR"
        variables = {"BASE_PATH": "myproject"}

        with pytest.raises(TemplateVariableError):
            substitute_template(template, variables)

    def test_missing_variable_can_be_left_intact(self):
        template = "use $BASE_PATH and $SOURCE_BRANCH"
        variables = {"BASE_PATH": "myproject"}

        result = substitute_template(template, variables, strict=False)

        assert result == "use myproject and $SOURCE_BRANCH"
