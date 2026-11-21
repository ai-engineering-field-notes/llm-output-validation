"""Check that each citation exists and that the quote is really in it and really carries the claim.

Three checks, all deterministic and cheap:
1. The cited source exists.
2. The quote appears in that source (after normalising whitespace, case and quote marks).
3. Every number in the claim appears in the quote, so a real quote cannot back an altered figure.
"""

import re

NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?%?")


def normalise(text: str) -> str:
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip().lower()


def verify(answer: list[dict], sources: dict[str, str]) -> list[str]:
    problems = []
    for i, c in enumerate(answer):
        source, quote, claim = c.get("source"), c.get("quote", ""), c.get("claim", "")
        if source not in sources:
            problems.append(f"claim {i}: source {source!r} does not exist")
            continue
        if not quote or normalise(quote) not in normalise(sources[source]):
            problems.append(f"claim {i}: quote not found in {source}")
            continue
        missing = [n for n in NUMBER.findall(claim) if n not in quote]
        if missing:
            problems.append(f"claim {i}: {', '.join(missing)} not in the quote")
    return problems
