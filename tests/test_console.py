"""Tests for Rich console utilities."""

from __future__ import annotations

from rich.console import Console

from branchspace.console import build_worktree_table
from branchspace.console import error
from branchspace.console import get_console
from branchspace.console import info
from branchspace.console import spinner
from branchspace.console import success
from branchspace.console import warning


def test_console_singleton():
    console = get_console()

    assert isinstance(console, Console)
    assert console is get_console()


def test_success_warning_error_info_messages(monkeypatch):
    messages: list[str] = []

    def fake_print(value: str) -> None:
        messages.append(value)

    console = get_console()
    monkeypatch.setattr(console, "print", fake_print)

    success("ok")
    warning("heads up")
    error("nope")
    info("fyi")

    assert "ok" in messages[0]
    assert "heads up" in messages[1]
    assert "nope" in messages[2]
    assert "fyi" in messages[3]


def test_build_worktree_table():
    table = build_worktree_table()

    assert table.title == "Worktrees"
    assert [column.header for column in table.columns] == ["Path", "Branch", "Status"]


def test_spinner_context_manager(monkeypatch):
    started: list[bool] = []
    stopped: list[bool] = []

    class DummyStatus:
        def start(self) -> None:
            started.append(True)

        def stop(self) -> None:
            stopped.append(True)

    def fake_status(message: str, spinner: str) -> DummyStatus:
        assert "Working" in message
        assert spinner == "dots"
        return DummyStatus()

    console = get_console()
    monkeypatch.setattr(console, "status", fake_status)

    with spinner("Working"):
        pass

    assert started == [True]
    assert stopped == [True]
