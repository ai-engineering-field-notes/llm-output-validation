# Structured output that breaks the parser

## Problem

`before/extract.py` asks for JSON and calls `json.loads`. Real replies arrive wrapped in code fences, with trailing commas, with enum values the prompt did not allow, or with fields missing. The job catches the exception and moves on, so failures disappear, and anything that parses is stored whether or not it is valid.

## Business pain

Pipelines that fail silently overnight: missing records nobody notices until a report is wrong, and bad values that break whatever reads the table next.

## Fix

`after/extract.py` validates every reply against a Pydantic schema (allowed enum values, lengths, id pattern). On failure it retries with the validation error in the prompt, at most three attempts, then writes the ticket and every error to a dead-letter list instead of dropping it. Code fences are stripped before parsing because that is formatting, not content.

Provider-side structured output modes reduce malformed JSON but do not check business rules such as an id format, so the schema check stays.

## Proof

```
uv run pytest demos/02-schema-retries
```

Before: of four realistic bad replies, two vanish and two are stored, one with priority `P1`. After: the fenced reply is accepted, a bad-then-good sequence succeeds on the third call with the error fed back, and a reply that never validates stops after three calls and lands in the dead-letter list.
