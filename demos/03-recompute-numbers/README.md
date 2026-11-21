# Plausible but wrong numbers

## Problem

`before/invoice.py` takes the total the model extracted from an invoice and approves it. Extraction models misread and transpose digits, and the result looks exactly as plausible as a right answer: 1,245.00 instead of 1,254.00.

## Business pain

Wrong figures reach the ledger, the report or the customer, and are found at reconciliation, if at all.

## Fix

`after/invoice.py` never trusts a figure it can check. Line amounts are recomputed from quantity and unit price, lines plus tax must equal the total, and the total and tax must appear verbatim in the source text. All arithmetic is in `Decimal`. Any mismatch routes the invoice to review with the reason.

## Proof

```
uv run pytest demos/03-recompute-numbers
```

Before: a transposed total and a misread line are both approved. After: the correct extraction is approved; the transposed total fails two checks; the misread line fails the line check even though the model made its sum and total agree with each other.
