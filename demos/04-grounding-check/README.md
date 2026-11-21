# Citations that do not support the claim

## Problem

`before/cite.py` checks that every claim carries a source id and a quote. Models produce citations in the right shape that point at documents that do not exist, quote text that is not in the document, or quote real text that says something different from the claim.

## Business pain

Credibility and legal exposure. In Mata v. Avianca (S.D.N.Y., 2023) lawyers filed a brief with cases ChatGPT had invented and were sanctioned $5,000; the citations looked real.

## Fix

`after/cite.py` runs three deterministic checks per claim: the source exists, the quote appears in it after normalising whitespace, case and quote marks, and every number in the claim also appears in the quote. A failed claim is removed or sent for review, never shown with its citation.

This proves a quote is real, not that it entails the claim. For that, add an entailment check (a second model or an NLI classifier) on top; the cheap checks remove the worst failures first and for free.

## Proof

```
uv run pytest demos/04-grounding-check
```

Before: all four claims pass. After: only the supported claim passes; the invented source, the invented quote and the changed number are each named.
