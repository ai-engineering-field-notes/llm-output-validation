# Treat model output as untrusted input

## Problem

`before/app.py` lets the model write the SQL and the HTML, then runs and renders whatever comes back. Anyone who can influence the model's input (a customer message, a document, a web page) can influence that output. OWASP lists this as LLM05:2025, Improper Output Handling.

## Business pain

Injection through the model rather than the user: other customers' records, stolen sessions, and in the worst published cases remote code execution (CVE-2024-5565 in Vanna.AI ran model-written Python through `exec`).

## Fix

`after/app.py` moves the decision out of the model. The model picks one of a fixed set of named queries and supplies a parameter; the app validates the parameter against a pattern and binds it. The model's prose is HTML-escaped before rendering. No string the model writes is executed or rendered as markup.

## Proof

```
uv run pytest demos/01-output-is-input
```

`tests/test_app.py` feeds both versions the output an injected model would produce. Before: customer C-1 gets customer C-2's order back and the page carries an `onerror` script. After: both payloads are rejected or escaped, and a normal lookup still returns its row.
