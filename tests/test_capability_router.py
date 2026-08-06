"""Capability routing: cheapest capable provider wins; no provider -> no route."""

from ai_os_kernel import CapabilityRouter, TaskSpec


def test_route_long_context_picks_cheapest(manifests):
    router = CapabilityRouter(manifests)
    res = router.route(TaskSpec(required_capabilities=["long_context"]))
    assert res.success
    # local has no long_context; cheapest capable is gemini (0.000002 input)
    assert res.provider.provider == "gemini"


def test_route_vision_prefers_gemini_when_cheap(manifests):
    router = CapabilityRouter(manifests)
    res = router.route(TaskSpec(required_capabilities=["vision"]))
    assert res.success
    # gemini supports vision at lowest cost
    assert res.provider.provider == "gemini"


def test_route_browser(manifests):
    router = CapabilityRouter(manifests)
    res = router.route(TaskSpec(required_capabilities=["browser"]))
    assert res.success
    assert res.provider.provider == "grok"


def test_route_prefer_local(manifests):
    router = CapabilityRouter(manifests)
    # json_mode: local supports it, but is it viable? prefer_local forces local.
    res = router.route(TaskSpec(required_capabilities=["json_mode"], prefer_local=True))
    assert res.success
    assert res.provider.provider == "local"


def test_route_impossible(manifests):
    router = CapabilityRouter(manifests)
    res = router.route(TaskSpec(required_capabilities=["video_generation", "browser"]))
    assert not res.success
    assert res.reason


def test_route_respects_exclusions(manifests):
    router = CapabilityRouter(manifests)
    res = router.route(
        TaskSpec(required_capabilities=["long_context"], exclude=["gemini"])
    )
    assert res.success and res.provider.provider != "gemini"


def test_route_budget_gate(manifests):
    router = CapabilityRouter(manifests)
    # zero budget excludes every cloud provider; only local (free) remains,
    # but local lacks long_context -> no route.
    res = router.route(TaskSpec(required_capabilities=["long_context"], max_budget_usd=0.0))
    assert not res.success


def test_route_json_mode_default(manifests):
    router = CapabilityRouter(manifests)
    res = router.route(TaskSpec(required_capabilities=["json_mode"]))
    assert res.success
    # all four support json_mode; cheapest input is local (0) -> would win,
    # but local lacks... nothing extra required, so cheapest = local.
    assert res.provider.provider == "local"
