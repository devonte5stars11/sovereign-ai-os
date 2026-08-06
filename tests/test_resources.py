"""Resource budgets and recovery policies."""

from ai_os_kernel import RecoveryPolicy, ResourceBudget


def test_default_budget():
    b = ResourceBudget()
    assert b.max_retries == 2
    assert b.max_parallel_workers == 5


def test_budget_roundtrip():
    b = ResourceBudget(budget_usd=0.75, time_seconds=900, max_tokens=300_000, max_retries=1)
    assert ResourceBudget.from_dict(b.to_dict()).to_dict() == b.to_dict()


def test_recovery_policy_default():
    r = RecoveryPolicy()
    assert r.ask_human_on_exhaustion is True


def test_recovery_chain():
    r = RecoveryPolicy(
        fallbacks=["gemini", "local_rag", "cached_summary"],
        ask_human_on_exhaustion=True,
    )
    d = r.to_dict()
    assert d["fallbacks"][0] == "gemini"
    assert RecoveryPolicy.from_dict(d).fallbacks == r.fallbacks
