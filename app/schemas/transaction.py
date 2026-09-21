from datetime import date
from decimal import Decimal
from typing import Literal

from pydantic import BaseModel, Field

class TransactionCreate(BaseModel):
    description: str = Field(min_length=1, max_length=255)
    amount: Decimal = Field(gt=0)
    category: str | None = Field(default=None, max_length=100)
    date: date
    transaction_type: Literal["income","expense"] = "expense"

class TransactionUpdate(BaseModel):
    description: str = Field(min_length=1, max_length=255)
    amount: Decimal = Field(gt=0)
    category: str | None = Field(default=None, max_length=100)
    date: date
    transaction_type: Literal["income", "expense"] = "expense"