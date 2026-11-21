"""Nightly job: ask the model for a ticket summary as JSON and store it."""

import json


def extract(ask, ticket: str, store: list) -> None:
    try:
        data = json.loads(ask(ticket))
        store.append({"ticket": ticket, "priority": data.get("priority"), "summary": data.get("summary")})
    except Exception:
        pass  # bad JSON: skip it, the job must not crash
