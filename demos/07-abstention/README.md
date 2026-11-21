# Confidently wrong answers

## Problem

`before/assistant.py` asks the model once and sends the answer. A model that is guessing sounds exactly as sure as one that knows, so the customer cannot tell the difference and neither can the app.

## Business pain

Bad answers delivered with full confidence, and the company owns them: in Moffatt v. Air Canada (2024 BCCRT 149) a tribunal held the airline liable for its chatbot's wrong bereavement-fare answer and rejected the argument that the chatbot was responsible for itself.

## Fix

`after/assistant.py` samples the same question five times. If at least 80% of samples agree, the answer goes out; otherwise the question goes to a person with the candidate answers attached. Agreement is a confidence signal that needs no log-probabilities and works with any model. The threshold is tuned on a labelled set.

It costs k calls per question, so use it where a wrong answer is expensive, or sample only when a first cheap check is unsure. It cannot catch an answer the model gets wrong consistently; retrieval and grounding checks cover those.

## Proof

```
uv run pytest demos/07-abstention
```

On a 20-question labelled fixture written for this demo (not a model benchmark): before, 6 wrong answers reach customers. After, at an 80% threshold, 16 questions are answered, 14 of them correctly, and the 4 guesses go to a human; the 2 consistent errors still get through. At 100% the coverage drops to 70% with the same 2 errors, and at 40% more wrong answers go out.
