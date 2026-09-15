from datetime import date
from decimal import Decimal

from pydantic import BaseModel

class TransactionCreate(BaseModel):
    description: str
    amount: Decimal
    category: str | None = None
    date: date
    transaction_type: str="expense"

class TransactionUpdate(BaseModel):
    description: str
    amount: Decimal
    category: str
    date: date
    transaction_type: str="expense"