"""Answer only when the model agrees with itself; otherwise hand the question to a person.

Ask the same question k times at a non-zero temperature. If the most common answer
holds at least `threshold` of the samples, send it. If not, the model is unsure, and
the question goes to a human queue with the candidate answers attached. Agreement is a
cheap confidence signal that works with any model, including ones that expose no
log-probabilities. Tune the threshold on a labelled set, not by feel.
"""

from collections import Counter


def normalise(answer: str) -> str:
    return " ".join(answer.lower().strip(" .").split())


def respond(samples: list[str], threshold: float = 0.8) -> dict:
    counts = Counter(normalise(s) for s in samples)
    top, n = counts.most_common(1)[0]
    agreement = n / len(samples)
    if agreement >= threshold:
        answer = next(s for s in samples if normalise(s) == top)
        return {"answer": answer, "route": "customer", "agreement": agreement}
    return {"answer": None, "route": "human", "agreement": agreement, "candidates": dict(counts)}


def evaluate(cases, threshold: float = 0.8) -> dict:
    answered = correct = 0
    for samples, gold in cases:
        r = respond(samples, threshold)
        if r["route"] == "customer":
            answered += 1
            correct += normalise(r["answer"]) == normalise(gold)
    return {"coverage": answered / len(cases), "accuracy_when_answered": correct / answered if answered else None,
            "wrong_answers_sent": answered - correct}
