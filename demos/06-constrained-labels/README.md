# Label drift in classifiers

## Problem

`before/route.py` routes tickets by checking whether the model's label contains a queue name. Over time the model returns `Refund request`, `Login problem`, `Technical (billing page error)`. Synonyms fall through to a default queue; labels that mention two queues go to whichever is checked first.

## Business pain

Tickets and documents land with the wrong team. Nobody sees an error, only slower resolution and customers asking twice.

## Fix

`after/route.py` defines a closed set of labels, including `unclear`, an explicit reject class the model may use when nothing fits. Only an exact match routes, after lowercasing and trimming. Anything else goes to a review queue and is counted, so drift becomes a number on a dashboard instead of misrouted work. Use the provider's enum or structured-output mode to make out-of-set labels rare, and keep the check because the mode is not the only path labels arrive by.

## Proof

```
uv run pytest demos/06-constrained-labels
```

Ten labels a drifting model produced, each with the right queue. Before: four of ten are wrong, three silently sent to `general` and one to the wrong team. After: no ticket reaches a wrong team. Five labels route (an exact match after lowercasing), and the five drifted ones go to review and are counted. The price is review volume: two of those five were labels the old router happened to get right.
