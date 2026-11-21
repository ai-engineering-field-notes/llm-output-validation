from pathlib import Path

DEMO = Path(__file__).parents[1]


def fixture(load):
    return load(DEMO / "tests" / "fixture.py", "abstention_fixture").CASES


def test_before_every_answer_goes_to_the_customer(load):
    before = load(DEMO / "before" / "assistant.py", "before_assistant")
    cases = fixture(load)
    sent_wrong = sum(before.respond(s)["answer"] != gold for s, gold in cases)
    assert len(cases) == 20 and sent_wrong == 6  # 4 guesses + 2 consistent errors


def test_after_guesses_go_to_a_human(load):
    after = load(DEMO / "after" / "assistant.py", "after_assistant")
    result = after.evaluate(fixture(load), threshold=0.8)
    assert result == {"coverage": 0.8, "accuracy_when_answered": 0.875, "wrong_answers_sent": 2}


def test_after_the_threshold_is_a_trade_off(load):
    after = load(DEMO / "after" / "assistant.py", "after_assistant")
    cases = fixture(load)
    strict = after.evaluate(cases, threshold=1.0)
    assert strict["coverage"] == 0.7 and strict["wrong_answers_sent"] == 2  # more to humans, same 2 errors
    loose = after.evaluate(cases, threshold=0.4)
    assert loose["wrong_answers_sent"] > 2


def test_after_low_agreement_carries_the_candidates(load):
    after = load(DEMO / "after" / "assistant.py", "after_assistant")
    r = after.respond(["5 days", "7 days", "10 days", "5 days", "3 days"])
    assert r["route"] == "human" and r["agreement"] == 0.4 and r["candidates"]["5 days"] == 2
