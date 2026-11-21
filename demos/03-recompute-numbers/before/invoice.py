"""Accounts-payable intake: the model reads an invoice and returns line items and a total."""


def accept(extraction: dict) -> dict:
    return {"vendor": extraction["vendor"], "total": float(extraction["total"]), "status": "approved"}
