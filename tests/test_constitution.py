"""Constitution + policy engine enforcement."""

import pytest

from ai_os_kernel import Constitution, PolicyEngine
from ai_os_kernel.constitution import PolicyViolation


def test_seven_principles():
    c = Constitution()
    assert len(c.principles) == 7


def test_cost_violation_raises():
    eng = PolicyEngine()
    with pytest.raises(PolicyViolation) as exc:
        eng.check_cost(estimated_usd=2.0, budget_usd=1.0)
    assert exc.value.principle_number == 3


def test_cost_ok_no_raise():
    eng = PolicyEngine()
    eng.check_cost(estimated_usd=0.5, budget_usd=1.0)  # no exception


def test_approval_required():
    eng = PolicyEngine(require_approval=True)
    with pytest.raises(PolicyViolation) as exc:
        eng.approve_if_needed("delete client sandbox")
    assert exc.value.principle_number == 4


def test_approval_bypassed_when_disabled():
    eng = PolicyEngine(require_approval=False)
    eng.approve_if_needed("delete client sandbox")  # no exception


def test_source_provenance_required():
    eng = PolicyEngine()
    with pytest.raises(PolicyViolation):
        eng.check_source_provided(has_source=False)
    eng.check_source_provided(has_source=True)  # no exception


def test_run_thresholds_reports_not_raises():
    eng = PolicyEngine()
    problems = eng.run_thresholds("wf", estimated_usd=5.0, budget_usd=1.0)
    assert problems  # non-empty
    assert eng.violations == problems
    # within budget -> clean
    assert eng.run_thresholds("wf", estimated_usd=0.5, budget_usd=1.0) == []
