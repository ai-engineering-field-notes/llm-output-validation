"""Four claims: one supported, one citing a source that does not exist, one with an invented quote,
and one that quotes the source correctly but changes the number."""

from pathlib import Path

DEMO = Path(__file__).parents[1]

SOURCES = {
    "policy-2026": "Refunds are issued within 14 days of an approved return. "
    "Items must be returned within 30 days of delivery.",
    "faq": "Shipping to Canada takes 5 to 7 business days.",
}

ANSWER = [
    {"claim": "Refunds go out within 14 days of an approved return.", "source": "policy-2026",
     "quote": "Refunds are issued within 14 days of an approved return."},
    {"claim": "Opened items cannot be returned.", "source": "policy-2025",
     "quote": "Opened items are not eligible for return."},
    {"claim": "Returns are free for members.", "source": "faq",
     "quote": "Members receive free return shipping."},
    {"claim": "You have 60 days to return an item.", "source": "policy-2026",
     "quote": "Items must be returned within 30 days of delivery."},
]


def test_before_every_claim_passes_because_every_claim_has_a_citation(load):
    before = load(DEMO / "before" / "cite.py", "before_cite")
    assert before.verify(ANSWER, SOURCES) == []


def test_after_only_the_supported_claim_passes(load):
    after = load(DEMO / "after" / "cite.py", "after_cite")
    assert after.verify(ANSWER, SOURCES) == [
        "claim 1: source 'policy-2025' does not exist",
        "claim 2: quote not found in faq",
        "claim 3: 60 not in the quote",
    ]


def test_after_tolerates_formatting_differences(load):
    after = load(DEMO / "after" / "cite.py", "after_cite")
    reformatted = [{**ANSWER[0], "quote": "refunds are issued  within 14 days\nof an approved return."}]
    assert after.verify(reformatted, SOURCES) == []
