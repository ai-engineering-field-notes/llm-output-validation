"""An order-lookup assistant, wired the way many first versions are.

The model writes the SQL and the HTML; the app runs and renders whatever comes back.
"""

import sqlite3


def answer(db: sqlite3.Connection, model_sql: str, model_html: str) -> str:
    rows = db.execute(model_sql).fetchall()
    return f"<div class='answer'>{model_html}</div><p>{len(rows)} rows</p>"
