"""The same assistant with the model's output treated as untrusted input.

The model no longer writes SQL. It picks one of a fixed set of queries and fills in
parameters, which are validated and bound. Its text is escaped before it reaches HTML.
"""

import html
import re
import sqlite3

QUERIES = {
    "orders_for_customer": "SELECT id, status, total FROM orders WHERE customer_id = ?",
    "order_status": "SELECT id, status FROM orders WHERE id = ?",
}
ID = re.compile(r"[A-Z]{1,4}-\d{1,8}")


class Rejected(ValueError):
    pass


def answer(db: sqlite3.Connection, plan: dict, model_text: str) -> str:
    sql = QUERIES.get(plan.get("query"))
    if sql is None:
        raise Rejected(f"unknown query {plan.get('query')!r}")
    arg = str(plan.get("arg", ""))
    if not ID.fullmatch(arg):
        raise Rejected(f"argument {arg!r} is not an id")
    rows = db.execute(sql, (arg,)).fetchall()
    return f"<div class='answer'>{html.escape(model_text)}</div><p>{len(rows)} rows</p>"
