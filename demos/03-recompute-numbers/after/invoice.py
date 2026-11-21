"""The same intake, with every figure the model returns recomputed or matched against the source text.

The model is good at finding numbers on a page. It is not a calculator, and it can
transpose digits or carry a figure from the wrong line. Arithmetic happens in code.
"""

import re
from decimal import Decimal, InvalidOperation

CENT = Decimal("0.01")
MONEY = re.compile(r"\d{1,3}(?:,\d{3})*(?:\.\d{2})|\d+\.\d{2}")


def money(value) -> Decimal:
    try:
        return Decimal(str(value).replace(",", "").replace("$", "")).quantize(CENT)
    except InvalidOperation:
        raise ValueError(f"not an amount: {value!r}")


def amounts_in(text: str) -> set[Decimal]:
    return {money(m) for m in MONEY.findall(text)}


def check(extraction: dict, source_text: str) -> list[str]:
    problems = []
    printed = amounts_in(source_text)
    lines_sum = Decimal("0")
    for item in extraction["lines"]:
        qty, unit, amount = Decimal(str(item["qty"])), money(item["unit_price"]), money(item["amount"])
        if (qty * unit).quantize(CENT) != amount:
            problems.append(f"{item['description']}: {qty} x {unit} is {(qty * unit).quantize(CENT)}, not {amount}")
        lines_sum += amount
    tax, total = money(extraction["tax"]), money(extraction["total"])
    if lines_sum + tax != total:
        problems.append(f"lines {lines_sum} + tax {tax} = {lines_sum + tax}, model says total {total}")
    for label, value in (("total", total), ("tax", tax)):
        if value not in printed:
            problems.append(f"{label} {value} does not appear in the document")
    return problems


def accept(extraction: dict, source_text: str) -> dict:
    problems = check(extraction, source_text)
    status = "approved" if not problems else "needs_review"
    return {"vendor": extraction["vendor"], "total": money(extraction["total"]), "status": status, "problems": problems}
