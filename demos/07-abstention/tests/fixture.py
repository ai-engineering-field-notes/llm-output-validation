"""A labelled fixture written for this demo, not a benchmark of any model.

Twenty questions, each with five sampled answers and the correct answer. It reproduces the
pattern the technique relies on: when a model knows, its samples agree; when it is guessing,
they scatter. Two cases break the pattern on purpose (consistently wrong), because
agreement cannot catch those.
"""

R = "Refunds take 14 days"
W = "Refunds take 7 days"

CASES = (
    # 12 questions the model knows: all five samples agree and are right
    [([f"answer {i}"] * 5, f"answer {i}") for i in range(12)]
    # 2 known, with one stray sample (4 of 5 agree, right)
    + [([R, R, R, R, W], R), (["30 days", "30 days", "30 days", "30 days", "60 days"], "30 days")]
    # 4 guesses: samples scatter and the first sample is wrong
    + [(["Yes", "No", "No", "Yes", "Only for members"], "Only for members"),
       (["5 days", "7 days", "10 days", "5 days", "3 days"], "7 days"),
       (["Visa only", "All cards", "Visa and Mastercard", "All cards", "Visa only"], "Visa and Mastercard"),
       (["Ontario", "Quebec", "All provinces", "Ontario", "BC"], "All provinces")]
    # 2 consistently wrong: all samples agree on a wrong answer
    + [([W] * 5, R), (["No fee"] * 5, "A $25 fee")]
)
