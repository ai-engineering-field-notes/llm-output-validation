"""Replays of model replies that break a JSON pipeline in practice."""

from pathlib import Path

DEMO = Path(__file__).parents[1]

GOOD = '{"priority": "high", "summary": "Card charged twice for order O-1", "customer_id": "C-17"}'
FENCED = "```json\n" + GOOD + "\n```"
TRAILING_COMMA = '{"priority": "high", "summary": "Card charged twice for order O-1", "customer_id": "C-17",}'
WRONG_ENUM = '{"priority": "P1", "summary": "Card charged twice for order O-1", "customer_id": "C-17"}'
MISSING = '{"priority": "high", "summary": "Card charged twice"}'


def replay(*replies):
    it = iter(replies)
    calls = []

    def ask(prompt):
        calls.append(prompt)
        return next(it)

    ask.calls = calls
    return ask


def test_before_bad_replies_vanish_or_store_garbage(load):
    before = load(DEMO / "before" / "extract.py", "before_extract")
    store = []
    for reply in (FENCED, TRAILING_COMMA, WRONG_ENUM, MISSING):
        before.extract(replay(reply), "ticket", store)
    # Two tickets silently dropped; of the two stored, one has a priority nothing downstream knows.
    assert len(store) == 2
    assert store[0]["priority"] == "P1"


def test_after_fenced_json_is_accepted(load):
    after = load(DEMO / "after" / "extract.py", "after_extract")
    store, dead = [], []
    assert after.extract(replay(FENCED), "ticket", store, dead).priority == "high"


def test_after_retries_with_the_error_then_succeeds(load):
    after = load(DEMO / "after" / "extract.py", "after_extract")
    store, dead = [], []
    ask = replay(TRAILING_COMMA, WRONG_ENUM, GOOD)
    assert after.extract(ask, "ticket", store, dead) is not None
    assert len(ask.calls) == 3 and "rejected" in ask.calls[1]
    assert len(store) == 1 and not dead


def test_after_gives_up_loudly(load):
    after = load(DEMO / "after" / "extract.py", "after_extract")
    store, dead = [], []
    ask = replay(MISSING, MISSING, MISSING, GOOD)
    assert after.extract(ask, "ticket", store, dead) is None
    assert len(ask.calls) == 3  # bounded: the fourth reply is never requested
    assert not store and len(dead) == 1 and len(dead[0]["errors"]) == 3
