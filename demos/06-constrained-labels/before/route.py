"""Ticket router: the prompt lists the queues, the model answers with a queue name."""

QUEUES = {"billing": "billing-team", "technical": "support-l2", "account": "account-team"}


def route(label: str) -> str:
    key = label.strip().lower()
    for name, queue in QUEUES.items():
        if name in key:
            return queue
    return "general"
