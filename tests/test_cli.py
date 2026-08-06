"""CLI command coverage: every command runs and exits cleanly."""

import pytest
from ai_os_kernel import cli


@pytest.mark.parametrize(
    "args",
    [
        ["capabilities"],
        ["route", "long_context"],
        ["route", "browser"],
        ["souls", "main", "cdl-expert"],
        ["vertical"],
        ["adapters"],
        ["chat", "hello"],
    ],
    ids=["capabilities", "route-lc", "route-browser", "souls", "vertical", "adapters", "chat"],
)
def test_cli_commands_run(args, capsys, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    assert cli.main(args) == 0
    out = capsys.readouterr().out
    assert out.strip()  # produced some output


def test_cli_chat_offline_echoes(capsys, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    cli.main(["chat", "hello world"])
    out = capsys.readouterr().out
    assert "[offline-demo]" in out


def test_cli_pipeline_uses_offline(monkeypatch, tmp_path, capsys):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)

    # Stub run_pipeline to avoid touching git/repo during the test.
    def fake_run(task, souls=None, **kwargs):
        return {
            "provider": "offline",
            "model": "offline-demo",
            "task": task,
            "markdown": "knowledge/output/x.md",
            "cost_usd": 0.0,
            "latency_ms": 0.0,
            "artifact_id": "abc",
            "graph_order": [],
            "souls": souls or [],
            "run_id": 1,
            "git_committed": False,
        }

    monkeypatch.setattr("ai_os_kernel.pipeline.run_pipeline", fake_run)
    assert cli.main(["pipeline", "test task"]) == 0
    out = capsys.readouterr().out
    assert "provider" in out


def test_cli_unknown_command():
    assert cli.main(["nope"]) == 2


def test_cli_help():
    assert cli.main(["--help"]) == 0
