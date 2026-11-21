"""Support assistant: ask the model once, return what it says."""


def respond(samples: list[str]) -> dict:
    return {"answer": samples[0], "route": "customer"}
