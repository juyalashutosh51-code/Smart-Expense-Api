from decimal import Decimal

from pydantic import BaseModel


class BudgetCreate(BaseModel):
    category: str
    amount: Decimal
    month: int
    year: int
    