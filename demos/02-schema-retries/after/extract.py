"""The same job with a schema, bounded retries that show the model its error, and a dead-letter list."""

import json
import re
from typing import Literal

from pydantic import BaseModel, Field, ValidationError


class TicketSummary(BaseModel):
    priority: Literal["low", "medium", "high", "urgent"]
    summary: str = Field(min_length=10, max_length=280)
    customer_id: str = Field(pattern=r"^C-\d+$")


FENCE = re.compile(r"^```(?:json)?\s*|\s*```$")


def extract(ask, ticket: str, store: list, dead_letter: list, max_attempts: int = 3) -> TicketSummary | None:
    prompt, errors = ticket, []
    for _ in range(max_attempts):
        raw = FENCE.sub("", ask(prompt).strip())
        try:
            result = TicketSummary.model_validate(json.loads(raw))
            store.append({"ticket": ticket, **result.model_dump()})
            return result
        except (json.JSONDecodeError, ValidationError) as e:
            errors.append(str(e).splitlines()[0])
            prompt = f"{ticket}\n\nYour last reply was rejected: {e}\nReturn only JSON matching the schema."
    dead_letter.append({"ticket": ticket, "errors": errors})
    return None
