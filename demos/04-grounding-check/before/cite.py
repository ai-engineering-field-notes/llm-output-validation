"""A research assistant returns claims, each with a source id and a supporting quote.

The check that ships first: every claim has a citation in the right shape.
"""


def verify(answer: list[dict], sources: dict[str, str]) -> list[str]:
    return [f"claim {i} has no citation" for i, c in enumerate(answer) if not c.get("source") or not c.get("quote")]
