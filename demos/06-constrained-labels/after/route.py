"""The same router with a closed set of labels and an explicit way to say "none of these".

The model must return exactly one value from Label (enforce it with your provider's
structured-output or enum mode where you can). Anything else is not guessed at: it goes
to a review queue and is counted, so drift shows up as a number instead of as misroutes.
"""

from collections import Counter
from enum import Enum


class Label(str, Enum):
    BILLING = "billing"
    TECHNICAL = "technical"
    ACCOUNT = "account"
    UNCLEAR = "unclear"  # the reject class: the model is allowed to say none of these fit


QUEUES = {Label.BILLING: "billing-team", Label.TECHNICAL: "support-l2", Label.ACCOUNT: "account-team",
          Label.UNCLEAR: "triage-review"}

drift = Counter()


def route(label: str) -> str:
    try:
        return QUEUES[Label(label.strip().lower())]  # case and spacing are formatting, not meaning
    except ValueError:
        drift[label] += 1
        return QUEUES[Label.UNCLEAR]
