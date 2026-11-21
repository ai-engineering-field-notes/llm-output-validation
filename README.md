# llm-output-validation

Treating model output as untrusted input. Seven demos, each a common way model output breaks the system that consumes it, and a fix you can copy, with a test that shows the failure and the fix.

Part of [AI Engineering Field Notes](https://github.com/ai-engineering-field-notes). Written from scratch for teaching; nothing here comes from an employer or client.

## Run the proof

```
uv run pytest
```

Runs on Linux, macOS and Windows with Python 3.11 or newer. No network, model or API key needed: each test replays the model replies that cause the failure, so the results are the same on every run.

## Demos

| # | Problem | Fix |
| --- | --- | --- |
| [01](demos/01-output-is-input) | Model output flows into SQL and HTML unchecked (OWASP LLM05) | Named queries with bound parameters, escaped text |
| [02](demos/02-schema-retries) | Structured output breaks the parser and failures vanish | Schema validation, bounded retries with the error, a dead-letter list |
| [03](demos/03-recompute-numbers) | Plausible but wrong extracted numbers | Recompute every figure and match it against the source |
| [04](demos/04-grounding-check) | Citations that do not support the claim | Check the source exists, the quote is in it and the numbers match |
| [05](demos/05-safe-markdown) | Model-written links and images phish and leak data | Host allowlists and render-safe markdown |
| [06](demos/06-constrained-labels) | Classifier labels drift and tickets misroute | A closed label set with an explicit reject class |
| [07](demos/07-abstention) | Confidently wrong answers | Self-consistency with a threshold that routes to a human |

## Layout

```
demos/<nn>-<name>/
  README.md    problem, business pain, fix, proof
  before/      the failure, reproduced
  after/       the fix
  tests/       shows the failure against before/ and the fix holding against after/
```

## How this was made

The code and tests were written with Claude and reviewed by hand. Every number in the READMEs comes from these tests or from the cited source.

## Licence

MIT
