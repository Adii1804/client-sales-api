from pydantic import BaseModel
from datetime import date
from decimal import Decimal
from typing import Any

class SalesReceiptResponse(BaseModel):
    receipt_id: str
    customer_mobile: str | None
    trans_date: date
    store: str
    payment_amount: Decimal
    items: Any
