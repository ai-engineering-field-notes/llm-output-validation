"""An invoice and three extractions of it: correct, a transposed total, and a misread line."""

from decimal import Decimal
from pathlib import Path

DEMO = Path(__file__).parents[1]

INVOICE = """Northwind Supply  Invoice 4471
Widget A    10 x 45.00     450.00
Widget B     4 x 187.50    750.00
Subtotal                 1,200.00
Tax                         54.00
Total due                1,254.00
"""

CORRECT = {
    "vendor": "Northwind Supply",
    "lines": [
        {"description": "Widget A", "qty": 10, "unit_price": "45.00", "amount": "450.00"},
        {"description": "Widget B", "qty": 4, "unit_price": "187.50", "amount": "750.00"},
    ],
    "tax": "54.00",
    "total": "1254.00",
}
TRANSPOSED = {**CORRECT, "total": "1245.00"}
MISREAD_LINE = {
    **CORRECT,
    "lines": [CORRECT["lines"][0], {"description": "Widget B", "qty": 4, "unit_price": "187.50", "amount": "570.00"}],
    "total": "1074.00",
}


def test_before_approves_a_transposed_total(load):
    before = load(DEMO / "before" / "invoice.py", "before_invoice")
    assert before.accept(TRANSPOSED) == {"vendor": "Northwind Supply", "total": 1245.0, "status": "approved"}
    assert before.accept(MISREAD_LINE)["status"] == "approved"


def test_after_approves_the_correct_extraction(load):
    after = load(DEMO / "after" / "invoice.py", "after_invoice")
    result = after.accept(CORRECT, INVOICE)
    assert result["status"] == "approved" and result["total"] == Decimal("1254.00")


def test_after_catches_the_transposed_total(load):
    after = load(DEMO / "after" / "invoice.py", "after_invoice")
    result = after.accept(TRANSPOSED, INVOICE)
    assert result["status"] == "needs_review"
    assert "lines 1200.00 + tax 54.00 = 1254.00, model says total 1245.00" in result["problems"]
    assert "total 1245.00 does not appear in the document" in result["problems"]


def test_after_catches_a_misread_line_even_when_the_sum_is_consistent(load):
    after = load(DEMO / "after" / "invoice.py", "after_invoice")
    result = after.accept(MISREAD_LINE, INVOICE)
    assert result["status"] == "needs_review"
    assert result["problems"][0] == "Widget B: 4 x 187.50 is 750.00, not 570.00"
