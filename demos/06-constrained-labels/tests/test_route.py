"""Labels collected from a classifier prompt over time: the model's wording drifts.

Each case is (what the model returned, the queue a human said was right)."""

from pathlib import Path

DEMO = Path(__file__).parents[1]

CASES = [
    ("billing", "billing-team"),
    ("technical", "support-l2"),
    ("account", "account-team"),
    ("Billing", "billing-team"),
    ("Refund request", "billing-team"),          # synonym, no keyword
    ("Payment / billing", "billing-team"),
    ("Login problem", "account-team"),           # synonym, no keyword
    ("Account-billing", "billing-team"),          # two keywords, dict order decides
    ("Technical (billing page error)", "support-l2"),
    ("unclear", "triage-review"),
]


def test_before_misroutes_silently(load):
    before = load(DEMO / "before" / "route.py", "before_route")
    wrong = [(label, before.route(label), right) for label, right in CASES if before.route(label) != right]
    assert wrong == [
        ("Refund request", "general", "billing-team"),
        ("Login problem", "general", "account-team"),
        ("Technical (billing page error)", "billing-team", "support-l2"),
        ("unclear", "general", "triage-review"),
    ]


def test_after_never_guesses(load):
    after = load(DEMO / "after" / "route.py", "after_route")
    after.drift.clear()
    routed = {label: after.route(label) for label, _ in CASES}
    exact = [label for label, right in CASES if routed[label] == right]
    assert exact == ["billing", "technical", "account", "Billing", "unclear"]
    # Everything else went to review rather than to a wrong team, and was counted.
    assert all(routed[label] == "triage-review" for label, _ in CASES if label not in exact)
    assert sum(after.drift.values()) == 5
